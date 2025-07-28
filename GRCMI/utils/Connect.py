def Connect(server_name, db_key = None, table_name = None):
	#---------------------------------------------------------------------------
	# Connect.py
	#
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
		raise Exception("Unable to import Granta Scripting Toolkit")    

	# Connect to the server
	try:
		mi = mpy.connect(server_name, autologon=True)
	except:
		raise Exception("Unable to connect to Server: " + server_name)

	# Connect to the database
	if db_key is not None:
		try:
			db = mi.get_db(db_key = db_key)
		except:
			raise Exception("Unable to load Database Key: " + db_key)

		if table_name is not None:
			# Get the table
			try:
				table = db.get_table(table_name)
			except:
				raise Exception("Unable to load Table: " + table_name)

			return mi, db, table
		else:
			return mi, db
	else:
		return mi