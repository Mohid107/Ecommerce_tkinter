import sys
import os
import random

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data.db import db

def seed():
    print("Clearing existing data...")
    try:
        db.execute("DELETE FROM Order_Items")
        db.execute("DELETE FROM Orders")  # Optional, but keeps things clean
        db.execute("DELETE FROM Products")
    except Exception as e:
        print(f"Warning during cleanup: {e}")
    

    categories = {
        "Electronics": [
            ("Smartphone X", 999.00, "High-end smartphone with AI camera", "smartphone.jfif"),
            ("Laptop Pro", 1499.00, "Professional laptop for creators", "laptop.jfif"),
            ("Noise Cancel Headphones", 299.00, "Wireless ANC headphones", "headphones.jpg"),
            ("Smart Watch", 399.00, "Fitness tracker and smartwatch", "SmartWatch.jpg"),
            ("4K Monitor", 350.00, "27-inch 4K IPS Display", "4k monitor.jfif"),
            ("Mechanical Keyboard", 120.00, "RGB mechanical keyboard", "Mech_Keyboad.jfif"),
            ("Wireless Mouse", 80.00, "Ergonomic wireless mouse", "wireless mouse.jfif"),
            ("Tablet Air", 600.00, "Lightweight tablet for reading", "Tablet Air.jfif"),
            ("Bluetooth Speaker", 150.00, "Portable waterproof speaker", "BT Speaker.jfif"),
            ("Gaming Console", 499.00, "Next-gen gaming experience", "Gaming Console.jfif"),
        ],
        "Fashion": [
            ("Classic T-Shirt", 25.00, "100% Cotton reliable fit", "Classic T-Shirt.jfif"),
            ("Denim Jeans", 60.00, "Slim fit dark wash jeans", "Denim Jeans.jfif"),
            ("Running Sneakers", 120.00, "Lightweight running shoes", "Shoes_casual.jpg"),
            ("Leather Jacket", 250.00, "Genuine leather biker jacket", "Leather Jacket.jfif"),
            ("Winter Scarf", 35.00, "Wool blend warm scarf", "Winter Scarf.jfif"),
            ("Sunglasses", 150.00, "Polarized aviator sunglasses", "Rayban.jpg"),
            ("Backpack", 80.00, "Durable travel backpack", "Backpack.jfif"),
            ("Wrist Watch", 200.00, "Classic analog watch", "whiteWatch.jpg"),
            ("Formal Shirt", 55.00, "White formal dress shirt", "Formal Shirt.jfif"),
            ("Hoodie", 45.00, "Cozy fleece hoodie", "Hoodie.jfif"),
        ],
        "Home": [
            ("Coffee Maker", 120.00, "Programmable drip coffee maker", "Coffee Maker.jfif"),
            ("Desk Lamp", 45.00, "LED adjustable desk lamp", "Desk Lamp.jfif"),
            ("Plant Pot", 25.00, "Ceramic indoor plant pot", "Plant Pot.jfif"),
            ("Throw Pillow", 30.00, "Decorative soft throw pillow", "Throw Pillow.jfif"),
            ("Wall Clock", 40.00, "Modern minimalist wall clock", "Wall Clock.jfif"),
            ("Blender", 80.00, "High-speed smoothie blender", "Blender.jfif"),
            ("Cookware Set", 200.00, "Non-stick pots and pans", "Cookware Set.jfif"),
            ("Towel Set", 50.00, "Plush egyptian cotton towels", "Towel Set.jfif"),
            ("Bed Sheets", 90.00, "Soft microfiber sheet set", "Bed Sheets.jfif"),
            ("Water Bottle", 15.00, "Insulated steel water bottle", "WaterBottle.jpg"),
        ]
    }

    count = 0
    for category, products in categories.items():
        for name, price, desc, img in products:
            db.execute("""
                INSERT INTO Products (name, price, description, stock, image_url)
                VALUES (?, ?, ?, ?, ?)
            """, (name, price, f"{category}: {desc}", random.randint(5, 50), img))
            count += 1
    
    print(f"Successfully seeded {count} products!")

if __name__ == "__main__":
    seed()
