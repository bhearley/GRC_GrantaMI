def Connect(server_name, db_key = None, table_name = None):
	#---------------------------------------------------------------------------
	# PURPOSE: Establish connection to a server, database, and table
	#
	# INPUTS:
	#   server_name   address of the Granta MI Server
	#                   ex: granta.ndc.nasa.gov
	#   db_key        database key name (optional)
	#                   ex: NasaGRC_MD_45_09-2-05
	#   table_name    name of table (optional)
	#                   ex: 'Material Pedigree'
	#---------------------------------------------------------------------------

	# Import Modules
	try:
		from GRANTA_MIScriptingToolkit import granta as mpy
	except:
		raise Exception("ERROR 0000: Unable to import Granta Scripting Toolkit.")    

	# Connect to the server
	try:
		mi = mpy.connect(server_name, autologon=True)
	except:
		if isinstance(server_name, str):
			raise Exception("ERROR 0001: Unable to connect to Server: " + server_name + '.')
		else:
			raise Exception("ERROR 0002: Invalid value for 'server_name'.")

	# Connect to the database
	if db_key is not None:
		try:
			db = mi.get_db(db_key = db_key)
		except:
			if isinstance(db_key, str):
				raise Exception("ERROR 0003: Unable to load Database Key: " + db_key + '.')
			else:
				raise Exception("ERROR 0004: Invalid value for 'db_key'.")

		if table_name is not None:
			# Get the table
			try:
				table = db.get_table(table_name)
			except:
				if isinstance(table_name, str):
					raise Exception("ERROR 0005: Unable to load Table: " + table_name + '.')
				else:
					raise Exception("ERROR 0006: Invalid value for 'table_name'.")

			return mi, db, table
		else:
			return mi, db
	else:
		return mi