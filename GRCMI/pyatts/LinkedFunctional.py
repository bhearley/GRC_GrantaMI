def LinkedFunctional(mi, dbs = None, tables = None):
    #   PURPOSE: Update all linked functional attributes
    #
    #   INPUTS:
    #       mi      Granta Server Connection
    #       dbs     List of database keys or database objects
    #       tables  List of table names or table objects

    # Preallocate Error Message
    msg = ''
    
    # Import Functions
    try:
        from GRANTA_MIScriptingToolkit import granta as mpy
    except:
        msg = msg + 'ERROR 2000: Unable to import Granta Scripting Toolkit. \n'
    

    # Preallocate databases dicitonary
    databases = {}

    # Get all databases on the server
    try:
        db_keys = list(mi.dbs_by_key.keys())
    except:
        msg = msg + "ERROR 2001: Unable to get databases on server. \n"
        return msg

    # No databases list defined - search all databases
    if dbs is None:
        # Add to the database dicitonary
        for key in db_keys:
            try:
                databases[mi.get_db(db_key = key)] = []
            except:
                msg = msg + "WARNING: Unable to get database " + key + " from server. \n"
    
    # User database list defined
    else:
        # Add dbs to list if not in list
        if isinstance(dbs, list) == False:
            dbs = [dbs]

        # Add user databases to the
        for db in dbs:
            # Check if item is string
            if isinstance(db, str):
                if db in db_keys:
                    try:
                        databases[mi.get_db(db_key = db)] = []
                    except:
                        msg = msg + "WARNING: Unable to get database " + db + " from server. \n"
                else:
                    msg = msg + "WARNING: database " + db + " not found on server.\n"

            # Check for database item
            else:
                try:
                    db_key = db.db_key 
                except:
                    msg = msg + "ERROR 2002: Invalid value for 'dbs' given.\n"
                    return msg
                
                if db_key in db_keys:
                    databases = {db:[]}
                else:
                    msg = msg + "WARNING: Unable to get database " + db_key + " from server. \n"

    # Get List of all search databases
    db_list = list(databases.keys())

    # Loop through search databases
    for db_i in db_list:
        # Get List of all tables
        table_list = []
        for table in db_i.tables:
            table_list.append(table.name)

        # No tables list defined - search all tables in the database
        if tables is None:
            for table in table_list:
                try:
                    databases[db_i].append(db_i.get_table(table))
                except:
                    msg = msg + "WARNING: Unable to get table " + table + " from database " + db_i.db_key + ". \n"
        
        # User defined tables
        else:
            # Add tables to list if not in list
            if isinstance(tables, list) == False:
                tables = [tables]

            # Check tables exit
            for table in tables:
                # Check if item is string
                if isinstance(table, str):
                    if table in table_list:
                        try:
                            databases[db_i].append(db_i.get_table(table))
                        except:
                            msg = msg + "WARNING: Unable to get table " + table + " from database " + db_i.db_key + ". \n"
                    else:
                        msg = msg + "WARNING: Table " + table + " not found in database " + key + ".\n"
                
                # Check for table item
                else:
                    try:
                        table_name = table.name
                    except:
                        msg = msg + "ERROR 2003: Invalid value for 'tables' given.\n"
                        return msg
                    
                    if table_name in table_list:
                        databases[db_i].append(table)
                    else:
                        msg = msg + "WARNING: Unable to get table " + table_name + " from database " + db_i.db_key + ". \n"


    # Find all attributes with associated keyphrase
    for db in db_list:
        for table in databases[db]:
            for attribute in table.attributes:

                # Find attributes with keyphrase
                if "Functional Linking Data" in attribute:

                    # Check type
                    if table.attributes[attribute].type != 'TABL':
                        msg = msg + "ERROR 2004: " + attribute + " in table " + table.name + " is not type TABL.\n"
                        return msg
                    
                    # Check Required Columns
                    req_cols = ['Database','Table', 'Attribute', 'Linking Attribute', 'Linking Value', 'Label', 'Link']
                    req_types = ['STXT','STXT', 'STXT', 'STXT', 'STXT', 'STXT', 'HLNK']
                    for col in req_cols:
                        # Check column exists
                        if col not in table.attributes[attribute].columns:
                            msg = msg + "ERROR 2005: Required column name " + col + " in " + attribute + " in table " + table.name + " was not found.\n"
                            return msg
                        
                        # Check column type is correct
                        if req_types[req_cols.index(col)] != table.attributes[attribute].column_types[table.attributes[attribute].columns.index(col)]:
                            msg = msg + "ERROR 2006: Required column name " + col + " in " + attribute + " in table " + table.name + " is not type " + req_types[req_cols.index(col)] + ".\n"
                            return msg
                    
                    # Get corresponding functional attribute
                    func_att = attribute.split("Functional Linking Data" )[0].strip()

                    # Check functional attribute exists
                    if func_att not in table.attributes:
                        msg = msg + "ERROR 2007: " + attribute + " in table " + table.name + " has no corresponding attribute named " +  func_att +  ".\n"
                        return msg

                    # Check corresponding attribute is functional
                    if table.attributes[func_att].type != 'FUNC':
                        msg = msg + "ERROR 2008: " + func_att + " in table " + table.name + " is not type FUNC.\n"
                        return msg
                    
                    # Check for at least two parameters
                    if len(table.attributes[func_att].parameters) < 2:
                        msg = msg + "ERROR 2009: " + func_att + " in table " + table.name + " must have at least two parameters, one functional and one discrete.\n"
                        return msg
                    
                    # Get continuous parameter name
                    x_param = None
                    for j in range(len(table.attributes[func_att].parameters)):
                        if table.attributes[func_att].parameters[list(table.attributes[func_att].parameters.keys())[j]].type != 'Discrete':
                            x_param = list(table.attributes[func_att].parameters.keys())[j]
                            break
                    
                    # Check that continuous parameter exists
                    if x_param is None:
                        msg = msg + "ERROR 2010: " + func_att + " in table " + table.name + " must have at least one continuous parameter.\n"
                        return msg

                    # Get discrete parameter name
                    l_param = None
                    for j in range(len(table.attributes[func_att].parameters)):
                        if table.attributes[func_att].parameters[list(table.attributes[func_att].parameters.keys())[j]].type == 'Discrete':
                            l_param = list(table.attributes[func_att].parameters.keys())[j]
                            break
                    
                    # Check that continuous parameter exists
                    if l_param is None:
                        msg = msg + "ERROR 2011: " + func_att + " in table " + table.name + " must have at least one discrete parameter.\n"
                        return msg
                    
                    # Search for records with populated values
                    srch_att = table.attributes[attribute]
                    srch_crit = srch_att.search_criterion(exists=True, in_column="Linking Value")
                    srch_res = table.search_for_records_where([srch_crit])

                    # Update Records
                    for record in srch_res:
                    
                        # Set the functional attribute
                        func = record.attributes[func_att]

                        # Set the tabular attribute
                        tabl = record.attributes[attribute]

                        # Determine column indices for the continuous and discrete parameters
                        for i, hdr in enumerate(func.column_headers):
                            hdr_val = hdr.split('[')[0].strip()
                            if hdr_val == x_param:
                                x_col = i
                            if hdr_val == l_param:
                                l_col = i

                        # Get the number of entries
                        num_curves = len(tabl.value)
                        
                        # Get Orginal Data
                        all_data = func.value[1:]

                        # Get the list of labels
                        lab_list = []
                        for i in range(num_curves):
                            lab_list.append(tabl.value[i][tabl.columns.index('Label')])


                        # Extract orginal local data
                        orig_data = []
                        for i in range(len(all_data)):
                            if all_data[i][l_col] not in lab_list:
                                orig_data.append(all_data[i])

                        # Clear the attribute and write local data
                        func.clear()
                        for i in range(len(orig_data)):
                            func.add_point({'y':float(orig_data[i][0]),
                                            x_param:float(orig_data[i][x_col]),
                                            l_param:orig_data[i][l_col]})

                        # Get linked data
                        for i in range(num_curves):
                            # Get Values
                            link_db = tabl.value[i][tabl.columns.index('Database')]
                            link_table = tabl.value[i][tabl.columns.index('Table')]
                            link_func = tabl.value[i][tabl.columns.index('Attribute')]
                            link_att = tabl.value[i][tabl.columns.index('Linking Attribute')]
                            link_val = tabl.value[i][tabl.columns.index('Linking Value')]
                            link_lab = tabl.value[i][tabl.columns.index('Label')]

                            # Check Database
                            if link_db is None:
                                link_db = db
                            else:
                                try:
                                    link_db = mi.get_db(db_key = link_db)
                                except:
                                    msg = msg + "ERROR 2012: Linking Database defined for " + attribute + " in record " + record.name + " in table " + table.name +" could not be found. Check the database key.\n"
                                    return msg
                                
                            # Check Table
                            if link_table is None:
                                msg = msg + "ERROR 2013: 'Table' must be defined in " + attribute + " in record " + record.name + " in table " + table.name +".\n"
                                return msg
                            try:
                                link_table = link_db.get_table(link_table)
                            except:
                                msg = msg + "ERROR 2014: Linking Table defined for " + attribute + " in record " + record.name + " in table " + table.name + " could not be found. Check the table name.\n"
                                return msg
                            
                            # Check Attribute
                            if link_func is None:
                                msg = msg + "ERROR 2015: 'Attribute' must be defined in " + attribute + " in record " + record.name + " in table " + table.name + ".\n"
                                return msg
                            try:
                                link_func = link_table.attributes[link_func]
                            except:
                                msg = msg + "ERROR 2016: Linking Functional Attribute defined for " + attribute + " in record " + record.name + " in table " + table.name + " could not be found. Check the attribute name.\n"
                                return msg
                            if link_func.type != 'FUNC':
                                msg = msg + "ERROR 2017: Linking Functional Attribute defined for " + attribute + " in record " + record.name + " in table " + table.name + " must be FUNC.\n"
                                return msg
                            
                            # Check Linking Attribute
                            if link_att is None:
                                msg = msg + "ERROR 2018: 'Linking Attribute' must be defined in " + attribute + " in record " + record.name + " in table " + table.name + ".\n"
                                return msg
                            try:
                                link_att = link_table.attributes[link_att]
                            except:
                                msg = msg + "ERROR 2019: Linking Attribute defined for " + attribute + " in record " + record.name + " in table " + table.name + " could not be found. Check the attribute name.\n"
                                return msg
                            link_types = ['DISC', 'STXT']
                            if link_att.type not in link_types:
                                msg = msg + "ERROR 2020: Invalid Linking Attribute Type defined for " + attribute + " in record " + record.name + " in table " + table.name + ". Linking Attribute must be STXT or DCT.\n"
                                return msg
                            
                            # Check Value
                            if link_val is None:
                                msg = msg + "ERROR 2021: 'Linking Value' must be defined in " + attribute + " in record " + record.name + " in table " + table.name + ".\n"
                                return msg
                            
                            # Check Label
                            if link_lab is None:
                                msg = msg + "ERROR 2022: 'Label' must be defined in " + attribute + " in record " + record.name + " in table " + table.name + ".\n"
                                return msg
                            if link_lab not in func.parameters[l_param].values:
                                msg = msg + "ERROR 2023: Label defined for " + attribute + " in record " + record.name + " in table " + table.name + " is not valid.\n"
                                return msg

                            # Perform Search
                            link_srch_crit = link_att.search_criterion(equal_to =link_val)
                            link_srch_res = link_table.search_for_records_where([link_srch_crit])

                            try:
                                link_record = link_srch_res[0]
                            except:
                                msg = msg + "ERROR 2024: No linked record found for " + attribute + " in record " + record.name + " in table " + table.name + ".\n"
                                return msg

                            # Organize the data
                            link_func = link_record.attributes[link_func.name]

                            # Get the X and Y Columns
                            link_params = list(link_func.parameters.keys())
                            link_x_colp = None
                            for i in range(len(link_params)):
                                if link_func.parameters[link_params[i]].unit == func.parameters[x_param].unit:
                                    link_x_colp = i
                                    break
                                else:
                                    try:
                                        conv_dict = db.dimensionally_equivalent_units(link_func.parameters[link_params[i]].unit)
                                        if func.parameters[x_param].unit in conv_dict.keys():
                                            link_x_colp = i
                                            break
                                    except:
                                        pass

                            if link_x_colp is None:
                                msg = msg + "ERROR 2024: Unable to convert parameter values for " + attribute + " in record " + record.name + " in table " + table.name + ".\n"
                                return msg
                            else:
                                for j, hdr in enumerate(link_func.column_headers):
                                    hdr_val = hdr.split('[')[0].strip()
                                    if hdr_val == link_params[link_x_colp]:
                                        link_x_col = j
                                        break

                            link_y_col = None
                            for j in range(len(link_params)):
                                if link_func.unit == func.unit:
                                    link_y_col = j
                                    break
                                else:
                                    try:
                                        conv_dict = db.dimensionally_equivalent_units(link_func.unit)
                                        if func.unit in conv_dict.keys():
                                            link_y_col = j
                                            break
                                    except:
                                        pass

                            if link_y_col is None:
                                msg = msg + "ERROR 2025: Unable to convert values for " + attribute + " in record " + record.name + " in table " + table.name + ".\n"
                                return msg

                            # Write Data
                            for j in range(1,len(link_func.value)):
                                try:
                                    # -- Write Functional Data
                                    y_val = float(link_func.value[j][link_y_col])
                                    source_unit = link_func.unit
                                    target_unit = func.unit
                                    if source_unit != target_unit:
                                        conv_dict = db.dimensionally_equivalent_units(source_unit)
                                        y_val = y_val*conv_dict[target_unit]['factor'] + conv_dict[target_unit]['offset']

                                    x_val = float(link_func.value[j][link_x_col])
                                    source_unit = link_func.parameters[link_params[link_x_colp]].unit
                                    target_unit = func.parameters[x_param].unit
                                    if source_unit != target_unit:
                                        conv_dict = db.dimensionally_equivalent_units(source_unit)
                                        x_val = x_val*conv_dict[target_unit]['factor'] + conv_dict[target_unit]['offset'] 

                                    func.add_point({'y':y_val,
                                                    x_param:x_val,
                                                    l_param:link_lab})
                                    
                                except:
                                    msg = msg + "ERROR 2026: Unable to add values for " + attribute + " in record " + record.name + " in table " + table.name +".\n"
                                    return msg
                                
                                    
                            # Update Link Text in Tabular Meta Attribute
                            tabl.value[i][tabl.columns.index('Link')] = mpy.Hyperlink(url=link_record.viewer_url , hyperlink_display="New", hyperlink_description=link_record.name)
                            
                        # Update the record
                        record.set_attributes([func, tabl])
                        record = mi.update([record])[0]

                        # Add success message
                        msg = msg + 'Succesfully updated ' + attribute + " in " + record.name + '. \n'
    return msg