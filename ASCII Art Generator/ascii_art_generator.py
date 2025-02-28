from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

COLOR_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", "."]
# COLOR_CHARS = ["0", "1", "*", "+", "-", "."]


# Resize image according to a new width while maintaining aspect ratio
def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

# Convert pixels to a string of colored ASCII characters
def pixels_to_colored_ascii(image, color_chars=COLOR_CHARS):
    pixels = image.load()
    width, height = image.size
    ascii_str = []

    for y in range(height):
        line = []
        for x in range(width):
            r, g, b = pixels[x, y]
            # Calculate grayscale value
            gray = (r + g + b) // 3
            # Select colored character
            char = color_chars[gray * len(color_chars) // 256]
            # Store character and color together
            line.append((char, (r, g, b)))
        ascii_str.append(line)

    return ascii_str

# Create colored ASCII art
def create_colored_ascii_art(ascii_data, output_path, font_path="arial.ttf", font_size=12):
    # Load font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    # Create output image
    line_height = font.getbbox("A")[3] - font.getbbox("A")[1]
    img_width = max(len(line) for line in ascii_data) * font_size
    img_height = len(ascii_data) * line_height
    image = Image.new("RGB", (img_width, img_height), color="white")
    draw = ImageDraw.Draw(image)

    # Draw colored characters
    y = 0
    for line in ascii_data:
        x = 0
        for char, color in line:
            draw.text((x, y), char, fill=color, font=font)
            x += font_size
        y += line_height

    # Save output image
    image.save(output_path)
    return image

# Convert image to colored ASCII art
def convert_image_to_colored_ascii(image_path, output_path, new_width=100):
    image = Image.open(image_path)
    resized_image = resize_image(image, new_width)
    ascii_data = pixels_to_colored_ascii(resized_image)
    return create_colored_ascii_art(ascii_data, output_path)

# GUI Application
class ASCIIArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Generator")
        self.root.geometry("800x600")

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(root, text="Save ASCII Art", command=self.save_ascii_art, state=tk.DISABLED)
        self.save_button.pack(pady=20)

        self.image_path = None
        self.ascii_image = None
        self.original_image = None

        self.root.bind("<Configure>", self.on_resize)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            self.ascii_image = convert_image_to_colored_ascii(self.image_path, "temp_ascii_image.png")
            self.original_image = self.ascii_image.copy()
            self.display_image(self.ascii_image)
            self.save_button.config(state=tk.NORMAL)

    def display_image(self, image):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        image_width, image_height = image.size

        if image_width > canvas_width or image_height > canvas_height:
            ratio = min(canvas_width / image_width, canvas_height / image_height)
            new_width = int(image_width * ratio)
            new_height = int(image_height * ratio)
            image = image.resize((new_width, new_height), Image.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_resize(self, event):
        if self.original_image:
            self.display_image(self.original_image)

    def save_ascii_art(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            self.ascii_image.save(save_path)
            messagebox.showinfo("Success", "ASCII Art saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ASCIIArtApp(root)
    root.mainloop()