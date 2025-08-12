#---------------------------------------------------------------------------
# TestMatrixAttribute.py
#
# PURPOSE: Test Matrix of Linked Functional Attribute
#
#---------------------------------------------------------------------------

# Import Functions
from powermi import Connect

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

    # Clear Demo 1
    table_name = "Machine Learning (Demo)"
    mi, db, table = Connect(server_name, db_key, table_name)
    record = table.search_for_records_by_name('Machine Learning Model')[0]

    # Clear Tabular Attributes
    tabl = record.attributes['Machine Learning Data Labels']
    for i in range(len(tabl.value)):
        tabl.value[i][tabl.columns.index('Column Name')] = None
        tabl.value[i][tabl.columns.index('Label')] = None
        tabl.value[i][tabl.columns.index('Unit')] = None
        tabl.value[i][tabl.columns.index('Link')] = None
    record.set_attributes([tabl])
    record = mi.update([record])[0]

    tabl = record.attributes['Training Data']
    for i in range(len(tabl.value)):
        tabl.value[i][tabl.columns.index('Attribute 1')] = None
        tabl.value[i][tabl.columns.index('Attribute 2')] = None
        tabl.value[i][tabl.columns.index('Attribute 3')] = None
        tabl.value[i][tabl.columns.index('Attribute 4')] = None
        tabl.value[i][tabl.columns.index('Link')] = None
    record.set_attributes([tabl])
    record = mi.update([record])[0]

    tabl = record.attributes['Validation Data']
    for i in range(len(tabl.value)):
        tabl.value[i][tabl.columns.index('Attribute 1')] = None
        tabl.value[i][tabl.columns.index('Attribute 2')] = None
        tabl.value[i][tabl.columns.index('Attribute 3')] = None
        tabl.value[i][tabl.columns.index('Attribute 4')] = None
        tabl.value[i][tabl.columns.index('Link')] = None
    record.set_attributes([tabl])
    record = mi.update([record])[0]

    # Clear Demo #2
    table_name = "Applications (Demo)"
    mi, db, table = Connect(server_name, db_key, table_name)
    record = table.search_for_records_by_name('IM7/8552/Al 6061 Sandwich')[0]

    # Clear Tabular Attributes
    tabl = record.attributes['Bill of Materials']
    for i in range(len(tabl.value)):
        tabl.value[i][tabl.columns.index('Material')] = None
        tabl.value[i][tabl.columns.index('Density')] = None
        tabl.value[i][tabl.columns.index('Modulus (11 axis)')] = None
        tabl.value[i][tabl.columns.index('Modulus (22 axis)')] = None
        tabl.value[i][tabl.columns.index("Poisson's Ratio (12 axis)")] = None
        tabl.value[i][tabl.columns.index("Poisson's Ratio (23 axis)")] = None
        tabl.value[i][tabl.columns.index('UTS (11 axis)')] = None
        tabl.value[i][tabl.columns.index('UTS (22 axis)')] = None
        tabl.value[i][tabl.columns.index('Link')] = None
    record.set_attributes([tabl])
    record = mi.update([record])[0]

    tabl = record.attributes['Standards']
    for i in range(len(tabl.value)):
        tabl.value[i][tabl.columns.index('Requirement ID')] = None
        tabl.value[i][tabl.columns.index('Requirement Description')] = None
        tabl.value[i][tabl.columns.index('Requirement Specification')] = None
        tabl.value[i][tabl.columns.index('Requirement Specification Unit')] = None
        tabl.value[i][tabl.columns.index('Requirement Criteria')] = None
        tabl.value[i][tabl.columns.index('Requirement Image')] = None
        tabl.value[i][tabl.columns.index('Link')] = None
    record.set_attributes([tabl])
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
    from powermi import Connect, RowLinkedTabular

    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    db_key = "NasaGRC_MD_45_09-2-05"
    mi, db = Connect(server_name, db_key)

    # Run
    msg = RowLinkedTabular(mi, db, ['Machine Learning (Demo)', 'Applications (Demo)'])
    print(msg)

# Run with defined database
if options == 2:
    # Clear Data
    ClearData()

    # Import Functions
    from powermi import Connect, RowLinkedTabular

    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    db_key = "NasaGRC_MD_45_09-2-05"
    mi, db = Connect(server_name, db_key)

    # Run
    msg = RowLinkedTabular(mi, db)
    print(msg)

if options == 3:
    # Clear Data
    ClearData()

    # Import Functions
    from powermi import Connect, RowLinkedTabular

    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    mi = Connect(server_name)

    # Run
    msg = RowLinkedTabular(mi)
    print(msg)