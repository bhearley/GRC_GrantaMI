def GetFileObject(file):
    #---------------------------------------------------------------------------
    #   PURPOSE: Get a file object importable to Granta MI.
    #
    #   INPUTS:
    #       file            filepath
    #   OUTPUTS  
    #       file_object     Record with populated data
    #---------------------------------------------------------------------------

    # Import Modules
    import os
    try:
        from GRANTA_MIScriptingToolkit import granta as mpy
    except:
        raise Exception("ERROR 0000: Unable to import Granta Scripting Toolkit.")

    # Create the file object
    file_object  = mpy.File()

    # Open the file
    try:
        with open(file, 'rb') as file_buffer:
            file_object.binary_data = file_buffer.read()
    except:
        if isinstance(file, str):
            raise Exception("ERROR 0007: Unable to read " + file + " as binary.")
        else:
            raise Exception("ERROR 0008: Invalid value for 'file'.")

    # Set the file name
    file_object.file_name = os.path.basename(file)

    return file_object