# -*- coding: ANSI -*-
import csv, time, json
import urllib.request

key = "AuBp6_arenVona3ldJD7QRZD-jXIweopYVRIFbq3-y2wV4pSglccvP4fqQvEnXk_"
encodage = 'ANSI'
entry_file = "inputs/PR_reste2.csv"
out_file = entry_file.replace('inputs', "outputs")
def getUrl(ville, adresse_brute, key):
    return  ("http://dev.virtualearth.net/REST/v1/Locations?CountryRegion=MA&locality=" +ville +"&addressLine="+adresse_brute+"&key="+key).replace(" ", "%20")

def writing_in(file, content):
    with open(file, 'a', newline='',  encoding=encodage) as csvfile:
        writer = csv.writer(csvfile, delimiter=';',   quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(content)

with open(entry_file, newline='', encoding=encodage) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    #writing_in(out_file, ['ogc_fid', 'adresse_brute', 'adressesite', 'ville_site', 'num_police', 'x', 'y', "nbr_geocode"])
    for row in reader:
        if(int(row['ogc_fid']) > 83203):

            res = json.loads(urllib.request.urlopen(getUrl(row['ville_site'], row['adressesite'], key)).read())  # .decode('utf-8')
            time.sleep(0.15)
            nbre = len(res["resourceSets"])
            print(res["resourceSets"][0]["resources"][0]["geocodePoints"][0]["coordinates"])
            coords = res["resourceSets"][0]["resources"][0]["geocodePoints"][0]["coordinates"]
            if(coords is not None):
                writing_in(out_file, [row['ogc_fid'], row['adresse_brute'],row['adressesite'], row['ville_site'], row['num_police'], coords[0], coords[1], nbre])
            else:
                print('not found')
                writing_in(out_file, [row['ogc_fid'], row['adresse_brute'], row['adressesite'] ,row['ville_site'], row['num_police'], row['x'], row['y'], "0"])

