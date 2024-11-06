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
from tkinter import filedialog as fidi


# Read file into a dataframe - Note this needs to be replaced with the ability to choose files in the future.

#Source Data location C:\Users\cdominguez\python\aggregationtool\Working\sourceData
#Script Location C:\Users\cdominguez\python\aggregationtool\Working

def select_file_dialog():
    filePath = fidi.askopenfilename(title="Select a file...")

#os.system('cls') #Doesn't work in IDLE

df1 = pd.read_csv(r'C:\Users\cdominguez\python\aggregationtool\Working\sourceData\MHDVMVC01.csv')
df2 = pd.read_csv(r'C:\Users\cdominguez\python\aggregationtool\Working\sourceData\amsvmvc01.csv')
df3 = pd.read_csv(r'C:\Users\cdominguez\python\aggregationtool\Working\sourceData\cljvmvc01.csv')
df4 = pd.read_csv(r'C:\Users\cdominguez\python\aggregationtool\Working\sourceData\tkovmvc01.csv')

se_df = pd.read_csv(r'C:\Users\cdominguez\python\aggregationtool\Working\sourceData\Sophos_Servers_Active.csv')

xdr_df = pd.read_csv(r'C:\Users\cdominguez\python\aggregationtool\Working\sourceData\endpoint_agents_page_2024-10-31T10_56_43_dedup.csv', low_memory=False)


# Extract the column A from each file into its own variable
MH_hostnames = df1.iloc[:, 0] #all rows in first column using iloc
US_hostnames = df2.iloc[:, 0]
CL_hostnames = df3.iloc[:, 0]
TK_hostnames = df4.iloc[:, 0]

sophos_enabled_list = se_df.iloc[:, 1]

#xdr_enabled_list = xdre1.iloc[:, 22]

print("Debugging here....\n")

xdr_enabled_list = ""
xdr_enabled_list = xdr_df[((xdr_df.iloc[:, 11] == "VERSION_SERVER_2008") \
                          |(xdr_df.iloc[:, 11] == "VERSION_SERVER_2012") \
                          |(xdr_df.iloc[:, 11] == "VERSION_SERVER_2012_R2")\
                          |(xdr_df.iloc[:, 11] == "VERSION_SERVER_2016")\
                          |(xdr_df.iloc[:, 11] == "VERSION_SERVER_2019")\
                          |(xdr_df.iloc[:, 11] == "Windows Server 2016, Version 1607")\
                          |(xdr_df.iloc[:, 11] == "Windows Server 2019, Version 1809")\
                          |(xdr_df.iloc[:, 11] == "Windows Server 2022")\
                          |(xdr_df.iloc[:, 11] == "Windows Server 2022, version 21H2")\
                           |(xdr_df.iloc[:, 14] == "Red Hat Enterprise Linux 8.10 (Ootpa)")\
                           |(xdr_df.iloc[:, 14] == "Red Hat Enterprise Linux 8.6 (Ootpa)")\
                           |(xdr_df.iloc[:, 14] == "Red Hat Enterprise Linux")\
                           |(xdr_df.iloc[:, 14] == "Red Hat Enterprise Linux 9.4 (Plow)")\
                           |(xdr_df.iloc[:, 14] == "Red Hat Enterprise Linux Server 7.5 (Maipo)"))\
                          &(xdr_df.iloc[:, 22].str.contains("VDI", na=False))\
                          ].iloc[:, 22]

#MH_powd_hostnames = df1[df1.iloc[:, 1] == "Powered On"].iloc[:, 22]

#xdr_enabled_list = (xdr_df [ xdr_df [ ~xdr_df.iloc[:, 22].str.contains("VDI", na=False)].iloc[:, 4] == "Active"].iloc[:, 22])

'''
xdr_enabled_list = xdr_df[(~xdr_df.iloc[:, 12].str.contains("LINUX", na=True)) \
                          & (~xdr_df.iloc[:, 11].str.contains("VERSION_WIN10", na=True))\
                          & (~xdr_df.iloc[:, 22].str.contains("VDI", na=True))\
                          & (xdr_df.iloc[:, 4] == "Active")].iloc[:, 22]
'''

'''
xdr_enabled_list = xdr_df[(~xdr_df.iloc[:, 11].str.contains("VERSION_SERVER_2008", na=True)) \
                          | (~xdr_df.iloc[:, 11].str.contains("VERSION_SERVER_2012", na=True))\
                          | (~xdr_df.iloc[:, 11].str.contains("VERSION_SERVER_2012_R2", na=True))].iloc[:, 22]
                          #& (xdr_df.iloc[:, 4] == "Active")].iloc[:, 22]
'''

#xdr_enabled_list = xdr_df[(~xdr_df.iloc[:, 11].str.contains("VERSION_SERVER_2008", na=False))].iloc[:, 22]

#xdr_enabled_list = xdr_df[(~xdr_df.iloc[:, 12].str.contains("OS_FAMILY_TEST", na=True))].iloc[:, 22]


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
MH_powd_hostnames = set(df1[df1.iloc[:, 1] == "Powered On"].iloc[:, 0])
US_powd_hostnames = set(df2[df2.iloc[:, 1] == "Powered On"].iloc[:, 0])
CL_powd_hostnames = set(df3[df3.iloc[:, 1] == "Powered On"].iloc[:, 0])
TK_powd_hostnames = set(df4[df4.iloc[:, 1] == "Powered On"].iloc[:, 0])
                  
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

#print("MH unique hosts: (count:", len(MH_unique_hosts),")")
#print("US unique hosts: (count:", len(US_unique_hosts),")")
#print("CL unique hosts: (count:", len(CL_unique_hosts),")")
#print("TK unique hosts: (count:", len(TK_unique_hosts),")")

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

# Check unique values in column B for each DataFrame (Debug Only - comment out (with ''') to switch off)
'''
print("\n")
print("Unique values in MH (df1) state column:", df1.iloc[:, 1].unique())
print("Unique values in US (df2) state column:", df2.iloc[:, 1].unique())
print("Unique values in CL (df3) state column:", df3.iloc[:, 1].unique())
print("Unique values in TK (df4) state column:", df4.iloc[:, 1].unique())
'''

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


''' Output the sets to the console '''
#print("MH_hostnames:", MH_hostnames_set)
#print("\nUS_hostnames:", US_hostnames_set)
#print("\nCL_hostnames:", CL_hostnames_set)
#print("\nTK_hostnames:", TK_hostnames_set)

# Stats for Charles

print("\n")
print("*****************************************************************")
print("| % Servers With XDR |", ((Total_XDR_Enabled_Hosts * 100) / Total_XDR_Compatible_Hosts),"|", Total_XDR_Enabled_Hosts,"/", Total_XDR_Compatible_Hosts,"         *")
print("*****************************************************************")
print("| % Servers With AV  |", ((len(sophos_enabled_list_set) * 100) / total_powd_hosts)," |", len(sophos_enabled_list_set), "/", total_powd_hosts,"        *")
print("| (Trend or Sophos)  |                                          *")
print("*****************************************************************")




