# =============================================
#   Restaurant Ordering System - GUI Version
#   Uses: OOP + tkinter (built-in with Python)
# =============================================

import tkinter as tk
from tkinter import messagebox

# ── OOP: Base Class ──────────────────────────
class FoodItem:
    def __init__(self, name, price):
        self.name  = name
        self.price = price

    def get_price(self):
        return self.price

# ── OOP: Inheritance ─────────────────────────
class MenuItem(FoodItem):
    def __init__(self, name, price):
        super().__init__(name, price)

    # OOP: Polymorphism
    def get_price(self):
        return self.price

# ── OOP: Inheritance + Polymorphism ──────────
class SpecialMenuItem(FoodItem):
    def __init__(self, name, price, discount):
        super().__init__(name, price)
        self.discount = discount

    def get_price(self):
        return self.price - (self.price * self.discount / 100)

# ── OOP: Encapsulation ────────────────────────
class Order:
    def __init__(self):
        self.__cart = []   # private list

    def add_item(self, item):
        self.__cart.append(item)

    def remove_item(self, index):
        if 0 <= index < len(self.__cart):
            self.__cart.pop(index)

    def get_items(self):
        return self.__cart

    def get_total(self):
        return sum(item.get_price() for item in self.__cart)

    def clear(self):
        self.__cart = []

# ── Menu Data ─────────────────────────────────
menu = [
    MenuItem("Spring Rolls",    150),
    MenuItem("Chicken Soup",    180),
    MenuItem("Garlic Bread",    120),
    MenuItem("Chicken Biryani", 350),
    MenuItem("Beef Burger",     280),
    MenuItem("Pasta Alfredo",   320),
    MenuItem("Coca Cola",        80),
    MenuItem("Ice Cream",       150),
    SpecialMenuItem("BBQ Platter",    600, 15),
    SpecialMenuItem("Mango Smoothie", 160, 10),
    SpecialMenuItem("Brownie Sundae", 250, 20),
]

order = Order()

# ── GUI App ───────────────────────────────────
window = tk.Tk()
window.title("Restaurant Ordering System")
window.geometry("750x520")
window.configure(bg="#1e1e2e")
window.resizable(False, False)

# Colors
BG      = "#1e1e2e"
PANEL   = "#2a2a3e"
RED     = "#e94560"
ORANGE  = "#f5a623"
WHITE   = "#ffffff"
GRAY    = "#aaaaaa"

# ── Helper: Label factory 
def label(parent, text, size=11, bold=False, color=WHITE, bg=BG):
    weight = "bold" if bold else "normal"
    return tk.Label(parent, text=text, font=("Helvetica", size, weight),
                    bg=bg, fg=color)

# ── Left: Menu Panel 
left = tk.Frame(window, bg=BG)
left.place(x=10, y=10, width=420, height=500)

label(left, "🍽  RESTAURANT MENU", 14, bold=True).pack(pady=(0, 8))

menu_frame = tk.Frame(left, bg=BG)
menu_frame.pack(fill="both", expand=True)

def refresh_menu():
    for w in menu_frame.winfo_children():
        w.destroy()

    for i, item in enumerate(menu):
        is_special = isinstance(item, SpecialMenuItem)
        price      = item.get_price()

        row = tk.Frame(menu_frame, bg=PANEL, pady=6, padx=10)
        row.pack(fill="x", pady=3)

        # Name
        name_text = f"⭐ {item.name}" if is_special else f"   {item.name}"
        label(row, name_text, 11, bg=PANEL,
              color=ORANGE if is_special else WHITE).pack(side="left")

        # Discount badge
        if is_special:
            label(row, f"({item.discount}% OFF)", 9, bg=PANEL, color=ORANGE).pack(side="left", padx=4)

        # Price
        label(row, f"Rs. {price:.0f}", 11, bold=True, bg=PANEL, color=RED).pack(side="right", padx=(0, 8))

        # Add button
        tk.Button(row, text="+ Add", font=("Helvetica", 9, "bold"),
                  bg=RED, fg=WHITE, relief="flat", padx=6, pady=2,
                  cursor="hand2",
                  command=lambda it=item: add_item(it)
                  ).pack(side="right", padx=4)

refresh_menu()

# ── Right: Cart Panel 
right = tk.Frame(window, bg=PANEL)
right.place(x=440, y=10, width=300, height=500)

label(right, "🛒  YOUR ORDER", 13, bold=True, bg=PANEL).pack(pady=(12, 6))

tk.Frame(right, bg=GRAY, height=1).pack(fill="x", padx=10)

cart_frame = tk.Frame(right, bg=PANEL)
cart_frame.pack(fill="both", expand=True, padx=10, pady=6)

