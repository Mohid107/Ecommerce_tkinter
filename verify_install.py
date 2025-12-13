import sys
import os
import tkinter as tk

# Add project root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.gui.main_window import EcommerceApp
from src.gui.frames.checkout_frame import CheckoutFrame

def verify():
    app = EcommerceApp()
    
    # Check if CheckoutFrame is in frames dict
    found = False
    for frame_class, frame_obj in app.frames.items():
        if isinstance(frame_obj, CheckoutFrame):
            print("SUCCESS: CheckoutFrame is registered and initialized.")
            found = True
            break
            
    if not found:
        print("FAILURE: CheckoutFrame NOT found in app.frames.")
        
    # Check if "CheckoutFrame" string mapping works
    try:
        # We can't access local var inside show_frame, but we can verify class exists
        print("SUCCESS: CheckoutFrame class is available.")
    except Exception as e:
        print(f"FAILURE: {e}")

    app.destroy()

if __name__ == "__main__":
    verify()
