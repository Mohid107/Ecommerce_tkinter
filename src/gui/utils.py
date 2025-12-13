import platform
import os
from PIL import Image, ImageTk

def setup_scroll(widget):
    """
    Binds mouse wheel events to a widget for scrolling.
    Uses <Enter> and <Leave> events to only bind global scroll when mouse is over the widget.
    """
    
    def _on_mousewheel(event):
        try:
            if platform.system() == "Windows":
                widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif platform.system() == "Darwin": # macOS
                widget.yview_scroll(int(-1 * event.delta), "units")
            else: # Linux
                if event.num == 4:
                    widget.yview_scroll(-1, "units")
                elif event.num == 5:
                    widget.yview_scroll(1, "units")
        except tk.TclError:
            pass # Widget might be destroyed or not scrollable

    def _bind_to_mousewheel(event):
        # Windows/macOS
        widget.bind_all("<MouseWheel>", _on_mousewheel)
        # Linux
        widget.bind_all("<Button-4>", _on_mousewheel)
        widget.bind_all("<Button-5>", _on_mousewheel)

    def _unbind_from_mousewheel(event):
        widget.unbind_all("<MouseWheel>")
        widget.unbind_all("<Button-4>")
        widget.unbind_all("<Button-5>")

    # Bind enter/leave events
    widget.bind("<Enter>", _bind_to_mousewheel)
    widget.bind("<Leave>", _unbind_from_mousewheel)

def unbind_scroll(widget):
    """Unbinds global scroll events immediately."""
    widget.unbind_all("<MouseWheel>")
    widget.unbind_all("<Button-4>")
    widget.unbind_all("<Button-5>")

def load_local_image(filename, size=None):
    """
    Loads an image from the 'media' directory.
    Args:
        filename (str): Name of the file in media/ folder (e.g., 'headphones.jpg').
        size (tuple): Optional (width, height) to resize.
    Returns:
        ImageTk.PhotoImage or None if failed.
    """
    if not filename:
        return None
        
    # Build absolute path to media folder
    # Assumes utils.py is in src/gui/, so project root is ../../
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    media_path = os.path.join(project_root, "media", filename)
    
    if not os.path.exists(media_path):
        return None

    try:
        pil_image = Image.open(media_path)
        if size:
            pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(pil_image)
    except Exception as e:
        print(f"Failed to load local image {filename}: {e}")
        return None
