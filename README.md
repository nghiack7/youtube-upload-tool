# 🎬 YouTube Upload Tool

A complete cross-platform YouTube upload/download solution with both **CLI** and **Desktop GUI** applications.

[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-blue)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-orange)](LICENSE)

## ✨ Features

### 🖥️ Desktop Application
- Beautiful modern GUI with PyQt6
- Upload videos with full metadata (title, description, tags, category, privacy, thumbnail)
- Download any YouTube video
- Manage your uploaded videos
- Real-time progress tracking
- Cross-platform (macOS & Windows)

### 💻 CLI Tool
- Upload videos from terminal
- Download videos from YouTube
- List your channel videos
- Batch processing support
- Perfect for automation and scripts

## 🚀 Quick Start

### Desktop App (Recommended)

**macOS:**
```bash
cd desktop-app
./install.sh
./youtube-uploader
```

**Windows:**
```bash
cd desktop-app
install.bat
youtube-uploader.bat
```

### CLI Tool

```bash
cd cli-tool
./youtube --auth  # First time authentication
./youtube --upload video.mp4 --title "My Video"
```

## 📖 Setup (One-Time)

### Step 1: Create OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3":
   - APIs & Services → Library → Search "YouTube Data API v3" → Enable
4. Create OAuth 2.0 credentials:
   - APIs & Services → Credentials → Create Credentials → OAuth client ID
   - Application type: **Desktop app**
   - Click "Create" and download the JSON file

### Step 2: Save Credentials

**macOS:** Save as `~/.youtube_uploader/client_secrets.json`  
**Windows:** Save as `C:\Users\YourName\.youtube_uploader\client_secrets.json`

Or use the **Browse** button in the desktop app's Settings tab!

### Step 3: Authenticate

**Desktop App:** Settings tab → "Authenticate with YouTube"  
**CLI:** `./youtube --auth`

## 📁 Project Structure

```
youtube-upload-tool/
├── cli-tool/                 # Command-line tool
│   ├── youtube              # Wrapper script
│   ├── youtube-upload.py    # Main Python script
│   ├── YOUTUBE_SETUP.md     # Setup guide
│   ├── QUICKREF.md          # Quick reference
│   └── venv/                # Python virtual environment
│
├── desktop-app/              # Desktop GUI application
│   ├── youtube_uploader.py  # Main app
│   ├── install.sh           # macOS installer
│   ├── install.bat          # Windows installer
│   ├── youtube-uploader     # macOS launcher
│   ├── README.md            # Desktop app docs
│   ├── QUICKSTART.md        # Quick start guide
│   ├── DESKTOP_APP.md      # Detailed guide
│   └── venv/                # Python virtual environment
│
└── README.md                 # This file
```

## 🎯 Usage Examples

### Desktop App

**Upload a video:**
1. Open the app
2. Go to 📤 Upload tab
3. Browse and select video file
4. Enter title, description, tags
5. Click "🚀 Upload to YouTube"

**Download a video:**
1. Go to 📥 Download tab
2. Paste YouTube URL
3. Click "📥 Download Video"

**Manage videos:**
1. Go to 📋 Manage tab
2. Click "📋 Load My Videos"
3. Select and open videos

### CLI Tool

**Upload with metadata:**
```bash
./youtube --upload video.mp4 \
  --title "My Video Title" \
  --description "Video description..." \
  --tags "tag1,tag2,tag3" \
  --category 22 \
  --privacy public \
  --thumbnail thumbnail.jpg
```

**Download a video:**
```bash
./youtube --download "https://youtube.com/watch?v=VIDEO_ID" --output ./videos
```

**List recent videos:**
```bash
./youtube --list --limit 10
```

## 📊 Categories

Available YouTube categories:
- 22 = People & Blogs (default)
- 1 = Film & Animation
- 2 = Autos & Vehicles
- 10 = Music
- 15 = Pets & Animals
- 17 = Sports
- 20 = Gaming
- 23 = Comedy
- 24 = Entertainment
- 25 = News & Politics
- 26 = Howto & Style
- 27 = Education
- 28 = Science & Technology

## 🔐 Privacy Options

- **public** - Visible to everyone
- **unlisted** - Only people with link can view
- **private** - Only you can view

## 📦 Dependencies

All dependencies are automatically installed by the installers:

- PyQt6 - GUI framework
- google-api-python-client - YouTube API
- google-auth-oauthlib - OAuth authentication
- google-auth-httplib2 - HTTP transport
- yt-dlp - Video downloader

## 🔧 System Requirements

- **Python:** 3.8 or higher
- **Operating System:** macOS 10.14+ or Windows 10+
- **Internet:** Required for uploads/downloads
- **Disk Space:** ~100 MB for dependencies

## 📚 Documentation

- **Desktop App:** `desktop-app/README.md`
- **Quick Start:** `desktop-app/QUICKSTART.md`
- **Detailed Guide:** `desktop-app/DESKTOP_APP.md`
- **CLI Setup:** `cli-tool/YOUTUBE_SETUP.md`
- **CLI Reference:** `cli-tool/QUICKREF.md`

## 🎨 Screenshots

The desktop app features:
- 📤 Upload tab with metadata forms
- 📥 Download tab
- 📋 Manage tab for your videos
- ⚙️ Settings tab for authentication

## 🔐 Security

- Uses OAuth 2.0 for secure authentication
- No API keys stored in code
- Credentials encrypted in token.json
- Respects Google's security policies

## 🆘 Troubleshooting

### "Not authenticated" error
- Go to Settings tab (desktop) or run `./youtube --auth` (CLI)
- Follow browser prompts

### "client_secrets.json not found"
- Create OAuth credentials (see Setup above)
- Save file to config directory
- Or use Browse button in Settings

### Upload fails
- Check internet connection
- Verify video format (MP4 recommended)
- Ensure title is not empty
- Check authentication status

## 📝 License

MIT License - Free to use for personal and commercial projects.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📞 Support

For detailed instructions, check the documentation in the respective folders.

---

**Made with ❤️ for content creators everywhere.**

🚀 **Start uploading today!**