# Totals at bottom of cart
bottom = tk.Frame(right, bg=PANEL)
bottom.pack(fill="x", padx=12, pady=6)

tk.Frame(bottom, bg=GRAY, height=1).pack(fill="x", pady=4)

subtotal_var = tk.StringVar(value="Rs. 0")
tax_var      = tk.StringVar(value="Rs. 0")
grand_var    = tk.StringVar(value="Rs. 0")

def total_row(parent, lbl, var):
    f = tk.Frame(parent, bg=PANEL)
    f.pack(fill="x")
    label(f, lbl, 10, bg=PANEL, color=GRAY).pack(side="left")
    tk.Label(f, textvariable=var, font=("Helvetica", 10, "bold"),
             bg=PANEL, fg=WHITE).pack(side="right")

total_row(bottom, "Subtotal:", subtotal_var)
total_row(bottom, "Tax (10%):", tax_var)
tk.Frame(bottom, bg=GRAY, height=1).pack(fill="x", pady=3)

f = tk.Frame(bottom, bg=PANEL)
f.pack(fill="x")
label(f, "Grand Total:", 12, bold=True, bg=PANEL).pack(side="left")
tk.Label(f, textvariable=grand_var, font=("Helvetica", 12, "bold"),
         bg=PANEL, fg=RED).pack(side="right")

tk.Button(bottom, text="🧾  Checkout",
          font=("Helvetica", 11, "bold"),
          bg=RED, fg=WHITE, relief="flat", pady=8, cursor="hand2",
          command=lambda: checkout()
          ).pack(fill="x", pady=(8, 0))

# ── Cart Logic ────────────────────────────────
def refresh_cart():
    for w in cart_frame.winfo_children():
        w.destroy()

    items = order.get_items()

    if not items:
        label(cart_frame, "Cart is empty.\nAdd items from the menu.",
              10, color=GRAY, bg=PANEL).pack(pady=30)
    else:
        for i, item in enumerate(items):
            row = tk.Frame(cart_frame, bg=PANEL)
            row.pack(fill="x", pady=2)

            label(row, item.name, 10, bg=PANEL).pack(side="left")
            label(row, f"Rs.{item.get_price():.0f}", 10, bold=True,
                  color=RED, bg=PANEL).pack(side="right", padx=(0, 4))

            tk.Button(row, text="✕", font=("Helvetica", 9),
                      bg=PANEL, fg=GRAY, relief="flat", cursor="hand2",
                      command=lambda idx=i: remove_item(idx)
                      ).pack(side="right")

    # Update totals
    sub   = order.get_total()
    tax   = sub * 0.10
    grand = sub + tax
    subtotal_var.set(f"Rs. {sub:.0f}")
    tax_var.set(f"Rs. {tax:.0f}")
    grand_var.set(f"Rs. {grand:.0f}")

def add_item(item):
    order.add_item(item)
    refresh_cart()

def remove_item(index):
    order.remove_item(index)
    refresh_cart()

def checkout():
    items = order.get_items()
    if not items:
        messagebox.showwarning("Empty Cart", "Please add items first!")
        return

    # Build bill text
    bill = "=" * 34 + "\n"
    bill += "        THE GRAND KITCHEN\n"
    bill += "=" * 34 + "\n"
    for item in items:
        bill += f"  {item.name:<20} Rs.{item.get_price():.0f}\n"
    bill += "-" * 34 + "\n"
    sub   = order.get_total()
    tax   = sub * 0.10
    grand = sub + tax
    bill += f"  {'Subtotal:':<20} Rs.{sub:.0f}\n"
    bill += f"  {'Tax (10%):':<20} Rs.{tax:.0f}\n"
    bill += f"  {'Grand Total:':<20} Rs.{grand:.0f}\n"
    bill += "=" * 34 + "\n"
    bill += "    Thank you! Enjoy your meal!"

    # Popup bill window
    win = tk.Toplevel(window)
    win.title("Your Bill")
    win.geometry("320x400")
    win.configure(bg=BG)
    win.resizable(False, False)
    win.grab_set()

    label(win, "🧾 YOUR BILL", 14, bold=True).pack(pady=10)

    text = tk.Text(win, font=("Courier", 10), bg=PANEL, fg=WHITE,
                   relief="flat", padx=10, pady=10, height=14)
    text.pack(fill="x", padx=16)
    text.insert("1.0", bill)
    text.config(state="disabled")

    def done():
        order.clear()
        refresh_cart()
        win.destroy()

    tk.Button(win, text="✔  Done", font=("Helvetica", 11, "bold"),
              bg=RED, fg=WHITE, relief="flat", pady=8, cursor="hand2",
              command=done).pack(fill="x", padx=16, pady=12)

# Init cart display
refresh_cart()

window.mainloop()