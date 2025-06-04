def WriteStaticLinks(mi, db, record, RecData, RL, status):
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

        # Loop through all attributes
        for att in RL:

            try:
                # Check if tablular attribute has data
                if len(RecData[att]['Values']) > 0:

                    # Skip if status is do not replace
                    if status == 'Do Not Replace':
                        continue

                    # Remove all previous data if status is replace
                    if status == 'Replace':
                        record.links[att].clear()

                    # Add new data
                    for i in range(len(RecData[att]['Values'])):

                        # Get the record link
                        table = db.get_table(RecData[att]['Table'])
                        linkrec = table.search_for_records_by_name(RecData[att]['Values'][i])[0]
                        new_linked_recs = record.links[att]
                        new_linked_recs.add(linkrec)
                        record.set_links(att, new_linked_recs)
                    

            except:
                pass

        # Update record
        record = mi.update_links([record])[0]

        return record