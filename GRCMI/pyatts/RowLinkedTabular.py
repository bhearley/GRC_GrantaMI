def RowLinkedTabular(mi, dbs = None, tables = None):
    #   PURPOSE: Update all row linked tabular attributes
    #
    #   INPUTS:
    #       mi      Granta Server Connection
    #       dbs     List of database keys or database objects
    #       tables  List of table names or table objects

    # Preallocate Error Message
    msg = ''

    # Import Functions
    import re
    try:
        from GRANTA_MIScriptingToolkit import granta as mpy
    except:
        msg = msg + 'ERROR 1000: Unable to import Granta Scripting Toolkit. \n'

    # Preallocate databases dicitonary
    databases = {}

    # Get all databases on the server
    try:
        db_keys = list(mi.dbs_by_key.keys())
    except:
        msg = msg + "ERROR 1001: Unable to get databases on server. \n"
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
                    msg = msg + "ERROR 1002: Invalid value for 'dbs' given.\n"
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
                        msg = msg + "ERROR 1003: Invalid value for 'tables' given.\n"
                        return msg
                    
                    if table_name in table_list:
                        databases[db_i].append(table)
                    else:
                        msg = msg + "WARNING: Unable to get table " + table_name + " from database " + db_i.db_key + ". \n"

    # Find all tabular attributes that contain the keyphrase
    for db in db_list:
        for table in databases[db]:
            for attribute in table.attributes:

                # Find attributes with keyphrase
                if table.attributes[attribute].type == 'TABL' and 'RWL' in table.attributes[attribute].columns:

                    # Check Required Columns
                    req_cols = ['Link', 'RWL']
                    req_types = ['HLNK', 'STXT']
                    for col in req_cols:
                        # Check column exists
                        if col not in table.attributes[attribute].columns:
                            msg = msg + "ERROR 1004: Required column name " + col + " in " + attribute + " in table " + table.name + " was not found.\n"
                            return msg
                        
                        # Check column type is correct
                        if req_types[req_cols.index(col)] != table.attributes[attribute].column_types[table.attributes[attribute].columns.index(col)]:
                            msg = msg + "ERROR 1005: Required column name " + col + " in " + attribute + " in table " + table.name + " is not type " + req_types[req_cols.index(col)] + ".\n"
                            return msg

                    # Search for records with populated values
                    srch_att = table.attributes[attribute]
                    srch_crit = srch_att.search_criterion(exists=True, in_column="RWL")
                    srch_res = table.search_for_records_where([srch_crit])

                    # Update Records
                    for record in srch_res:
                        # Set the tabular attribute
                        tabl = record.attributes[attribute]

                        # Get the number of entries
                        num_rows = len(tabl.value)

                        # Preallocate new tabular data
                        tab_data_cols = []

                        # Find linked tabular data
                        for i in range(num_rows):
                            # Preallocate new row
                            tab_data_new = []

                            # Get the RWL Value
                            RWL = tabl.value[i][tabl.columns.index('RWL')]

                            # Check if RWL Exists
                            if RWL is None or RWL == '':
                                continue

                            # Extract information from RWL
                            RWL_data = RWL.split(';')

                            if len(RWL_data) == 5:
                                db_rwl = db
                                tab_rwl = table
                                link_att = RWL_data[0].strip()
                                link_val = RWL_data[1].strip()
                                link_tab = RWL_data[2].strip()
                                link_col = RWL_data[3].strip()
                                link_col_val = RWL_data[4].strip()
                            
                            elif len(RWL_data) == 6:
                                db_rwl = db

                                # Get the table
                                try:
                                    tab_rwl = db_rwl.get_table(RWL_data[0].strip())
                                except:
                                    msg = msg + "ERROR 1007: Table defined in RWL in " + attribute + " in table " + table.name + " was not found.\n"
                                    return msg

                                link_att = RWL_data[1].strip()
                                link_val = RWL_data[2].strip()
                                link_tab = RWL_data[3].strip()
                                link_col = RWL_data[4].strip()
                                link_col_val = RWL_data[5].strip()

                            elif len(RWL_data) == 7:
                                # Get the database
                                try:
                                    db_rwl = mi.get_db(db_key = RWL_data[0].strip())
                                except:
                                    msg = msg + "ERROR 1006: Database key defined in RWL in " + attribute + " in table " + table.name + " was not found.\n"
                                    return msg

                                # Get the table
                                try:
                                    tab_rwl = db_rwl.get_table(RWL_data[1].strip())
                                except:
                                    msg = msg + "ERROR 1007: Table defined in RWL in " + attribute + " in table " + table.name + " was not found.\n"
                                    return msg

                                link_att = RWL_data[2].strip()
                                link_val = RWL_data[3].strip()
                                link_tab = RWL_data[4].strip()
                                link_col = RWL_data[5].strip()
                                link_col_val = RWL_data[6].strip()

                            else:
                                msg = msg + "ERROR 1008: Invalid syntax  in RWL in " + attribute + " in table " + table.name + ". See documentation.\n"
                                return msg

                            # Check Linking Attribute
                            try:
                                link_att = tab_rwl.attributes[link_att]
                            except:
                                msg = msg + "ERROR 1009: Linking Attribute defined for " + attribute + " in record " + record.name + " in table " + tab_rwl.name + " could not be found. Check the attribute name.\n"
                                return msg
                            link_types = ['DISC', 'STXT']
                            if link_att.type not in link_types:
                                msg = msg + "ERROR 1010: Invalid Linking Attribute Type defined for " + attribute + " in record " + record.name + " in table " + tab_rwl.name + ". Linking Attribute must be STXT or DISC.\n"
                                return msg
                            
                            # Check Linked Tabular Attribute
                            try:
                                link_tab = tab_rwl.attributes[link_tab]
                            except:
                                msg = msg + "ERROR 1011: Linked Tabular Attribute defined for " + attribute + " in record " + record.name + " in table " + tab_rwl.name + " could not be found. Check the attribute name.\n"
                                return msg
                            if link_tab.type != 'TABL':
                                msg = msg + "ERROR 1012: Invalid Linked Tabular Attribute Type defined for " + attribute + " in record " + record.name + " in table " + tab_rwl.name + ". Linked Tabular Attribute must be TABL.\n"
                                return msg
                            
                            # Check Linked Tabular Column
                            if link_col not in link_tab.columns:
                                msg = msg + "ERROR 1013: Linked Tabular Column defined for " + attribute + " in record " + record.name + " in table " + tab_rwl.name + " could not be found. Check the column name.\n"
                                return msg
                            link_types = ['DISC', 'STXT']
                            if link_tab.column_types[link_tab.columns.index(link_col)] not in link_types:
                                
                                # Set exit flag
                                e_flag = 0

                                # Check if linked column
                                if link_tab.column_types[link_tab.columns.index(link_col)] == '':

                                    # Get linked column type
                                    try:
                                        col_type = link_tab.linking_table.attributes[link_col].type
                                        if col_type in link_types:
                                            e_flag = 1
                                    except:
                                        pass
                                
                                if e_flag == 0:
                                    msg = msg + "ERROR 1014: Invalid Linked Tabular Column Type defined for " + attribute + " in record " + record.name + " in table " + tab_rwl.name + ". Linking Tabular Column must be STXT or DISC.\n"
                                    return msg
                            
                            # Perform Search
                            link_srch_crit = link_att.search_criterion(equal_to =link_val)
                            link_srch_res = tab_rwl.search_for_records_where([link_srch_crit])
                            try:
                                link_record = link_srch_res[0]
                            except:
                                msg = msg + "ERROR 1015: No linked record found for " + attribute + " in record " + record.name + " in table " + table.name + ".\n"
                                return msg
                            
                            # Find the row
                            row_data = None
                            for j in range(len(link_record.attributes[link_tab.name].value)):
                                # Get the value
                                lval = link_record.attributes[link_tab.name].value[j][link_record.attributes[link_tab.name].columns.index(link_col)] 
                                if isinstance(lval, list):
                                    lval = lval[0]


                                # Find the row
                                if lval == link_col_val:
                                    source_col_names = link_record.attributes[link_tab.name].columns
                                    row_data_raw = link_record.attributes[link_tab.name].value[j]
                                    row_data = []
                                    for r in row_data_raw:

                                        if isinstance(r, list):
                                            r = r[0]

                                        row_data.append(r)

                                    unit_data = link_record.attributes[link_tab.name].units.data[j]
                                    break

                            # Check that a row was found
                            if row_data is None:
                                msg = msg + "ERROR 1016: Linking Value " + link_col_val + " was not found in column " + link_col + " in " + link_tab.name + " in record " + link_record.name + " in table " + tab_rwl.name + ".\n"
                                return msg
                            
                            # Configuration Function
                            def GetConfig(msg):

                                # Initialize Configuration Dictionary
                                config = {}

                                # Search for Configuration in Meta-Attributes
                                if "Configuration" in tabl.meta_attributes.keys():

                                    # Get Configuration Information
                                    config_att = tabl.meta_attributes['Configuration']

                                    # Check that configuration attribute is table
                                    if config_att.type != "TABL":
                                        msg = msg + "ERROR 1017: Configuration Meta-Attribute in " + attribute + " in table " + table.name + " must be type TABL.\n"
                                        return config, msg, 1

                                    # Check that there's one row of data - if not, assume no configuration
                                    if len(config_att.value) < 1:
                                        for col in tabl.columns:
                                            if col in link_tab.columns and col in tabl.columns:
                                                if col != 'RWL' and col !='Link':
                                                    config[col] = col
                                        return config, msg, 0

                                    # Check Required Columns
                                    req_cols = ['Database', 'Table', 'Attribute']
                                    req_types = ['STXT', 'STXT', 'STXT']
                                    for col in req_cols:

                                        # Check column exists
                                        if col not in config_att.columns:
                                            msg = msg + "ERROR 1018: Required column name " + col + " in Configuration Meta-Attribute in " + attribute + " in table " + table.name + " was not found.\n"
                                            return config, msg, 1
                                        
                                        # Check column type is correct
                                        if req_types[req_cols.index(col)] != config_att.column_types[config_att.columns.index(col)]:
                                            msg = msg + "ERROR 1019: Required column name " + col + " in Configuration Meta-Attribute in " + attribute + " in table " + table.name + " is not type " + req_types[req_cols.index(col)] + ".\n"
                                            return config, msg, 1

                                    # Find the correct row
                                    row = None
                                    for k in range(len(config_att.value)):
                                        if config_att.value[k][config_att.columns.index('Attribute')] == link_tab.name:
                                            # Check the database
                                            if config_att.value[k][config_att.columns.index('Database')] is None:
                                                config_db = db_rwl
                                            else:
                                                try:
                                                    config_db = mi.get_db(db_key = config_att.value[k][config_att.columns.index('Database')].strip())
                                                except:
                                                    msg = msg + "ERROR 1020: Database key defined in Configuration Meta-Attribute in " + attribute + " in table " + table.name + " was not found.\n"
                                                    return config, msg, 1

                                            if config_db.db_key != db_rwl.db_key:
                                                continue

                                            # Check the table
                                            if config_att.value[k][config_att.columns.index('Table')] is None:
                                                config_tab = tab_rwl
                                            else:
                                                try:
                                                    config_tab = config_db.get_table(config_att.value[k][config_att.columns.index('Table')].strip())
                                                except:
                                                    msg = msg + "ERROR 1021: Table name defined in Configuration Meta-Attribute in " + attribute + " in table " + table.name + " was not found.\n"
                                                    return config, msg, 1

                                            if config_tab.name != tab_rwl.name:
                                                continue

                                            # Get the row
                                            row = config_att.value[k]

                                    if row is None:
                                        for col in tabl.columns:
                                            if col in link_tab.columns and col in tabl.columns:
                                                if col != 'RWL' and col !='Link':
                                                    config[col] = col
                                        return config, msg, 0

                                    # Find matching attributes
                                    for k, r in enumerate(row):

                                        # Check for STXT Column Type
                                        try:
                                            if config_att.column_types[k] != "STXT":
                                                continue
                                        except:
                                            continue

                                        # Get configuration value
                                        if config_att.columns[k] not in ['Database', 'Table', 'Attribute']:
                                            if r is None or r == '':
                                                continue

                                            val = r.split(':')
                                            if len(val) != 2:
                                                msg = msg + "ERROR 1022: Invalid format in Configuration Meta-Attribute in " + attribute + " in table " + table.name + ". See documentation\n"
                                                return config, msg, 1
                                            
                                            source = val[0].strip()
                                            if source not in link_tab.columns:
                                                msg = msg + "ERROR 1023: Column name " + source + " defined in Configuration Meta-Attribute in " + attribute + " in table " + table.name + " not found in " + link_tab.name + " in " + link_record.name + ".\n"
                                                return config, msg, 1
                                            target = val[1].strip()

                                            if target not in tabl.columns:
                                                msg = msg + "ERROR 1024: Column name " + target + " defined in Configuration Meta-Attribute in " + attribute + " in table " + table.name + " not found in " + tabl.name + " in " + record.name + ".\n"
                                                return config, msg, 1
                                            
                                            config[target] =  source

                                    return config, msg, 0

                                else:
                                    for col in tabl.columns:
                                        if col in link_tab.columns and col in tabl.columns:
                                            if col != 'RWL' and col !='Link':
                                                config[col] = col
                                    return config, msg, 0

                            # Get Configuration
                            config, msg, err_flag = GetConfig(msg)
                            if err_flag == 1:
                                return msg


                            # Get new row data
                            for col in config.keys():
                                # Get the column index
                                try:
                                    s_col_idx = source_col_names.index(config[col])
                                except:
                                    continue
                                

                                if col in tabl.columns:
                                    # Add the column name
                                    if i == 0:
                                        tab_data_cols.append(col)

                                    # Get the target index
                                    t_col_idx = tabl.columns.index(col)
    
                                    # Get the source value
                                    val = row_data[s_col_idx]
                                    if val is None:
                                        tab_data_new.append(val)
                                        continue

                                    # Get the source type
                                    try:
                                        stype = link_record.attributes[link_tab.name].column_types[s_col_idx]
                                    except:
                                        tab_data_new.append(val)
                                        continue

                                    # Get the target type
                                    ttype = tabl.column_types[t_col_idx]

                                    # Check Type Compataiblity
                                    # -- Text Attributes
                                    if stype == 'STXT' or stype == 'LTXT' or stype == 'DISC':
                                        # Convert Strings Directly
                                        if ttype == 'LTXT' or ttype == 'STXT':
                                            new_val = val

                                        # Check string is in discrete option
                                        elif ttype == 'DISC':
                                            try:
                                                if isinstance(val, list):
                                                    val = val[0]
                                            except:
                                                pass
                                            if val in tabl.definition.discrete_values[t_col_idx]:
                                                new_val = val
                                            else:
                                                msg = msg + "ERROR 1026: " + val + " in record " + link_record.name + " is not in the discrete options for column " + config[col] + " in " + tabl.name + " in record " + record.name + ".\n"
                                                return msg
                                            
                                        # Check for integer
                                        elif ttype == "INPT":
                                            try:
                                                new_val = int(val)
                                            except:
                                                msg = msg + "ERROR 1025: Incompatible column types between " + col + " in " + link_tab.name + " in record " + link_record.name + " and " + config[col] + " in " + tabl.name + " in record " + record.name + ".\n"
                                                return msg
                                        
                                        # Check for POINT
                                        elif ttype == "POIN":

                                            # Get Units
                                            t_unit = tabl.units.default_units[t_col_idx]

                                            # Get Point Value
                                            if '(' in val:
                                                s_unit = re.findall(r'\(([^)]+)\)', val)
                                                val = val.split('(')[0].strip()
                                            else:
                                                s_unit = ''
                                            try:
                                                val = float(val)
                                            except:
                                                msg = msg + "ERROR 1025: Incompatible column types between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ".\n"
                                                return msg
                                            if s_unit == '' and t_unit == '':
                                                new_val = val
                                            elif s_unit == t_unit:
                                                new_val = val
                                            else:
                                                conv_dict = db_rwl.dimensionally_equivalent_units(s_unit)
                                                if t_unit in conv_dict:
                                                    new_val = new_val*conv_dict[t_unit]['factor'] + conv_dict[t_unit]['offset']
                                                else:
                                                    msg = msg + "ERROR 1028: Incompatible units between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ".\n"
                                                return msg
                                            
                                        else:
                                            msg = msg + "ERROR 1025: Incompatible column types between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ".\n"
                                            return msg

                                    elif stype == 'POIN':
                                        # Get Value
                                        try:
                                            val = val[0]
                                        except:
                                            pass

                                        # Get the source unit
                                        s_unit = unit_data[s_col_idx]
                                        if isinstance(s_unit, list):
                                            s_unit = s_unit[0]

                                        # Convert to integer
                                        if ttype == "INPT":
                                            if s_unit == '':
                                                new_val = int(val)
                                            else:
                                                msg = msg + "ERROR 1027: Incompatible column types between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ". POIN cannot be converted to INPT with associated units.\n"
                                                return msg
                                        
                                        # Convert to point
                                        elif ttype == "POIN":
                                            t_unit = tabl.units.default_units[t_col_idx]
                                            if isinstance(t_unit, list):
                                                t_unit = t_unit[0]

                                            if s_unit == '' and t_unit == '':
                                                new_val = val
                                            elif s_unit == t_unit:
                                                new_val = val
                                            else:
                                                conv_dict = db_rwl.dimensionally_equivalent_units(s_unit)
                                                if t_unit in conv_dict:
                                                    new_val = new_val*conv_dict[t_unit]['factor'] + conv_dict[t_unit]['offset']
                                                else:
                                                    msg = msg + "ERROR 1028: Incompatible units between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ".\n"
                                                return msg
                                            
                                        elif ttype == "STXT" or ttype == "LTXT":
                                            new_val = str(val)
                                            if s_unit != '':
                                                new_val = new_val + " (" + s_unit +")"

                                        else:
                                            msg = msg + "ERROR 1025: Incompatible column types between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ".\n"
                                            return msg

                                    elif stype == 'RNGE':
                                        # Get Value
                                        try:
                                            val = val[0]
                                        except:
                                            pass

                                        # Get the source unit
                                        s_unit = unit_data[s_col_idx]
                                        if isinstance(s_unit, list):
                                            s_unit = s_unit[0]

                                        if ttype == "RNGE":
                                            
                                            t_unit = tabl.units.default_units[t_col_idx]
                                            if isinstance(t_unit, list):
                                                t_unit = t_unit[0]

                                            if s_unit == '' and t_unit == '':
                                                new_val = val
                                            elif s_unit == t_unit:
                                                new_val = val
                                            else:
                                                conv_dict = db_rwl.dimensionally_equivalent_units(s_unit)
                                                if t_unit in conv_dict:
                                                    new_val['low'] = new_val['low']*conv_dict[t_unit]['factor'] + conv_dict[t_unit]['offset']
                                                    new_val['high'] = new_val['high']*conv_dict[t_unit]['factor'] + conv_dict[t_unit]['offset']
                                                else:
                                                    msg = msg + "ERROR 1028: Incompatible units between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ".\n"
                                                    return msg
                                        
                                        elif ttype == "STXT" or ttype == "LTXT":
                                            new_val = 'low: ' + str(val['low']) + ' high:' + str(val['high'])
                                            if s_unit != '':
                                                new_val = new_val + " (" + s_unit +")"

                                        else:
                                            msg = msg + "ERROR 1025: Incompatible column types between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ".\n"
                                            return msg


                                    elif stype == 'INPT':
                                        if ttype == 'INPT':
                                            new_val = val

                                        elif ttype == "STXT" or ttype == "LTXT":
                                            new_val = str(val)

                                        elif ttype == 'POIN':
                                            t_unit = tabl.units.default_units[t_col_idx]
                                            if isinstance(t_unit, list):
                                                t_unit = t_unit[0]

                                            if t_unit == '':
                                                new_val = val
                                            else:
                                                msg = msg + "ERROR 1029: Incompatible column types between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ". INPT cannot be converted to POIN with associated units.\n"
                                                return msg
                                            
                                        else:
                                            msg = msg + "ERROR 1025: Incompatible column types between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ".\n"
                                            return msg

                                    elif stype == 'PICT':
                                        if ttype == "PICT":
                                            new_val = val
                                        else:
                                            msg = msg + "ERROR 1025: Incompatible column types between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ".\n"
                                            return msg

                                    elif stype == 'FILE':
                                        if ttype == "FILE":
                                            new_val = val
                                        else:
                                            msg = msg + "ERROR 1025: Incompatible column types between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ".\n"
                                            return msg

                                    elif stype == 'HLNK':
                                        if ttype == "HLNK":
                                            new_val = val
                                        else:
                                            msg = msg + "ERROR 1025: Incompatible column types between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ".\n"
                                            return msg

                                    elif stype == 'LOGI':
                                        if ttype == 'LOGI':
                                            new_val = val
                                        elif ttype == 'STXT' or ttype == 'LTXT':
                                            new_val = str(val)
                                        else:
                                            msg = msg + "ERROR 1025: Incompatible column types between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ".\n"
                                            return msg
                                        
                                    elif stype == 'DTTM':
                                        if ttype == 'DTTM':
                                            new_val = val
                                        elif ttype == 'STXT' or ttype == 'LTXT':
                                            new_val = str(val)
                                        else:
                                            msg = msg + "ERROR 1025: Incompatible column types between " + col + " in " + link_tab.name + " in " + link_record.name + " and " + config[col] + " in " + tabl.name + " in " + record.name + ".\n"
                                            return msg
                                    
                                # Add data to new row
                                tab_data_new.append(new_val)


                            for col in tab_data_cols:
                                tabl.value[i][tabl.columns.index(col)] = tab_data_new[tab_data_cols.index(col)]
                                
                            # Create the link
                            tabl.value[i][tabl.columns.index('Link')] = mpy.Hyperlink(url=link_record.viewer_url , hyperlink_display="New", hyperlink_description=link_record.name)

                        # Update the record   
                        record.set_attributes([tabl])
                        record = mi.update([record])[0]

                        # Add success message
                        msg = msg + 'Succesfully updated ' + attribute + " in " + record.name + '. \n'

    return msg