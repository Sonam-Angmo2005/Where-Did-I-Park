
import tkinter as tk
from tkinter import messagebox

# Save parking location
def save_location():
    zone = zone_entry.get()
    slot = slot_entry.get()

    if zone == "":
        messagebox.showwarning("Warning", "Please select a parking zone!")
        return

    with open("parking_data.txt", "w") as file:
        file.write(zone + "\n" + slot)

    messagebox.showinfo("Success", "Parking location saved successfully!")


# View saved location
def view_location():
    try:
        with open("parking_data.txt", "r") as file:
            data = file.readlines()

        zone = data[0].strip()
        slot = data[1].strip()

        result_label.config(
            text=f"Your vehicle is parked in {zone}\nParking Slot: {slot or 'Not specified'}"
        )

    except FileNotFoundError:
        messagebox.showinfo("Information", "No parking location saved yet.")


# Update parking location
def update_location():
    save_location()


# Main window
root = tk.Tk()
root.title("Where Did I Park?")
root.geometry("500x550")
root.config(bg="#eef2f7")

# Heading
heading = tk.Label(
    root,
    text="Where Did I Park?",
    font=("Arial", 24, "bold"),
    bg="#eef2f7",
    fg="#243b55"
)
heading.pack(pady=20)

subtitle = tk.Label(
    root,
    text="Remember your vehicle parking location",
    font=("Arial", 11),
    bg="#eef2f7"
)
subtitle.pack(pady=5)

# Parking form
form = tk.Frame(root, bg="white", padx=25, pady=25)
form.pack(padx=30, pady=20, fill="x")

tk.Label(
    form,
    text="Select Parking Zone",
    font=("Arial", 12, "bold"),
    bg="white"
).pack(anchor="w")

zone_entry = tk.StringVar()

zone_menu = tk.OptionMenu(
    form, zone_entry,
    "Zone A", "Zone B", "Zone C", "Zone D"
)
zone_menu.pack(fill="x", pady=10)

tk.Label(
    form,
    text="Parking Slot (Optional)",
    font=("Arial", 12, "bold"),
    bg="white"
).pack(anchor="w")

slot_entry = tk.Entry(form, font=("Arial", 12))
slot_entry.pack(fill="x", pady=10)

# Buttons
tk.Button(
    form,
    text="Save Location",
    command=save_location,
    bg="#2878b5",
    fg="white",
    font=("Arial", 12, "bold"),
    pady=8
).pack(fill="x", pady=8)

tk.Button(
    form,
    text="View Location",
    command=view_location,
    bg="#27845b",
    fg="white",
    font=("Arial", 12, "bold"),
    pady=8
).pack(fill="x", pady=8)

tk.Button(
    form,
    text="Update Location",
    command=update_location,
    bg="#d18a28",
    fg="white",
    font=("Arial", 12, "bold"),
    pady=8
).pack(fill="x", pady=8)

# Display saved location
result_label = tk.Label(
    root,
    text="Your saved parking location will appear here.",
    font=("Arial", 12),
    bg="#eef2f7",
    fg="#243b55",
    wraplength=400
)
result_label.pack(pady=20)

root.mainloop()
