# Import Modules
from GRCMI import Connect, UnitConversion


# ----------------------------------------------------------------------------
# Test Connect.py

try:
    # Connect to the database
    server_name = "https://granta.ndc.nasa.gov"
    db_key = "NasaGRC_MD_45_09-2-05"
    table_name = "Material Pedigree"
    mi, db, table = Connect(server_name, db_key, table_name)

    print('Connect.py Succesful!')

except:
    print('Connect.py Failed!')

# ----------------------------------------------------------------------------
# Test UnitConversion.py

try:
    # Perform Unit Conversion
    source_unit = 'Pa'
    source_value = 1e6
    target_unit = 'MPa'
    target_value = UnitConversion(source_unit, source_value, target_unit)

    if target_value == 1:
        print('UnitConversion.py Succesful!')
    else:
        print('UnitConversion.py Failed!')
except:
    print('UnitConversion.py Failed!')
