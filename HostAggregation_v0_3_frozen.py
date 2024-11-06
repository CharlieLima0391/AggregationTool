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

# Read file into a dataframe - Note this needs to be replaced with the ability to choose files in the future.

#Source Data location C:\Users\cdominguez\python\aggregationtool\Working\sourceData
#Script Location C:\Users\cdominguez\python\aggregationtool\Working

class FileSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Selection")

         # Set desired window size
        window_width = 530
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
            "Americas": tk.StringVar(),
            "Japan": tk.StringVar(),
            "China": tk.StringVar(),
            "United Kingdom": tk.StringVar(),
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
unitedKingdom_DataFrame = pd.read_csv(app.file_paths["United Kingdom"].get())
americas_DataFrame = pd.read_csv(app.file_paths["Americas"].get())
china_DataFrame = pd.read_csv(app.file_paths["China"].get())
japan_DataFrame = pd.read_csv(app.file_paths["Japan"].get())

# Load inventory files
sophosInventory_DataFrame = pd.read_csv(app.file_paths["Sophos Inventory"].get())
xdrInventory_DataFrame = pd.read_csv(app.file_paths["XDR Inventory"].get(), low_memory=False)

# Extract the column A from each file into its own variable
MH_hostnames = unitedKingdom_DataFrame.iloc[:, 0]  # all rows in first column using iloc
US_hostnames = americas_DataFrame.iloc[:, 0]
CL_hostnames = china_DataFrame.iloc[:, 0]
TK_hostnames = japan_DataFrame.iloc[:, 0]

sophos_enabled_list = sophosInventory_DataFrame.iloc[:, 1]

#xdr_enabled_list = xdre1.iloc[:, 22]

print("Debugging here....\n")

xdr_enabled_list = ""
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

print("Current 'xdr_enabled_list' Length:", len(xdr_enabled_list), "\n")
print("************************************************************\n")

# Convert lists into Sets for comparison
MH_hostnames_set = set(MH_hostnames)
US_hostnames_set = set(US_hostnames)
CL_hostnames_set = set(CL_hostnames)
TK_hostnames_set = set(TK_hostnames)

sophos_enabled_list_set = set(sophos_enabled_list)

xdr_enabled_list_set = set(xdr_enabled_list)

# Number of Powered On Hosts
MH_powd_hostnames = set(unitedKingdom_DataFrame[unitedKingdom_DataFrame.iloc[:, 1] == "Powered On"].iloc[:, 0])
US_powd_hostnames = set(americas_DataFrame[americas_DataFrame.iloc[:, 1] == "Powered On"].iloc[:, 0])
CL_powd_hostnames = set(china_DataFrame[china_DataFrame.iloc[:, 1] == "Powered On"].iloc[:, 0])
TK_powd_hostnames = set(japan_DataFrame[japan_DataFrame.iloc[:, 1] == "Powered On"].iloc[:, 0])
                  
# Get common hosts to all sets (should be none as they are different geographic locations)
AllSets_Common_Hosts = MH_hostnames_set & US_hostnames_set & CL_hostnames_set & TK_hostnames_set

Number_Of_Common_Hosts = len(AllSets_Common_Hosts)

if Number_Of_Common_Hosts < 1:
    print("Hosts Common to all sets (aka Duplicates): None")
else:
    print("Hosts Common to all sets (aka Duplicates):", Number_Of_Common_Hosts)

#Unique Host Count
MH_unique_hosts = MH_hostnames_set - (US_hostnames_set | CL_hostnames_set | TK_hostnames_set)
US_unique_hosts = US_hostnames_set - (MH_hostnames_set | CL_hostnames_set | TK_hostnames_set)
CL_unique_hosts = CL_hostnames_set - (MH_hostnames_set | US_hostnames_set | TK_hostnames_set)
TK_unique_hosts = TK_hostnames_set - (MH_hostnames_set | US_hostnames_set | CL_hostnames_set)

# Hosts in each environment with Sophos
MH_sophos_enabled = MH_powd_hostnames & sophos_enabled_list_set
US_sophos_enabled = US_powd_hostnames & sophos_enabled_list_set
CL_sophos_enabled = CL_powd_hostnames & sophos_enabled_list_set
TK_sophos_enabled = TK_powd_hostnames & sophos_enabled_list_set

