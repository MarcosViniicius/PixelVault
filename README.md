# Image Steganography Tool

Hide text messages and files inside PNG images using LSB (Least Significant Bit) steganography. Data remains invisible to the human eye while being fully recoverable.

## Features

- 📝 **Hide text messages** with title and metadata
- 📁 **Hide any file type** (documents, PDFs, archives, etc.)
- 🖼️ **Multi-image support** - automatically splits large data
- 🔄 **Dual extraction** - from images or Base64 backup file
- 🎨 **Auto carrier images** - downloads random dog images as carriers
- 📊 **Progress tracking** - visual feedback during operations
- 💾 **Organized output** - folders numbered by type (text_N, archive_N)

## Quick Start

### Installation
```bash
pip install -r requirements.txt
python main.py
```

### Requirements
- Python 3.7+
- Internet connection (for carrier images)
- Dependencies: `rich`, `stegano`, `Pillow`, `requests`

### Usage

**Option 1: Read/Extract**
- Choose folder (text_N or archive_N)
- Select extraction method (images or Base64 file)
- Data is reconstructed automatically

**Option 2: Hide Text**
- Enter title and text content
- Type `-- END --` to finish
- Images generated automatically

**Option 3: Hide File**
- Place file in `./input/files/`
- Select from menu
- File split across images + Base64 backup saved

## Output Structure

```
output/
├── text_1/              # Hidden text messages
│   ├── 1_output.png
│   └── 2_output.png
├── archive_1/           # Hidden files
│   ├── 1_output.png
│   ├── base64/
│   │   └── payload.txt  # Base64 backup
│   └── extracted_file.* # After extraction
└── temp/                # Temporary files
```

## How It Works

**LSB Steganography**: Modifies the least significant bits of RGB pixels to store data. Changes are imperceptible but fully recoverable.

**Capacity**: Each image holds ~70-280 KB depending on resolution.
```
Capacity = (Width × Height × 3) ÷ 8 × 0.75 safety factor
```

**Format**: Data stored as JSON with metadata (title/filename, part number, content).

## ⚠️ CRITICAL: Sharing & Storage

### 🚨 Data Loss Risk

**Hidden data is FRAGILE and DESTROYED by:**
- Image recompression or format conversion
- Messaging apps (WhatsApp, Telegram, Discord, etc.)
- Social media (Facebook, Instagram, Twitter, etc.)
- Cloud storage direct upload (Google Photos, iCloud, etc.)
- Email optimization, resizing, or JPEG conversion

### ✅ SAFE Methods

**1. Compress Before Sharing (RECOMMENDED)**
```bash
# Create encrypted archive
7z a -tzip -p -mem=AES256 hidden.zip ./output/text_1/*.png
```
Send as **document/file** (NOT as image):
- ✅ ZIP/RAR/7z archives
- ✅ Email attachments
- ✅ Cloud storage (as archive)
- ✅ Messaging apps (as document)

**2. Local Storage (SAFEST)**
- ✅ Hard drive/SSD/USB drives
- ✅ External storage
- ✅ Network storage (NAS)

**3. Verification**
Always test extraction after transfer:
- Extract data immediately
- Compare file hashes (MD5/SHA-256)
- Check file size hasn't changed

### ❌ NEVER
- Send raw PNG via messaging apps
- Upload to social media
- Convert to JPEG/WebP
- Edit images after hiding data
- Trust platforms without testing

### 💡 Recommended Workflow
```
1. Hide data → 2. Test locally → 3. Create ZIP archive → 
4. Send as document → 5. Recipient extracts → 6. Recipient recovers data
```

## Technical Details

**Data Format:**
```json
// Text
{"title": "...", "part": 1, "total": 3, "text": "..."}

// File
{"filename": "...", "part": 1, "total": 5, "data": "base64..."}
```

**Image Processing:**
- PNG format only (lossless)
- RGB color mode
- Dog CEO API for carrier images
- UTF-8 character boundary respect

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No hidden data found | Image was recompressed or modified |
| Network error | Check internet, Dog API may be down |
| File extraction fails | Missing parts or try Base64 extraction |
| Data loss after sharing | ❌ Cannot recover - use ZIP archives next time |
| Folder not found | Create `input/files/` manually |

## Project Structure

```
metadados/
├── main.py              # Menu & navigation
├── writer.py            # Hide text/files
├── reader.py            # Extract text/files
├── config.py            # Settings
├── helpers/             # Utilities
│   ├── image_helper.py
│   ├── text_helper.py
│   ├── file_helper.py
│   ├── byte_converter_helper.py
│   └── multiline_helper.py
├── input/files/         # Files to hide
└── output/              # Generated images
```

## Limitations

- PNG only (lossy formats destroy data)
- Detectable by steganalysis tools
- Requires internet for carrier images
- Not for highly sensitive data (add encryption separately)

## Use Cases

Secure communication • File concealment • Document backup • Digital watermarking • Privacy protection • Educational demos • Creative puzzles • Data archival

## Contributing

Welcome contributions: encryption integration, GUI, custom images, batch processing, additional formats, password protection.

## License & Credits

Educational and personal use. Built with [Stegano](https://github.com/cedricbonhomme/Stegano), [Rich](https://github.com/Textualize/rich), [Pillow](https://python-pillow.org/), [Dog CEO API](https://dog.ceo/dog-api/).

---

⚠️ **For educational purposes. Users responsible for legal compliance.**
