def GetFileObject(file, desc = None):
    #---------------------------------------------------------------------------
    #   PURPOSE: Get a file object importable to Granta MI.
    #
    #   INPUTS:
    #       file            string          file path of file to upload
    #       desc            string          description of the file (optional)
    #
    #   OUTPUTS  
    #       file_object     FileObject      File object importable to a FILE or 
    #                                       PICT attribute
    #---------------------------------------------------------------------------

    # Import Modules
    import os
    try:
        from GRANTA_MIScriptingToolkit import granta as mpy
    except:
        raise Exception("Unable to import Granta Scripting Toolkit.")

    # Create the file object
    file_object  = mpy.File()

    # Open the file
    try:
        with open(file, 'rb') as file_buffer:
            file_object.binary_data = file_buffer.read()
    except:
        if isinstance(file, str):
            raise Exception("Unable to read " + file + " as binary.")
        else:
            raise Exception("Invalid value for 'file'. 'file' must be a string.")

    # Set the file name
    file_object.file_name = os.path.basename(file)
    if desc is not None:
        if isinstance(desc, str) == False:
            raise Exception("Invalid value for 'desc'. 'desc' must be a string.")
        file_object.description = desc

    return file_object