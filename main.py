import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
from PIL import Image
import os

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()  # Variable for output PDF name
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        
        self.initialize_ui()

    def initialize_ui(self):
        # Title label
        title_label = tk.Label(self.root, text="Image To PDF Converter", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Select Images button
        select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        select_images_button.pack(pady=(0, 10))

        # Selected images listbox
        self.selected_images_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        # Output PDF name entry
        label = tk.Label(self.root, text="Enter Output PDF Name:")
        label.pack()
        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify='center')
        pdf_name_entry.pack()

        # Convert button
        convert_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_images_to_pdf)
        convert_button.pack(pady=(20, 40))

    def select_images(self):
        # Select multiple images and update listbox
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("image files", "*.png;*.jpg;*.jpeg")])
        self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        # Update listbox with selected images
        self.selected_images_listbox.delete(0, tk.END)
        for image_path in self.image_paths:
            _, image_name = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END, image_name)

    def convert_images_to_pdf(self):
        # Check if any images are selected
        if not self.image_paths:
            print("No images selected")
            return
        
        # Get output PDF path from user input or use default
        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"
        
        pdf = canvas.Canvas(output_pdf_path)
        
        # Set available width and height
        available_width = 540
        available_height = 720

        for image_path in self.image_paths:
            img = Image.open(image_path)
            scale_factor = min(available_width / img.width, available_height / img.height)
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor

            # Center the image on the page
            x_centered = (612 - new_width) / 2
            y_centered = (792 - new_height) / 2

            # Set background color and draw the image
            pdf.setFillColorRGB(1, 1, 1)  # White background
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawImage(image_path, x_centered, y_centered, width=new_width, height=new_height)
            pdf.showPage()
        
        pdf.save()
        print(f"PDF saved to {output_pdf_path}")

# Main function to start the application
def main():
    root = tk.Tk()
    root.title("Image to PDF")
    converter = ImageToPDFConverter(root)
    root.geometry("400x600")
    root.mainloop()

# Run the application
if __name__ == "__main__":
    main()
