from GRCMI import Connect

server_name = "https://granta.ndc.nasa.gov"
db_key = "NasaGRC_MD_45_09-2-05"
table = 'Models (Demo)'
mi, db, table = Connect(server_name, db_key, table)

record = table.search_for_records_by_name('Simulation Data Record')[0]
func = record.attributes['Simulation Data: Stress vs Strain']
func.clear()

stress = [
-1.53E+07,
4.99E+07,
1.25E+08,
1.88E+08,
2.58E+08,
3.25E+08,
3.57E+08,
3.73E+08,
3.85E+08,
3.95E+08,
4.05E+08,
4.17E+08,
4.27E+08,
4.36E+08,
4.47E+08,
4.59E+08,
4.81E+08,
5.02E+08,
5.23E+08,
5.45E+08,
5.67E+08,
5.86E+08,
6.01E+08,
6.14E+08,
6.24E+08,
6.33E+08,
6.40E+08,
6.45E+08,
6.50E+08,
6.54E+08,
6.58E+08,
6.61E+08,
6.63E+08,
6.66E+08,
]

strain = [
-0.007812618,
0.025553243,
0.06376732,
0.096063393,
0.13206051,
0.17058861,
0.20808017,
0.24906585,
0.28874988,
0.32660625,
0.36304356,
0.40201761,
0.4438246,
0.48554454,
0.53887983,
0.61290131,
0.84690903,
1.2475507,
1.7590038,
2.4286374,
3.1843897,
3.9754037,
4.7798436,
5.6143446,
6.4581342,
7.3031139,
8.167543,
9.0133713,
9.8762627,
10.759123,
11.632618,
12.477095,
13.331617,
14.189054,
]

for i in range(len(stress)):
    func.add_point({'y':stress[i],
                    'Strain':strain[i],
                    'Simulation Data':'Simulation'},
                    )
    
record.set_attributes([func])
record = mi.update([record])[0]
    
