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

# from GRCMI import Connect, GetParent, GetRecord

# server_name = "https://granta.ndc.nasa.gov"
# db_key = "NasaGRC_MD_45_09-2-05"
# table_name = "GRCMI Demo"
# mi, db, table = Connect(server_name, db_key, table_name)

# folder, GUIDS, flag, msg = GetParent(mi, db, table, ['Demo', 'Metals', 'Aluminum Alloys'])
# record  = GetRecord(mi, db, table, 'Aluminum 6061', folder)
# Data = {'Modulus vs Temperature':{  'X':{'Value':[-194,
#                                         -64.5,
#                                         16.9,
#                                         76.6,
#                                         131,
#                                         169,
#                                         206,
#                                         242,
#                                         274,
#                                         312,
#                                         -194,
#                                         -64.5,
#                                         16.9,
#                                         76.6,
#                                         131,
#                                         169,
#                                         206,
#                                         242,
#                                         274,
#                                         312,
#                                         ],
#                                         'Units':'°C'},
#                                     'Y':{'Value':[
#                                         78550000000,
#                                         72700000000,
#                                         70250000000,
#                                         69200000000,
#                                         67900000000,
#                                         66150000000,
#                                         63050000000,
#                                         59100000000,
#                                         54950000000,
#                                         49350000000,
#                                         [7.66E+10,	8.05E+10],
#                                         [7.09E+10,	7.45E+10],
#                                         [6.85E+10,	7.20E+10],
#                                         [6.75E+10,	7.09E+10],
#                                         [6.62E+10,	6.96E+10],
#                                         [6.45E+10,	6.78E+10],
#                                         [6.15E+10,	6.46E+10],
#                                         [5.76E+10,	6.06E+10],
#                                         [5.36E+10,	5.63E+10],
#                                         [4.81E+10,	5.06E+10],
#                                         ],
#                                         'Units':'Pa'},
#                                     'Series Number':{'Value':
#                                                      [1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2]}
#                                         }
#         }
# record = WriteFunctional(mi, db, record, Data, list(Data.keys()), 'Replace')