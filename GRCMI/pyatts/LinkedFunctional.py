def LinkedFunctional(mi, db = None, table = None):
    #   PURPOSE: Update all linked functional attributes
    #
    #   INPUTS:
    #       mi      Granta Server Connection
    #       db      Selected Granta Database
    #       table   Selected Granta Table (optional)

    # Set List of Search Tables
    if table is not None:
        temp = 1
    else:
        tables = [table]

    temp = 1