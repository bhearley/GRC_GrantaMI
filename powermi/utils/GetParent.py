def GetParent(mi, db, table, tree):
    #---------------------------------------------------------------------------
    #   PURPOSE: Returns the GUID for every folder/generic record and the 
    #            final parent record for a desired tree path
    #   INPUTS:
    #       mi      SessionObject       Granta Server Connection
    #       db      DatabaseObject      Selected Granta Database
    #       table   TableObject         Selected Granta Table
    #       tree    list(string)        List of folder nmames
    #
    #   OUTPUTS
    #       parent  RecordObject        Parent record
    #       GUIDS   list(string)        List of GUIDS for each item in tree
    #       flag    integer             Indicator if finding a parent was successful
    #                                       0 - Yes
    #                                       1 - No
    #       msg     string              Error message
    #---------------------------------------------------------------------------

    # Import Modules
    import easygui
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
    
    if isinstance(tree, list) == False:
        raise Exception("Invalid input for 'tree'. 'tree' must be a list of string values.")
    for t in tree:
        if isinstance(t, str) == False:
            raise Exception("Invalid input for 'tree'. 'tree' must be a list of string values.")

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

            # Create the current tree
            curr_tree = ''
            for j in range(0,i+1):
                curr_tree = curr_tree + tree[j] + ' > '
            curr_tree = curr_tree[:len(curr_tree)-3]

            # Ask if user wants to create the folder
            ans1 = easygui.ynbox(msg='The folder ' + curr_tree + ' is not currently in table ' + table.name +  '. Do you want to create it?', title='Folder Not Found')
            if ans1 == True:
                new_record = table.create_record(name=tree[i], parent = folder, folder=True)
                new_record.type = mpy.RecordType.Folder
                recs = mi.update([new_record])
                try:
                    folder = mi.update([folder])[0]
                except:
                    pass
                guid = recs[0].record_guid
            else:
                flag = 1
                msg = 'Folder ' + curr_tree + ' not created.'
                break
        else:
            guid = folder.children[children.index(tree[i])].record_guid

        # If user does not want to create the folder, quit the process
        if flag == 1:
            break

        # Add GUIDS to list
        GUIDS.append(guid)

        # Get new parent
        folder = db.get_record_by_id(vguid=guid)

    return folder, GUIDS, flag, msg

