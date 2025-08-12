def WriteStaticLinks(mi, db, table, record, LinkData, attributes = None):
    #---------------------------------------------------------------------------
    #   PURPOSE: Write static links to a record
    #
    #   INPUTS:
    #   INPUTS:
    #       mi          SessionObject       Granta Server Connection
    #       db          DatabaseObject      Selected Granta Database
    #       record      RecordObject        Granta MI record to write data to
    #       LinkData    dict                Python Dictionary containing record 
    #                                       links to write
    #       attributes  list(str)           List of Single Value Attributes
    #
    #   OUTPUTS  
    #       record      RecordObject        Record with populated data
    #---------------------------------------------------------------------------

    # Import Modules
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

    if isinstance(LinkData, dict) == False:
        raise Exception("Invalid input for 'LinkData'. 'LinkData must be a dict.")
    
    if attributes is None:
        attributes = list(LinkData.keys())

    if isinstance(attributes, list) == False:
        raise Exception("Invalid input for 'attributes'. 'attributes must be a list of strings.")
    
    for att in attributes:
        if isinstance(att, str) == False:
            raise Exception("Invalid input for 'attributes'. 'attributes must be a list of string values.")
        
        if att not in LinkData.keys():
            raise Exception("Invalid input for 'attributes'. Value " + att + " not found in LinkData.")
        

    # Loop through all attributes
    for att in attributes:

        if att not in record.links:
            raise Exception("Record Link Group " + att + " not found in " + record.name + ". Check data dicitonary.")
        
        if isinstance(LinkData[att], dict) == False:
            raise Exception("Invalid data dictionary format. Field " + att + " in data dicitonary is not a dictionary. ")
        
        if 'Records' not in LinkData[att].keys():
            raise Exception("Invalid data dictionary format. 'Records must be in field " + att + " in data dicitonary. ")
        
        if isinstance(LinkData[att]['Records'], list) == False:
            try:
                LinkData[att]['Records'] = list(LinkData[att]['Records'])
            except:
                raise Exception("Invalid data dictionary format. 'Records must be a list of strings in field " + att + " in data dicitonary. ")

        for i in range(len(LinkData[att]['Records'])):
            # Check input
            if isinstance(LinkData[att]['Records'][i], str) == False:
                raise Exception("Invalid data dictionary format. 'Records must be a list of strings in field " + att + " in data dicitonary. ")

            # Get the database
            try:
                db_key = LinkData[att]['Database'][i]
                db_link = mi.get_db(db_key = db_key)
            except:
                db_link = db

            # Get the table
            try:
                table_name = LinkData[att]['Table'][i]
                table_link = db_link.get_table(table_name)
            except:
                table_link = table

            # Search for the record
            linkrec = table_link.search_for_records_by_name(LinkData[att]['Records'][i])
            if len(linkrec) == 0:
                raise Exception(LinkData[att]['Records'][i] + ' not found in ' + table_link.name + ' in.')
            for rec in linkrec:
                new_linked_recs = record.links[att]
                new_linked_recs.add(rec)
                record.set_links(att, new_linked_recs)

    # Update record
    record = mi.update_links([record])[0]

    return record