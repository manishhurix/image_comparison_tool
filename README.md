# Image Comparison Tool

A comprehensive Python tool for comparing images using structural similarity analysis. Features both command-line interface (CLI) and web-based interface using Streamlit.

## Features

- **Structural Similarity Index (SSIM)** for accurate image comparison
- **Automatic image resizing** to handle different dimensions
- **Visual difference highlighting** with color-coded output
- **Multiple interface options**: CLI and Web UI
- **Batch processing** support for multiple image pairs
- **Detailed analysis** including similarity scores and difference percentages
- **Export capabilities** for difference images and reports

## Installation

1. **Clone or download the project:**
   ```bash
   git clone <repository-url>
   cd image_compare
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface (CLI)

#### Basic Usage
```bash
# Compare two images
python main.py image1.jpg image2.jpg

# Compare with difference image saving
python main.py image1.jpg image2.jpg --save-diff

# Specify custom output path
python main.py image1.jpg image2.jpg --save-diff --output custom_diff.png
```

#### Advanced CLI Usage
```bash
# Single comparison mode
python main.py single image1.jpg image2.jpg --save-diff

# Batch comparison mode
python main.py batch folder1/ folder2/ --output-dir results/

# Help
python main.py --help
```

#### Batch Processing
```bash
# Compare all images in two folders
python main.py batch images_folder1/ images_folder2/
```

### Web Interface

1. **Launch the web app:**
   ```bash
   streamlit run web_app.py
   ```

2. **Open your browser** and navigate to the provided URL (usually `http://localhost:8501`)

3. **Upload two images** and view the comparison results

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)

## Output

### CLI Output Example
```
Comparing images:
  Image 1: image1.jpg
  Image 2: image2.jpg
--------------------------------------------------
Image Comparison Results:
========================
Are images identical: False
Similarity score: 85.67%
Difference percentage: 14.33%

Original image shapes:
- Image 1: (800, 600, 3)
- Image 2: (1024, 768, 3)

Resized to common shape: (800, 600, 3)
Difference image saved to: diff_output/diff.png
```

### Web Interface Features
- **Real-time comparison** with visual feedback
- **Side-by-side image display**
- **Color-coded similarity indicators**
- **Downloadable results** (difference images and reports)
- **Detailed metrics** and analysis

## Project Structure

```
image_compare/
├── main.py              # CLI entry point
├── comparator.py        # Core comparison logic
├── utils.py            # Utility functions
├── web_app.py          # Streamlit web interface
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── diff_output/       # Output directory for diff images
```

## Technical Details

### Core Components

1. **ImageComparator Class** (`comparator.py`)
   - Handles image loading and preprocessing
   - Performs SSIM-based comparison
   - Generates visual difference images
   - Supports batch processing

2. **Utility Functions** (`utils.py`)
   - Image loading and validation
   - Automatic resizing to common dimensions
   - Format conversion and saving
   - Side-by-side comparison creation

3. **CLI Interface** (`main.py`)
   - Argument parsing with argparse
   - Support for single and batch modes
   - Error handling and user feedback

4. **Web Interface** (`web_app.py`)
   - Modern Streamlit-based UI
   - Real-time image upload and comparison
   - Interactive results display
   - Download functionality

### Algorithm

The tool uses **Structural Similarity Index (SSIM)** from scikit-image:

1. **Image Preprocessing:**
   - Load images using OpenCV
   - Resize to smallest common dimensions
   - Convert to grayscale for SSIM calculation

2. **Similarity Calculation:**
   - Compute SSIM score (0-1 range)
   - Convert to percentage (0-100%)
   - Calculate difference percentage

3. **Visual Difference Generation:**
   - Create color-coded difference map
   - Highlight changes in red
   - Blend with original image for clarity

## Examples

### Example 1: Identical Images
```bash
python main.py identical1.jpg identical2.jpg
```
**Output:** Similarity: 100%, Difference: 0%

### Example 2: Similar Images
```bash
python main.py similar1.jpg similar2.jpg --save-diff
```
**Output:** Similarity: 85%, Difference: 15%

### Example 3: Different Images
```bash
python main.py different1.jpg different2.jpg
```
**Output:** Similarity: 45%, Difference: 55%

## Advanced Features

### Batch Processing
Compare multiple image pairs from two folders:
```bash
python main.py batch folder1/ folder2/ --output-dir results/
```

### Custom Output Paths
```bash
python main.py image1.jpg image2.jpg --save-diff --output custom_path/diff.png
```

### Web Interface Features
- **Real-time preview** of uploaded images
- **Automatic dimension detection**
- **Color-coded similarity indicators**
- **Expandable detailed information**
- **Export functionality**

## Troubleshooting

### Common Issues

1. **"Image file not found"**
   - Ensure image paths are correct
   - Check file permissions

2. **"Unsupported image format"**
   - Use supported formats: JPG, PNG, BMP, TIFF
   - Check file extensions

3. **"Cannot load image"**
   - Verify image files are not corrupted
   - Try with different images

4. **Streamlit not starting**
   - Ensure all dependencies are installed
   - Check if port 8501 is available

### Performance Tips

- **Large images** are automatically resized for faster processing
- **Batch processing** is optimized for multiple comparisons
- **Web interface** provides real-time feedback during processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Dependencies

- **opencv-python**: Image processing and I/O
- **scikit-image**: SSIM calculation and image analysis
- **numpy**: Numerical operations
- **streamlit**: Web interface
- **Pillow**: Additional image handling support

## Version History

- **v1.0.0**: Initial release with CLI and web interfaces
- Features: SSIM comparison, visual diff, batch processing 