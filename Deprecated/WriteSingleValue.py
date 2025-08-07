def WriteSingleValue(mi, db, record, RecData, SV = None):
    #---------------------------------------------------------------------------
    #   PURPOSE: Write single value attribute data to a record
    #
    #   INPUTS:
    #       mi      Granta Server Connection
    #       db      Selected Granta Database
    #       table   Selected Granta Table
    #       record  Granta MI record to write data to
    #       RecData Python Dictionary containing record data to write
    #       SV      List of Single Value Attributes
    #   OUTPUTS  
    #       record  Record with populated data
    #---------------------------------------------------------------------------

    # Import Modules
    from datetime import datetime
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
    
    if SV is None:
        SV = list(RecData.keys())
    if isinstance(SV, list) == False:
        raise Exception("ERROR 0018: Invalid input for 'SV' - input must be a list of strings.")
    for S in SV:
        if isinstance(S, str) == False:
            raise Exception("ERROR 0018: Invalid input for 'SV' - input must be a list of string values.")
        if S not in RecData.keys():
            raise Exception("ERROR 0018: Invalid input for 'SV' - Value " + S + " not found in RecData.")
    

    # Data Validation Function
    def data_validation(val, dtype):
        # Short Text
        if dtype == 'STXT':
            if isinstance(val, str) == False:
                try:
                    val = str(val)
                except:
                    raise Exception("ERROR 0023: Invalid value in data dictionary for " + att + ". Unable to convert to string for STXT.")
            if len(val) > 255:
                raise Exception("ERROR 0024: Invalid value in data dictionary for " + att + ". Too many characters for STXT (Max 255).")
            return val

        # Long Text
        if dtype == 'LTXT':
            if isinstance(val, str) == False:
                try:
                    val = str(val)
                except:
                    raise Exception("ERROR 0025: Invalid value in data dictionary for " + att + ". Unable to convert to string for LTXT.")
            if len(val) > 1e6:
                raise Exception("ERROR 0026: Invalid value in data dictionary for " + att + ". Too many characters for LTXT (Max 1,000,000).")
            return val

        # Discrete
        if dtype == 'DISC':
            if val not in record.attributes[att].possible_discrete_values:
                raise Exception("ERROR 0027: Invalid value in data dictionary for " + att + ". Value is not in the available discrete options.")
            return val

        # Point
        if dtype == 'POIN':
            if isinstance(val, float) == False:
                try:
                    val = float(val)
                except:
                    raise Exception("ERROR 0028: Invalid value in data dictionary for " + att + ". " + "Unable to convert value to point.")
                
            # Get Default Unit
            unit = record.attributes[att].unit
            if unit != '':
                # Get data dictionary unit
                try:
                    data_unit = RecData[att]['Units']
                except:
                    raise Exception("ERROR 0029: 'Units' field not available in data dicitonary for " + att + ".")
                if isinstance(data_unit, str) == False:
                    raise Exception("ERROR 0030: Invalid units in data dictionary for " + att + ". " + "Units value must be a string.")
                
                if unit == data_unit:
                    return val

                else:
                    conv_dict = db.dimensionally_equivalent_units(data_unit)
                    if unit not in conv_dict.keys():
                        raise Exception("ERROR 0031: Unable to convert " + data_unit + " in data dictionary to " + unit + " in Granta MI for " + att + ".")
                    val = val*conv_dict[unit]['factor'] + conv_dict[unit]['offset']
                    return val

            else:
                return val

        # Range
        if dtype == 'RNGE':
            if isinstance(val, list) == False:
                try:
                    val = float(val)
                except:
                    raise Exception("ERROR 0032: Invalid value in data dictionary for " + att + ". " + "Value must be a list containing two point values.")
            if len(val) != 2:
                raise Exception("ERROR 0032: Invalid value in data dictionary for " + att + ". " + "Value must be a list containing two point values.")
            for v in val:
                try:
                    float(v)
                except:
                    raise Exception("ERROR 0032: Invalid value in data dictionary for " + att + ". " + "Value must be a list containing two point values.")
                
            # Get Default Unit
            unit = record.attributes[att].unit
            if unit != '':
                # Get data dictionary unit
                try:
                    data_unit = RecData[att]['Units']
                except:
                    raise Exception("ERROR 0029: 'Units' field not available in data dicitonary for " + att + ".")
                if isinstance(data_unit, str) == False:
                    raise Exception("ERROR 0030: Invalid units in data dictionary for " + att + ". " + "Units value must be a string.")
                
                if unit == data_unit:
                    val = {'low':min(val), 'high':max(val)}
                    return val

                else:
                    conv_dict = db.dimensionally_equivalent_units(data_unit)
                    if unit not in conv_dict.keys():
                        raise Exception("ERROR 0031: Unable to convert " + data_unit + " in data dictionary to " + unit + " in Granta MI for " + att + ".")
                    val[0] = val[0]*conv_dict[unit]['factor'] + conv_dict[unit]['offset']
                    val[1] = val[1]*conv_dict[unit]['factor'] + conv_dict[unit]['offset']
                    val = {'low':min(val), 'high':max(val)}
                    return val

            else:
                val = {'low':min(val), 'high':max(val)}
                return val

        # Integer
        if dtype == 'INPT':
            if isinstance(val, int) == False:
                try:
                    val = int(val)
                except:
                    raise Exception("ERROR 0033: Invalid value in data dictionary for " + att + ". " + "Unable to convert value to integer.")
                
            return val

        # Logic
        if record.attributes[att].type == 'LOGI':
            if val not in ['Yes', 'No', True, False]:
                raise Exception("ERROR 0034: Invalid value in data dictionary for " + att + ". " + "Logical value must be 'Yes', 'No', True, or False.")
            if val == 'Yes':
                val = True
            elif val == 'No':
                val = False
            return val

        # Date
        if record.attributes[att].type == 'DTTM':
            try:
                val = datetime.strptime(val, "%m/%d/%Y")
                return val
            except:
                raise Exception("ERROR 0035: Invalid value in data dictionary for " + att + ". " + "Unable to convert value to date.")
            
        # File
        if record.attributes[att].type == 'FILE':
            if isinstance(val, mpy.mi_attribute_value_classes.File) == False:
                raise Exception("ERROR 0036: Invalid value in data dictionary for " + att + ". " + "Use GetFileObject to get a Granta MI File Object.")
            return val
        
        # Image
        if record.attributes[att].type == 'PICT':
            if isinstance(val, mpy.mi_attribute_value_classes.File) == False:
                raise Exception("ERROR 0036: Invalid value in data dictionary for " + att + ". " + "Use GetFileObject to get a Granta MI File Object.")
            if val.value.file_name.split('.')[-1] not in ['png', 'jpg', 'bmp', 'tif']:
                raise Exception("ERROR 0037: Invalid value in data dictionary for " + att + ". " + "Granta MI File Object must be an image for a PICT attribute.")
            
            return val
        
        # Hyperlink
        if record.attributes[att].type == 'HLNK':
            if isinstance(val, mpy.mi_attribute_value_classes.Hyperlink) == False:
                raise Exception("ERROR 0036: Invalid value in data dictionary for " + att + ". " + "Use GetHyperLink to get a Granta MI Hyperlink Object.")
            return val


    # Preallocate List of Attributes to update
    AttList = []

    # Loop through all single value attibutes
    for att in SV:
        if att not in record.attributes:
            raise Exception("ERROR 0020: Attribute " + att + " not found in " + record.name + ". Check data dicitonary.")
        
        if isinstance(RecData[att], dict) == False:
            raise Exception("ERROR 0021: Invalid data dictionary format. Field " + att + " in data dicitonary is not a dictionary. ")

        if "Value" not in RecData[att].keys():
            raise Exception("ERROR 0022: Invalid data dictionary format. 'Value' not found in " + att + " in data dicitonary.")

        # Perform Data Validation
        if RecData[att]['Value'] != None:

            # Get Value
            val = RecData[att]['Value']

            # Get data validation
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

            # Add attribute to update list
            AttList.append(record.attributes[att])
       
    # Write Data
    if len(AttList) > 0:
        # Set the Attributes
        record.set_attributes(AttList)

        # Update the record
        record = mi.update([record])[0]

    return record