# Host in each Environment with XDR
MH_xdr_enabled = MH_powd_hostnames & xdr_enabled_list_set
US_xdr_enabled = US_powd_hostnames & xdr_enabled_list_set
CL_xdr_enabled = CL_powd_hostnames & xdr_enabled_list_set
TK_xdr_enabled = TK_powd_hostnames & xdr_enabled_list_set


# Powered-on hosts without Sophos
MH_without_sophos = MH_powd_hostnames - sophos_enabled_list_set
US_without_sophos = US_powd_hostnames - sophos_enabled_list_set
CL_without_sophos = CL_powd_hostnames - sophos_enabled_list_set
TK_without_sophos = TK_powd_hostnames - sophos_enabled_list_set

# Powered-on hosts without XDR
MH_without_xdr = MH_powd_hostnames - xdr_enabled_list_set
US_without_xdr = US_powd_hostnames - xdr_enabled_list_set
CL_without_xdr = CL_powd_hostnames - xdr_enabled_list_set
TK_without_xdr = TK_powd_hostnames - xdr_enabled_list_set

print("\nMH unique hosts Powered On:", len(MH_powd_hostnames), "(Total count:", len(MH_unique_hosts),")")
print("US unique hosts Powered On:", len(US_powd_hostnames), "(Total count:", len(US_unique_hosts),")")
print("CL unique hosts Powered On:", len(CL_powd_hostnames), "(Total count:", len(CL_unique_hosts),")")
print("TK unique hosts Powered On:", len(TK_powd_hostnames), "(Total count:", len(TK_unique_hosts),")")

total_powd_hosts = len(MH_powd_hostnames)+len(US_powd_hostnames)+len(CL_powd_hostnames)+len(TK_powd_hostnames)

print("\nGlobal Total Powered On hosts:", total_powd_hosts)

Total_XDR_Compatible_Hosts = (len(MH_xdr_enabled)+len(CL_xdr_enabled)+len(US_xdr_enabled)+len(TK_xdr_enabled)+len(MH_without_xdr)+len(CL_without_xdr)+len(US_without_xdr)+len(TK_without_xdr))
Total_XDR_Enabled_Hosts = len(MH_xdr_enabled)+len(CL_xdr_enabled)+len(US_xdr_enabled)+len(TK_xdr_enabled)

#Number of sophos enabled hosts (according to the sophos list)
print("\nSophos Enabled Host Count:", len(sophos_enabled_list_set))

#Number of XDR Enabled hosts (servers only - according to the XDR Export)
print("\nXDR Total Number of Hosts:", len(xdr_enabled_list))
print("XDR Total Number Compatible Host:", Total_XDR_Compatible_Hosts)
print("XDR Enabled Server Host Count (Supported Only):", Total_XDR_Enabled_Hosts)
print("XDR Disabled Server Host Count (Supported Only):", len(MH_without_xdr)+len(CL_without_xdr)+len(US_without_xdr)+len(TK_without_xdr))

#Number of Sophos Enabled and Disabled Devices
print("\nMH")
print("Sophos Present:", len(MH_sophos_enabled), "\nSophos Not Present:", len(MH_without_sophos))
print("XDR Present:", len(MH_xdr_enabled), "\nXDR Not Present:", len(MH_without_xdr))
print("\nUS")
print("Sophos Present:", len(US_sophos_enabled), "\nSophos Disabled:", len(US_without_sophos))
print("XDR Present:", len(US_xdr_enabled), "\nXDR Not Present:", len(US_without_xdr))
print("\nCL")
print("Sophos Present:", len(CL_sophos_enabled), "\nSophos Disabled:", len(CL_without_sophos))
print("XDR Present:", len(CL_xdr_enabled), "\nXDR Not Present:", len(CL_without_xdr))
print("\nTK")
print("Sophos Present:", len(TK_sophos_enabled), "\nSophos Disabled:", len(TK_without_sophos))
print("XDR Present:", len(TK_xdr_enabled), "\nXDR Not Present:", len(TK_without_xdr))

# Stats for Charles
print("\n")
print("*****************************************************************")
print("| % Servers With XDR |", ((Total_XDR_Enabled_Hosts * 100) / Total_XDR_Compatible_Hosts),"|", Total_XDR_Enabled_Hosts,"/", Total_XDR_Compatible_Hosts,"         *")
print("*****************************************************************")
print("| % Servers With AV  |", ((len(sophos_enabled_list_set) * 100) / total_powd_hosts)," |", len(sophos_enabled_list_set), "/", total_powd_hosts,"        *")
print("| (Trend or Sophos)  |                                          *")
print("*****************************************************************")




