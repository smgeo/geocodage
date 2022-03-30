import csv, time, json
import urllib.request

key = "AuBp6_arenVona3ldJD7QRZD-jXIweopYVRIFbq3-y2wV4pSglccvP4fqQvEnXk_"
encodage = 'ANSI'
entry_file = "inputs/saham_g2.csv"
out_file = entry_file.replace('inputs', "outputs")
def getUrl(ville, adresse, key):
    return  ("http://dev.virtualearth.net/REST/v1/Locations?CountryRegion=MA&locality=" +ville +"&addressLine="+adresse+"&key="+key).replace(" ", "%20")

def writing_in(file, content):
    with open(file, 'a', newline='',  encoding=encodage) as csvfile:
        writer = csv.writer(csvfile, delimiter=';',   quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(content)

with open(entry_file, newline='', encoding=encodage) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    #writing_in(out_file, ['id', 'Adresse', 'Ville', 'N_Police', 'Coord Z', 'longeur_champs', 'geocoding_level', 'x', 'y', "nbr_geocode"])
    for row in reader:
        if(int(row['id']) > 47471):

            res = json.loads(urllib.request.urlopen(getUrl(row['Ville'], row['Adresse'], key)).read())  # .decode('utf-8')
            time.sleep(0.15)
            nbre = len(res["resourceSets"])
            print(res["resourceSets"][0]["resources"][0]["geocodePoints"][0]["coordinates"])
            coords = res["resourceSets"][0]["resources"][0]["geocodePoints"][0]["coordinates"]
            if(coords is not None):
                writing_in(out_file, [row['id'], row['Adresse'], row['Ville'], row['N_Police'], row['Coord Z'], row['longeur_champs'], 'adresse', coords[0], coords[1], nbre])
            else:
                print('not found')
                writing_in(out_file, [row['id'], row['Adresse'], row['Ville'], row['N_Police'], row['Coord Z'], row['longeur_champs'], 'not_found', row['x'], row['y'], "0"])


            #     print((location.latitude, location.longitude))
            #     writing_in(out_file, [row['id'], row['Adresse'], row['Ville'], row['N_Police'], row['Coord Z'], row['longeur_champs'], 'adresse', location.latitude, location.longitude])
            #
            # else:
            #     print("just ville :")
            #     location = geolocator.geocode(row['Ville'])
            #     if(location is not None):
            #         print((location.latitude, location.longitude))
            #         writing_in(out_file, [row['id'], row['Adresse'], row['Ville'], row['N_Police'], row['Coord Z'],
            #                               row['longeur_champs'], 'ville', location.latitude, location.longitude])
            #
            #     else:
            #         print('not found')
            #         writing_in(out_file, [row['id'], row['Adresse'], row['Ville'], row['N_Police'], row['Coord Z'], row['longeur_champs'], 'not_found', row['x'], row['y']])