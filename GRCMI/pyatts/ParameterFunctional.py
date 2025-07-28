def ParameterFunctional(mi, dbs = None, tables = None):
    #   PURPOSE: Update all parameter based functional attributes
    #
    #   INPUTS:
    #       mi      Granta Server Connection
    #       dbs     List of database keys or database objects (optional)
    #       tables  List of table names or table objects (optional)

    # Preallocate Error Message
    msg = ''
    
    # Import Functions
    import numpy as np
    import re
    try:
        from GRANTA_MIScriptingToolkit import granta as mpy
    except:
        msg = msg + 'ERROR 3000: Unable to import Granta Scripting Toolkit \n'
    
    # Preallocate databases dicitonary
    databases = {}

    # Get all databases on the server
    try:
        db_keys = list(mi.dbs_by_key.keys())
    except:
        msg = msg + "ERROR 3001: Unable to get databases on server. \n"
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
                    msg = msg + "ERROR 3002: Invalid value for 'dbs' given.\n"
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
                        msg = msg + "ERROR 3003: Invalid value for 'tables' given.\n"
                        return msg
                    
                    if table_name in table_list:
                        databases[db_i].append(table)
                    else:
                        msg = msg + "WARNING: Unable to get table " + table_name + " from database " + db_i.db_key + ". \n"

    # Find all attributes with Functional Parameter Definition
    for db in db_list:
        for table in databases[db]:
            for attribute in table.attributes:

                # Find attributes with keyphrase
                if "Functional Parameter Definition" in attribute:

                    # Check type
                    if table.attributes[attribute].type != 'TABL':
                        msg = msg + "ERROR 3004: " + attribute + " in table " + table.name + " is not type TABL.\n"
                        return msg
                    
                    # Check Required Columns
                    req_cols = ['Series Number','Expression', 'Range', 'Range Units', 'Function Units']
                    req_types = ['STXT','LTXT', 'LTXT', 'STXT', 'STXT']
                    for col in req_cols:
                        # Check column exists
                        if col not in table.attributes[attribute].columns:
                            msg = msg + "ERROR 3005: Required column name " + col + " in " + attribute + " in table " + table.name + " was not found.\n"
                            return msg
                        
                        # Check column type is correct
                        if req_types[req_cols.index(col)] != table.attributes[attribute].column_types[table.attributes[attribute].columns.index(col)]:
                            msg = msg + "ERROR 3006: Required column name " + col + " in " + attribute + " in table " + table.name + " is not type " + req_types[req_cols.index(col)] + ".\n"
                            return msg
                    
                    # Get corresponding functional attribute
                    func_att = attribute.split("Functional Parameter Definition")[0].strip()

                    # Check functional attribute exists
                    if func_att not in table.attributes:
                        msg = msg + "ERROR 3007: " + attribute + " in table " + table.name + " has no corresponding attribute named " +  func_att +  ".\n"
                        return msg

                    # Check corresponding attribute is functional
                    if table.attributes[func_att].type != 'FUNC':
                        msg = msg + "ERROR 3008: " + func_att + " in table " + table.name + " is not type FUNC.\n"
                        return msg
                    
                    # Check for at least two parameters
                    if len(table.attributes[func_att].parameters) < 2:
                        msg = msg + "ERROR 3009: " + func_att + " in table " + table.name + " is not type must have at least two parameters, one functional and one discrete.\n"
                        return msg
                    
                    # Check that 'Series Number' exists as a parameter
                    if 'Series Number' not in table.attributes[func_att].parameters.keys():
                        msg = msg + "ERROR 3010: " + func_att + " in table " + table.name + " must have a discrete parameter named 'Series Number'.\n"
                        return msg
                    
                    # Check that the 'Series Number' parameter is discrete
                    if table.attributes[func_att].parameters['Series Number'].type != 'Discrete':
                        msg = msg + "ERROR 3011: " + func_att + " in table " + table.name + " must have a discrete parameter named 'Series Number'.\n"
                        return msg
                    
                    # Search for records with populated values
                    srch_att = table.attributes[attribute]
                    srch_crit = srch_att.search_criterion(exists=True, in_column="Expression")
                    srch_res = table.search_for_records_where([srch_crit])

                    # Update Records
                    for record in srch_res:

                        # Clear the functional attribute
                        func = record.attributes[func_att]
                        func.clear()

                        # Loop through tabular entries
                        tabl = record.attributes[attribute]
                        for i in range(len(tabl.value)):

                            # Unpack Row
                            s_num = tabl.value[i][tabl.columns.index('Series Number')]
                            exp = tabl.value[i][tabl.columns.index('Expression')]
                            rng = tabl.value[i][tabl.columns.index('Range')]
                            rng_u = tabl.value[i][tabl.columns.index('Range Units')]
                            func_u = tabl.value[i][tabl.columns.index('Function Units')]

                            # Check that all are populated
                            if s_num is None:
                                msg = msg + "ERROR 3012: Series Number in attribute " + attribute + " in record " + record.name + " in table " + table.name + " must be defined.\n"
                                return msg
                            
                            if exp is None:
                                msg = msg + "ERROR 3013: Expression in attribute " + attribute + " in record " + record.name + " in table " + table.name + " must be defined.\n"
                                return msg
                            
                            if rng is None:
                                msg = msg + "ERROR 3014: Expression in attribute " + attribute + " in record " + record.name + " in table " + table.name + " must be defined.\n"
                                return msg
                            
                            if rng_u is None:
                                rng_u = ''

                            if func_u is None:
                                func_u = ''

                            # Find all parameters
                            params = re.findall(r'\[([^\]]+)\]', exp)
                            for k, p_full in enumerate(params):

                                # Defined using point attributes
                                if ';' not in p_full:
                                    # Split units
                                    p = p_full.split('(')[0].strip()

                                    # Check for existing attribute
                                    if p not in record.attributes:
                                        msg = msg + "ERROR 3015: Attribute " + p + " in table " + table.name + " not found. Check Expression definition in record " + record.name + " in " + attribute + ".\n"
                                        return msg
                                    
                                    if record.attributes[p].type != 'POIN':
                                        msg = msg + "ERROR 3016: Attribute " + p + " in table " + table.name + " is not type POIN. Check Expression definition in record " + record.name + " in " + attribute + ".\n"
                                        return msg
                                    
                                    # Get value and unit
                                    val = record.attributes[p].value
                                    unit = record.attributes[p].unit

                                    # Check that attribute is defined
                                    if val == []:
                                        msg = msg + "ERROR 3017: Attribute " + p + " in record " + record.name + " in table " + table.name + " not defined.\n"
                                        return msg

                                # Defined using tabular attributes
                                else:
                                    # Get tabular attribute info
                                    p_full = p_full.split(';')
                                    if len(p_full) != 4:
                                        msg = msg + "ERROR 3018: Invalid parmaeter definition in row " + str(k+1) + " in " + attribute + " in record " + record.name + " in table " + table.name + ". See documentation.\n"
                                        return msg
                                    p_tabl = p_full[0].strip()
                                    p_lcol = p_full[1].strip()
                                    p_lval = p_full[2].strip()
                                    p_full = p_full[3].strip()
                                    p_col = p_full.split('(')[0].strip()

                                    # Check for existing attribute
                                    if p_tabl not in record.attributes:
                                        msg = msg + "ERROR 3019: Attribute " + p_tabl + " in table " + table.name + " not found. Check Expression definition in record " + record.name + " in " + attribute + ".\n"
                                        return msg
                                    
                                    # Check for attribute type
                                    if record.attributes[p_tabl].type != 'TABL':
                                        msg = msg + "ERROR 3020: Attribute " + p_tabl + " in table " + table.name + " is not type TABL. Check Expression definition in record " + record.name + " in " + attribute + ".\n"
                                        return msg
                                    p_tabl = record.attributes[p_tabl]

                                    # Get linking column ID
                                    try:
                                        lcol = p_tabl.columns.index(p_lcol)
                                    except:
                                        msg = msg + "ERROR 3021: Column " + p_lcol + " in " + p_tabl.name +  " in table " + table.name + " not found. Check Expression definition in record " + record.name + " in " + attribute + ".\n"
                                        return msg
                                    
                                    # Find row
                                    lrow = None
                                    for j in range(len(p_tabl.value)):
                                        if p_tabl.value[j][lcol] == p_lval:
                                            lrow = j
                                    if lrow is None:
                                        msg = msg + "ERROR 3022: " + p_lval + " not found in column " + p_lcol + " in " + p_tabl.name + " in record " + record.name + " in table " + table.name + " not found. Check Expression definition in record " + record.name + " in " + attribute + ".\n"
                                        return msg
                                    
                                    # Get defining column ID
                                    try:
                                        col = p_tabl.columns.index(p_col)
                                    except:
                                        msg = msg + "ERROR 3023: Column " + p_col + " in " + p_tabl.name + "in record " + record.name + " in table " + table.name + " not found. Check Expression definition in record " + record.name + " in " + attribute + ".\n"
                                        return msg
                                    
                                    # Check column type
                                    if p_tabl.column_types[col] != "POIN":
                                        msg = msg + "ERROR 3024: Column " + p_col + " in " + p_tabl.name + "in record " + record.name + " in table " + table.name + " is not type POIN. Check Expression definition in record " + record.name + " in " + attribute + ".\n"
                                        return msg

                                    # Get the value and unit
                                    val = p_tabl.value[lrow][col][0]
                                    unit = p_tabl.units.data[lrow][col]

                                    if val is None:
                                        msg = msg + "ERROR 3025: Row " + str(lrow) + ", Column " + p_col + " in " + p_tabl.name + " in record " + record.name + " in table " + table.name + " is not defined..\n"
                                        return msg

                                # Check for unit conversion
                                if unit != '':
                                    def_unit = re.findall(r'\(([^)]+)\)', p_full)

                                    if def_unit == []:
                                        msg = msg + "ERROR 3026: " + params[k] + " in record " + record.name + " in table " + table.name + " needs units defined in " + attribute + " between ().\n"
                                        return msg
                                    
                                    if def_unit[0] != unit:
                                        conv_dict = db.dimensionally_equivalent_units(unit)
                                        if def_unit[0] not in conv_dict.keys():
                                            msg = msg + "ERROR 3027: Invalid unit conversion defined for " + params[k] + " in record " + record.name + " in table " + table.name + " in " + attribute + ". Units " + unit + " and " + def_unit[0] + " are incompatible.\n"
                                            return msg
                                        val = val*conv_dict[def_unit[0]]['factor'] + conv_dict[def_unit[0]]['offset']

                                # Replace values in expression
                                exp = exp.replace('[' + params[k] + ']', str(val))

                            # Check for defined x parameter
                            x_param = None
                            if ':' in rng:
                                x_param = rng.split(':')[0].strip()
                                if x_param in func.parameters.keys():
                                    if func.parameters[x_param].type == 'Discrete':
                                        msg = msg + "ERROR 3029: Parameter " + x_param + " in " + func.name + " in table " + table.name + " cannot be discrete. Check Range definition.\n"
                                        return msg
                                    x_param_u = func.parameters[x_param].unit
                                else:
                                    msg = msg + "ERROR 3028: Parameter " + x_param + " is not in " + func.name + " in table " + table.name + ". Check Range definition.\n"
                                    return msg
                                rng = rng.split(':')[1]

                            else:
                                for p in func.parameters.keys():
                                    if func.parameters[p].type != "Discrete":
                                        x_param = p
                                        x_param_u = func.parameters[p].unit
                                        break
                            if x_param is None:
                                msg = msg + "ERROR 3030: No viable parameter found for " + func.name + " in table " + table.name + ".\n"
                                return msg

                            # Check units
                            conv_flag = 0
                            if rng_u != x_param_u:
                                conv_dict = db.dimensionally_equivalent_units(x_param_u)
                                if rng_u not in conv_dict.keys():
                                    msg = msg + "ERROR 3031: Invalid unit conversion defined for Parameter " + x_param + " in " + func.name + " in record " + record.name + " in table " + table.name + " in " + attribute + ". Units " + x_param_u + " and " + rng_u + " are incompatible.\n"
                                    return msg
                                conv_flag = 1
                                
                            # Get X Range Values
                            if ';' in rng:
                                vals = rng.split(';')
                                try:
                                    p_array = np.linspace(float(vals[0]), float(vals[1]), int(vals[2]))
                                except:
                                    msg = msg + "ERROR 3032: Invalid format for 'Range' in record " + record.name + " in table " + table.name + " in " + attribute + ". See documentation for correct format options. \n"
                                    return msg
                                
                            else:
                                p_array = np.fromstring(rng, sep=',')
                                if len(p_array) == 0:
                                    msg = msg + "ERROR 3032: Invalid format for 'Range' in record " + record.name + " in table " + table.name + " in " + attribute + ". See documentation for correct format options. \n"
                                    return msg
                                
                            # Convert X Values
                            if conv_flag == 1:
                                p_array = p_array*conv_dict[rng_u]['factor'] + conv_dict[rng_u]['offset']
                                
                            # Calculate Y Values
                            f_array = np.zeros((len(p_array),))
                            for j in range(len(p_array)):
                                try:
                                    val_exp = exp.replace('x', str(p_array[j]))
                                    if '^' in val_exp:
                                        val_exp = val_exp.replace('^', '**')
                                    f_array[j] = eval(val_exp)
                                except:
                                    msg = msg + "ERROR 3033: Invalid format for Expression in " + attribute + " in record " + record.name + " in table " + table.name + ". See documentation for correct format options. \n"
                                    return msg
                                
                            # Check unit conversion for y
                            if func_u != func.unit:
                                conv_dict = db.dimensionally_equivalent_units(func_u)
                                if func.unit not in conv_dict.keys():
                                    msg = msg + "ERROR 3034: Invalid unit conversion defined for Function Unit in " + attribute + " in record " + record.name + " in table " + table.name + ". \n"
                                    return msg
                                f_array = f_array*conv_dict[func.unit]['factor'] + conv_dict[func.unit]['offset']
                            
                            # Get the series number
                            try:
                                s_num = func.parameters['Series Number'].values[func.parameters['Series Number'].values.index(s_num)]
                            except:
                                msg = msg + "ERROR 3035: Series Number not found in discrete options for " + func.name + " in table " + table.name + ".\n"
                                return msg
                            
                            # Write the Data
                            for j in range(len(p_array)):
                                func.add_point({'y':f_array[j],
                                                    x_param:p_array[j],
                                                    'Series Number':s_num})

                        # Update the record   
                        record.set_attributes([func])
                        record = mi.update([record])[0]
    return msg