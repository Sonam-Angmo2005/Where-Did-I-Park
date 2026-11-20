
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import cv2
import qrcode

DATA_FILE = "parking_data.json"
QR_FOLDER = "zone_qr_codes"


class ParkingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Where Did I Park? - Version 2")
        self.root.geometry("600x700")
        self.root.configure(bg="#eef3f8")

        self.vehicle_var = tk.StringVar()
        self.zone_var = tk.StringVar()
        self.slot_var = tk.StringVar()

        self.create_interface()

    def create_interface(self):

        tk.Label(
            self.root,
            text="WHERE DID I PARK?",
            font=("Arial", 23, "bold"),
            bg="#eef3f8",
            fg="#17365d"
        ).pack(pady=15)

        tk.Label(
            self.root,
            text="QR-Based Two-Wheeler Parking Locator",
            font=("Arial", 12),
            bg="#eef3f8"
        ).pack(pady=5)

        form = tk.Frame(self.root, bg="white", padx=25, pady=25)
        form.pack(padx=25, pady=15, fill="x")

        tk.Label(
            form, text="Vehicle Number:",
            font=("Arial", 12, "bold"), bg="white"
        ).pack(anchor="w")

        tk.Entry(
            form, textvariable=self.vehicle_var,
            font=("Arial", 12), width=35
        ).pack(pady=8, fill="x")

        tk.Label(
            form, text="Parking Zone:",
            font=("Arial", 12, "bold"), bg="white"
        ).pack(anchor="w", pady=(10, 0))

        self.zone_box = ttk.Combobox(
            form,
            textvariable=self.zone_var,
            values=["Zone A", "Zone B", "Zone C", "Zone D"],
            state="readonly",
            font=("Arial", 12)
        )
        self.zone_box.pack(pady=8, fill="x")

        tk.Button(
            form,
            text="SCAN QR CODE USING WEBCAM",
            command=self.scan_qr,
            bg="#2874a6",
            fg="white",
            font=("Arial", 11, "bold"),
            pady=8
        ).pack(fill="x", pady=8)

        tk.Label(
            form, text="Parking Slot Number:",
            font=("Arial", 12, "bold"), bg="white"
        ).pack(anchor="w", pady=(10, 0))

        tk.Entry(
            form, textvariable=self.slot_var,
            font=("Arial", 12)
        ).pack(pady=8, fill="x")

        tk.Button(
            form,
            text="GENERATE ZONE QR CODES",
            command=self.generate_qr_codes,
            bg="#6c757d",
            fg="white",
            font=("Arial", 10, "bold"),
            pady=7
        ).pack(fill="x", pady=8)

        buttons = tk.Frame(self.root, bg="#eef3f8")
        buttons.pack(pady=10)

        tk.Button(
            buttons, text="SAVE LOCATION",
            command=self.save_location,
            bg="#218838", fg="white",
            font=("Arial", 10, "bold"),
            width=16, pady=9
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            buttons, text="VIEW LOCATION",
            command=self.view_location,
            bg="#2874a6", fg="white",
            font=("Arial", 10, "bold"),
            width=16, pady=9
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            buttons, text="UPDATE LOCATION",
            command=self.update_location,
            bg="#d68910", fg="white",
            font=("Arial", 10, "bold"),
            width=16, pady=9
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            buttons, text="CLEAR FORM",
            command=self.clear_form,
            bg="#c0392b", fg="white",
            font=("Arial", 10, "bold"),
            width=16, pady=9
        ).grid(row=1, column=1, padx=5, pady=5)

        self.result_label = tk.Label(
            self.root,
            text="Your parking information will appear here.",
            font=("Arial", 11),
            bg="#eef3f8",
            fg="#17365d",
            justify="left",
            wraplength=520
        )
        self.result_label.pack(pady=20)

        tk.Label(
            self.root,
            text="Version 2 - Improved QR-Based Parking Locator",
            font=("Arial", 9),
            bg="#eef3f8",
            fg="gray"
        ).pack(side="bottom", pady=12)

    def scan_qr(self):

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            messagebox.showerror(
                "Camera Error",
                "Unable to access the webcam. Check your camera connection."
            )
            return

        detector = cv2.QRCodeDetector()

        messagebox.showinfo(
            "QR Scanner",
            "Show a generated parking-zone QR code to your webcam.\n"
            "Press Q in the camera window to stop scanning."
        )

        scanned_zone = None

        while True:
            success, frame = camera.read()

            if not success:
                break

            data, points, _ = detector.detectAndDecode(frame)

            if data:
                cleaned = data.strip().upper().replace("_", " ")

                valid_zones = {
                    "A": "Zone A",
                    "ZONE A": "Zone A",
                    "B": "Zone B",
                    "ZONE B": "Zone B",
                    "C": "Zone C",
                    "ZONE C": "Zone C",
                    "D": "Zone D",
                    "ZONE D": "Zone D"
                }

                if cleaned in valid_zones:
                    scanned_zone = valid_zones[cleaned]
                    break

            cv2.imshow("Scan Parking Zone QR Code", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        camera.release()
        cv2.destroyAllWindows()

        if scanned_zone:
            self.zone_var.set(scanned_zone)
            messagebox.showinfo(
                "QR Scanned",
                "Parking zone identified: " + scanned_zone
            )
        else:
            messagebox.showwarning(
                "Scanning Finished",
                "No valid parking-zone QR code was scanned."
            )

    def generate_qr_codes(self):

        os.makedirs(QR_FOLDER, exist_ok=True)

        for zone in ["Zone A", "Zone B", "Zone C", "Zone D"]:
            qr = qrcode.make(zone)
            filename = zone.replace(" ", "_") + ".png"
            qr.save(os.path.join(QR_FOLDER, filename))

        messagebox.showinfo(
            "QR Codes Generated",
            "QR codes for all four parking zones have been saved in the "
            + QR_FOLDER + " folder."
        )

    def read_data(self):

        if not os.path.exists(DATA_FILE):
            return {}

        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}

    def save_location(self):

        vehicle = self.vehicle_var.get().strip().upper()
        zone = self.zone_var.get()
        slot = self.slot_var.get().strip()

        if not vehicle or not zone or not slot:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the vehicle number, parking zone and slot."
            )
            return

        data = self.read_data()

        data[vehicle] = {
            "vehicle": vehicle,
            "zone": zone,
            "slot": slot,
            "saved_at": datetime.now().strftime("%d-%m-%Y %I:%M %p")
        }

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

        self.result_label.config(
            text=f"Location Saved Successfully!\n\n"
                 f"Vehicle: {vehicle}\n"
                 f"Zone: {zone}\n"
                 f"Slot: {slot}\n"
                 f"Saved At: {data[vehicle]['saved_at']}"
        )

        messagebox.showinfo(
            "Success",
            "Parking location saved successfully!"
        )

    def view_location(self):

        vehicle = self.vehicle_var.get().strip().upper()

        if not vehicle:
            messagebox.showwarning(
                "Vehicle Required",
                "Enter the vehicle number to view its parking location."
            )
            return

        data = self.read_data()

        if vehicle not in data:
            messagebox.showinfo(
                "Not Found",
                "No parking record found for this vehicle."
            )
            return

        record = data[vehicle]

        self.zone_var.set(record["zone"])
        self.slot_var.set(record["slot"])

        self.result_label.config(
            text=f"Saved Parking Details\n\n"
                 f"Vehicle: {record['vehicle']}\n"
                 f"Zone: {record['zone']}\n"
                 f"Slot: {record['slot']}\n"
                 f"Saved At: {record['saved_at']}"
        )

    def update_location(self):

        vehicle = self.vehicle_var.get().strip().upper()
        data = self.read_data()

        if not vehicle:
            messagebox.showwarning(
                "Vehicle Required",
                "Enter the vehicle number first."
            )
            return

        if vehicle not in data:
            messagebox.showinfo(
                "Record Not Found",
                "No existing record found. Save the location first."
            )
            return

        self.save_location()

    def clear_form(self):

        self.vehicle_var.set("")
        self.zone_var.set("")
        self.slot_var.set("")

        self.result_label.config(
            text="Your parking information will appear here."
        )


if __name__ == "__main__":

    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()
