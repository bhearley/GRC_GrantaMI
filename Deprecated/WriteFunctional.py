def WriteFunctional(mi, db, record, RecData, FN = None, status = None):
    #   PURPOSE: Write functional attribute data to a record
    #
    #   INPUTS:
    #       mi      Granta Server Connection
    #       db      Selected Granta Database
    #       table   Selected Granta Table
    #       record  Granta MI record to write data to
    #       RecData Python Dictionary containing record data to write
    #       FN      List of Functional Attributes
    #       status  conflict statis
    #   OUTPUTS  
    #       record  Record with populated data

    # Import Modules
    try:
        from GRANTA_MIScriptingToolkit import granta as mpy
    except:
        raise Exception("ERROR 0000: Unable to import Granta Scripting Toolkit.")
    
    # Check inputs
    if isinstance(mi, mpy.mi.Session) == False:
        raise Exception("ERROR 0009: Invalid input for 'mi' - input must be a Granta MI Session object.")
    
    if isinstance(record, mpy.mi_record_classes.Record) == False:
        raise Exception("ERROR 0016: Invalid input for 'record' - input must be a Record.")
    
    if record.type != mpy.RecordType.Record:
        raise Exception("ERROR 0016: Invalid input for 'record' - input must be a Record.")
    
    if isinstance(RecData, dict) == False:
        raise Exception("ERROR 0017: Invalid input for 'RecData' - input must be a dict.")
    
    if FN is None:
        FN = list(RecData.keys())
    if isinstance(FN, list) == False:
        raise Exception("ERROR 0018: Invalid input for 'FV' - input must be a list of strings.")
    for F in FN:
        if isinstance(F, str) == False:
            raise Exception("ERROR 0018: Invalid input for 'FV' - input must be a list of string values.")
        if F not in RecData.keys():
            raise Exception("ERROR 0018: Invalid input for 'FV' - Value " + F + " not found in RecData.")
        
    if status is None:
        status = 'Replace'
    if isinstance(status, str) == False:
        raise Exception("ERROR 0018: Invalid input for 'status' - input must be either 'Append' or 'Replace'.")
    if status not in ['Append', 'Replace']:
        raise Exception("ERROR 0018: Invalid input for 'status' - input must be either 'Append' or 'Replace'.")

    # Preallocate List of Attributes to update
    AttList = []

    # Loop through all attributes
    for att in FN:

        if att not in record.attributes:
            raise Exception("ERROR 0020: Attribute " + att + " not found in " + record.name + ". Check data dicitonary.")
        
        if isinstance(RecData[att], dict) == False:
            raise Exception("ERROR 0021: Invalid data dictionary format. Field " + att + " in data dicitonary is not a dictionary. ")

        if 'Y' not in RecData[att].keys():
            raise Exception("ERROR 0021: Invalid data dictionary format. Field " + att + " in data dicitonary does not contain 'Y'. ")
        if 'Value' not in RecData[att]['Y'].keys():
            raise Exception("ERROR 0021: Invalid data dictionary format. Field 'Y' in " + att + " in data dicitonary does not contain 'Value'. ")

        if RecData[att]['Y']['Value'] is not None:

            # Check value of Y
            if isinstance(RecData[att]['Y']['Value'], list) == False:
                try:
                    RecData[att]['Y']['Value'] = list(RecData[att]['Y']['Value'])
                except:
                    raise Exception("ERROR 0021: Invalid value for field 'Y' in " + att + " in data dicitonary. 'Value' must contain a list. ")

            # Get Default Unit for Y
            unit = record.attributes[att].unit
            convy = {'factor':1,
                     'offset':0}
            if unit != '':
                # Get data dictionary unit
                try:
                    data_unit = RecData[att]['Y']['Units']
                except:
                    raise Exception("ERROR 0029: 'Units' field not available in data dicitonary for 'Y' in " + att + ".")
                if isinstance(data_unit, str) == False:
                    raise Exception("ERROR 0030: Invalid units in data dictionary for 'Y' in " + att + ". " + "Units value must be a string.")
                
                if unit != data_unit:
                    convy = db.dimensionally_equivalent_units(data_unit)
                    if unit not in convy.keys():
                        raise Exception("ERROR 0031: Unable to convert " + data_unit + " in data dictionary to " + unit + " in Granta MI for " + att + ". Check definition of 'Y' Units field.")
                    convy = convy[unit]
            
            # Unpack Parameter and Function Values
            keys = []
            for key in RecData[att].keys():
                if key in record.attributes[att].parameters.keys():
                    keys.append(key)

            # If generic 'X' field is used, set first unrestricted numeric to X
            if 'X' in RecData[att].keys():
                for param in  record.attributes[att].parameters.keys():
                    if  record.attributes[att].parameters[param].type == "Unrestricted numeric":
                        RecData[att][param] = RecData[att].pop('X')
                        keys.append(param)
                        break
            if len(keys) == 0:
                raise Exception("ERROR 0021: Invalid data dictionary format. No parameter for " + att + " found in the data dictionary. ")

            # Check all unrestricted numeric parameters have the same length as Y
            num_param = []
            convx_all = {}
            disc_param = []
            for key in keys:
                if record.attributes[att].parameters[key].type == "Unrestricted numeric":
                    num_param.append(key)
                    if 'Value' not in RecData[att][key].keys():
                        raise Exception("ERROR 0021: Invalid data dictionary format. Field '" + key + "' in " + att + " in data dicitonary does not contain 'Value'. ")
                    if isinstance(RecData[att][key]['Value'], list) == False:
                        try:
                            RecData[att][key]['Value'] = list(RecData[att]['Y']['Value'])
                        except:
                            raise Exception("ERROR 0021: Invalid value for field '" + key + "' in " + att + " in data dicitonary. 'Value' must contain a list. ")
                    if len(RecData[att][key]['Value']) != len(RecData[att]['Y']['Value']):
                        raise Exception("ERROR 0021: Invalid value for field '" + key + "' in " + att + " in data dicitonary. List length does not match 'Y'. ")

                    unit = record.attributes[att].parameters[key].unit
                    convx_all[key] = {'factor':1,
                                      'offset':0}
                    if unit != '':
                        # Get data dictionary unit
                        try:
                            data_unit = RecData[att][key]['Units']
                        except:
                            raise Exception("ERROR 0029: 'Units' field not available in data dicitonary for '" + key + "' in " + att + ".")
                        if isinstance(data_unit, str) == False:
                            raise Exception("ERROR 0030: Invalid units in data dictionary for '" + key + "' in " + att + ". " + "Units value must be a string.")
                        
                        if unit != data_unit:
                            convx = db.dimensionally_equivalent_units(data_unit)
                            if unit not in convx.keys():
                                raise Exception("ERROR 0031: Unable to convert " + data_unit + " in data dictionary to " + unit + " in Granta MI for " + att + ". Check definition of '" + key + "' Units field.")
                            convx_all[key] = convx[unit]
                
                
                elif record.attributes[att].parameters[key].type == "Discrete":
                    disc_param.append(key)
                    if 'Value' not in RecData[att][key].keys():
                        raise Exception("ERROR 0021: Invalid data dictionary format. Field '" + key + "' in " + att + " in data dicitonary does not contain 'Value'. ")

                    if isinstance(RecData[att][key]['Value'], list) == False:
                        new_val = []
                        for i in range(len(RecData[att]['Y']['Value'])):
                            new_val.append(RecData[att][key]['Value'] )
                        RecData[att][key]['Value'] = new_val

                    if len(RecData[att][key]['Value']) != len(RecData[att]['Y']['Value']):
                        raise Exception("ERROR 0021: Invalid value for field '" + key + "' in " + att + " in data dicitonary. List length does not match 'Y'. ")

                    for i, item in enumerate(RecData[att][key]['Value']):
                        if isinstance(item,str) == False:
                            try:
                                item = str(item)
                                RecData[att][key]['Value'][i] = item
                            except:
                                raise Exception("ERROR 0021: Invalid value for field '" + key + "' in " + att + " in data dicitonary. Discrete parameter value must be a string or list of strings. ")

                        if item not in record.attributes[att].parameters[key].values:
                            raise Exception("ERROR 0021: Invalid value for field '" + key + "' in " + att + " in data dicitonary. 'Value' is not in the discrete options for the parameter.")


            # Get functional data       
            func = record.attributes[att]

            # Clear any previous data if status is Replace
            if status == 'Replace':
                func.clear()

            # Add Data Points
            for i in range(len(RecData[att]['Y']['Value'])):
                func_dict = {}
                # -- Add y
                y_val = RecData[att]['Y']['Value'][i]
                if isinstance(y_val, list) == False:
                    try:
                        y_val = float(y_val*convy['factor'] + convy['offset'])
                    except:
                        raise Exception("ERROR 0021: Invalid value for field 'Y' in " + att + " in data dicitonary. 'Value' could not be converted to float.")
                    func_dict['y'] = y_val
                else:
                    if len(y_val) != 2:
                        raise Exception("ERROR 0021: Invalid value for field 'Y' in " + att + " in data dicitonary. 'Value' could not be converted to float.")

                    try:
                        y_val[0] = float(y_val[0]*convy['factor'] + convy['offset'])
                        y_val[1] = float(y_val[1]*convy['factor'] + convy['offset'])
                        y_val = {'low':min([float(y_val[0]), float(y_val[1])]),
                                'high':max([float(y_val[0]), float(y_val[1])])}
                    except:
                        raise Exception("ERROR 0021: Invalid value for field 'Y' in " + att + " in data dicitonary. Range in 'Value' could not be converted to float.")

                    if record.attributes[att].unit != '':
                        min_key = 'Y Min (' + att + ' [' + record.attributes[att].unit + '])'
                        max_key = 'Y Max (' + att + ' [' + record.attributes[att].unit + '])'
                    else:
                        min_key = 'Y Min (' + att + ')'
                        max_key = 'Y Max (' + att + ')'
                    func_dict['ymin'] = y_val['low']
                    func_dict['ymax'] = y_val['high']

                # -- Add Numeric Parameters
                for p in num_param:
                    x_val = RecData[att][p]['Value'][i]
                    try:
                        x_val = float(x_val*convx_all[p]['factor'] + convx_all[p]['offset'])
                    except:
                        raise Exception("ERROR 0021: Invalid value for field '" + key + "' in " + att + " in data dicitonary. 'Value' could not be converted to float.")

                    func_dict[p] = x_val

                # -- Add discrete Parameters
                for p in disc_param:
                    func_dict[p] = RecData[att][p]['Value'][i]
                    
                # Add Point
                if 'y' in func_dict.keys():
                    func.add_point(func_dict)
                else:
                    func.add_range(func_dict)

            if 'Metadata' in RecData[att].keys():
                meta_atts = list(RecData[att]['Metadata'].keys())
                for meta_att in meta_atts:
                    if meta_att not in record.attributes[att].meta_attributes:
                        raise Exception("ERROR 0036: Meta-Attribute " + meta_att + " not found in " + att + " in " + record.name + ". Check data dicitonary.")

                    if isinstance(RecData[att]['Metadata'][meta_att], dict) == False:
                        raise Exception("ERROR 0037: Invalid data dictionary format. Field " + meta_att + " in " + att+ " in data dicitonary is not a dictionary. ")

                    if "Value" not in RecData[att]['Metadata'][meta_att].keys():
                        raise Exception("ERROR 0038: Invalid data dictionary format. 'Value' not found in " + meta_att + " in " + att + " in data dicitonary.")

                    # Get Value
                    val = RecData[att]['Metadata'][meta_att]['Value']

                    # Get data validation
                    val = data_validation(val, record.attributes[att].meta_attributes[meta_att].type)

                    # Write value to record
                    if record.attributes[att].meta_attributes[meta_att].type in ['FILE', 'PICT']:
                        record.attributes[att].meta_attributes[meta_att].object = val
                    else:    
                        record.attributes[att].meta_attributes[meta_att].value = val

            # Add attribute to list of attributes to update
            AttList.append(func)

    # Write Data
    if len(AttList) > 0:
        # Set the Attributes
        record.set_attributes(AttList)

        # Update the record
        record = mi.update([record])[0]

    return record