# 🎬 YouTube Upload Tool - Desktop Application

Beautiful cross-platform desktop GUI for uploading and downloading YouTube videos.

![YouTube Upload Tool](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-Free-orange)

## ✨ Features

✅ **Modern GUI** - Beautiful PyQt6 interface with tabs and forms  
✅ **Upload Videos** - Direct upload to YouTube with full metadata support  
✅ **Download Videos** - Download from any YouTube URL  
✅ **Manage Videos** - List, view, and open your uploaded videos  
✅ **OAuth Authentication** - Secure browser-based authentication  
✅ **Progress Tracking** - Real-time upload/download progress  
✅ **Cross-Platform** - Works on macOS and Windows  
✅ **Thumbnail Support** - Upload custom thumbnails  
✅ **Privacy Control** - Choose public, unlisted, or private  

## 🚀 Quick Start

### macOS

```bash
cd /Users/nguyennghia/.openclaw/workspace/tools/youtube-uploader-desktop
./install.sh
./youtube-uploader
```

### Windows

Double-click `install.bat`, then double-click `youtube-uploader.bat`

## 📖 Setup (One-Time)

### Step 1: Create OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3":
   - APIs & Services → Library → Search "YouTube Data API v3" → Enable
4. Create OAuth 2.0 credentials:
   - APIs & Services → Credentials → Create Credentials → OAuth client ID
   - Application type: **Desktop app**
   - Name: "YouTube Upload Tool"
   - Click "Create" and download the JSON file

### Step 2: Save Credentials

**macOS:** Save as `~/.youtube_uploader/client_secrets.json`  
**Windows:** Save as `C:\Users\YourName\.youtube_uploader\client_secrets.json`

Or use the **Browse** button in the app's Settings tab!

### Step 3: Authenticate

1. Open the app
2. Go to **⚙️ Settings** tab
3. Click **🔑 Authenticate with YouTube**
4. Sign in when browser opens
5. Grant permissions

Done! You're ready to upload! 🎉

## 🎯 How to Use

### Upload Videos

1. Go to **📤 Upload** tab
2. Click **Browse** to select video file (MP4, MOV, AVI, MKV, WebM)
3. Enter **Title** (required)
4. Add **Description** (optional)
5. Add **Tags** (optional, comma-separated)
6. Choose **Category** (default: People & Blogs)
7. Choose **Privacy** (public/unlisted/private)
8. Add **Thumbnail** (optional, JPG/PNG/WebP)
9. Click **🚀 Upload to YouTube**
10. Watch the progress bar and wait for completion!

### Download Videos

1. Go to **📥 Download** tab
2. **Paste YouTube URL**
3. **Choose save location** (default: Downloads)
4. Click **📥 Download Video**
5. Wait for download to complete

### Manage Your Videos

1. Go to **📋 Manage** tab
2. Click **📋 Load My Videos**
3. Browse your recent uploads
4. **Select** a video
5. Click **🔗 Open Selected Video** to open in browser

### Settings

1. Go to **⚙️ Settings** tab
2. Check **authentication status**
3. Click **🔑 Authenticate with YouTube** if needed
4. Use **Browse** button to add client_secrets.json
5. Click **📖 Help** for OAuth setup instructions

## 📁 File Locations

**Config Directory:**
- **macOS:** `~/.youtube_uploader/`
- **Windows:** `C:\Users\YourName\.youtube_uploader\`

**Files:**
- `client_secrets.json` - OAuth credentials (you create this)
- `token.json` - Saved authentication token (auto-created)

## 🎨 Screenshots

The app has 4 beautiful tabs:

### 📤 Upload Tab
- Video file browser
- Metadata forms (title, description, tags)
- Category dropdown (13 categories)
- Privacy selector
- Thumbnail browser
- Progress bar with status

### 📥 Download Tab
- YouTube URL input
- Output directory browser
- Download button

### 📋 Manage Tab
- Load recent videos
- Video list with titles and URLs
- Open in browser button

### ⚙️ Settings Tab
- Authentication status
- OAuth authentication button
- Client secrets configuration
- Help instructions

## 🔧 System Requirements

- **Python:** 3.8 or higher
- **Operating System:** macOS 10.14+ or Windows 10+
- **Internet:** Required for uploads/downloads
- **Disk Space:** 100 MB for dependencies

## 📦 Dependencies

- PyQt6 - GUI framework
- google-api-python-client - YouTube API
- google-auth-oauthlib - OAuth authentication
- google-auth-httplib2 - HTTP transport
- yt-dlp - Video download

All dependencies are automatically installed by the installer.

## 🎯 Supported Formats

**Upload:**
- Video: MP4, MOV, AVI, MKV, WebM (MP4 recommended)
- Thumbnail: JPG, JPEG, PNG, WebP (1280x720 recommended)

**Download:**
- All YouTube video formats
- Best quality selected by default

## 📊 Categories

1. People & Blogs (default)
2. Film & Animation
3. Autos & Vehicles
4. Music
5. Pets & Animals
6. Sports
7. Gaming
8. Comedy
9. Entertainment
10. News & Politics
11. Howto & Style
12. Education
13. Science & Technology

## 🔐 Privacy Options

- **Public** - Visible to everyone on YouTube
- **Unlisted** - Only people with the link can view
- **Private** - Only you can view

## ❓ Troubleshooting

### "Not authenticated" error

**Solution:**
1. Go to Settings tab
2. Click "Authenticate with YouTube"
3. Follow browser prompts

### "client_secrets.json not found"

**Solution:**
1. Create OAuth credentials (see Setup above)
2. Save file to config directory
3. Or use "Browse for client_secrets.json" button in Settings

### Upload fails

**Solutions:**
- Check internet connection
- Verify video file format (MP4 recommended)
- Ensure title is not empty
- Check file size (YouTube limit: 256 GB or 12 hours)
- Verify authentication status

### Download fails

**Solutions:**
- Verify YouTube URL is correct
- Check internet connection
- Ensure output directory exists
- Try different video URL

### App won't open

**Solutions:**
- Ensure Python 3.8+ is installed
- Reinstall dependencies: `./install.sh` or `install.bat`
- Check console for error messages

## 🔐 Security

- Uses OAuth 2.0 for secure authentication
- No API keys stored in code
- Credentials encrypted in token.json
- Respects Google's security policies

## 📜 License

Free to use for personal and commercial projects.

## 🆘 Support

For detailed instructions:
- See `QUICKSTART.md` - Quick start guide
- See `DESKTOP_APP.md` - Full documentation
- Click **📖 Help** button in app's Settings tab

## 🎉 Credits

Built with:
- PyQt6 - Beautiful Python GUI framework
- Google APIs - YouTube Data API v3
- yt-dlp - Powerful video downloader

---

**Enjoy uploading! 🚀**

Made with ❤️ for content creators everywhere.
