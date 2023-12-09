import tkinter as tk
from PIL import Image, ImageTk
import gui.functions as gui
from sorting.sort import *
from gui.functions import *
from database.db import db

class GUIClass():
    def __init__(self):
        self.images = []

        gui.window = self
        # value is set for functions.py to use

        self.window = tk.Tk()

        self.window.frame

        self.title("Stock Display and Control")

        self.lowest_first = True
        self.sort_button = tk.Button(self.window, text="Sort Highest Stock First", command=switch_order)
        self.stock_button = tk.Button(self.window, text="Edit Stock!", command=edit_stock)

        self.sort_button.pack(pady=10)
        self.stock_button.pack(pady=10)

        self.geometry(975, 600)

        self.generate_grid()
        # generates the grid of products in database.db

    def generate_grid(self):

        try: self.master.destroy()
        except AttributeError: pass
        
        self.master = tk.Frame(self.window)

        items = db.items_to_list()
        items = sort_products(items, self.lowest_first)

        for item in items:
            image_path = item['path']
            stock = item['stock']
            name = item['name']

            # resizes image
            image = ImageTk.PhotoImage(Image.open(image_path).resize((120, 120)))

            # keeps image object in memory to prevent GC from removing it
            for images in self.images:
                if images["name"] == name:
                    images["image"] = image
                    break
            else:
                self.images.append({
                    "name": name,
                    "image": image
                })

            frame = tk.Frame(self.master)
            frame.pack(side=tk.LEFT)

            image_label = tk.Label(frame, image=image)
            name_label = tk.Label(frame, text=name)
            stock_label = tk.Label(frame, text=f"Stock: {stock}")

            image_label.pack()
            name_label.pack()
            stock_label.pack()
            
        self.master.pack(anchor=tk.SW)

    def geometry(self, width, height):
        self.window.geometry(f"{width}x{height}")
    
    def title(self, title:str):
        self.window.title(title)

    def run(self):
        self.window.mainloop()
