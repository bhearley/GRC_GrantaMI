def GetFileObject(file):
    # #   PURPOSE: Get the file object importable to Granta MI
    #
    #   INPUTS:
    #       file            filepath
    #   OUTPUTS  
    #       file_object     Record with populated data

    # Import Modules
    from GRANTA_MIScriptingToolkit import granta as mpy
    import os

    # Create the file object
    file_object  = mpy.File()

    # Open the file
    with open(file, 'rb') as file_buffer:
        file_object.binary_data = file_buffer.read()

    # Set the file name
    file_object.file_name = os.path.basename(file)

    return file_object