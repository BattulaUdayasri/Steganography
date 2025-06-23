import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from PIL import Image, ImageTk
import os

from aes_encryption import encrypt_message, decrypt_message
from steganography import encode_image, decode_image

class StegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Secure Image Steganography GUI")
        self.root.geometry("700x600")
        self.image_path = None

        # Message
        tk.Label(root, text="🔏 Message to hide:", font=("Arial", 12)).pack()
        self.message_entry = ScrolledText(root, width=80, height=5)
        self.message_entry.pack(pady=5)

        # Password
        tk.Label(root, text="🔑 Password for encryption:", font=("Arial", 12)).pack()
        self.password_entry = tk.Entry(root, show="*", width=50)
        self.password_entry.pack(pady=5)

        # Image preview
        self.preview_label = tk.Label(root)
        self.preview_label.pack()

        # Buttons
        tk.Button(root, text="📂 Select Image", command=self.select_image).pack(pady=5)
        tk.Button(root, text="🔐 Encrypt & Hide", command=self.encrypt_and_hide).pack(pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(pady=5)

        # Extracted message
        tk.Label(root, text="🧾 Extracted Message:", font=("Arial", 12)).pack()
        self.output_text = ScrolledText(root, width=80, height=5)
        self.output_text.pack(pady=5)

        tk.Button(root, text="🔍 Extract & Decrypt", command=self.extract_and_decrypt).pack(pady=5)

        # Drag-and-drop
        #self.root.bind("<Drag>", lambda e: "break")
        #self.root.bind("<Drop>", self.drop_image)

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg")])
        if path:
            self.image_path = path
            self.show_image(path)
            messagebox.showinfo("Image Selected", path)

    def drop_image(self, event):
        self.image_path = event.data
        self.show_image(self.image_path)

    def show_image(self, path):
        img = Image.open(path)
        img.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(img)
        self.preview_label.config(image=photo)
        self.preview_label.image = photo

    def encrypt_and_hide(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image.")
            return

        msg = self.message_entry.get("1.0", tk.END).strip()
        password = self.password_entry.get()
        if not msg or not password:
            messagebox.showerror("Error", "Message and password are required.")
            return

        try:
            self.progress.start(10)
            encrypted = encrypt_message(msg, password)
            output_path = os.path.splitext(self.image_path)[0] + "_output.png"
            encode_image(self.image_path, encrypted, output_path)
            self.progress.stop()
            messagebox.showinfo("Success", f"Message hidden in:\n{output_path}")
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Error", str(e))

    def extract_and_decrypt(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image.")
            return

        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Enter password to decrypt.")
            return

        try:
            self.progress.start(10)
            extracted = decode_image(self.image_path)
            decrypted = decrypt_message(extracted, password)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, decrypted)
            self.progress.stop()
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Error", "Wrong password or no message found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()
