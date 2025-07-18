# Import Function
from GRCMI import Connect, LinkedFunctional


# Connect to the database
server_name = "https://granta.ndc.nasa.gov"
db_key = "NasaGRC_MD_45_09-2-05"
table_name = "Material Pedigree"
mi, db, table = Connect(server_name, db_key, table_name)

LinkedFunctional(mi, db)
