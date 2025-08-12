def WriteRecordData(mi, db, record, RecData, attributes = None, status = None):
    #---------------------------------------------------------------------------
    #   PURPOSE: Write all attribute data to a record
    #
    #   INPUTS:
    #   INPUTS:
    #       mi          SessionObject       Granta Server Connection
    #       db          DatabaseObject      Selected Granta Database
    #       record      RecordObject        Granta MI record to write data to
    #       RecData     dict                Python Dictionary containing record 
    #                                       data to write
    #       attributes  list(str)           List of Single Value Attributes
    #       status      string              Conflict resolution status
    #                                           'Replace' - replace all data
    #                                           'Append'  - append to existing
    #                                                       data
    #                                           'Do Not Replace' - skip if data
    #                                                              exists
    #
    #   OUTPUTS  
    #       record      RecordObject        Record with populated data
    #---------------------------------------------------------------------------

    # Import Modules
    from datetime import datetime
    try:
        from GRANTA_MIScriptingToolkit import granta as mpy
    except:
        raise Exception("Unable to import Granta Scripting Toolkit.")
    
    # Check inputs
    if isinstance(mi, mpy.mi.Session) == False:
        raise Exception("Invalid input for 'mi'. 'mi' must be a Granta MI Session object.")
    
    if isinstance(db, mpy.mi_tree_classes.Database) == False:
        raise Exception("Invalid input for 'db'. 'db' must be a Granta MI Database object.")
    
    if isinstance(record, mpy.mi_record_classes.Record) == False:
        raise Exception("Invalid input for 'record'. 'record' must be a Record object.")

    if isinstance(RecData, dict) == False:
        raise Exception("Invalid input for 'RecData'. 'RecData must be a dict.")
    
    if attributes is None:
        attributes = list(RecData.keys())

    if isinstance(attributes, list) == False:
        raise Exception("Invalid input for 'attributes'. 'attributes must be a list of strings.")
    
    for att in attributes:
        if isinstance(att, str) == False:
            raise Exception("Invalid input for 'attributes'. 'attributes must be a list of string values.")
        
        if att not in RecData.keys():
            raise Exception("Invalid input for 'attributes'. Value " + att + " not found in RecData.")
        
    if status is None:
        status = 'Replace'

    if isinstance(status, str) == False:
        raise Exception("Invalid input for 'status'. 'status' must be either 'Append','Replace', or 'Do Not Replace'.")
    
    if status not in ['Append', 'Replace','Do Not Replace']:
        raise Exception("Invalid input for 'status'. 'status' must be either 'Append', 'Replace', or 'Do Not Replace'.")
    

    # Single Value Data Validation
    def data_validation(val, dtype, opts = [], unit = '', data_unit = '', hlink_flag = 0):
        # Short Text
        if dtype == 'STXT':
            if isinstance(val, str) == False:
                try:
                    val = str(val)
                except:
                    raise Exception("Invalid value in data dictionary for " + att + ". Unable to convert to string for STXT.")
            if len(val) > 255:
                raise Exception("Invalid value in data dictionary for " + att + ". Too many characters for STXT (Max 255).")
            return val

        # Long Text
        if dtype == 'LTXT':
            if isinstance(val, str) == False:
                try:
                    val = str(val)
                except:
                    raise Exception("Invalid value in data dictionary for " + att + ". Unable to convert to string for LTXT.")
            if len(val) > 1e6:
                raise Exception("Invalid value in data dictionary for " + att + ". Too many characters for LTXT (Max 1,000,000).")
            return val

        # Discrete
        if dtype == 'DISC':
            if val not in opts:
                raise Exception("Invalid value in data dictionary for " + att + ". Value is not in the available discrete options.")
            return val

        # Point
        if dtype == 'POIN':
            if isinstance(val, float) == False:
                try:
                    val = float(val)
                except:
                    raise Exception("Invalid value in data dictionary for " + att + ". " + "Unable to convert value to point.")
                
            # Get Default Unit
            if unit != '':
                
                if unit == data_unit:
                    return val

                else:
                    conv_dict = db.dimensionally_equivalent_units(data_unit)
                    if unit not in conv_dict.keys():
                        raise Exception("Unable to convert " + data_unit + " in data dictionary to " + unit + " in Granta MI for " + att + ".")
                    val = val*conv_dict[unit]['factor'] + conv_dict[unit]['offset']
                    return val

            else:
                return val

        # Range
        if dtype == 'RNGE':
            if isinstance(val, list) == False:
                try:
                    val = list(val)
                except:
                    raise Exception("Invalid value in data dictionary for " + att + ". " + "Value must be a list containing two point values.")
            if len(val) != 2:
                raise Exception("Invalid value in data dictionary for " + att + ". " + "Value must be a list containing two point values.")
            for v in val:
                if v is not None:
                    try:
                        float(v)
                    except:
                        raise Exception("Invalid value in data dictionary for " + att + ". " + "Value must be a list containing two point values.")
                
            # Get Default Unit
            if unit != '':

                if unit == data_unit:
                    val = {'low':val[0], 'high':val[1]}
                    return val

                else:
                    conv_dict = db.dimensionally_equivalent_units(data_unit)
                    if unit not in conv_dict.keys():
                        raise Exception("Unable to convert " + data_unit + " in data dictionary to " + unit + " in Granta MI for " + att + ".")
                    try:
                        val[0] = val[0]*conv_dict[unit]['factor'] + conv_dict[unit]['offset']
                    except:
                        pass
                    try:
                        val[1] = val[1]*conv_dict[unit]['factor'] + conv_dict[unit]['offset']
                    except:
                        pass
                    val = {'low':val[0], 'high':val[1]}
                    return val

            else:
                val = {'low':val[0], 'high':val[1]}
                return val

        # Integer
        if dtype == 'INPT':
            if isinstance(val, int) == False:
                try:
                    val = int(val)
                except:
                    raise Exception("Invalid value in data dictionary for " + att + ". " + "Unable to convert value to integer.")
                
            return val

        # Logic
        if dtype == 'LOGI':
            if val not in ['Yes', 'No', True, False]:
                raise Exception("Invalid value in data dictionary for " + att + ". " + "Logical value must be 'Yes', 'No', True, or False.")
            if val == 'Yes':
                val = True
            elif val == 'No':
                val = False
            return val

        # Date
        if dtype == 'DTTM':
            try:
                val = datetime.strptime(val, "%m/%d/%Y")
                return val
            except:
                raise Exception("Invalid value in data dictionary for " + att + ". " + "Unable to convert value to date.")
            
        # File
        if dtype == 'FILE':
            if isinstance(val, mpy.mi_attribute_value_classes.File) == False:
                raise Exception("Invalid value in data dictionary for " + att + ". " + "Use GetFileObject to get a Granta MI File Object.")
            return val
        
        # Image
        if dtype == 'PICT':
            if isinstance(val, mpy.mi_attribute_value_classes.File) == False:
                raise Exception("Invalid value in data dictionary for " + att + ". " + "Use GetFileObject to get a Granta MI File Object.")
            if val.value.file_name.split('.')[-1] not in ['png', 'jpg', 'bmp', 'tif']:
                raise Exception("Invalid value in data dictionary for " + att + ". " + "Granta MI File Object must be an image for a PICT attribute.")
            
            return val
        
        # Hyperlink
        if dtype == 'HLNK':
            if hlink_flag == 0:
                if isinstance(val, str) == False:
                    raise Exception("Invalid value in data dictionary for " + att + ". Value must be a string.")
            else:
                if isinstance(val, mpy.mi_attribute_value_classes.Hyperlink) == False:
                    raise Exception("Invalid value in data dictionary for " + att + ". " + "Use GetHyperLink to get a Granta MI Hyperlink Object.")
            return val

    # Functional Data
    def functional_data(func, RecData, att, db):

        # Check RecData Structure
        if isinstance(RecData[att], dict) == False:
            raise Exception("Invalid data dictionary format. Field " + att + " in data dicitonary is not a dictionary. ")

        if 'Y' not in RecData[att].keys():
            raise Exception("Invalid data dictionary format. Field " + att + " in data dicitonary does not contain 'Y'. ")
        if 'Value' not in RecData[att]['Y'].keys():
            raise Exception("Invalid data dictionary format. Field 'Y' in " + att + " in data dicitonary does not contain 'Value'. ")

        # Get Data in RecData
        if RecData[att]['Y']['Value'] is not None:

            # Check value of Y
            if isinstance(RecData[att]['Y']['Value'], list) == False:
                try:
                    RecData[att]['Y']['Value'] = list(RecData[att]['Y']['Value'])
                except:
                    raise Exception("Invalid value for field 'Y' in " + att + " in data dicitonary. 'Value' must contain a list. ")

            # Get Default Unit for Y
            unit = func.unit
            convy = {'factor':1,
                     'offset':0}
            if unit != '':
                # Get data dictionary unit
                try:
                    data_unit = RecData[att]['Y']['Units']
                except:
                    raise Exception("'Units' field not available in data dicitonary for 'Y' in " + att + ".")
                if isinstance(data_unit, str) == False:
                    raise Exception("Invalid units in data dictionary for 'Y' in " + att + ". " + "Units value must be a string.")
                
                if unit != data_unit:
                    convy = db.dimensionally_equivalent_units(data_unit)
                    if unit not in convy.keys():
                        raise Exception("Unable to convert " + data_unit + " in data dictionary to " + unit + " in Granta MI for " + att + ". Check definition of 'Y' Units field.")
                    convy = convy[unit]
            
            # Unpack Parameter and Function Values
            keys = []
            for key in RecData[att].keys():
                if key in func.parameters.keys():
                    keys.append(key)

            # If generic 'X' field is used, set first unrestricted numeric to X
            if 'X' in RecData[att].keys():
                for param in  func.parameters.keys():
                    if  func.parameters[param].type == "Unrestricted numeric":
                        RecData[att][param] = RecData[att].pop('X')
                        keys.append(param)
                        break
            if len(keys) == 0:
                raise Exception("Invalid data dictionary format. No parameter for " + att + " found in the data dictionary. ")

            # Check all unrestricted numeric parameters have the same length as Y
            num_param = []
            convx_all = {}
            disc_param = []
            for key in keys:
                if func.parameters[key].type == "Unrestricted numeric":
                    num_param.append(key)
                    if 'Value' not in RecData[att][key].keys():
                        raise Exception("Invalid data dictionary format. Field '" + key + "' in " + att + " in data dicitonary does not contain 'Value'. ")
                    if isinstance(RecData[att][key]['Value'], list) == False:
                        try:
                            RecData[att][key]['Value'] = list(RecData[att]['Y']['Value'])
                        except:
                            raise Exception("Invalid value for field '" + key + "' in " + att + " in data dicitonary. 'Value' must contain a list. ")
                    if len(RecData[att][key]['Value']) != len(RecData[att]['Y']['Value']):
                        raise Exception("Invalid value for field '" + key + "' in " + att + " in data dicitonary. List length does not match 'Y'. ")

                    unit = func.parameters[key].unit
                    convx_all[key] = {'factor':1,
                                      'offset':0}
                    if unit != '':
                        # Get data dictionary unit
                        try:
                            data_unit = RecData[att][key]['Units']
                        except:
                            raise Exception("'Units' field not available in data dicitonary for '" + key + "' in " + att + ".")
                        if isinstance(data_unit, str) == False:
                            raise Exception("Invalid units in data dictionary for '" + key + "' in " + att + ". " + "Units value must be a string.")
                        
                        if unit != data_unit:
                            convx = db.dimensionally_equivalent_units(data_unit)
                            if unit not in convx.keys():
                                raise Exception("Unable to convert " + data_unit + " in data dictionary to " + unit + " in Granta MI for " + att + ". Check definition of '" + key + "' Units field.")
                            convx_all[key] = convx[unit]
                
                
                elif func.parameters[key].type == "Discrete":
                    disc_param.append(key)
                    if 'Value' not in RecData[att][key].keys():
                        raise Exception("Invalid data dictionary format. Field '" + key + "' in " + att + " in data dicitonary does not contain 'Value'. ")

                    if isinstance(RecData[att][key]['Value'], list) == False:
                        new_val = []
                        for i in range(len(RecData[att]['Y']['Value'])):
                            new_val.append(RecData[att][key]['Value'] )
                        RecData[att][key]['Value'] = new_val

                    if len(RecData[att][key]['Value']) != len(RecData[att]['Y']['Value']):
                        raise Exception("Invalid value for field '" + key + "' in " + att + " in data dicitonary. List length does not match 'Y'. ")

                    for i, item in enumerate(RecData[att][key]['Value']):
                        if isinstance(item,str) == False:
                            try:
                                item = str(item)
                                RecData[att][key]['Value'][i] = item
                            except:
                                raise Exception("Invalid value for field '" + key + "' in " + att + " in data dicitonary. Discrete parameter value must be a string or list of strings. ")

                        if item not in func.parameters[key].values:
                            raise Exception("Invalid value for field '" + key + "' in " + att + " in data dicitonary. 'Value' is not in the discrete options for the parameter.")

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
                        raise Exception("Invalid value for field 'Y' in " + att + " in data dicitonary. 'Value' could not be converted to float.")
                    func_dict['y'] = y_val
                else:
                    if len(y_val) != 2:
                        raise Exception("Invalid value for field 'Y' in " + att + " in data dicitonary. 'Value' could not be converted to float.")

                    try:
                        y_val[0] = float(y_val[0]*convy['factor'] + convy['offset'])
                        y_val[1] = float(y_val[1]*convy['factor'] + convy['offset'])
                        y_val = {'low':min([float(y_val[0]), float(y_val[1])]),
                                'high':max([float(y_val[0]), float(y_val[1])])}
                    except:
                        raise Exception("Invalid value for field 'Y' in " + att + " in data dicitonary. Range in 'Value' could not be converted to float.")
                    func_dict['ymin'] = y_val['low']
                    func_dict['ymax'] = y_val['high']

                # -- Add Numeric Parameters
                for p in num_param:
                    x_val = RecData[att][p]['Value'][i]
                    try:
                        x_val = float(x_val*convx_all[p]['factor'] + convx_all[p]['offset'])
                    except:
                        raise Exception("Invalid value for field '" + key + "' in " + att + " in data dicitonary. 'Value' could not be converted to float.")

                    func_dict[p] = x_val

                # -- Add discrete Parameters
                for p in disc_param:
                    func_dict[p] = RecData[att][p]['Value'][i]
                    
                # Add Point
                if 'y' in func_dict.keys():
                    func.add_point(func_dict)
                else:
                    func.add_range(func_dict)

        return func
    
    # Tabular Data
    def tabular_data(tabl, RecData, att):

        # Check RecData Structure
        if isinstance(RecData[att], dict) == False:
            raise Exception("Invalid data dictionary format. Field " + att + " in data dicitonary is not a dictionary. ")
        if 'Value' not in RecData[att].keys():
            raise Exception("Invalid data dictionary format. Field " + att + " in data dicitonary does not contain 'Value'. ")

        # Get Data in RecData
        if RecData[att]['Value'] is not None:
            # Check structure of Value
            if isinstance(RecData[att]['Value'], list) == False:
                raise Exception("Invalid data dictionary format. 'Value' in " + att + " must be a list of lists (one for each row). ")
            for row in RecData[att]['Value']:
                if isinstance(row, list) == False:
                    raise Exception("Invalid data dictionary format. 'Value' in " + att + " must be a list of lists (one for each row). ")
            
            # Check structure of columns
            if 'Columns' not in RecData[att].keys():
                raise Exception("Invalid data dictionary format. Field " + att + " in data dicitonary does not contain 'Columns'. ")
            if isinstance(RecData[att]['Columns'], list) == False:
                raise Exception("Invalid data dictionary format. 'Columns' in " + att + " must be a list of string values. ")
            for col in RecData[att]['Columns']:
                if isinstance(col, str) == False:
                    raise Exception("Invalid data dictionary format. 'Columns' in ' " + att + " must be a list of string values. ")
                
            # Check that they're equal in length
            if len(RecData[att]['Columns']) != len(RecData[att]['Value'][0]):
                raise Exception("Invalid data dictionary format. Length of 'Columns' each row in 'Value' in ' " + att + " are not the same. ")
            
            # Clear any previous data if status is Replace
            if status == 'Replace':
                while tabl.shape[1] > 0:
                    tabl.delete_row(0)

            # Add data
            for row in RecData[att]['Value']:
                new_row = []
                # -- Preallocate row with None
                for i in range(len(tabl.columns)):
                    new_row.append(None)

                for i in range(len(RecData[att]['Columns'])):
                    if RecData[att]['Columns'][i] in tabl.columns:
                        col_id = tabl.columns.index(RecData[att]['Columns'][i])
                        col_type = tabl.definition.column_types[col_id]
                        val = row[i]

                        if val is not None:
                            # Get data validation
                            if col_type == 'DISC':  
                                val = data_validation(val, col_type, opts = tabl.definition.discrete_values[i])
                            elif col_type in ['POIN', 'RNGE']:
                                # Get data dictionary unit
                                try:
                                    data_unit = RecData[att]['Units'][col_id]
                                except:
                                    raise Exception("'Units' field not available in data dicitonary for " + att + ".")
                                if isinstance(data_unit, str) == False:
                                    raise Exception("Invalid units in data dictionary for " + att + ". " + "Units value must be a string.")
                                val = data_validation(val, col_type, unit = tabl.definition.column_units[i], data_unit=data_unit)
                            
                            elif col_type == 'HLNK':
                                val = data_validation(val, col_type, hlink_flag= 1)

                            else:
                                val = data_validation(val, col_type)

                        new_row[col_id] = val

                    elif RecData[att]['Columns'][i] == 'Linking Value':
                        col_id = -1
                        col_type = 'STXT'
                        val = row[i]
                        val = data_validation(row[i], col_type)
                        new_row[col_id] = val

                 # Check if the row exists, write data if it doesn't
                if new_row not in tabl.value:
                    tabl.add_row()
                    for k in range(len(new_row)):
                        tabl.value[tabl.shape[1]-1][k] = new_row[k]

        return tabl

    # Preallocate List of Attributes to update
    AttList = []

    # Loop through all attributes
    for att in attributes:
        if att not in record.attributes:
            raise Exception("Attribute " + att + " not found in " + record.name + ". Check data dicitonary.")
        
        if isinstance(RecData[att], dict) == False:
            raise Exception("Invalid data dictionary format. Field " + att + " in data dicitonary is not a dictionary. ")

        # Write data to record
        if record.attributes[att].type == 'FUNC':
            func = record.attributes[att]
            func = functional_data(func, RecData, att, db)

        elif record.attributes[att].type == 'TABL':
            tabl = record.attributes[att]
            tabl = tabular_data(tabl, RecData, att)

        else:
            # Check that single value exists
            if "Value" not in RecData[att].keys():
                    raise Exception("Invalid data dictionary format. 'Value' not found in " + att + " in data dicitonary.")
            
            # Check for existing value
            if RecData[att]['Value'] != None or status == 'Replace':

                # Skip if status is 'Do Not Rpelace'
                if status == "Do Not Replace":
                    continue
            
                # Get Value
                val = RecData[att]['Value']

                # Get data validation
                if record.attributes[att].type == 'DISC':  
                    val = data_validation(val, record.attributes[att].type, opts = record.attributes[att].possible_discrete_values)

                elif record.attributes[att].type  in ['POIN', 'RNGE']:
                    # Get data dictionary unit
                    try:
                        data_unit = RecData[att]['Units']
                    except:
                        raise Exception("'Units' field not available in data dicitonary for " + att)
                    if isinstance(data_unit, str) == False:
                        raise Exception("Invalid units in data dictionary for " + att + ". Units value must be a string.")
                    val = data_validation(val, record.attributes[att].type , unit = record.attributes[att].unit, data_unit=data_unit)

                else:
                    val = data_validation(val, record.attributes[att].type)

                # Write value to record
                if record.attributes[att].type in ['FILE', 'PICT']:
                    record.attributes[att].object = val
                else:    
                    record.attributes[att].value = val

        # Check meta-attributes
        if 'Metadata' in RecData[att].keys():
            meta_atts = list(RecData[att]['Metadata'].keys())
            for meta_att in meta_atts:
                if meta_att not in record.attributes[att].meta_attributes:
                    raise Exception("Meta-Attribute " + meta_att + " not found in " + att + " in " + record.name + ". Check data dicitonary.")

                if isinstance(RecData[att]['Metadata'][meta_att], dict) == False:
                    raise Exception("Invalid data dictionary format. Field " + meta_att + " in " + att+ " in data dicitonary is not a dictionary. ")

                # Write data to record
                if record.attributes[att].meta_attributes[meta_att].type == 'FUNC':
                    func = record.attributes[att].meta_attributes[meta_att]
                    func = functional_data(func, RecData[att]['Metadata'], meta_att, db)

                elif record.attributes[att].meta_attributes[meta_att].type == 'TABL':
                    tabl = record.attributes[att].meta_attributes[meta_att]
                    tabl = tabular_data(tabl, RecData[att]['Metadata'], meta_att)

                else:
                    if "Value" not in RecData[att]['Metadata'][meta_att].keys():
                        raise Exception("Invalid data dictionary format. 'Value' not found in " + meta_att + " in " + att + " in data dicitonary.")

                    if RecData[att]['Metadata'][meta_att]['Value'] != None or status == 'Replace':

                        # Get Value
                        val = RecData[att]['Metadata'][meta_att]['Value']

                        # Get data validation
                        if record.attributes[att].meta_attributes[meta_att].type == 'DISC':  
                            val = data_validation(val, record.attributes[att].meta_attributes[meta_att].type, opts = record.attributes[att].meta_attributes[meta_att].possible_discrete_values)

                        elif record.attributes[att].meta_attributes[meta_att].type  in ['POIN', 'RNGE']:
                            # Get data dictionary unit
                            try:
                                data_unit = RecData[att]['Metadata'][meta_att]['Units']
                            except:
                                raise Exception("'Units' field not available in data dicitonary for " + att + ".")
                            if isinstance(data_unit, str) == False:
                                raise Exception("Invalid units in data dictionary for " + att + ". " + "Units value must be a string.")
                            val = data_validation(val, record.attributes[att].meta_attributes[meta_att].type , unit = record.attributes[att].meta_attributes[meta_att].unit, data_unit=data_unit)

                        else:
                            val = data_validation(val, record.attributes[att].meta_attributes[meta_att].type)

                        # Write value to record
                        if record.attributes[att].meta_attributes[meta_att].type in ['FILE', 'PICT']:
                            record.attributes[att].meta_attributes[meta_att].object = val
                        else:    
                            record.attributes[att].meta_attributes[meta_att].value = val

                # Add meta-attribute to update list
                AttList.append(record.attributes[att].meta_attributes[meta_att])

        # Add attribute to update list
        AttList.append(record.attributes[att])
       
    # Write Data
    if len(AttList) > 0:
        # Set the Attributes
        record.set_attributes(AttList)

        # Update the record
        record = mi.update([record])[0]

    return record