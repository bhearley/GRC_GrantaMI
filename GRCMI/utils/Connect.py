def Connect(server_name, db_key = None, table_name = None):
	#---------------------------------------------------------------------------
	# PURPOSE: Establish connection to a server, database, and table
	#
	# INPUTS:
	#   server_name		string	   			address of the Granta MI Server
	#                   						ex: 'granta.ndc.nasa.gov'
	#   db_key        	string				database key name (optional)
	#                   						ex: 'NasaGRC_MD_45_09-2-05'
	#   table_name    	string				name of table (optional)
	#                   						ex: 'Material Pedigree'
	#
	# OUTPUTS:
	#   mi          	SessionObject       Granta Server Connection
	#   db          	DatabaseObject      Selected Granta Database
	#   table       	TableObject         Selected Granta Table
	#---------------------------------------------------------------------------

	# Import Modules
	try:
		from GRANTA_MIScriptingToolkit import granta as mpy
	except:
		raise Exception("Unable to import Granta Scripting Toolkit.")    

	# Connect to the server
	try:
		mi = mpy.connect(server_name, autologon=True)
	except:
		if isinstance(server_name, str):
			raise Exception("Unable to connect to Server: " + server_name)
		else:
			raise Exception("Invalid value for 'server_name'. 'server_name' must be a string.")

	# Connect to the database
	if db_key is not None:
		try:
			db = mi.get_db(db_key = db_key)
		except:
			if isinstance(db_key, str):
				raise Exception("Unable to load Database Key: " + db_key)
			else:
				raise Exception("Invalid value for 'db_key'. 'db_key' must be a string.")

		# Connect to the table
		if table_name is not None:
			try:
				table = db.get_table(table_name)
			except:
				if isinstance(table_name, str):
					raise Exception("Unable to load Table: " + table_name)
				else:
					raise Exception("Invalid value for 'table_name'. 'table_name' must be a string.")

			return mi, db, table
		else:
			return mi, db
	else:
		return mi