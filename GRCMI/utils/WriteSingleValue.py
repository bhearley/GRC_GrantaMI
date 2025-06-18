def WriteSingleValue(mi, record, RecData, SV, status):
    #   PURPOSE: Write single value attribute data to a record
    #
    #   INPUTS:
    #       mi      Granta Server Connection
    #       db      Selected Granta Database
    #       table   Selected Granta Table
    #       record  Granta MI record to write data to
    #       RecData Python Dictionary containing record data to write
    #       SV      List of Single Value Attributes
    #       status  conflict status
    #   OUTPUTS  
    #       record  Record with populated data

    from datetime import datetime

    # Preallocate List of Attributes to update
    AttList = []

    # Loop through all single value attibutes
    for att in SV:
        try:
            if RecData[att]['Value'] != None:

                # Check for existing value
                if record.attributes[att].value is not None and status == "Do Not Replace":
                    continue
                
                # Check for Logic
                if record.attributes[att].type == 'LOGI':
                    if RecData[att]['Value'] == 'Yes':
                        RecData[att]['Value'] = True
                    else:
                        RecData[att]['Value'] = False

                # Check for Date
                if record.attributes[att].type == 'DTTM':
                    RecData[att]['Value'] = datetime.strptime(RecData[att]['Value'], "%m/%d/%Y")

                # Write Value
                record.attributes[att].value = RecData[att]['Value']

                # Write Units
                if RecData[att]['Units'] != None:
                    record.attributes[att].unit = RecData[att]['Units']
                
                # Write Metadata
                if len(list(RecData[att]['Metadata'].keys())) != 0:
                    meta_atts = list(RecData[att]['Metadata'].keys())

                    # Loop through all meta attributes for the attribute
                    for meta_att in meta_atts:
                        if RecData[att]['Metadata'][meta_att]['Value'] != None:
                            # Write Metadata Value
                            record.attributes[att].meta_attributes[meta_att].value = RecData[att]['Metadata'][meta_att]['Value']

                            # Write Units
                            if RecData[att]['Metadata'][meta_att]['Units'] != None:
                                record.attributes[att].meta_attributes[meta_att].unit = RecData[att]['Metadata'][meta_att]['Value']

                            # Add meta attribute to list of attributes to update
                            AttList.append(record.attributes[att].meta_attributes[meta_att])

                # Add attribute to list of attributes to update
                AttList.append(record.attributes[att])

            # Check for range values
            # -- Range attributes will not have "Value" populated, but will have a 'Maximum' and/or 'Minimum' meta attribute(s) populated
            if record.attributes[att].type == 'RNGE':
                # Get list of meta attributes
                meta_atts = list(RecData[att]['Metadata'].keys())

                # Preallocate min/max values and units
                min_val = None
                min_units = None
                min_name = None
                max_val = None
                max_units = None
                max_name = None

                # Loop through all meta attributes
                for meta_att in meta_atts:

                    # Check for minimum value
                    if "Minimum" in meta_att:
                        min_val = RecData[att]['Metadata'][meta_att]['Value']
                        if RecData[att]['Metadata'][meta_att]['Units'] != None:
                            min_units = RecData[att]['Metadata'][meta_att]['Units']
                        min_name = meta_att

                    # Check for maximum Value
                    if "Maximum" in meta_att:
                        max_val = RecData[att]['Metadata'][meta_att]['Value']
                        if RecData[att]['Metadata'][meta_att]['Units'] != None:
                            max_units = RecData[att]['Metadata'][meta_att]['Units']
                        max_name = meta_att

                # Check if either a max or min exists
                if min_val != None and max_val != None:

                    # Set Range Units
                    if min_name != None:
                        meta_atts.remove(min_name)
                        units = min_units
                    if max_name != None:
                        meta_atts.remove(max_name)
                        units = max_units

                    # Write Range Value
                    record.attributes[att].value =  (min_val, max_val)
                    if units != None:
                        record.attributes[att].unit = units

                    # Add attribute to list of attributes to update
                    AttList.append(record.attributes[att])

                    # Loop through all meta attributes for the attribute
                    for meta_att in meta_atts:
                        if RecData[att]['Metadata'][meta_att]['Value'] != None:

                            # Write Metadata Value
                            record.attributes[att].meta_attributes[meta_att].value = RecData[att]['Metadata'][meta_att]['Value']

                            # Write Units
                            if RecData[att]['Metadata'][meta_att]['Units'] != None:
                                record.attributes[att].meta_attributes[meta_att].unit = RecData[att]['Metadata'][meta_att]['Units']

                            # Add meta attribute to list of attributes to update
                            AttList.append(record.attributes[att].meta_attributes[meta_att])

        except:
            pass

    # Write Data
    if len(AttList) > 0:
        # Set the Attributes
        record.set_attributes(AttList)

        # Update the record
        record = mi.update([record])[0]

    return record