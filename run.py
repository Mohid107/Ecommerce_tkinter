import sys
import os

# Add the project root to the python path so 'src' can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    try:
        from src.gui.main_window import EcommerceApp
        app = EcommerceApp()
        app.mainloop()
    except ImportError as e:
        print(f"Error starting application: {e}")
        print("Make sure you are running this script from the project root.")
        input("Press Enter to exit...")

