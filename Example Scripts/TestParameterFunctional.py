#---------------------------------------------------------------------------
# TestParameterFunctionalAttribute.py
#
# PURPOSE: Test Functionality of Parameter Functional Attribute
#
#---------------------------------------------------------------------------

# Set Options
#   0   Clear Only
#   1   Run with defined table and database
#   2   Run with defined database
#   3   Run for entire server
options = 1

# Functions
def ClearData():
    # Import Functions
    from GRCMI import Connect

    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    db_key = "NasaGRC_MD_45_09-2-05"
    table_name = "Development Table #1"
    mi, db, table = Connect(server_name, db_key, table_name)

    # Get the record
    record = table.search_for_records_by_name('Parameter Based Functional Attribute Demo')[0]

    # Clear the functional data
    func = record.attributes['FP Demo']
    func.clear()
    record.set_attributes([func])
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
    from GRCMI import Connect, ParameterFunctional

    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    db_key = "NasaGRC_MD_45_09-2-05"
    table_name = "Development Table #1"
    mi, db, table = Connect(server_name, db_key, table_name)

    # Run
    msg = ParameterFunctional(mi, dbs = db, tables = table)
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