#!/bin/bash
# YouTube Upload Tool - Desktop App Installer (macOS)

set -e

echo "🎬 YouTube Upload Tool - Desktop App Installer"
echo "=============================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet PyQt6 google-api-python-client google-auth-oauthlib google-auth-httplib2 yt-dlp

echo "✅ Dependencies installed"

# Create launcher script
echo ""
echo "🚀 Creating launcher script..."

cat > youtube-uploader << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 youtube_uploader.py
EOF

chmod +x youtube-uploader

echo "✅ Launcher script created"

# Create config directory
CONFIG_DIR="$HOME/.youtube_uploader"
mkdir -p "$CONFIG_DIR"

echo ""
echo "✅ Installation complete!"
echo ""
echo "📁 Configuration directory: $CONFIG_DIR"
echo ""
echo "🚀 To launch the app:"
echo "   ./youtube-uploader"
echo ""
echo "📖 Next steps:"
echo "   1. Create OAuth credentials at https://console.cloud.google.com/"
echo "   2. Save client_secrets.json to: $CONFIG_DIR"
echo "   3. Open the app and click 'Authenticate with YouTube'"
echo ""
echo "📖 Full guide: DESKTOP_APP.md"
