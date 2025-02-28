# ASCII Art Generator

This project is an **ASCII Art Generator** that converts images into colored ASCII art. It features a **graphical user interface (GUI)** built with **Tkinter**, allowing users to upload images, convert them to ASCII art, and save the results.

## Features

- 📂 **Image Upload**: Upload any image file (**JPG, JPEG, PNG**) to convert it into ASCII art.
- 🎨 **Colored ASCII Art**: Generates ASCII art with **colored characters** based on the original image's colors.
- 📏 **Resizable Output**: Maintains the **aspect ratio** of the original image while resizing.
- 💾 **Save Functionality**: Save the generated **ASCII art** as a PNG file.
- 🖥️ **User-Friendly GUI**: Easy-to-use interface for uploading images and saving ASCII art.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/ascii-art-generator.git
   cd ascii-art-generator
   ```
2. **Install the required dependencies**:
   ```sh
   pip install pillow tk
   ```

## Usage

1. **Run the application**:
   ```sh
   python ascii_art_generator.py
   ```
2. **Use the GUI** to:
   - Upload an image.
   - View the generated ASCII art.
   - Save it as an image file.

## Code Overview

### 📌 Main Functions

- `resize_image(image, new_width=100)`: Resizes the image while maintaining the aspect ratio.
- `pixels_to_colored_ascii(image, color_chars=COLOR_CHARS)`: Converts image pixels to a string of **colored ASCII characters**.
- `create_colored_ascii_art(ascii_data, output_path, font_path="arial.ttf", font_size=12)`: Creates an image from ASCII data and saves it.
- `convert_image_to_colored_ascii(image_path, output_path, new_width=100)`: Converts an image to **colored ASCII art** and saves it.

### 🖼️ GUI Application

- `ASCIIArtApp`: The main class for the **Tkinter GUI application**.
  - Allows users to upload images.
  - Displays the generated **ASCII art**.
  - Provides an option to save the output.

## Example

🔹 **Example ASCII Art Output**

_(Add a sample ASCII image or screenshot of the GUI here)_

## Contributing

🚀 Contributions are **welcome**! If you have suggestions, improvements, or bug fixes:

- Open an **issue**.
- Submit a **pull request**.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **[Pillow](https://python-pillow.org/)** - Python Imaging Library (PIL) fork used for image processing.
- **Tkinter** - Standard Python interface to the Tk GUI toolkit.

---
📢 If you like this project, don't forget to ⭐ the repo!

