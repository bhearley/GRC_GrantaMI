def GetRecord(mi, db, table, name, parent = None, short_name = None):
    #---------------------------------------------------------------------------
    #   PURPOSE: Get the new record by either creating one if it doesn't exist 
    #           or fetching one that does exist
    #
    #   INPUTS:
    #       mi          SessionObject       Granta Server Connection
    #       db          DatabaseObject      Selected Granta Database
    #       table       TableObject         Selected Granta Table
    #       name        string              Name of the new record
    #       parent      RecordObject        Parent record
    #       short_name  string              Short name of the new record 
    #                                       (optional)
    #   OUTPUTS  
    #       record      RecordObject        Record to write data to
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
    
    if isinstance(table, mpy.mi_tree_classes.Table) == False:
        raise Exception("Invalid input for 'table'. 'table must be a Granta MI Table object.")
    
    if isinstance(name, str) == False:
        raise Exception("Invalid input for 'name', 'name' must be a string.")
    
    if parent is None:
        parent = table
    else:
        if isinstance(parent, mpy.mi_record_classes.Record) == False and isinstance(parent, mpy.mi_tree_classes.Table) == False:
            raise Exception("Invalid input for 'parent', 'parent' must be a Granta MI Table,Folder, Record, or Generic Record object.")
    if short_name is None:
        short_name = name
    if isinstance(short_name, str) == False:
        raise Exception("Invalid input for 'short_name'. 'short_name' must be a string.")
    
    # Search for the record
    rec_list = table.search_for_records_by_name(name)

    # Initialize GUID
    guid = None

    # Search through found records
    for rec in rec_list:
        if isinstance(parent, mpy.mi_record_classes.Record) == True:
            if rec.parent.record_guid == parent.record_guid:
                guid = rec.record_guid
        else:
            guid = rec.record_guid

    if guid is None:
        # Create a new record if it doesn't exist 
        new_record = table.create_record(name= name, parent = parent)
        recs = mi.update([new_record])
        guid = recs[0].record_guid
        if isinstance(parent, mpy.mi_record_classes.Record) == True:
            parent = mi.update([parent])[0]

    # Get record from GUID
    record = db.get_record_by_id(vguid=guid)

    # Set short name
    if short_name is not None:
        record.short_name = short_name

    return record