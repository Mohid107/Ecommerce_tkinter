import tkinter as tk
from tkinter import ttk, messagebox
from src.constants import AppConstants, Messages, ViewNames
from src import theme

class UserSignupView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_service = self.controller.user_service
        
        theme.setup_styles(self)
        self._setup_ui()

    def _setup_ui(self):
        # Container for centering
        container = ttk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ttk.Label(container, text="Create User Account", font=("Helvetica", 24, "bold")).pack(pady=(0, 30))

        # Form Frame
        form_frame = ttk.Frame(container)
        form_frame.pack()

        # Input Fields Configuration
        fields = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("DOB (Optional)", "dob"), # Updated label
            ("Phone", "phone"),
            ("Email", "email"),
            ("Username", "username"),
            ("Password", "password"),
        ]
        
        self.entries = {}
        
        for label_text, key in fields:
            self._create_input_field(form_frame, label_text, key)
            
        # Register Button
        ttk.Button(container, text="Register", command=self.signup, style="Primary.TButton").pack(pady=20, fill="x")
        
        # Back Button
        ttk.Button(container, text="Back to Login", command=lambda: self.controller.show_view(ViewNames.LOGIN)).pack()

    def _create_input_field(self, parent, label_text, key):
        frame = ttk.Frame(parent)
        frame.pack(pady=5, fill="x")
        
        # Using larger font as requested "font thora bra kr dyna"
        entry_font = ("Helvetica", 12)
        
        if key == "password":
            entry = ttk.Entry(frame, font=entry_font, show="*")
        else:
            entry = ttk.Entry(frame, font=entry_font)
            
        # Placeholder behavior
        entry.insert(0, label_text)
        entry.bind("<FocusIn>", lambda e: self._on_focus_in(entry, label_text))
        entry.bind("<FocusOut>", lambda e: self._on_focus_out(entry, label_text))
        entry.config(foreground="grey")
        
        entry.pack(fill="x", ipady=8) # Taller input fields
        self.entries[key] = entry

    def _on_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(foreground="black", show="*" if entry == self.entries.get("password") else "")

    def _on_focus_out(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(foreground="grey", show="")

    def signup(self):
        data = {}
        for key, entry in self.entries.items():
            value = entry.get()
            # Check if value is still placeholder
            placeholder = [f[0] for f in [
                ("First Name", "first_name"),
                ("Last Name", "last_name"),
                ("DOB (Optional)", "dob"),
                ("Phone", "phone"),
                ("Email", "email"),
                ("Username", "username"),
                ("Password", "password")
            ] if f[1] == key][0]
            
            if value == placeholder or not value.strip():
                if key in ["username", "password"]: # Key fields
                    messagebox.showerror("Error", f"{placeholder} is required!")
                    return
                data[key] = None
            else:
                data[key] = value

        if data["password"] is None: 
             messagebox.showerror("Error", "Password is required!")
             return

        try:
            self.user_service.signup(
                username=data["username"],
                password=data["password"],
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                phone=data.get("phone"),
                email=data.get("email"),
                dob=data.get("dob") # Pass DOB
            )
            messagebox.showinfo("Success", Messages.SIGNUP_SUCCESS)
            self.controller.show_view(ViewNames.LOGIN)
        except Exception as e:
            messagebox.showerror("Error", str(e))
