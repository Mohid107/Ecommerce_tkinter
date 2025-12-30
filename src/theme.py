# src/gui/theme.py

from tkinter import ttk

# -------------------------------
# COLORS
# -------------------------------
class Colors:
    PRIMARY = "#1A5276"        # Professional Dark Blue
    SECONDARY = "#5D6D7E"      # Sophisticated Gray-Blue
    ACCENT = "#D35400"         # Muted Orange/Terra-cotta for CTAs
    BACKGROUND = "#FAFAFA"     # Very light off-white/gray
    CARD_BG = "#FFFFFF"        # Pure White
    TEXT_PRIMARY = "#2C3E50"   # Dark Blue-Gray text
    TEXT_SECONDARY = "#7F8C8D" # Medium Gray text
    ERROR = "#C0392B"          # Deep Red
    SUCCESS = "#27AE60"        # Standard Success Green

# -------------------------------
# FONTS
# -------------------------------
class Fonts:
    TITLE = ("Helvetica", 24, "bold")
    SUBTITLE = ("Helvetica", 16)
    HEADER = ("Helvetica", 18, "bold")
    SUBHEADER = ("Helvetica", 14, "bold")
    BODY = ("Helvetica", 12)
    BUTTON = ("Helvetica", 12, "bold")
    SMALL = ("Helvetica", 10)

# -------------------------------
# STYLE CONFIGURATION
# -------------------------------
def setup_styles(root):
    style = ttk.Style(root)

    # Set theme to 'clam' for modern look
    style.theme_use("clam")

    # Card/Panel background (White box)
    style.configure("Card.TFrame", background=Colors.CARD_BG, relief="flat")

    # Labels
    style.configure("TLabel", background=Colors.BACKGROUND, foreground=Colors.TEXT_PRIMARY, font=Fonts.BODY)
    # Header Labels inside Card
    style.configure("Header.TLabel", background=Colors.CARD_BG, foreground=Colors.PRIMARY, font=Fonts.HEADER)
    # Body Labels inside Card
    style.configure("Card.TLabel", background=Colors.CARD_BG, foreground=Colors.TEXT_PRIMARY, font=Fonts.BODY)

    # Buttons
    style.configure("TButton",
                    background=Colors.PRIMARY,
                    foreground="white",
                    font=Fonts.BUTTON,
                    padding=10,
                    borderwidth=0)
    style.map("TButton",
              foreground=[("active", "white")],
              background=[("active", Colors.SECONDARY)])

    # Link Button (for Sign Up/Forgot Password) - looks like text
    style.configure("Link.TButton",
                    background=Colors.CARD_BG,
                    foreground=Colors.PRIMARY,
                    font=Fonts.BODY,
                    borderwidth=0)
    style.map("Link.TButton",
              foreground=[("active", Colors.SECONDARY)],
              background=[("active", Colors.CARD_BG)])

    # Primary Button (Solid Blue)
    style.configure("Primary.TButton", 
                    background=Colors.PRIMARY, 
                    foreground="white",
                    font=Fonts.BUTTON,
                    padding=10,
                    borderwidth=0)
    style.map("Primary.TButton",
              background=[("active", Colors.SECONDARY)],
              foreground=[("active", "white")])

    # Secondary Button (Gray/Light)
    style.configure("Secondary.TButton", 
                    background=Colors.SECONDARY, 
                    foreground=Colors.TEXT_PRIMARY,
                    font=Fonts.BUTTON,
                    padding=10,
                    borderwidth=0)
    style.map("Secondary.TButton",
              background=[("active", Colors.ACCENT)],
              foreground=[("active", "white")])

    # Entry fields
    style.configure("TEntry",
                    fieldbackground="white",
                    foreground=Colors.TEXT_PRIMARY,
                    padding=5,
                    font=Fonts.BODY)

    # Treeview (for product/cart tables)
    style.configure("Treeview",
                    background="white",
                    foreground=Colors.TEXT_PRIMARY,
                    fieldbackground="white",
                    font=Fonts.BODY)
    style.configure("Treeview.Heading",
                    font=Fonts.SUBHEADER,
                    background=Colors.PRIMARY,
                    foreground="white")
