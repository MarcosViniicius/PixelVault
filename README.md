# Image Text Writer

A Python-based steganography tool that enables you to hide and retrieve text messages within PNG images using the LSB (Least Significant Bit) technique. This application provides a secure and invisible way to embed text data into images without perceptible quality loss.

## Overview

Image Text Writer is a command-line application that leverages steganography to conceal textual information within digital images. By modifying the least significant bits of pixel RGB values, it embeds data in a way that remains invisible to the human eye while maintaining the image's visual integrity.

The tool automatically handles large text content by splitting it across multiple images, manages metadata for proper reconstruction, and provides an intuitive interface for both hiding and extracting hidden messages.

## Key Features

### Text Embedding
- **Automatic Image Acquisition**: Downloads random dog images from an external API to serve as carrier images
- **Multi-Image Support**: Automatically splits large text content across multiple images when needed
- **Smart Capacity Calculation**: Estimates image capacity and determines the required number of images
- **Metadata Management**: Stores title, part number, and total parts for accurate message reconstruction
- **Organized Output**: Creates numbered folders with sequential image files for easy organization
- **Real-Time Feedback**: Displays progress indicators during image generation
- **Safety Margins**: Implements buffer zones to prevent data corruption during embedding

### Text Extraction
- **Intelligent Reconstruction**: Reads and combines multi-part messages in the correct sequence
- **Data Validation**: Verifies integrity and reports missing or corrupted segments
- **Folder-Based Organization**: Manages multiple hidden messages through organized folder structure
- **Error Reporting**: Provides detailed diagnostics for troubleshooting issues
- **Complete Message Display**: Shows extracted title and full reconstructed text

### User Interface
- **Rich Terminal Interface**: Colorful, intuitive console interface using the Rich library
- **Interactive Menu System**: Clear navigation with visual feedback
- **Progress Indicators**: Real-time status updates for long operations
- **Multiline Input**: Custom text input with configurable termination marker
- **Formatted Displays**: Panel layouts and tables for enhanced readability

## How It Works

The application uses **LSB (Least Significant Bit) steganography** to hide text within PNG images. This technique works by:

1. Converting text to JSON format with metadata (title, part number, total parts)
2. Encoding the JSON data as bytes
3. Modifying the least significant bits of each RGB pixel value to store one bit of data
4. Saving the modified image as PNG (lossless format preserves hidden data)

The modifications are so subtle that they're imperceptible to human vision, making the hidden message effectively invisible while maintaining the image's visual quality.

### Embedding Process
1. User inputs title and text content
2. System downloads a random dog image from an API
3. Calculates the image's data capacity (with safety margin)
4. Splits text into chunks if it exceeds single-image capacity
5. Creates JSON payloads with metadata for each part
6. Embeds data using LSB steganography
7. Saves images in organized numbered folders

### Extraction Process
1. User selects a folder containing hidden message images
2. System locates all numbered output images (`1_output.png`, `2_output.png`, etc.)
3. Extracts hidden JSON data from each image
4. Validates and sorts parts by sequence number
5. Reconstructs and displays the complete original message

## Requirements

- Python 3.7 or higher
- Internet connection (for downloading carrier images)

### Dependencies
- `rich` - Terminal formatting and UI components
- `stegano` - LSB steganography implementation
- `Pillow` (PIL) - Image processing
- `requests` - HTTP requests for image downloads

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd metadados
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

### Main Menu Options

**Option 1: Read text from an existing image**
- Select a folder from the output directory
- The system will automatically detect and reconstruct hidden messages
- Multi-part messages are reassembled in the correct order

**Option 2: Create a new image and add text**
- Enter a title for your hidden message
- Paste or type your text content
- Type `-- END --` on a new line to finish input
- The system automatically generates the required images

**Press Enter: Exit the program**

## Output Structure

Generated images are stored in the `output` directory with the following structure:

```
output/
├── text_1/
│   ├── 1_output.png
│   ├── 2_output.png
│   └── ...
├── text_2/
│   ├── 1_output.png
│   └── ...
└── text_N/
    └── 1_output.png
```

- Each folder (e.g., `text_1`, `text_2`) contains one complete hidden message
- Images are numbered sequentially (`1_output.png`, `2_output.png`, etc.)
- Multiple images in a folder represent different parts of the same message

## Technical Details

### Capacity Calculation
The system calculates image capacity using the formula:
```
Capacity (bytes) = (Width × Height × 3 RGB channels ÷ 8 bits) × Safety Factor
```

Default safety factor: 0.75 (75% of theoretical capacity to ensure reliability)

### Text Splitting Algorithm
- Respects UTF-8 character boundaries
- Ensures no character is split across images
- Calculates byte size per character for accurate splitting
- Maintains encoding integrity throughout the process

### Data Format
Hidden data is stored as JSON:
```json
{
  "title": "Message Title",
  "part": 1,
  "total": 3,
  "text": "Portion of the hidden text..."
}
```

### Image Processing
- Converts all images to RGB color mode for consistency
- Uses PNG format (lossless compression preserves hidden data)
- Downloads carrier images from Dog API (https://dog.ceo/dog-api/)
- Implements error handling for network and file operations

## Use Cases

- **Secure Communication**: Hide sensitive messages in plain sight
- **Digital Watermarking**: Embed metadata or ownership information
- **Privacy Protection**: Conceal personal information in images
- **Educational Purposes**: Demonstrate steganography concepts
- **Creative Projects**: Create puzzles or treasure hunts with hidden clues
- **Data Archival**: Store text backups in image format

## Security Considerations

- LSB steganography is detectable by steganalysis tools
- Not suitable for highly sensitive or classified information
- Images should be transmitted via lossless channels (lossy compression destroys hidden data)
- Consider encrypting text before embedding for additional security
- Avoid using the same carrier image multiple times

## Limitations

- Only works with PNG images (lossless format required)
- Hidden data is lost if image is converted to lossy formats (JPEG, WebP with lossy compression)
- Large text requires multiple images
- Requires internet connection to download carrier images
- Detection possible with statistical analysis tools

## Project Structure

```
metadados/
├── main.py                  # Main application entry point and menu system
├── reader.py                # Image reading and text extraction logic
├── writer.py                # Image creation and text embedding logic
├── requirements.txt         # Python dependencies
├── helpers/
│   └── multiline_helper.py  # Multi-line text input handler
└── output/                  # Generated images with hidden messages
```

## Troubleshooting

**No hidden data found**
- Ensure you're reading images created by this tool
- Verify the image hasn't been compressed or modified

**Network errors**
- Check your internet connection
- The Dog API might be temporarily unavailable

**Text too large error**
- The system will automatically split text across multiple images
- If issues persist, try breaking text into smaller messages

**Folder not found**
- The `output` directory is created automatically on first use
- Ensure you have write permissions in the application directory

## Contributing

Contributions are welcome! Areas for improvement:
- Support for additional image formats
- Custom carrier image selection
- Encryption integration
- GUI interface
- Compression before embedding
- Password protection for hidden messages

## License

This project is provided as-is for educational and personal use.

## Acknowledgments

- Built with [Stegano](https://github.com/cedricbonhomme/Stegano) library
- UI powered by [Rich](https://github.com/Textualize/rich)
- Image processing via [Pillow](https://python-pillow.org/)
- Carrier images from [Dog CEO API](https://dog.ceo/dog-api/)

---

**Note**: This tool is designed for educational purposes and legitimate use cases. Users are responsible for ensuring their use complies with applicable laws and regulations.
