# 🎬 YouTube Upload Tool - Complete Solution

## ✅ What's Been Created

A complete YouTube upload/download solution with **three tools**:

### 1. CLI Tool (Command Line)
**Location:** `/Users/nguyennghia/.openclaw/workspace/tools/youtube`

- Upload videos from terminal
- Download videos from YouTube
- List channel videos
- Great for automation and scripts

### 2. Desktop GUI Application (macOS & Windows)
**Location:** `/Users/nguyennghia/.openclaw/workspace/tools/youtube-uploader-desktop/`

- Beautiful PyQt6 GUI
- Upload with metadata forms
- Download any YouTube video
- Manage your uploads
- Real-time progress tracking
- Cross-platform (macOS + Windows)

### 3. OpenClaw Skill
**Location:** `~/.openclaw/skills/youtube/SKILL.md`

- Integration with OpenClaw
- Can be used in automated workflows
- Scriptable and programmable

## 🚀 Quick Start

### Desktop App (Recommended for Most Users)

**macOS:**
```bash
cd /Users/nguyennghia/.openclaw/workspace/tools/youtube-uploader-desktop
./install.sh
./youtube-uploader
```

**Windows:**
Double-click `install.bat`, then double-click `youtube-uploader.bat`

### CLI Tool (For Automation)

```bash
cd /Users/nguyennghia/.openclaw/workspace/tools
./youtube --upload video.mp4 --title "My Video"
```

## 📖 Setup (One-Time)

### Step 1: Create OAuth Credentials

1. Go to https://console.cloud.google.com/
2. Create project → Enable "YouTube Data API v3"
3. Create OAuth client ID → **Desktop app**
4. Download JSON file

### Step 2: Save Credentials

**macOS:** `~/.youtube_uploader/client_secrets.json`
**Windows:** `C:\Users\YourName\.youtube_uploader\client_secrets.json`

### Step 3: Authenticate

**Desktop App:** Settings tab → "Authenticate with YouTube"  
**CLI:** `./youtube --auth`

## 🎯 Features Comparison

| Feature | CLI Tool | Desktop App |
|---------|----------|-------------|
| Upload Videos | ✅ | ✅ |
| Download Videos | ✅ | ✅ |
| List Videos | ✅ | ✅ |
| GUI | ❌ | ✅ |
| Progress Bar | ❌ | ✅ |
| Thumbnail Upload | ✅ | ✅ |
| Metadata Forms | ❌ | ✅ |
| Batch Upload | ✅ | ❌ |
| Automation | ✅ | ❌ |
| Cross-Platform | ✅ | ✅ |

## 📁 File Structure

```
.openclaw/workspace/tools/
├── youtube                          # CLI tool
│   ├── youtube                      # Wrapper script
│   ├── youtube-upload.py            # Python script
│   ├── YOUTUBE_SETUP.md             # Setup guide
│   ├── QUICKREF.md                  # Quick reference
│   └── venv/                        # Python env
│
└── youtube-uploader-desktop/        # Desktop app
    ├── youtube_uploader.py          # Main app
    ├── install.sh                   # macOS installer
    ├── install.bat                  # Windows installer
    ├── youtube-uploader             # macOS launcher
    ├── README.md                    # Full docs
    ├── QUICKSTART.md                # Quick start
    ├── DESKTOP_APP.md              # Detailed guide
    └── venv/                        # Python env
```

## 🎬 Usage Examples

### Desktop App

**Upload:**
1. Open app → 📤 Upload tab
2. Browse video file
3. Enter title, description, tags
4. Click "🚀 Upload to YouTube"

**Download:**
1. Open app → 📥 Download tab
2. Paste YouTube URL
3. Click "📥 Download Video"

**Manage:**
1. Open app → 📋 Manage tab
2. Click "📋 Load My Videos"
3. Select and open videos

### CLI Tool

**Upload:**
```bash
./youtube --upload video.mp4 \
  --title "My Video" \
  --description "Description..." \
  --tags "tag1,tag2" \
  --category 22 \
  --privacy public
```

**Download:**
```bash
./youtube --download "https://youtube.com/watch?v=ID" --output ./videos
```

**List:**
```bash
./youtube --list --limit 10
```

## 🎨 Desktop App Features

### 📤 Upload Tab
- Video file browser
- Title input (required)
- Description textarea
- Tags input (comma-separated)
- Category dropdown (13 categories)
- Privacy selector (public/unlisted/private)
- Thumbnail browser
- Real-time progress bar
- Status messages

### 📥 Download Tab
- YouTube URL input
- Output directory browser
- Download button

### 📋 Manage Tab
- Load recent videos
- Video list with titles and URLs
- Open in browser

### ⚙️ Settings Tab
- Authentication status
- OAuth authentication button
- Client secrets browser
- Help instructions

## 🔐 Security

- OAuth 2.0 authentication (no API keys in code)
- Credentials stored locally
- Secure token storage
- Respects Google's security policies

## 📊 System Requirements

- **Python:** 3.8+
- **OS:** macOS 10.14+ or Windows 10+
- **Internet:** Required
- **Disk:** ~100 MB for dependencies

## 📦 Dependencies

All automatically installed:
- PyQt6 (GUI)
- google-api-python-client (YouTube API)
- google-auth-oauthlib (OAuth)
- yt-dlp (downloader)

## 🎯 Best Use Cases

### Use Desktop App When:
- You prefer visual interfaces
- Need to upload occasionally
- Want to manage videos visually
- Like progress bars and status updates

### Use CLI Tool When:
- Automating uploads
- Batch processing
- Scripting workflows
- Integrating with other tools
- Working with OpenClaw automation

## 📚 Documentation

- **CLI Tool:** `tools/YOUTUBE_SETUP.md`, `tools/QUICKREF.md`
- **Desktop App:** `tools/youtube-uploader-desktop/README.md`
- **Quick Start:** `tools/youtube-uploader-desktop/QUICKSTART.md`
- **OpenClaw Skill:** `skills/youtube/SKILL.md`

## 🎉 Next Steps

1. **Choose your tool:**
   - Desktop app for GUI
   - CLI for automation

2. **Complete setup:**
   - Create OAuth credentials
   - Save client_secrets.json
   - Authenticate

3. **Start uploading!**
   - Desktop: Open app and browse video
   - CLI: Run `./youtube --upload video.mp4 --title "Title"`

## 🆘 Troubleshooting

**Issues?** Check the relevant documentation:
- Desktop app: `DESKTOP_APP.md`
- CLI tool: `YOUTUBE_SETUP.md`
- OAuth: Click "Help" in Settings tab

---

**All tools ready to use!** Just complete OAuth setup once, then upload away! 🚀
