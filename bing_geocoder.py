import csv, time, random
from geopy.geocoders import Bing
encodage = 'ANSI'
entry_file = "inputs/sahame3.csv"
out_file = entry_file.replace('inputs', "outputs")

def writing_in(file, content):
    with open(file, 'a', newline='',  encoding=encodage) as csvfile:
        writer = csv.writer(csvfile, delimiter=';',   quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(content)

with open(entry_file, newline='', encoding=encodage) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    #writing_in(out_file, ['id', 'Adresse', 'Ville', 'N_Police', 'Coord Z', 'longeur_champs', 'geocoding_level', 'x', 'y'])
    for row in reader:
        if(int(row['id']) > 39305):
            geolocator = Bing('AuBp6_arenVona3ldJD7QRZD-jXIweopYVRIFbq3-y2wV4pSglccvP4fqQvEnXk_')
            print(row['Adresse']+" "+row['Ville'])
            location = geolocator.geocode(row['Adresse']+" "+row['Ville'])
            time.sleep(0.5)
            if(location is not None):
                print((location.latitude, location.longitude))
                writing_in(out_file, [row['id'], row['Adresse'], row['Ville'], row['N_Police'], row['Coord Z'], row['longeur_champs'], 'adresse', location.latitude, location.longitude])

            else:
                print("just ville :")
                location = geolocator.geocode(row['Ville'])
                if(location is not None):
                    print((location.latitude, location.longitude))
                    writing_in(out_file, [row['id'], row['Adresse'], row['Ville'], row['N_Police'], row['Coord Z'],
                                          row['longeur_champs'], 'ville', location.latitude, location.longitude])

                else:
                    print('not found')
                    writing_in(out_file, [row['id'], row['Adresse'], row['Ville'], row['N_Police'], row['Coord Z'], row['longeur_champs'], 'not_found', row['x'], row['y']])