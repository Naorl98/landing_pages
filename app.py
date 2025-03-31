import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import os
from generator import generate_landing_page, get_templates, get_themes

class LandingPageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Landing Page Creator")
        self.root.geometry("700x900")
        self.root.configure(bg="#1a1a1a")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", foreground="black", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6, background="#007acc", foreground="white")
        style.map("TButton", background=[("active", "#005b99")])
        style.configure("TEntry", padding=6)
        style.configure("TCombobox", padding=6)

        self.template_var = tk.StringVar()
        self.theme_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.bg_image_path = tk.StringVar()
        self.logo_image_path = tk.StringVar()
        self.logo_position_var = tk.StringVar(value="none")

        self.link_frames = []

        self.setup_ui()

    def setup_ui(self):
        padding = {'padx': 10, 'pady': 6}

        tk.Label(self.root, text="Landing Page Builder", font=("Segoe UI", 20, "bold"), bg="#1a1a1a", fg="white").pack(pady=(20, 10))

        form = ttk.Frame(self.root)
        form.pack(padx=25, pady=10, fill="both", expand=True)

        def add_form_row(row, label, widget):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", **padding)
            widget.grid(row=row, column=1, columnspan=2, sticky="ew", **padding)

        form.columnconfigure(1, weight=1)

        row = 0
        add_form_row(row, "Template:", ttk.Combobox(form, textvariable=self.template_var, values=get_templates(), width=48))
        row += 1
        add_form_row(row, "Color Theme:", ttk.Combobox(form, textvariable=self.theme_var, values=get_themes(), width=48))
        row += 1
        add_form_row(row, "Page Title:", ttk.Entry(form, textvariable=self.title_var, width=50))

        row += 1
        ttk.Label(form, text="Description:").grid(row=row, column=0, sticky="nw", **padding)
        self.desc_text = tk.Text(form, width=50, height=5, wrap="word", font=("Segoe UI", 10))
        self.desc_text.grid(row=row, column=1, columnspan=2, sticky="ew", **padding)

        row += 1
        add_form_row(row, "Email:", ttk.Entry(form, textvariable=self.email_var, width=50))
        row += 1
        add_form_row(row, "Phone:", ttk.Entry(form, textvariable=self.phone_var, width=50))

        row += 1
        ttk.Label(form, text="Links (Add multiple):").grid(row=row, column=0, sticky="w", **padding)
        self.links_container = ttk.Frame(form)
        self.links_container.grid(row=row, column=1, columnspan=2, sticky="nsew", **padding)
        self.add_link_field()

        row += 1
        ttk.Button(form, text="+ Add Link", command=self.add_link_field).grid(row=row, column=1, sticky="w", **padding)

        row += 1
        ttk.Label(form, text="Background Image:").grid(row=row, column=0, sticky="w", **padding)
        ttk.Entry(form, textvariable=self.bg_image_path, width=36).grid(row=row, column=1, **padding)
        ttk.Button(form, text="Browse", command=self.browse_bg_image).grid(row=row, column=2, **padding)

        row += 1
        ttk.Label(form, text="Logo Image:").grid(row=row, column=0, sticky="w", **padding)
        ttk.Entry(form, textvariable=self.logo_image_path, width=36).grid(row=row, column=1, **padding)
        ttk.Button(form, text="Browse", command=self.browse_logo_image).grid(row=row, column=2, **padding)

        row += 1
        add_form_row(row, "Logo Position:", ttk.Combobox(form, textvariable=self.logo_position_var,
                                                          values=["none", "top-left", "top-right", "middle", "bottom-left", "bottom-right"], width=48))

        row += 1
        ttk.Button(form, text="Generate Page", command=self.generate).grid(row=row, column=1, sticky="e", **padding)
        ttk.Button(form, text="Preview", command=self.preview).grid(row=row, column=2, sticky="w", **padding)

    def add_link_field(self):
        frame = ttk.Frame(self.links_container)
        title_var = tk.StringVar()
        url_var = tk.StringVar()

        ttk.Entry(frame, textvariable=title_var, width=20).pack(side="left", padx=(0, 5))
        ttk.Entry(frame, textvariable=url_var, width=30).pack(side="left")

        frame.pack(pady=2, anchor="w")
        self.link_frames.append((title_var, url_var))

    def browse_bg_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            self.bg_image_path.set(path)

    def browse_logo_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            self.logo_image_path.set(path)

    def generate(self):
        links = []
        for title_var, url_var in self.link_frames:
            link = url_var.get().strip()
            title = title_var.get().strip()
            if link:
                links.append({"url": link, "title": title})

        data = {
            "title": self.title_var.get(),
            "description": self.desc_text.get("1.0", "end").strip(),
            "email": self.email_var.get(),
            "phone": self.phone_var.get(),
            "links": links,
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
