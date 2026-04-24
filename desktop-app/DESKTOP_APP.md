# YouTube Upload Tool - Desktop Application

Cross-platform desktop GUI for macOS and Windows with PyQt6.

## Features

✅ **Beautiful GUI** - Modern interface with tabs and forms
✅ **Drag & Drop** - Easy file selection
✅ **Upload Videos** - Direct upload to YouTube with metadata
✅ **Download Videos** - Download from any YouTube URL
✅ **Manage Videos** - List and open your uploaded videos
✅ **OAuth Authentication** - Secure browser-based auth
✅ **Progress Tracking** - Real-time upload progress
✅ **Cross-Platform** - Works on macOS and Windows

## Installation

### Prerequisites

```bash
# Install Python dependencies
pip install PyQt6 google-api-python-client google-auth-oauthlib google-auth-httplib2 yt-dlp
```

### Run the Application

**macOS:**
```bash
cd /Users/nguyennghia/.openclaw/workspace/tools/youtube-uploader-desktop
python3 youtube_uploader.py
```

**Windows:**
```bash
cd C:\Users\YourName\.openclaw\workspace\tools\youtube-uploader-desktop
python youtube_uploader.py
```

## Setup (One-Time)

### 1. Create OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3":
   - APIs & Services → Library → Search "YouTube Data API v3" → Enable
4. Create OAuth 2.0 credentials:
   - APIs & Services → Credentials → Create Credentials → OAuth client ID
   - Application type: **Desktop app**
   - Name: "YouTube Upload Tool"
   - Click "Create" and download the JSON file
5. Place the JSON file in:
   - **macOS:** `~/.youtube_uploader/client_secrets.json`
   - **Windows:** `C:\Users\YourName\.youtube_uploader\client_secrets.json`

### 2. Authenticate

1. Open the desktop app
2. Go to **⚙️ Settings** tab
3. Click **🔑 Authenticate with YouTube**
4. Browser will open - sign in and grant permissions
5. Done! You can now upload videos

## Usage

### 📤 Upload Tab

1. **Select Video** - Click "Browse..." to choose video file
2. **Add Metadata**:
   - Title (required)
   - Description
   - Tags (comma-separated)
   - Category
   - Privacy (public/unlisted/private)
3. **Add Thumbnail** (optional) - Click "Browse..." for image
4. **Click "🚀 Upload to YouTube"**
5. Watch progress bar and wait for completion

### 📥 Download Tab

1. **Enter YouTube URL** - Paste any YouTube video URL
2. **Choose Save Location** - Default is Downloads folder
3. **Click "📥 Download Video"**
4. Wait for download to complete

### 📋 Manage Tab

1. **Click "📋 Load My Videos"** - Lists your recent uploads
2. **Select Video** - Click to highlight
3. **Click "🔗 Open Selected Video"** - Opens in browser

### ⚙️ Settings Tab

- **Authenticate** - Connect your YouTube account
- **Client Secrets** - Configure OAuth credentials
- **Help** - Instructions for creating credentials

## File Locations

**Configuration Directory:**
- **macOS:** `~/.youtube_uploader/`
- **Windows:** `C:\Users\YourName\.youtube_uploader\`

**Files:**
- `client_secrets.json` - OAuth credentials (you create this)
- `token.json` - Saved auth token (auto-generated)

## Features by Tab

### Upload Tab
- Video file browser
- Title, description, tags inputs
- Category dropdown (13 categories)
- Privacy selector (public/unlisted/private)
- Thumbnail image browser
- Real-time progress bar
- Status messages

### Download Tab
- YouTube URL input
- Output directory browser
- One-click download

### Manage Tab
- Load recent videos from your channel
- Video list with titles and URLs
- Open videos in browser

### Settings Tab
- Authentication status indicator
- OAuth authentication button
- Client secrets configuration
- Help instructions

## Screenshots

The application has 4 tabs:
1. **📤 Upload** - Main upload interface
2. **📥 Download** - Download videos
3. **📋 Manage** - Manage your uploads
4. **⚙️ Settings** - Configuration

## Troubleshooting

### "Not authenticated" error
- Go to Settings tab
- Click "Authenticate with YouTube"
- Follow browser prompts

### "client_secrets.json not found"
- Create OAuth credentials (see Setup above)
- Place file in config directory
- Or use "Browse for client_secrets.json" button

### Upload fails
- Check internet connection
- Verify video file format (MP4 recommended)
- Ensure title is not empty
- Check authentication status

### Download fails
- Verify YouTube URL is correct
- Check internet connection
- Ensure output directory exists

## Video Format Support

**Upload:** MP4, MOV, AVI, MKV, WebM (MP4 recommended)
**Thumbnail:** JPG, JPEG, PNG, WebP

## Category Options

- People & Blogs (default)
- Film & Animation
- Autos & Vehicles
- Music
- Pets & Animals
- Sports
- Gaming
- Comedy
- Entertainment
- News & Politics
- Howto & Style
- Education
- Science & Technology

## Privacy Options

- **Public** - Visible to everyone
- **Unlisted** - Only people with link can view
- **Private** - Only you can view

## Advanced Usage

### Batch Upload

The desktop app doesn't support batch uploads directly, but you can:
1. Use the CLI tool for batch operations
2. Manually upload multiple videos through the app

### Keyboard Shortcuts

- **Tab** - Switch between tabs
- **Enter** - Start upload/download
- **Escape** - Cancel dialogs

## Building Executable

### macOS (.app)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="YouTubeUploader" youtube_uploader.py
```

### Windows (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="YouTubeUploader" youtube_uploader.py
```

## Requirements

- Python 3.8+
- PyQt6
- google-api-python-client
- google-auth-oauthlib
- google-auth-httplib2
- yt-dlp
- Internet connection

## License

Free to use for personal and commercial projects.

## Support

For issues or questions, check the help button in Settings tab.
