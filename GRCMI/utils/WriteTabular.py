def WriteTabular(mi, record, RecData, TB, status):
    #   PURPOSE: Write tabualr attribute data to a record
    #
    #   INPUTS:
    #       mi      Granta Server Connection
    #       db      Selected Granta Database
    #       table   Selected Granta Table
    #       record  Granta MI record to write data to
    #       RecData Python Dictionary containing record data to write
    #       TB      List of Functional Attributes
    #       status  conflict stats
    #   OUTPUTS  
    #       record  Record with populated data

    # Preallocate List of Attributes to update
    AttList = []

    # Loop through all attributes
    for att in TB:

        try:
            # Check if tablular attribute has data
            if len(RecData[att]['Values']) > 0:

                # Skip if status is do not replace
                if status == 'Do Not Replace':
                    continue

                # Get the tabular data
                tab = record.attributes[att]

                # Remove all previous data if status is replace
                if status == 'Replace':
                    while tab.shape[1] > 0:
                        tab.delete_row(0)

                # Get Linked Columns
                row_loc = []
                for i in range(len(tab.linked_columns)):
                    if tab.linked_columns[i] == False:
                        row_loc.append(tab.columns[i])

                # Add new data
                for i in range(len(RecData[att]['Values'])):
                    # Get Local Data Columns Only
                    col = RecData[att]['Columns'] 
                    row = RecData[att]['Values'][i]

                    # Get all existing data
                    tab_exist = []
                    for j in range(tab.shape[1]):
                        tab_row = []
                        for k in range(len(col)):
                            col_name = col[k]
                            col_idx = tab.columns.index(col_name)
                            tab_row.append(tab.value[j][col_idx])
                        tab_exist.append(tab_row)

                    # Check if the row exists, write data if it doesn't
                    if row not in tab_exist:
                        tab.add_row()
                        for k in range(len(tab.columns)):
                            if tab.columns[k] in col:
                                tab.value[tab.shape[1]-1][k] = row[col.index(tab.columns[k])]
                                try:
                                    tab.units[k] = RecData[att]['Units'][k]
                                except:
                                    pass

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