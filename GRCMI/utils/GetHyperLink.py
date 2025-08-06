def GetHyperLink(link, disp = None, desc = None):
    #---------------------------------------------------------------------------
    #   PURPOSE: Get a hyperlink object importable to Granta MI.
    #
    #   INPUTS:
    #       link            hyperlink string
    #       disp            display option for when the link is pressed
    #       desc            description of the link
    #   OUTPUTS  
    #       file_object     hyperlink object importable to an HLNK attribute
    #---------------------------------------------------------------------------

    # Import Modules
    import os
    try:
        from GRANTA_MIScriptingToolkit import granta as mpy
    except:
        raise Exception("ERROR 0000: Unable to import Granta Scripting Toolkit.")
    
    # Check Inputs
    if isinstance(link, str) == False:
        Exception("ERROR 0007: " + link + " is not a string.")

    if disp is None:
        disp = 'New'
    if isinstance(disp, str) == False:
        Exception("ERROR 0007: " + disp + " is not a string.")
    if disp not in ['New', 'Top', 'Content']:
        Exception("ERROR 0007: Invalid value for 'disp. Value must be 'New', 'Top', or 'Content'.")
    if desc is None:
        desc = link
    if isinstance(desc, str) == False:
        Exception("ERROR 0007: " + disp + " is not a string.")

    # Create the file object
    hlink_object = mpy.Hyperlink(url=link, hyperlink_display=disp, hyperlink_description=desc)

    return hlink_object