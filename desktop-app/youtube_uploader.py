"""
YouTube Upload Tool - Desktop GUI Application
Cross-platform (macOS & Windows) with PyQt6
"""

import sys
import os
import json
import threading
from pathlib import Path
from datetime import datetime

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLineEdit, QTextEdit, QFileDialog, QProgressBar,
        QLabel, QComboBox, QTabWidget, QListWidget, QMessageBox,
        QGroupBox, QFormLayout, QSpinBox
    )
    from PyQt6.QtCore import QThread, pyqtSignal, Qt
    from PyQt6.QtGui import QFont, QIcon
except ImportError:
    print("❌ PyQt6 not installed. Install with:")
    print("   pip install PyQt6")
    sys.exit(1)


class YouTubeUploaderThread(QThread):
    """Background thread for YouTube uploads"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(str)  # Returns video URL
    error = pyqtSignal(str)

    def __init__(self, video_path, title, description, tags, category, privacy, thumbnail=None):
        super().__init__()
        self.video_path = video_path
        self.title = title
        self.description = description
        self.tags = tags
        self.category = category
        self.privacy = privacy
        self.thumbnail = thumbnail

    def run(self):
        try:
            self.status.emit("🔐 Authenticating...")

            # Import YouTube upload logic
            import google.oauth2.credentials
            import google_auth_oauthlib.flow
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials

            SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

            # Get token path
            token_path = Path.home() / '.youtube_uploader' / 'token.json'

            # Load or get credentials
            if token_path.exists():
                credentials = Credentials.from_authorized_user_file(str(token_path), SCOPES)
                if credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
            else:
                self.status.emit("🔑 No credentials found. Please authenticate first.")
                self.error.emit("Not authenticated. Please click 'Authenticate' button.")
                return

            self.status.emit("📤 Starting upload...")

            # Build YouTube service
            youtube = build('youtube', 'v3', credentials=credentials)

            # Prepare upload body
            body = {
                'snippet': {
                    'title': self.title,
                    'description': self.description,
                    'tags': self.tags,
                    'categoryId': str(self.category)
                },
                'status': {
                    'privacyStatus': self.privacy,
                    'selfDeclaredMadeForKids': False
                }
            }

            # Create upload request
            media = MediaFileUpload(self.video_path, chunksize=-1, resumable=True)

            request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )

            # Upload with progress
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    self.progress.emit(progress)

            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # Upload thumbnail if provided
            if self.thumbnail and os.path.exists(self.thumbnail):
                self.status.emit("🖼️ Uploading thumbnail...")
                youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=self.thumbnail
                ).execute()

            self.status.emit("✅ Upload complete!")
            self.finished.emit(video_url)

        except Exception as e:
            self.error.emit(f"Upload failed: {str(e)}")
            import traceback
            traceback.print_exc()


class AuthThread(QThread):
    """Background thread for OAuth authentication"""
    status = pyqtSignal(str)
    success = pyqtSignal()
    error = pyqtSignal(str)

    def run(self):
        try:
            import google_auth_oauthlib.flow
            from google.oauth2.credentials import Credentials

            SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

            # Check for client secrets
            secrets_path = Path.home() / '.youtube_uploader' / 'client_secrets.json'

            if not secrets_path.exists():
                self.error.emit("client_secrets.json not found. Please configure first.")
                return

            self.status.emit("🔑 Opening browser for authentication...")

            # Run OAuth flow
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                str(secrets_path), SCOPES)
            credentials = flow.run_local_server(port=0)

            # Save credentials
            token_path = Path.home() / '.youtube_uploader' / 'token.json'
            token_path.parent.mkdir(parents=True, exist_ok=True)

            with open(token_path, 'w') as f:
                f.write(credentials.to_json())

            self.status.emit("✅ Authentication successful!")
            self.success.emit()

        except Exception as e:
            self.error.emit(f"Authentication failed: {str(e)}")


class YouTubeUploaderApp(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Upload Tool")
        self.setGeometry(100, 100, 900, 700)
        self.current_video = None
        self.current_thumbnail = None

        # Create config directory
        self.config_dir = Path.home() / '.youtube_uploader'
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.setup_ui()
        self.check_auth_status()

    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Header
        header = QLabel("🎬 YouTube Upload Tool")
        header.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        # Tab widget
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # Upload Tab
        upload_tab = self.create_upload_tab()
        tabs.addTab(upload_tab, "📤 Upload")

        # Download Tab
        download_tab = self.create_download_tab()
        tabs.addTab(download_tab, "📥 Download")

        # Manage Tab
        manage_tab = self.create_manage_tab()
        tabs.addTab(manage_tab, "📋 Manage")

        # Settings Tab
        settings_tab = self.create_settings_tab()
        tabs.addTab(settings_tab, "⚙️ Settings")

    def create_upload_tab(self):
        """Create upload tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Video selection
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

        # Metadata form
        metadata_group = QGroupBox("📝 Video Metadata")
        metadata_layout = QFormLayout()

        self.title_input = QLineEdit()
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
            ("28", "Science & Technology")
        ]
        for cat_id, cat_name in categories:
            self.category_combo.addItem(cat_name, cat_id)
        metadata_layout.addRow("Category:", self.category_combo)

        self.privacy_combo = QComboBox()
        self.privacy_combo.addItems(["public", "unlisted", "private"])
        metadata_layout.addRow("Privacy:", self.privacy_combo)

        metadata_group.setLayout(metadata_layout)
        layout.addWidget(metadata_group)

        # Thumbnail
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

        # Progress
        progress_group = QGroupBox("📊 Upload Progress")
        progress_layout = QVBoxLayout()

        self.status_label = QLabel("Ready to upload")
        progress_layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Upload button
        upload_btn = QPushButton("🚀 Upload to YouTube")
        upload_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        upload_btn.clicked.connect(self.upload_video)
        layout.addWidget(upload_btn)

        return widget

    def create_download_tab(self):
        """Create download tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # URL input
        url_group = QGroupBox("🔗 YouTube URL")
        url_layout = QHBoxLayout()

        self.download_url_input = QLineEdit()
        self.download_url_input.setPlaceholderText("https://youtube.com/watch?v=...")

        url_layout.addWidget(self.download_url_input)
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)

        # Output directory
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

        # Download button
        download_btn = QPushButton("📥 Download Video")
        download_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        download_btn.clicked.connect(self.download_video)
        layout.addWidget(download_btn)

        # Download progress
        self.download_status = QLabel("Ready to download")
        layout.addWidget(self.download_status)

        layout.addStretch()
        return widget

    def create_manage_tab(self):
        """Create manage tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # List button
        list_btn = QPushButton("📋 Load My Videos")
        list_btn.setFont(QFont("Arial", 12))
        list_btn.clicked.connect(self.list_videos)
        layout.addWidget(list_btn)

        # Video list
        self.video_list = QListWidget()
        layout.addWidget(self.video_list)

        # Open button
        open_btn = QPushButton("🔗 Open Selected Video")
        open_btn.clicked.connect(self.open_selected_video)
        layout.addWidget(open_btn)

        return widget

    def create_settings_tab(self):
        """Create settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Auth section
        auth_group = QGroupBox("🔐 YouTube Authentication")
        auth_layout = QVBoxLayout()

        self.auth_status_label = QLabel("Checking authentication status...")
        auth_layout.addWidget(self.auth_status_label)

        auth_btn = QPushButton("🔑 Authenticate with YouTube")
        auth_btn.clicked.connect(self.authenticate)
        auth_layout.addWidget(auth_btn)

        auth_group.setLayout(auth_layout)
        layout.addWidget(auth_group)

        # Client secrets
        secrets_group = QGroupBox("📄 Client Secrets")
        secrets_layout = QVBoxLayout()

        secrets_label = QLabel("Place your OAuth client_secrets.json file in:")
        secrets_layout.addWidget(secrets_label)

        secrets_path = QLabel(str(self.config_dir / "client_secrets.json"))
        secrets_path.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 10px; border-radius: 5px; }")
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

    def browse_video(self):
        """Browse for video file"""
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            str(Path.home()),
            "Video Files (*.mp4 *.mov *.avi *.mkv *.webm);;All Files (*)"
        )
        if file:
            self.current_video = file
            self.video_path_input.setText(file)

            # Auto-fill title from filename
            if not self.title_input.text():
                title = Path(file).stem
                self.title_input.setText(title.replace("-", " ").replace("_", " ").title())

    def browse_thumbnail(self):
        """Browse for thumbnail image"""
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Thumbnail Image",
            str(Path.home()),
            "Image Files (*.jpg *.jpeg *.png *.webp);;All Files (*)"
        )
        if file:
            self.current_thumbnail = file
            self.thumbnail_path_input.setText(file)

    def browse_output(self):
        """Browse for output directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            str(Path.home())
        )
        if directory:
            self.output_path_input.setText(directory)

    def browse_secrets(self):
        """Browse for client_secrets.json"""
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select client_secrets.json",
            str(Path.home()),
            "JSON Files (*.json);;All Files (*)"
        )
        if file:
            import shutil
            shutil.copy(file, self.config_dir / "client_secrets.json")
            QMessageBox.information(self, "Success", "Client secrets file copied successfully!")
            self.check_auth_status()

    def upload_video(self):
        """Upload video to YouTube"""
        if not self.current_video:
            QMessageBox.warning(self, "Error", "Please select a video file first.")
            return

        if not self.title_input.text():
            QMessageBox.warning(self, "Error", "Please enter a video title.")
            return

        # Get metadata
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        tags = [t.strip() for t in self.tags_input.text().split(",") if t.strip()]
        category = int(self.category_combo.currentData())
        privacy = self.privacy_combo.currentText()
        thumbnail = self.current_thumbnail

        # Start upload thread
        self.upload_thread = YouTubeUploaderThread(
            self.current_video, title, description, tags, category, privacy, thumbnail
        )
        self.upload_thread.progress.connect(self.progress_bar.setValue)
        self.upload_thread.status.connect(self.status_label.setText)
        self.upload_thread.finished.connect(self.on_upload_complete)
        self.upload_thread.error.connect(self.on_upload_error)
        self.upload_thread.start()

    def on_upload_complete(self, url):
        """Handle successful upload"""
        QMessageBox.information(
            self,
            "Upload Complete!",
            f"✅ Your video has been uploaded!\n\n🔗 {url}"
        )
        self.progress_bar.setValue(0)
        self.status_label.setText("Upload complete!")

    def on_upload_error(self, error):
        """Handle upload error"""
        QMessageBox.critical(self, "Upload Error", str(error))
        self.status_label.setText("Upload failed!")
        self.progress_bar.setValue(0)

    def download_video(self):
        """Download video from YouTube"""
        url = self.download_url_input.text()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a YouTube URL.")
            return

        output_dir = self.output_path_input.text()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            import yt_dlp

            self.download_status.setText("📥 Downloading...")

            ydl_opts = {
                'format': 'best',
                'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
                'quiet': False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.download_status.setText("✅ Download complete!")
            QMessageBox.information(self, "Success", "Video downloaded successfully!")

        except Exception as e:
            self.download_status.setText("❌ Download failed!")
            QMessageBox.critical(self, "Download Error", str(e))

    def list_videos(self):
        """List user's videos"""
        try:
            from googleapiclient.discovery import build
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request

            SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
            token_path = self.config_dir / 'token.json'

            if not token_path.exists():
                QMessageBox.warning(self, "Error", "Not authenticated. Please authenticate first.")
                return

            credentials = Credentials.from_authorized_user_file(str(token_path), SCOPES)
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())

            youtube = build('youtube', 'v3', credentials=credentials)

            request = youtube.search().list(
                part='snippet',
                forMine=True,
                type='video',
                order='date',
                maxResults=20
            )

            response = request.execute()

            self.video_list.clear()

            for item in response.get('items', []):
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                url = f"https://www.youtube.com/watch?v={video_id}"
                self.video_list.addItem(f"{title}\n{url}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to list videos: {str(e)}")

    def open_selected_video(self):
        """Open selected video in browser"""
        import webbrowser
        current_item = self.video_list.currentItem()
        if current_item:
            text = current_item.text()
            url = text.split('\n')[-1]
            webbrowser.open(url)

    def authenticate(self):
        """Start OAuth authentication"""
        self.auth_thread = AuthThread()
        self.auth_thread.status.connect(self.auth_status_label.setText)
        self.auth_thread.success.connect(lambda: QMessageBox.information(
            self, "Success", "Authentication successful! You can now upload videos."
        ))
        self.auth_thread.error.connect(lambda err: QMessageBox.critical(
            self, "Authentication Error", err
        ))
        self.auth_thread.start()

    def check_auth_status(self):
        """Check if user is authenticated"""
        token_path = self.config_dir / 'token.json'
        secrets_path = self.config_dir / 'client_secrets.json'

        if token_path.exists():
            self.auth_status_label.setText("✅ Authenticated")
            self.auth_status_label.setStyleSheet("QLabel { color: green; font-weight: bold; }")
        elif secrets_path.exists():
            self.auth_status_label.setText("⚠️ Not authenticated - Click 'Authenticate' button")
            self.auth_status_label.setStyleSheet("QLabel { color: orange; font-weight: bold; }")
        else:
            self.auth_status_label.setText("❌ No credentials found")
            self.auth_status_label.setStyleSheet("QLabel { color: red; font-weight: bold; }")

    def show_oauth_help(self):
        """Show OAuth setup help"""
        help_text = """
How to Create YouTube OAuth Credentials:

1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable YouTube Data API v3:
   - APIs & Services → Library → Search "YouTube Data API v3" → Enable
4. Create OAuth 2.0 credentials:
   - APIs & Services → Credentials → Create Credentials → OAuth client ID
   - Application type: Desktop app
   - Name: YouTube Upload Tool
   - Click "Create" and download the JSON file
5. Place the JSON file in:
   """ + str(self.config_dir / "client_secrets.json") + """

Then click "Authenticate with YouTube" button.
        """

        QMessageBox.information(self, "OAuth Setup Help", help_text)


def main():
    app = QApplication(sys.argv)
    window = YouTubeUploaderApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
