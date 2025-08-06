def GetRecord(mi, db, table, name, parent, short_name = None):
    #---------------------------------------------------------------------------
    #   PURPOSE: Get the new record by either creating one if it doesn't exist or fetching one 
    #            that does exist
    #   INPUTS:
    #       mi          Granta Server Connection
    #       db          Selected Granta Database
    #       table       Selected Granta Table
    #       name        Name of the new record
    #       short_name  Short name of the new record
    #       parent      Parent record
    #
    #   OUTPUTS  
    #       record  Record to write data to
    #---------------------------------------------------------------------------

    # Import Modules
    try:
        from GRANTA_MIScriptingToolkit import granta as mpy
    except:
        raise Exception("ERROR 0000: Unable to import Granta Scripting Toolkit.")
    
    # Check inputs
    if isinstance(mi, mpy.mi.Session) == False:
        raise Exception("ERROR 0009: Invalid input for 'mi' - input must be a Granta MI Session object.")
    
    if isinstance(db, mpy.mi_tree_classes.Database) == False:
        raise Exception("ERROR 0010: Invalid input for 'db' - input must be a Granta MI Database object.")
    
    if isinstance(table, mpy.mi_tree_classes.Table) == False:
        raise Exception("ERROR 0011: Invalid input for 'table' - input must be a Granta MI Table object.")
    
    if isinstance(name, str) == False:
        raise Exception("ERROR 0013: Invalid input for 'name' - input must be a string.")
    
    if isinstance(parent, mpy.mi_record_classes.Record) == False:
        raise Exception("ERROR 0014: Invalid input for 'parent' - input must be a Granta MI Folder, Record, or Generic Record object.")
    if short_name is None:
        short_name = name
    if isinstance(short_name, str) == False:
        raise Exception("ERROR 0015: Invalid input for 'short_name' - input must be a string.")
    
    # Search for the record
    rec_list = table.search_for_records_by_name(name)

    # Initialize GUID
    guid = None

    # Search through found records
    for rec in rec_list:
            if rec.parent.record_guid == parent.record_guid:
                guid = rec.record_guid

    if guid is None:
        # Create a new record if it doesn't exist 
        new_record = table.create_record(name= name, parent = parent)
        recs = mi.update([new_record])
        guid = recs[0].record_guid
        parent = mi.update([parent])[0]

    # Get record from GUID
    record = db.get_record_by_id(vguid=guid)

    # Set short name
    if short_name is not None:
        record.short_name = short_name

    return record