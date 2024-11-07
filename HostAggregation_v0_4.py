#!/usr/bin/env python3

# HostAggregation_v0_3.py

#	Chris Quintero Dominguez
#	26/10/2024
#	Sophos/XDR Reporting Tool

#	Purpose: Take a list of hostnames from different documents and compare them to provide a list of hosts
#	that have:
#
#		- Hosts with/without sophos deployed
#		- Hosts with/without XDR deployed

# Import Relevant Modules

import os
import tkinter as tk
import pandas as pd

from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

# Read file into a dataframe - Note this needs to be replaced with the ability to choose files in the future.

#Source Data location C:\Users\cdominguez\python\aggregationtool\Working\sourceData
#Script Location C:\Users\cdominguez\python\aggregationtool\Working

class FileSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Selection")

         # Set desired window size
        window_width = 600
        window_height = 300

        # Get the screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the center position
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the geometry of the window with width x height + x_offset + y_offset
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Dictionary to store file paths for each region and inventory
        self.file_paths = {
            "Americas VM Inventory": tk.StringVar(),
            "Japan VM Inventory": tk.StringVar(),
            "China VM Inventory": tk.StringVar(),
            "United Kingdom VM Inventory": tk.StringVar(),
            "Sophos Inventory": tk.StringVar(),
            "XDR Inventory": tk.StringVar()
        }

        # Create the layout
        row = 0
        for label in self.file_paths:
            # Label for each selection
            tk.Label(root, text=label).grid(row=row, column=0, padx=10, pady=5)

            # Entry to display selected file path
            entry = tk.Entry(root, textvariable=self.file_paths[label], width=50)
            entry.grid(row=row, column=1, padx=10, pady=5)

            # Button to open file dialog for each selection
            button = tk.Button(root, text="Select File", command=lambda l=label: self.select_file(l))
            button.grid(row=row, column=2, padx=10, pady=5)

            row += 1
            
            # Add a horizontal line after "United Kingdom VM Inventory"
            if label == "United Kingdom VM Inventory":
                separator = ttk.Separator(root, orient="horizontal")
                separator.grid(row=row, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
                row += 1

        # OK button to confirm selections
        tk.Button(root, text="OK", command=self.confirm_selection).grid(row=row, column=1, pady=20)

    def select_file(self, label):
        """Open a file dialog to select a file and store the path in the appropriate entry"""
        file_path = filedialog.askopenfilename(title=f"Select file for {label}")
        if file_path:
            self.file_paths[label].set(file_path)

    def confirm_selection(self):
        """Confirm file selection and proceed if all files are selected"""
        for label, path_var in self.file_paths.items():
            if not path_var.get():
                messagebox.showwarning("Incomplete Selection", f"Please select a file for {label}.")
                return

        self.root.quit()  # All files are selected, Close the dialog box and continue execution
        self.root.destroy()  # Closes the window

# Run the file selection application
root = tk.Tk()
app = FileSelectionApp(root)
root.mainloop()  # Wait until the file selection dialog is closed

# Use the selected file paths
unitedKingdom_DataFrame = pd.read_csv(app.file_paths["United Kingdom VM Inventory"].get())
americas_DataFrame = pd.read_csv(app.file_paths["Americas VM Inventory"].get())
china_DataFrame = pd.read_csv(app.file_paths["China VM Inventory"].get())
japan_DataFrame = pd.read_csv(app.file_paths["Japan VM Inventory"].get())

# Load inventory files
sophosInventory_DataFrame = pd.read_csv(app.file_paths["Sophos Inventory"].get())
xdrInventory_DataFrame = pd.read_csv(app.file_paths["XDR Inventory"].get(), low_memory=False)

# Extract the column A from each file into its own variable
MH_hostnames = unitedKingdom_DataFrame.iloc[:, 0]  # all rows in first column using iloc
US_hostnames = americas_DataFrame.iloc[:, 0]
CL_hostnames = china_DataFrame.iloc[:, 0]
TK_hostnames = japan_DataFrame.iloc[:, 0]

sophos_enabled_list = sophosInventory_DataFrame.iloc[:, 1]

# xdr_enabled_list = xdre1.iloc[:, 22]

xdr_enabled_list = "" # This cleares the list before repopulating (as a precuation to avoid artifacts from previous runs.)
xdr_enabled_list = xdrInventory_DataFrame[((xdrInventory_DataFrame.iloc[:, 11] == "VERSION_SERVER_2008") \
                          |(xdrInventory_DataFrame.iloc[:, 11] == "VERSION_SERVER_2012") \
                          |(xdrInventory_DataFrame.iloc[:, 11] == "VERSION_SERVER_2012_R2")\
                          |(xdrInventory_DataFrame.iloc[:, 11] == "VERSION_SERVER_2016")\
                          |(xdrInventory_DataFrame.iloc[:, 11] == "VERSION_SERVER_2019")\
                          |(xdrInventory_DataFrame.iloc[:, 11] == "Windows Server 2016, Version 1607")\
                          |(xdrInventory_DataFrame.iloc[:, 11] == "Windows Server 2019, Version 1809")\
                          |(xdrInventory_DataFrame.iloc[:, 11] == "Windows Server 2022")\
                          |(xdrInventory_DataFrame.iloc[:, 11] == "Windows Server 2022, version 21H2")\
                           |(xdrInventory_DataFrame.iloc[:, 14] == "Red Hat Enterprise Linux 8.10 (Ootpa)")\
                           |(xdrInventory_DataFrame.iloc[:, 14] == "Red Hat Enterprise Linux 8.6 (Ootpa)")\
                           |(xdrInventory_DataFrame.iloc[:, 14] == "Red Hat Enterprise Linux")\
                           |(xdrInventory_DataFrame.iloc[:, 14] == "Red Hat Enterprise Linux 9.4 (Plow)")\
                           |(xdrInventory_DataFrame.iloc[:, 14] == "Red Hat Enterprise Linux Server 7.5 (Maipo)"))\
                          &(xdrInventory_DataFrame.iloc[:, 22].str.contains("VDI", na=False))\
                          ].iloc[:, 22].drop_duplicates()

print("*******************************************************************\n")
print("Current Servers with XDR Active' Length:", len(xdr_enabled_list), "\n")
print("*******************************************************************\n")

