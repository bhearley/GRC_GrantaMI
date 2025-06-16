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
    import numpy as np
    import re
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
    if isinstance(source_value, float):
        val = eval(data[0].replace('x', str(source_value)))

    elif isinstance(source_value, int):
        val = eval(data[0].replace('x', str(source_value)))

    elif isinstance(source_value, np.ndarray):
        str_val = data[0].replace('x', np.array2string(source_value, threshold=np.inf))
        str_val = str_val.replace('[','np.array([')
        str_val = str_val.replace(']','])')
        str_val = re.sub(r'(?<=\d)\s+(?=[-]?\d)', ', ', str_val)
        val = eval(str_val)

    else:
        raise TypeError("Source value must be float, integer, or np.ndarray")
    

    # Convert to Target Unit
    data = U[target_unit]
    if isinstance(source_value, float):
        target_value = eval(data[1].replace('x', str(val)))

    elif isinstance(source_value, int):
        target_value = eval(data[1].replace('x', str(val)))

    elif isinstance(val,np.ndarray):
        str_val = data[1].replace('x', np.array2string(val, threshold=np.inf))
        str_val = str_val.replace('[','np.array([')
        str_val = str_val.replace(']','])')
        str_val = re.sub(r'(?<=\d)\s+(?=[-]?\d)', ', ', str_val)
        target_value = eval(str_val)

    else:
        raise TypeError("Target value must be float, integer, or np.ndarray")

    return target_value