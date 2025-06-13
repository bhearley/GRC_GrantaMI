def GetRecord(mi, db, table, name, short_name, parent):
    #   PURPOSE: Get the new record by either creating one if it doesn't exist or fetching one 
    #            that does exist
    #   INPUTS:
    #       mi          Granta Server Connection
    #       db          Selected Granta Database
    #       table       Selected Granta Table
    #       name        Name of the new record
    #       short_name  Shorrt name of the new record
    #       parent      Parent record
    #
    #   OUTPUTS  
    #       record  Record to write data to


    # Get the Record
    try:
        # Create a new record if it doesn't exist 
        new_record = table.create_record(name= name, parent = parent)
        recs = mi.update([new_record])
        guid = recs[0].record_guid
        folder = mi.update([folder])[0]
    except:
        # Find the record in the children if it does exist
        children = []
        for j in range(len(parent.children)):
            children.append(parent.children[j].name)
        guid = parent.children[children.index(name)].record_guid

    record = db.get_record_by_id(vguid=guid)
    if short_name is not None:
        record.short_name = short_name

    return record