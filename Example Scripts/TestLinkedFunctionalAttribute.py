#---------------------------------------------------------------------------
# TestLinkedFunctionalAttribute.py
#
# PURPOSE: Test Functionality of Linked Functional Attribute
#
#---------------------------------------------------------------------------

# Import Functions
from GRCMI import Connect, LinkedFunctional

# Set Options
#   0   Clear Only
#   1   Run with defined table and database
#   2   Run with defined database
#   3   Run for entire server
options = 1

# Functions
def ClearData():
    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    db_key = "NasaGRC_MD_45_09-2-05"
    table_name = "Models (Demo)"
    mi, db, table = Connect(server_name, db_key, table_name)
    record = table.search_for_records_by_name('Simulation Data Record')[0]
    func = record.attributes['Simulation Data: Stress vs Strain']
    tabl = record.attributes['Simulation Data: Stress vs Strain Functional Linking Data']

    # Get Orginal Data
    # -- Get All Functional Data
    all_data = func.value[1:]

    # -- Extract orginal local data
    orig_data = []
    for i in range(len(all_data)):
        if all_data[i][3] not in ['Test']:
            orig_data.append(all_data[i])

    # Clear the attribute and write local data
    func.clear()
    for i in range(len(orig_data)):
        func.add_point({'y':float(orig_data[i][0]),
                        'Strain':float(orig_data[i][2]),
                        'Simulation Data':orig_data[i][3]})
        
    # Clear the Link
    for i in range(len(tabl.value)):
        tabl.value[i][tabl.columns.index('Link')] = None
        
    record.set_attributes([func, tabl])
    record = mi.update([record])[0]

    return

# Clear only
if options == 0:
    # Clear Data
    ClearData()

# Run with defined tables
if options == 1:
    # Clear Data
    ClearData()

    # Import Functions
    from GRCMI import Connect, LinkedFunctional

    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    db_key = "NasaGRC_MD_45_09-2-05"
    table_name = "Models (Demo)"
    mi, db, table = Connect(server_name, db_key, table_name)

    # Run
    msg = LinkedFunctional(mi, dbs = db, tables = table)
    print(msg)

# Run with defined database
if options == 2:
    # Clear Data
    ClearData()

    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    db_key = "NasaGRC_MD_45_09-2-05"
    table_name = "Development Table #2"
    mi, db, table = Connect(server_name, db_key, table_name)

    # Run
    msg = LinkedFunctional(mi, dbs = db)
    print(msg)

if options == 3:
    # Clear Data
    ClearData()

    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    db_key = "NasaGRC_MD_45_09-2-05"
    table_name = "Development Table #2"
    mi, db, table = Connect(server_name, db_key, table_name)

    # Run
    msg = LinkedFunctional(mi)
    print(msg)