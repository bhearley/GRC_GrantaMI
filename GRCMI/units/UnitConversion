def UnitConversion(source_unit, source_value, target_unit):
    #---------------------------------------------------------------------------
    # UnitConversion.py
    #
    # PURPOSE: Perform Unit Conversion
    #
    # INPUTS:
    #    source_unit    the units to convert from
    #    source_value   the value for conversion
    #    target_unit    the units to convert to
    #
    # OUTPUTS:
    #    target_value   the value after conversion
    #---------------------------------------------------------------------------

    # Import Modules
    import requests

    # Load the units library
    url = 'https://raw.githubusercontent.com/bhearley/GRC_GrantaMI/refs/heads/main/GRCMI/units/unit_library.json'
    response = requests.get(url)

    # Check for valid file
    if response.status_code == 200:
        U = response.json()  # Parse the JSON response
    else:
        raise Exception("Error reading the material library.")

    # Check for valid keys
    if source_unit not in U.keys():
        raise ValueError("Source Unit " + source_unit + " not found in material library.")
    if target_unit not in U.keys():
        raise ValueError("Target Unit " + target_unit + " not found in material library.")
        
    # Convert to Global Unit
    data = U[source_unit]
    val = eval(data[0].replace('x', str(source_value)))
    
    # Convert to Target Unit
    data = U[target_unit]
    target_value = eval(data[1].replace('x', str(val)))

    return target_value