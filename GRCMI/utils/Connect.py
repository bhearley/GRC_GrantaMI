def Connect(server_name, db_key, table_name):
  #---------------------------------------------------------------------------
  # Connect.py
  #
  # PURPOSE: Establish connection to a server, database, and table
  #
  # INPUTS:
  #   server_name   address of the Granta MI Server
  #                   ex: granta.ndc.nasa.gov
  #   db_key        database key name
  #                   ex: NasaGRC_MD_45_09-2-05
  #   table_name    name of table
  #                   ex: 'Material Pedigree'
  #---------------------------------------------------------------------------
  
  # Import Modules
  from GRANTA_MIScriptingToolkit import granta as mpy

  # Connect to the server
  try:
    mi = mpy.connect(server_name, autologon=True)
  except:
    raise Exception("Unable to connect to Server: " + server_name)
  
  # Connect to the database
  try:
    db = mi.get_db(db_key = db_key)
  except:
    raise Exception("Unable to load Database Key: " + db_key)
  
  # Get the table
  try:
    table = db.get_table(table_name)
  except:
    raise Exception("Unable to load Table: " + table_name)
  
  return mi, db, table