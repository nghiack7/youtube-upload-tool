# YouTube Upload Tool - Quick Start

## 🚀 Quick Installation

### macOS

```bash
cd /Users/nguyennghia/.openclaw/workspace/tools/youtube-uploader-desktop
chmod +x install.sh
./install.sh
```

Then run:
```bash
./youtube-uploader
```

### Windows

Double-click `install.bat`, then double-click `youtube-uploader.bat`

## 📖 Setup (One-Time)

### 1. Create OAuth Credentials

1. Go to https://console.cloud.google.com/
2. Create project → Enable "YouTube Data API v3"
3. Create OAuth client ID → **Desktop app**
4. Download JSON file

### 2. Save Credentials

**macOS:** Save as `~/.youtube_uploader/client_secrets.json`
**Windows:** Save as `C:\Users\YourName\.youtube_uploader\client_secrets.json`

Or use the **Browse** button in the app's Settings tab!

### 3. Authenticate

1. Open the app
2. Go to **⚙️ Settings** tab
3. Click **🔑 Authenticate with YouTube**
4. Sign in when browser opens

## 🎬 Upload Your First Video

1. **📤 Upload tab**
2. **Browse** for video file
3. **Enter title** (required)
4. Add description, tags if you want
5. **Click "🚀 Upload to YouTube"**

That's it! 🎉

## 📥 Download Videos

1. **📥 Download tab**
2. **Paste YouTube URL**
3. **Choose save location**
4. **Click "📥 Download Video"**

## 📋 Manage Your Videos

1. **📋 Manage tab**
2. **Click "📋 Load My Videos"**
3. **Select** and **Open** any video

## 🎨 App Features

✅ Beautiful, modern GUI
✅ Upload with metadata (title, description, tags, thumbnail)
✅ Download any YouTube video
✅ List and manage your uploads
✅ Real-time upload progress
✅ Secure OAuth authentication
✅ Works on macOS and Windows

## 📁 File Locations

**Config Directory:**
- macOS: `~/.youtube_uploader/`
- Windows: `C:\Users\YourName\.youtube_uploader\`

**Files:**
- `client_secrets.json` - OAuth credentials (you create)
- `token.json` - Saved auth token (auto-created)

## ❓ Need Help?

Check the full guide: `DESKTOP_APP.md`

Or click the **📖 Help** button in the app's Settings tab!

---

**Enjoy uploading! 🚀**
