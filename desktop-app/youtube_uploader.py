"""
YouTube Upload Tool - Desktop GUI Application
Cross-platform (macOS & Windows) with PyQt6
"""

import os
import stat
import sys
import time
from pathlib import Path

try:
    from PyQt6.QtCore import Qt, QThread, pyqtSignal
    from PyQt6.QtGui import QFont
    from PyQt6.QtWidgets import (
        QApplication,
        QComboBox,
        QFileDialog,
        QFormLayout,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QListWidget,
        QMainWindow,
        QMessageBox,
        QProgressBar,
        QPushButton,
        QTabWidget,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )
except ImportError:
    print("❌ PyQt6 not installed. Install with:")
    print("   pip install PyQt6")
    sys.exit(1)


# Single scope that covers both upload and list operations. Using one scope
# everywhere keeps the stored token compatible across features.
SCOPES = ["https://www.googleapis.com/auth/youtube"]
CONFIG_DIR = Path.home() / ".youtube_uploader"
TOKEN_PATH = CONFIG_DIR / "token.json"
SECRETS_PATH = CONFIG_DIR / "client_secrets.json"

# Upload in 50 MiB chunks. chunksize=-1 (the previous value) loads the entire
# video into RAM before transmitting — a 4 GB clip OOMs a low-memory machine.
UPLOAD_CHUNK_SIZE = 50 * 1024 * 1024

RETRIABLE_STATUS_CODES = {500, 502, 503, 504}
MAX_RETRIES = 5


