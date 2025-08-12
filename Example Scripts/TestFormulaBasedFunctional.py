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
    from powermi import Connect

    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    db_key = "NasaGRC_MD_45_09-2-05"
    table_name = "Models (Demo)"
    mi, db, table = Connect(server_name, db_key, table_name)

    # Get the record
    record = table.search_for_records_by_name('Formula-Based Demo')[0]

    # Clear the functional data
    func = record.attributes['Demo Function']
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
    from powermi import Connect, FormulaBasedFunctional

    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    db_key = "NasaGRC_MD_45_09-2-05"
    table_name = "Models (Demo)"
    mi, db, table = Connect(server_name, db_key, table_name)

    # Run
    msg = FormulaBasedFunctional(mi, db, table)
    print(msg)

# Run with defined database
if options == 2:
    # Clear Data
    ClearData()

    # Import Functions
    from powermi import Connect, FormulaBasedFunctional

    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    db_key = "NasaGRC_MD_45_09-2-05"
    mi, db = Connect(server_name, db_key)

    # Run
    msg = FormulaBasedFunctional(mi, db)
    print(msg)

if options == 3:
    # Clear Data
    ClearData()

    # Import Functions
    from powermi import Connect, FormulaBasedFunctional

    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    mi = Connect(server_name)

    # Run
    msg = FormulaBasedFunctional(mi)
    print(msg)