def GetParent(mi, db, table, tree):
    #   PURPOSE: GetParent.py returns the GUID for every folder/generic record and the 
    #            final parent record for a desired tree path
    #   INPUTS:
    #       mi      Granta Server Connection
    #       db      Selected Granta Database
    #       table   Selected Granta Table
    #       tree    List of folder nmames
    #
    #   OUTPUTS
    #       parent  Parent record
    #       GUIDS   List of GUIDS for each item in tree
    #       flag    Indicator if finding a parent was successful
    #                   0 - Yes
    #                   1 - No
    #       msg     Error message

    # Import Modules
    import easygui

    # Initialize folder, GUIDS, flag, and msg
    folder = table
    GUIDS = []
    flag = 0
    msg = ''

    # Loop through folders in the tree
    for i in range(len(tree)):   
        # Get List of Children
        children = []
        for j in range(len(folder.children)):
            children.append(folder.children[j].name) 

        # Check if folder exists
        if tree[i] not in children:
            # Ask if user want to create
            ans1 = easygui.ynbox(msg='The Folder ' + tree[i] + ' is not currently in the database. Do you want to create it?', title='Folder Not Found')
            if ans1 == True:
                new_record = table.create_record(name=tree[i], parent = folder, folder=True)
                new_record.type = "Folder"
                recs = mi.update([new_record])
                folder = mi.update([folder])[0]
                guid = recs[0].record_guid
            else:
                flag = 1
                msg = 'Folder ' + tree[i] + ' not created. Skipping to next import file.'
                break
        else:
            guid = folder.children[children.index(tree[i])].record_guid

        if flag == 1:
            break

        GUIDS.append(guid)
        folder = db.get_record_by_id(vguid=guid)

    return folder, GUIDS, flag, msg