def WriteTabular(mi, db, table, record, RecData, TB):
    #   PURPOSE: Write tabualr attribute data to a record
    #
    #   INPUTS:
    #       mi      Granta Server Connection
    #       db      Selected Granta Database
    #       table   Selected Granta Table
    #       record  Granta MI record to write data to
    #       RecData Python Dictionary containing record data to write
    #       TB      List of Functional Attributes
    #   OUTPUTS  
    #       record  Record with populated data

    # Preallocate List of Attributes to update
    AttList = []

    # Loop through all attributes
    for att in TB:

        try:
            # Check if tablular attribute has data
            if len(RecData[att]['Values']) > 0:
                tab = record.attributes[att]

                # Remove all previous data
                if RecData[att]['Conflict'] == 'Replace':
                    while tab.shape[1] > 0:
                        tab.delete_row(0)

                # Add new data
                for i in range(len(RecData[att]['Values'])):
                    # Check if row exists
                    flag = 0
                    if RecData[att]['Conflict'] == 'Append':
                        row = RecData[att]['Values'][i]
                        for kk in range(tab.shape[1]):
                            row_chk = []
                            for ii in range(len(row)):
                                row_chk.append(1)
                            for jj in range(len(row)):
                                if tab.value[kk][jj] == row[jj]:
                                    row_chk[jj] = 0
                            if sum(row_chk) == 0:
                                flag = 1

                    # Write new row of data
                    if flag == 0:
                        tab.add_row()
                        for j in range(len(RecData[att]['Values'][i])):
                            col_idx = tab.columns.index(RecData[att]['Columns'][j])                 
                            tab.value[i][col_idx] = RecData[att]['Values'][i][j]
                            if RecData[att]['Units'][j] != None:
                                tab.units.data[i][col_idx] = RecData[att]['Units'][j]

                # Add attribute to list of attributes to update
                AttList.append(tab)
        except:
            pass

    # Write Data
    if len(AttList) > 0:
        # Set the Attributes
        record.set_attributes(AttList)

        # Update the record
        record = mi.update([record])[0]

    return record