def _secure_write(path: Path, data: str) -> None:
    """Atomically write a credential file with 0600 permissions."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "w") as f:
            f.write(data)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    # Defensive chmod in case umask widened the mode
    try:
        os.chmod(tmp, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
    os.replace(tmp, path)


def _load_credentials():
    """Load, refresh, and persist OAuth credentials. Returns None if unusable."""
    from google.auth.exceptions import RefreshError
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    if not TOKEN_PATH.exists():
        return None

    try:
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    except (ValueError, OSError):
        return None

    if creds.valid:
        return creds

    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except RefreshError:
            return None
        # Persist the refreshed token so the next run doesn't refresh again
        _secure_write(TOKEN_PATH, creds.to_json())
        return creds

    return None


class YouTubeUploaderThread(QThread):
    """Background thread for YouTube uploads.

    `finished` intentionally avoided — QThread already exposes that name.
    """

    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    upload_finished = pyqtSignal(str)
    upload_error = pyqtSignal(str)

    def __init__(self, video_path, title, description, tags, category, privacy,
                 thumbnail=None, parent=None):
        super().__init__(parent)
        self.video_path = video_path
        self.title = title
        self.description = description
        self.tags = tags
        self.category = category
        self.privacy = privacy
        self.thumbnail = thumbnail
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    def run(self):
        media = None
        try:
            from googleapiclient.discovery import build
            from googleapiclient.errors import HttpError
            from googleapiclient.http import MediaFileUpload

            self.status.emit("🔐 Authenticating...")
            credentials = _load_credentials()
            if credentials is None:
                self.upload_error.emit(
                    "Not authenticated. Please click 'Authenticate' first."
                )
                return

            if not os.path.isfile(self.video_path):
                self.upload_error.emit(
                    f"Video file does not exist: {self.video_path}"
                )
                return

            self.status.emit("📤 Starting upload...")
            youtube = build(
                "youtube", "v3", credentials=credentials, cache_discovery=False
            )

            body = {
                "snippet": {
                    "title": self.title,
                    "description": self.description,
                    "tags": self.tags,
                    "categoryId": str(self.category),
                },
                "status": {
                    "privacyStatus": self.privacy,
                    "selfDeclaredMadeForKids": False,
                },
            }

            media = MediaFileUpload(
                self.video_path,
                chunksize=UPLOAD_CHUNK_SIZE,
                resumable=True,
            )

            request = youtube.videos().insert(
                part=",".join(body.keys()),
                body=body,
                media_body=media,
            )

            response = None
            retry = 0
            while response is None:
                if self._cancelled:
                    self.upload_error.emit("Upload cancelled.")
                    return
                try:
                    chunk_status, response = request.next_chunk()
                    if chunk_status:
                        self.progress.emit(int(chunk_status.progress() * 100))
                    retry = 0
                except HttpError as e:
                    if e.resp.status in RETRIABLE_STATUS_CODES and retry < MAX_RETRIES:
                        retry += 1
                        sleep_s = min(2 ** retry, 60)
                        self.status.emit(
                            f"⏳ Transient error ({e.resp.status}); "
                            f"retrying in {sleep_s}s..."
                        )
                        time.sleep(sleep_s)
                        continue
                    raise
                except (IOError, ConnectionError) as e:
                    if retry < MAX_RETRIES:
                        retry += 1
                        sleep_s = min(2 ** retry, 60)
                        self.status.emit(
                            f"⏳ Network error ({e}); retrying in {sleep_s}s..."
                        )
                        time.sleep(sleep_s)
                        continue
                    raise

            video_id = response.get("id") if isinstance(response, dict) else None
            if not video_id:
                self.upload_error.emit(f"Unexpected API response: {response!r}")
                return
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            if self.thumbnail and os.path.isfile(self.thumbnail):
                self.status.emit("🖼️ Uploading thumbnail...")
                try:
                    youtube.thumbnails().set(
                        videoId=video_id, media_body=self.thumbnail
                    ).execute()
                except HttpError as e:
                    # Don't fail the whole upload if just the thumbnail is rejected
                    self.status.emit(f"⚠️ Thumbnail upload failed: {e}")

            self.progress.emit(100)
            self.status.emit("✅ Upload complete!")
            self.upload_finished.emit(video_url)

        except Exception as e:
            self.upload_error.emit(f"Upload failed: {e}")
        finally:
            # MediaFileUpload opens a file descriptor via `.stream()`; release it
            if media is not None:
                fd = getattr(media, "_fd", None)
                if fd is not None:
                    try:
                        fd.close()
                    except Exception:
                        pass


class AuthThread(QThread):
    """Background thread for OAuth authentication."""

    status = pyqtSignal(str)
    auth_success = pyqtSignal()
    auth_error = pyqtSignal(str)

    def run(self):
        try:
            import google_auth_oauthlib.flow

            if not SECRETS_PATH.exists():
                self.auth_error.emit(
                    "client_secrets.json not found. Configure it in Settings."
                )
                return

            self.status.emit("🔑 Opening browser for authentication...")
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                str(SECRETS_PATH), SCOPES
            )
            credentials = flow.run_local_server(port=0)

            _secure_write(TOKEN_PATH, credentials.to_json())
            self.status.emit("✅ Authentication successful!")
            self.auth_success.emit()

        except Exception as e:
            self.auth_error.emit(f"Authentication failed: {e}")


class DownloadThread(QThread):
    """Background thread for yt-dlp downloads so the UI stays responsive."""

    status = pyqtSignal(str)
    download_finished = pyqtSignal()
    download_error = pyqtSignal(str)

    def __init__(self, url, output_dir, parent=None):
        super().__init__(parent)
        self.url = url
        self.output_dir = output_dir

    def run(self):
        try:
            import yt_dlp

            self.status.emit("📥 Downloading...")
            ydl_opts = {
                "format": "best",
                "outtmpl": os.path.join(self.output_dir, "%(title)s.%(ext)s"),
                # Remote-supplied %(title)s can contain path separators or traversal
                # sequences. restrictfilenames sanitizes them to safe ASCII.
                "restrictfilenames": True,
                "noplaylist": True,
                "quiet": True,
                "no_warnings": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.download_finished.emit()
        except Exception as e:
            self.download_error.emit(str(e))


class ListVideosThread(QThread):
    """Background thread for listing videos without blocking the UI."""

    result = pyqtSignal(list)
    list_error = pyqtSignal(str)

    def run(self):
        try:
            from googleapiclient.discovery import build

            credentials = _load_credentials()
            if credentials is None:
                self.list_error.emit(
                    "Not authenticated. Please authenticate first."
                )
                return

            youtube = build(
                "youtube", "v3", credentials=credentials, cache_discovery=False
            )
            request = youtube.search().list(
                part="snippet",
                forMine=True,
                type="video",
                order="date",
                maxResults=25,
            )
            response = request.execute()

            items = []
            for item in response.get("items", []):
                vid = (item.get("id") or {}).get("videoId")
                title = (item.get("snippet") or {}).get("title", "(no title)")
                if vid:
                    items.append((title, f"https://www.youtube.com/watch?v={vid}"))
            self.result.emit(items)
        except Exception as e:
            self.list_error.emit(str(e))


class YouTubeUploaderApp(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Upload Tool")
        self.setGeometry(100, 100, 900, 700)
        self.current_video = None
        self.current_thumbnail = None

        self.config_dir = CONFIG_DIR
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Hold strong refs so Qt doesn't GC a running QThread mid-flight
        self._threads = []

        self.setup_ui()
        self.check_auth_status()

    # ----- thread lifecycle -----
    def _track_thread(self, thread: QThread) -> None:
        self._threads.append(thread)
        thread.finished.connect(lambda t=thread: self._untrack_thread(t))

    def _untrack_thread(self, thread: QThread) -> None:
        try:
            self._threads.remove(thread)
        except ValueError:
            pass
        thread.deleteLater()

    def closeEvent(self, event):
        for t in list(self._threads):
            if t.isRunning():
                if hasattr(t, "cancel"):
                    t.cancel()
                t.quit()
                t.wait(5000)
        super().closeEvent(event)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        header = QLabel("🎬 YouTube Upload Tool")
        header.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        tabs.addTab(self.create_upload_tab(), "📤 Upload")
        tabs.addTab(self.create_download_tab(), "📥 Download")
        tabs.addTab(self.create_manage_tab(), "📋 Manage")
        tabs.addTab(self.create_settings_tab(), "⚙️ Settings")

    def create_upload_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        video_group = QGroupBox("📹 Video File")
        video_layout = QHBoxLayout()
        self.video_path_input = QLineEdit()
        self.video_path_input.setPlaceholderText("Select video file...")
        self.video_path_input.setReadOnly(True)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_video)
        video_layout.addWidget(self.video_path_input)
        video_layout.addWidget(browse_btn)
        video_group.setLayout(video_layout)
        layout.addWidget(video_group)

        metadata_group = QGroupBox("📝 Video Metadata")
        metadata_layout = QFormLayout()

        self.title_input = QLineEdit()
        self.title_input.setMaxLength(100)  # YouTube caps titles at 100 chars
        self.title_input.setPlaceholderText("Enter video title...")
        metadata_layout.addRow("Title:", self.title_input)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter video description...")
        self.description_input.setMaximumHeight(100)
        metadata_layout.addRow("Description:", self.description_input)

        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Enter tags (comma-separated)...")
        metadata_layout.addRow("Tags:", self.tags_input)

        self.category_combo = QComboBox()
        categories = [
            ("22", "People & Blogs"),
            ("1", "Film & Animation"),
            ("2", "Autos & Vehicles"),
            ("10", "Music"),
            ("15", "Pets & Animals"),
            ("17", "Sports"),
            ("20", "Gaming"),
            ("23", "Comedy"),
            ("24", "Entertainment"),
            ("25", "News & Politics"),
            ("26", "Howto & Style"),
            ("27", "Education"),
            ("28", "Science & Technology"),
        ]
        for cat_id, cat_name in categories:
            self.category_combo.addItem(cat_name, cat_id)
        metadata_layout.addRow("Category:", self.category_combo)

        self.privacy_combo = QComboBox()
        self.privacy_combo.addItems(["public", "unlisted", "private"])
        metadata_layout.addRow("Privacy:", self.privacy_combo)

        metadata_group.setLayout(metadata_layout)
        layout.addWidget(metadata_group)

        thumbnail_group = QGroupBox("🖼️ Thumbnail (Optional)")
        thumbnail_layout = QHBoxLayout()
        self.thumbnail_path_input = QLineEdit()
        self.thumbnail_path_input.setPlaceholderText("Select thumbnail image...")
        self.thumbnail_path_input.setReadOnly(True)
        thumbnail_browse_btn = QPushButton("Browse...")
        thumbnail_browse_btn.clicked.connect(self.browse_thumbnail)
        thumbnail_layout.addWidget(self.thumbnail_path_input)
        thumbnail_layout.addWidget(thumbnail_browse_btn)
        thumbnail_group.setLayout(thumbnail_layout)
        layout.addWidget(thumbnail_group)

        progress_group = QGroupBox("📊 Upload Progress")
        progress_layout = QVBoxLayout()
        self.status_label = QLabel("Ready to upload")
        progress_layout.addWidget(self.status_label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        self.upload_btn = QPushButton("🚀 Upload to YouTube")
        self.upload_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.upload_btn.clicked.connect(self.upload_video)
        layout.addWidget(self.upload_btn)

        return widget

    def create_download_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        url_group = QGroupBox("🔗 YouTube URL")
        url_layout = QHBoxLayout()
        self.download_url_input = QLineEdit()
        self.download_url_input.setPlaceholderText("https://youtube.com/watch?v=...")
        url_layout.addWidget(self.download_url_input)
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)

        output_group = QGroupBox("💾 Save Location")
        output_layout = QHBoxLayout()
        self.output_path_input = QLineEdit()
        self.output_path_input.setPlaceholderText(str(Path.home() / "Downloads"))
        self.output_path_input.setText(str(Path.home() / "Downloads"))
        output_browse_btn = QPushButton("Browse...")
        output_browse_btn.clicked.connect(self.browse_output)
        output_layout.addWidget(self.output_path_input)
        output_layout.addWidget(output_browse_btn)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        self.download_btn = QPushButton("📥 Download Video")
        self.download_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.download_btn.clicked.connect(self.download_video)
        layout.addWidget(self.download_btn)

        self.download_status = QLabel("Ready to download")
        layout.addWidget(self.download_status)

        layout.addStretch()
        return widget

    def create_manage_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.list_btn = QPushButton("📋 Load My Videos")
        self.list_btn.setFont(QFont("Arial", 12))
        self.list_btn.clicked.connect(self.list_videos)
        layout.addWidget(self.list_btn)

        self.video_list = QListWidget()
        layout.addWidget(self.video_list)

        open_btn = QPushButton("🔗 Open Selected Video")
        open_btn.clicked.connect(self.open_selected_video)
        layout.addWidget(open_btn)

        return widget

    def create_settings_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        auth_group = QGroupBox("🔐 YouTube Authentication")
        auth_layout = QVBoxLayout()
        self.auth_status_label = QLabel("Checking authentication status...")
        auth_layout.addWidget(self.auth_status_label)
        auth_btn = QPushButton("🔑 Authenticate with YouTube")
        auth_btn.clicked.connect(self.authenticate)
        auth_layout.addWidget(auth_btn)
        auth_group.setLayout(auth_layout)
        layout.addWidget(auth_group)

        secrets_group = QGroupBox("📄 Client Secrets")
        secrets_layout = QVBoxLayout()
        secrets_label = QLabel("Place your OAuth client_secrets.json file in:")
        secrets_layout.addWidget(secrets_label)
        secrets_path = QLabel(str(SECRETS_PATH))
        secrets_path.setStyleSheet(
            "QLabel { background-color: #f0f0f0; padding: 10px; border-radius: 5px; }"
        )
        secrets_layout.addWidget(secrets_path)
        browse_secrets_btn = QPushButton("Browse for client_secrets.json")
        browse_secrets_btn.clicked.connect(self.browse_secrets)
        secrets_layout.addWidget(browse_secrets_btn)
        secrets_help = QPushButton("📖 How to create OAuth credentials")
        secrets_help.clicked.connect(self.show_oauth_help)
        secrets_layout.addWidget(secrets_help)
        secrets_group.setLayout(secrets_layout)
        layout.addWidget(secrets_group)

        layout.addStretch()
        return widget

    # ---------- event handlers ----------
    def browse_video(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            str(Path.home()),
            "Video Files (*.mp4 *.mov *.avi *.mkv *.webm);;All Files (*)",
        )
        if file:
            self.current_video = file
            self.video_path_input.setText(file)
            if not self.title_input.text():
                title = Path(file).stem
                self.title_input.setText(title.replace("-", " ").replace("_", " ").title())

    def browse_thumbnail(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Thumbnail Image",
            str(Path.home()),
            "Image Files (*.jpg *.jpeg *.png *.webp);;All Files (*)",
        )
        if file:
            self.current_thumbnail = file
            self.thumbnail_path_input.setText(file)

    def browse_output(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Output Directory", str(Path.home())
        )
        if directory:
            self.output_path_input.setText(directory)

    def browse_secrets(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select client_secrets.json",
            str(Path.home()),
            "JSON Files (*.json);;All Files (*)",
        )
        if not file:
            return
        try:
            with open(file, "r", encoding="utf-8") as src:
                data = src.read()
        except OSError as e:
            QMessageBox.critical(self, "Error", f"Could not read file: {e}")
            return
        _secure_write(SECRETS_PATH, data)
        QMessageBox.information(self, "Success", "Client secrets installed (0600).")
        self.check_auth_status()

    def upload_video(self):
        if not self.current_video:
            QMessageBox.warning(self, "Error", "Please select a video file first.")
            return
        if not os.path.isfile(self.current_video):
            QMessageBox.warning(self, "Error", "Selected video no longer exists.")
            return
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Error", "Please enter a video title.")
            return

        title = self.title_input.text().strip()
        description = self.description_input.toPlainText()
        tags = [t.strip() for t in self.tags_input.text().split(",") if t.strip()]
        try:
            category = int(self.category_combo.currentData())
        except (TypeError, ValueError):
            category = 22
        privacy = self.privacy_combo.currentText()
        thumbnail = self.current_thumbnail

        self.upload_btn.setEnabled(False)
        thread = YouTubeUploaderThread(
            self.current_video, title, description, tags, category, privacy, thumbnail
        )
        thread.progress.connect(self.progress_bar.setValue)
        thread.status.connect(self.status_label.setText)
        thread.upload_finished.connect(self.on_upload_complete)
        thread.upload_error.connect(self.on_upload_error)
        thread.finished.connect(lambda: self.upload_btn.setEnabled(True))
        self._track_thread(thread)
        thread.start()

    def on_upload_complete(self, url):
        QMessageBox.information(
            self,
            "Upload Complete!",
            f"✅ Your video has been uploaded!\n\n🔗 {url}",
        )
        self.progress_bar.setValue(0)
        self.status_label.setText("Upload complete!")

    def on_upload_error(self, error):
        QMessageBox.critical(self, "Upload Error", str(error))
        self.status_label.setText("Upload failed!")
        self.progress_bar.setValue(0)

    def download_video(self):
        url = self.download_url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a YouTube URL.")
            return

        output_dir = self.output_path_input.text().strip() or str(Path.home() / "Downloads")
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            QMessageBox.critical(self, "Error", f"Cannot create output directory: {e}")
            return

        self.download_btn.setEnabled(False)
        thread = DownloadThread(url, output_dir)
        thread.status.connect(self.download_status.setText)
        thread.download_finished.connect(self._on_download_finished)
        thread.download_error.connect(self._on_download_error)
        thread.finished.connect(lambda: self.download_btn.setEnabled(True))
        self._track_thread(thread)
        thread.start()

    def _on_download_finished(self):
        self.download_status.setText("✅ Download complete!")
        QMessageBox.information(self, "Success", "Video downloaded successfully!")

    def _on_download_error(self, err):
        self.download_status.setText("❌ Download failed!")
        QMessageBox.critical(self, "Download Error", err)

    def list_videos(self):
        self.list_btn.setEnabled(False)
        self.video_list.clear()
        thread = ListVideosThread()
        thread.result.connect(self._on_videos_listed)
        thread.list_error.connect(self._on_list_error)
        thread.finished.connect(lambda: self.list_btn.setEnabled(True))
        self._track_thread(thread)
        thread.start()

    def _on_videos_listed(self, items):
        for title, url in items:
            self.video_list.addItem(f"{title}\n{url}")

    def _on_list_error(self, err):
        QMessageBox.critical(self, "Error", f"Failed to list videos: {err}")

    def open_selected_video(self):
        import webbrowser

        current_item = self.video_list.currentItem()
        if not current_item:
            return
        text = current_item.text()
        url = text.split("\n")[-1]
        # Only open HTTPS URLs — guards against a bad list response leaking a shell-ish string
        if url.startswith("https://www.youtube.com/") or url.startswith("https://youtube.com/"):
            webbrowser.open(url)

    def authenticate(self):
        thread = AuthThread()
        thread.status.connect(self.auth_status_label.setText)
        thread.auth_success.connect(self._on_auth_success)
        thread.auth_error.connect(self._on_auth_error)
        thread.finished.connect(self.check_auth_status)
        self._track_thread(thread)
        thread.start()

    def _on_auth_success(self):
        QMessageBox.information(
            self, "Success", "Authentication successful! You can now upload videos."
        )

    def _on_auth_error(self, err):
        QMessageBox.critical(self, "Authentication Error", err)

    def check_auth_status(self):
        if TOKEN_PATH.exists():
            self.auth_status_label.setText("✅ Authenticated")
            self.auth_status_label.setStyleSheet(
                "QLabel { color: green; font-weight: bold; }"
            )
        elif SECRETS_PATH.exists():
            self.auth_status_label.setText(
                "⚠️ Not authenticated - Click 'Authenticate' button"
            )
            self.auth_status_label.setStyleSheet(
                "QLabel { color: orange; font-weight: bold; }"
            )
        else:
            self.auth_status_label.setText("❌ No credentials found")
            self.auth_status_label.setStyleSheet(
                "QLabel { color: red; font-weight: bold; }"
            )

    def show_oauth_help(self):
        help_text = (
            "How to Create YouTube OAuth Credentials:\n\n"
            "1. Go to https://console.cloud.google.com/\n"
            "2. Create a new project\n"
            "3. Enable YouTube Data API v3:\n"
            "   APIs & Services → Library → Search 'YouTube Data API v3' → Enable\n"
            "4. Create OAuth 2.0 credentials:\n"
            "   APIs & Services → Credentials → Create Credentials → OAuth client ID\n"
            "   Application type: Desktop app\n"
            "   Click 'Create' and download the JSON file\n"
            f"5. Place the JSON file in:\n   {SECRETS_PATH}\n\n"
            "Then click 'Authenticate with YouTube'."
        )
        QMessageBox.information(self, "OAuth Setup Help", help_text)


def main():
    app = QApplication(sys.argv)
    window = YouTubeUploaderApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
