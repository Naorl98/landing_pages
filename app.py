import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import os
from generator import generate_landing_page, get_templates, get_themes

class LandingPageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Landing Page Creator")
        self.root.geometry("600x750")
        self.root.configure(bg="#f4f4f4")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#f4f4f4", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("TEntry", padding=4)
        style.configure("TCombobox", padding=4)

        self.template_var = tk.StringVar()
        self.theme_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.link_vars = [tk.StringVar() for _ in range(5)]
        self.bg_image_path = tk.StringVar()
        self.logo_image_path = tk.StringVar()
        self.logo_position_var = tk.StringVar(value="none")

        self.setup_ui()

    def setup_ui(self):
        padding = {'padx': 10, 'pady': 5}

        row = 0
        ttk.Label(self.root, text="Select Template:").grid(row=row, column=0, **padding)
        self.template_dropdown = ttk.Combobox(self.root, textvariable=self.template_var, values=get_templates(), width=40)
        self.template_dropdown.grid(row=row, column=1, columnspan=2, **padding)

        row += 1
        ttk.Label(self.root, text="Color Theme:").grid(row=row, column=0, **padding)
        self.theme_dropdown = ttk.Combobox(self.root, textvariable=self.theme_var, values=get_themes(), width=40)
        self.theme_dropdown.grid(row=row, column=1, columnspan=2, **padding)

        row += 1
        ttk.Label(self.root, text="Page Title:").grid(row=row, column=0, **padding)
        ttk.Entry(self.root, textvariable=self.title_var, width=45).grid(row=row, column=1, columnspan=2, **padding)

        row += 1
        ttk.Label(self.root, text="Description:").grid(row=row, column=0, **padding)
        ttk.Entry(self.root, textvariable=self.desc_var, width=45).grid(row=row, column=1, columnspan=2, **padding)

        row += 1
        ttk.Label(self.root, text="Email:").grid(row=row, column=0, **padding)
        ttk.Entry(self.root, textvariable=self.email_var, width=45).grid(row=row, column=1, columnspan=2, **padding)

        row += 1
        ttk.Label(self.root, text="Phone:").grid(row=row, column=0, **padding)
        ttk.Entry(self.root, textvariable=self.phone_var, width=45).grid(row=row, column=1, columnspan=2, **padding)

        for i in range(5):
            row += 1
            ttk.Label(self.root, text=f"Link {i+1}:").grid(row=row, column=0, **padding)
            ttk.Entry(self.root, textvariable=self.link_vars[i], width=45).grid(row=row, column=1, columnspan=2, **padding)

        row += 1
        ttk.Label(self.root, text="Background Image:").grid(row=row, column=0, **padding)
        ttk.Entry(self.root, textvariable=self.bg_image_path, width=35).grid(row=row, column=1, **padding)
        ttk.Button(self.root, text="Browse", command=self.browse_bg_image).grid(row=row, column=2, **padding)

        row += 1
        ttk.Label(self.root, text="Logo Image:").grid(row=row, column=0, **padding)
        ttk.Entry(self.root, textvariable=self.logo_image_path, width=35).grid(row=row, column=1, **padding)
        ttk.Button(self.root, text="Browse", command=self.browse_logo_image).grid(row=row, column=2, **padding)

        row += 1
        ttk.Label(self.root, text="Logo Position:").grid(row=row, column=0, **padding)
        ttk.Combobox(self.root, textvariable=self.logo_position_var,
                     values=["none", "left-up", "right-up", "middle", "left-down", "right-down"], width=40).grid(row=row, column=1, columnspan=2, **padding)

        row += 1
        ttk.Button(self.root, text="Generate Page", command=self.generate).grid(row=row, column=1, **padding)
        ttk.Button(self.root, text="Preview", command=self.preview).grid(row=row, column=2, **padding)

    def browse_bg_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            self.bg_image_path.set(path)

    def browse_logo_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            self.logo_image_path.set(path)

    def generate(self):
        data = {
            "title": self.title_var.get(),
            "description": self.desc_var.get(),
            "email": self.email_var.get(),
            "phone": self.phone_var.get(),
            "links": [link.get() for link in self.link_vars if link.get()],
            "theme": self.theme_var.get(),
            "background_image": self.bg_image_path.get(),
            "logo_image": self.logo_image_path.get(),
            "logo_position": self.logo_position_var.get()
        }

        template = self.template_var.get()
        if not template:
            messagebox.showerror("Error", "Please select a template.")
            return

        filename = generate_landing_page(template, data)
        messagebox.showinfo("Success", f"Landing page generated: {filename}")

    def preview(self):
        try:
            latest_dir = sorted(os.listdir("output/"))[-1]
            path = os.path.join("output", latest_dir, "index.html")
            webbrowser.open(path)
        except Exception as e:
            messagebox.showerror("Error", f"No generated file to preview.\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LandingPageApp(root)
    root.mainloop()
