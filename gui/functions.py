import tkinter as tk
from tkinter import messagebox
from database.db import db

SEARCH_PLACEHOLDER:str = "Product Name.."
""" PlaceHolder Text """

UPDATE_PLACEHOLDER:str = "New Stock.."
""" PlaceHolder Text """

window = None
""" Window Object. it's set later on """

def entry_click(entry, default_text):
    """ Login For Text Input Placeholder """
    
    if entry.get() == default_text:
        entry.delete(0, tk.END)
        entry.config(fg='black')

def entry_leave(entry, default_text):
    """ Login For Text Input Placeholder """
    
    if entry.get() == '':
        entry.insert(0, default_text)
        entry.config(fg='grey')

def switch_order():
    """ Changed the Sort button Text based on sort method.. Regenerates Grid to update sort method """

    window.lowest_first = window.sort_button.cget("text") != "Sort Highest Stock First"
    window.sort_button.config(text=f"Sort {'Highest' if window.lowest_first else 'Lowest'} Stock First")
    window.generate_grid()

def edit_stock():
    """ Creates the Top Level menu to Edit a products Stock """

    window.stock = tk.Toplevel(window.window)
    window.stock.geometry("400x300")

    window.stock.title = "Search Product By Name"

    window.search_entry = tk.Entry(window.stock, fg='grey')
    window.search_entry.insert(0, SEARCH_PLACEHOLDER)
    window.search_entry.bind('<FocusIn>', lambda _: entry_click(window.search_entry, SEARCH_PLACEHOLDER))
    window.search_entry.bind('<FocusOut>', lambda _: entry_leave(window.search_entry, SEARCH_PLACEHOLDER))

    window.update_entry = tk.Entry(window.stock, fg='grey')
    window.update_entry.insert(0, UPDATE_PLACEHOLDER)
    window.update_entry.bind('<FocusIn>', lambda _: entry_click(window.update_entry, UPDATE_PLACEHOLDER))
    window.update_entry.bind('<FocusOut>', lambda _: entry_leave(window.update_entry, UPDATE_PLACEHOLDER))

    window.search_button = tk.Button(window.stock, text="Search Item", command=lambda: search_stock(window, window.search_entry.get()))
    window.update_button = tk.Button(window.stock, text="Update Stock", command=lambda: update_stock(window, window.update_entry.get()))

    window.search_entry.pack(pady=10)
    window.search_button.pack(pady=5)

def cleanup(window):
    """ Clean up. destroys and unsets objects created within edit_stock """

    window.search_entry.destroy()
    window.search_button.destroy()
    window.update_entry.destroy()
    window.stock.destroy()

    del window.selected_product
    del window.search_entry
    del window.search_button
    del window.update_entry
    del window.stock

def update_stock(window, value:str):
    """ Updates Stock based on the searched item and current input value. Throws Error if value is not a valid integer """

    value = str(value).strip()
    if value == UPDATE_PLACEHOLDER:
        return
    
    try:
        window.selected_product = db.update_stock_by_name(window.selected_product["name"], int(value))
    except ValueError:
        return showError("Invalid Input", f'Invalid Integer "{value}"')
    
    # only regenerates the grid if product is found and successfully updates
    if window.selected_product:
        window.generate_grid()

    showInfo("Success", f'Successfully Updated Stock for: "{window.selected_product["name"]}". New Stock: "{value}"')

def search_stock(window, value:str):
    """ Searches Product by current input value. Throws Error if product is not found"""

    value = str(value).strip()
    if value == SEARCH_PLACEHOLDER:
        return
    
    window.selected_product = db.find_item_by_name(value)
    
    if not window.selected_product:
        return showError("Lookup Error", f'Item with name "{value}" not found.')

    # only displays update stock buttons after a valid product is searched
    window.update_entry.pack(pady=10)
    window.update_button.pack(pady=5)
    
def showError(title, message):
    """ Shows Error Message """

    cleanup(window)
    return messagebox.showerror(title,message)

def showInfo(title, message):
    """ Shows Info Message """

    cleanup(window)
    return messagebox.showinfo(title, message)
