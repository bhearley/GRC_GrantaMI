def WriteFunctional(mi, record, RecData, FN, status):
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

    # Preallocate List of Attributes to update
    AttList = []

    # Loop through all attributes
    for att in FN:

        # Check if both X and Y data exists
        try:
            if RecData[att]['X Values'] != None and RecData[att]['Y Values'] != None:  

                # Skip if conflict status is Do Not Repalce
                if status == 'Do Not Repalce':
                    continue

                # Get functional data       
                func = record.attributes[att]

                # Clear any previous data if status is Replace
                if status == 'Replace':
                    func.clear()

                # Add Data Points
                for i in range(min([len(RecData[att]['X Values']), len(RecData[att]['Y Values'])])):
                    func.add_point({'y': float(RecData[att]['Y Values'][i]),
                                    list(func.xaxis.keys())[0]: float(RecData[att]['X Values'][i])
                                    })
                # Update units
                func.parameters[list(func.xaxis.keys())[0]].unit = RecData[att]['Units'][0]
                func.unit = RecData[att]['Units'][1]
                func.update_header_units()

                # Add attribute to list of attributes to update
                AttList.append(func)

        except:
            pass

    # Write Data
    if len(AttList) > 0:
        # Set the Attributes
        record.set_attributes(AttList)

        # Update the record
        record = mi.update([record])[0]

    return record