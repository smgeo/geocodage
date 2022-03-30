import csv, time, random
from geopy.geocoders import Nominatim

entry_file = "C:/Users/k43773/Documents/parawork/cat/axa_test1.csv"
out_file = ""


with open(entry_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        geolocator = Nominatim(user_agent="tast"+str(random.random()))
        print(row['adresse']+" "+row['Nom_ville']+" "+row['Pays'])
        location = geolocator.geocode(row['adresse']+" "+row['Nom_ville']+" "+row['Pays'])
        time.sleep(1.2)
        if(location is not None):
            print((location.latitude, location.longitude))
        else:
            print("just ville :")
            location = geolocator.geocode(row['Nom_ville']+" "+row['Pays'])
            if(location is not None):
                print((location.latitude, location.longitude))
            else:
                print('not found')