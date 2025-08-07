def GetHyperLink(link, disp = None, desc = None):
    #---------------------------------------------------------------------------
    #   PURPOSE: Get a hyperlink object importable to Granta MI.
    #
    #   INPUTS:
    #       link            string              hyperlink string
    #       disp            sting               display option for when the link is pressed
    #       desc            string              description of the link
    #
    #   OUTPUTS  
    #       hlnk_object     HyperLinkObject     hyperlink object importable to 
    #                                           an HLNK attribute
    #---------------------------------------------------------------------------

    # Import Modules
    try:
        from GRANTA_MIScriptingToolkit import granta as mpy
    except:
        raise Exception("Unable to import Granta Scripting Toolkit.")
    
    # Check Inputs
    if isinstance(link, str) == False:
        raise Exception("Invalid value for 'link'. 'link' must be a string.")

    if disp is None:
        disp = 'New'
    if isinstance(disp, str) == False:
        raise Exception("Invalid value for 'disp'. 'disp' must be 'New', 'Top', or 'Content'.")
    if disp not in ['New', 'Top', 'Content']:
        raise Exception("Invalid value for 'disp'. 'disp' must be 'New', 'Top', or 'Content'.")
    if desc is None:
        desc = link
    if isinstance(desc, str) == False:
        raise Exception("Invalid value for 'desc'. 'desc' must be a string.")

    # Create the file object
    hlink_object = mpy.Hyperlink(url=link, hyperlink_display=disp, hyperlink_description=desc)

    return hlink_object