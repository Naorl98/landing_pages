import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import os
from generator import generate_landing_page, get_templates, get_themes

class LandingPageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Landing Page Creator")
        self.root.geometry("680x780")
        self.root.configure(bg="#1a1a1a")  # Soft black background

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel",  foreground="black", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, background="#007acc", foreground="white")
        style.map("TButton",
                  foreground=[("active", "white")],
                  background=[("active", "#005b99")])
        style.configure("TEntry", padding=6)
        style.configure("TCombobox", padding=6)

        self.template_var = tk.StringVar()
        self.theme_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.link_vars = [tk.StringVar() for _ in range(3)]
        self.bg_image_path = tk.StringVar()
        self.logo_image_path = tk.StringVar()
        self.logo_position_var = tk.StringVar(value="none")

        self.setup_ui()

    def setup_ui(self):
        padding = {'padx': 10, 'pady': 6}

        # Title
        title_label = tk.Label(
            self.root, text="Landing Page Builder",
            font=("Segoe UI", 18, "bold"),
            bg="#1a1a1a", fg="white"
        )
        title_label.pack(pady=(25, 10))

        # Form
        form = ttk.Frame(self.root)
        form.pack(padx=25, pady=10, fill="both", expand=True)

        def form_row(row, label, widget):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", **padding)
            widget.grid(row=row, column=1, columnspan=2, sticky="ew", **padding)

        form.columnconfigure(1, weight=1)

        row = 0
        form_row(row, "Template:", ttk.Combobox(form, textvariable=self.template_var, values=get_templates(), width=46))
        row += 1
        form_row(row, "Color Theme:", ttk.Combobox(form, textvariable=self.theme_var, values=get_themes(), width=46))
        row += 1
        form_row(row, "Page Title:", ttk.Entry(form, textvariable=self.title_var, width=48))
        row += 1
        form_row(row, "Description:", ttk.Entry(form, textvariable=self.desc_var, width=48))
        row += 1
        form_row(row, "Email:", ttk.Entry(form, textvariable=self.email_var, width=48))
        row += 1
        form_row(row, "Phone:", ttk.Entry(form, textvariable=self.phone_var, width=48))

        for i in range(3):
            row += 1
            form_row(row, f"Link {i+1}:", ttk.Entry(form, textvariable=self.link_vars[i], width=48))

        # Background Image Upload
        row += 1
        ttk.Label(form, text="Background Image:").grid(row=row, column=0, sticky="w", **padding)
        ttk.Entry(form, textvariable=self.bg_image_path, width=35).grid(row=row, column=1, **padding)
        ttk.Button(form, text="Browse", command=self.browse_bg_image).grid(row=row, column=2, **padding)

        # Logo Image Upload
        row += 1
        ttk.Label(form, text="Logo Image:").grid(row=row, column=0, sticky="w", **padding)
        ttk.Entry(form, textvariable=self.logo_image_path, width=35).grid(row=row, column=1, **padding)
        ttk.Button(form, text="Browse", command=self.browse_logo_image).grid(row=row, column=2, **padding)

        # Logo Position
        row += 1
        form_row(row, "Logo Position:", ttk.Combobox(form, textvariable=self.logo_position_var,
                                                      values=["none", "left-up", "right-up", "middle", "left-down", "right-down"], width=46))

        # Action Buttons
        row += 1
        ttk.Button(form, text="Generate", command=self.generate).grid(row=row, column=1, sticky="e", **padding)
        ttk.Button(form, text="Preview", command=self.preview).grid(row=row, column=2, sticky="w", **padding)

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
