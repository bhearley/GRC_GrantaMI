#---------------------------------------------------------------------------
#   PURPOSE: Test GRCMI Utility Functions
#---------------------------------------------------------------------------

# Import Functions
from powermi import *
import json
import os
from pathlib import Path

# Function to find files
def find_file(root_dir, filename):
    root_path = Path(root_dir)
    matches = list(root_path.rglob(filename))
    return matches

# Connect to server
server_name = "https://granta.ndc.nasa.gov"
db_key = "NasaGRC_MD_45_09-2-05"
table_name = "GRCMI Demo"
mi, db, table = Connect(server_name, db_key, table_name)

# Load the Demo Data
try:
    data_file = find_file(os.getcwd(), 'DemoData.json')
    with open(data_file[0],'r', encoding='utf-8') as f:
        RecData = json.load(f)
except:
    raise Exception(f'Unable to open DemoData.json.' )

# Check for the image and files
img_name = 'NASA_logo.png'
file_name = 'NASA_Schema.pdf'

img_file = find_file(os.getcwd(), img_name)
if len(img_file) == 0:
    raise Exception(f'{img_name} is not in home directory.' )

file_file = find_file(os.getcwd(), file_name)
if len(file_file) == 0:
    raise Exception(f'{file_name} is not in home directory.' )

# Load the Demo Links Data
try:
    link_file = find_file(os.getcwd(), 'DemoLinks.json')
    with open(link_file[0],'r', encoding='utf-8') as f:
        LinkData = json.load(f)
except:
    raise Exception(f'Unable to open DemoLinks.json.' )

# Get File Object
RecData['Test File']['Value'] = GetFileObject(os.path.join(os.getcwd(), 'Example Scripts', RecData['Test File']['Value']))
RecData['Test Tabular']['Value'][0][RecData['Test Tabular']['Columns'].index('Test Tab File')] = GetFileObject(os.path.join(os.getcwd(), 'Example Scripts', RecData['Test Tabular']['Value'][0][RecData['Test Tabular']['Columns'].index('Test Tab File')]))

# Get Image Object
RecData['Test Picture']['Value'] = GetFileObject(os.path.join(os.getcwd(), 'Example Scripts', RecData['Test Picture']['Value']))
RecData['Test Tabular']['Value'][0][RecData['Test Tabular']['Columns'].index('Test Tab Picture')] = GetFileObject(os.path.join(os.getcwd(), 'Example Scripts', RecData['Test Tabular']['Value'][0][RecData['Test Tabular']['Columns'].index('Test Tab Picture')]))

# Get Hyperlink Object for Tabular Only
RecData['Test Tabular']['Value'][0][RecData['Test Tabular']['Columns'].index('Test Tab Hyperlink')] = GetHyperLink( RecData['Test Tabular']['Value'][0][RecData['Test Tabular']['Columns'].index('Test Tab Hyperlink')])

# Define the file tree and get the parent folder
file_tree = ['Demo', 'Parent 1', 'Parent 2']
parent, GUIDS, flag, msg = GetParent(mi, db, table, file_tree)

# Get record
record = GetRecord(mi, db, table, 'New Record', parent)

# Write Record Data
record = WriteRecordData(mi, db, record, RecData, list(RecData.keys()), 'Replace')

# Create Linked record
link_record = GetRecord(mi, db, table, 'Linked Record', table)

# Write Record Links
record = WriteStaticLinks(mi, db, table, record, LinkData, list(LinkData.keys()))