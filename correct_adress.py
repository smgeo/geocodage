# -*- coding: utf-8 -*-
import csv
encodage_file = "ANSI"
F_entree = "inputs/PR_atraite2.csv"
out_file = F_entree.replace('inputs', "outputs").replace(".csv", "_corr.csv")

# adresse_dict = {"N" : "",
#                 "etage" : ""}
ad = "adresse_si"  # nom de la collone de l'adresse
ad_c = "adresse_corrige"
abr_liste = [(" appartement ", " app "), ("apart", " app "),(" appt ", " app "),(" apt ", " app "),(" etg ", " etage "), (" etag ", " etage "),(" res ", " residence "), (" lot ", " lotissement "), (" bd ", " boulevard "), (" cr ", " commune "), (" rte ", " route "), (" av ", " avenue "), (" qu ", " quartier ")]
special_carct_list = [("°", " "), ("É", "E"), ("Â", "A"), ("È", "E"), ("é", "e"), ("-", " "), ("«", ""), ("»", ""), ("Î", "I"), ("/", ""), ("Ô", "O"), ("*", ""), (".", " "), ("Ï", "I"), ("'", ""),("è", "e"), (",", " ") ]
cle_liste = [" n " ," bp ", " app ", " etage ","complexe ", "immeuble " , "residence " , "rue ", "hay ", "quartier ","lotissement ", " boulevard ", " avenue ",  " douar ", " commune " ]


def special_carcter(addr):
    for ele in special_carct_list :
        addr = addr.replace(ele[0], ele[1])
    return addr

def replace_abr(addr):
    for ele in abr_liste:
        addr = addr.replace(ele[0], ele[1])
    return  addr


def getVille(addr):
    vl = addr.split(" ")[len(addr.split(" "))-1]
    vl1 = addr.split(" ")[len(addr.split(" "))-2]

    if( vl1.find("ain")>-1 or vl1.find("sidi")>-1 or vl1.find("ben")>-1 or vl1.find("beni")>-1 or vl1.find("el")>-1 or vl1.find("dar")>-1 or vl1.find("oulad")>-1 or vl1.find("ouled")>-1 or vl1.find("moulay")>-1 or vl1.find("mly")>-1 or vl1.find("oulad")>-1 or vl1.find("ait")>-1):
        ville = vl1+" "+vl
        return (addr.replace(ville, ""), ville)
    else:
        return (addr.replace(vl, ""), vl)

def last_extraction(cle, addresse):
    cats = cle_liste.copy()
    cats.remove(cle)
    #print("cle : "+cle)
    arm = addresse.split(cle)[1]
    #print("first arm : "+arm)
    for elem in cats:
        #print(elem)
        arm = arm.replace(elem, " # ")
        #print("transform : "+arm)
    print("last : "+arm)
    cat = arm.split("#")[0].replace(" de ", "").replace("urbaine", "").replace("rurale", "")
    # if(cle != " etage "):
    return (addresse.replace(cle+ arm.split("#")[0], " "), cat)
    # else :
    #     return (addresse.replace(arm.split("#")[0], " "), cat)

def get_categori(cle, addresse):
    if(addresse.find(cle) > -1):
        cats = cle_liste.copy()
        cats.remove(cle)

        if(cle == " etage "):
            etg = addresse.split(cle)[0].split(" ")
            if(etg [len(etg)-1].find("eme")>-1 or etg [len(etg)-1].find("er") >-1):
                etage_cat = etg [len(etg)-1]+" etage "
                print("etage_cat : "+etage_cat)
                return (addresse.replace(etage_cat, ""), etage_cat)
            else:
                return  last_extraction(cle, addresse)
        else :
            return last_extraction(cle, addresse)
    else:
        return (addresse, "")

def writing_in(file, content):
    with open(file, 'a', newline='',  encoding=encodage_file) as csvfile:
        writer = csv.writer(csvfile, delimiter=';',   quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(content)


def correction(addr):
    ladresse = []
    addr = replace_abr(special_carcter(addr).lower())
    if(len(addr.split(" "))>3):
        fct = getVille(addr)
        adresse_rest = fct[0]
        ville = fct[1]
        value = get_categori(" app ", adresse_rest)
        app_value = value[1]
        adresse_rest = value[0]

        value = get_categori(" etage ", adresse_rest)
        etage_value = value[1]
        adresse_rest = value[0]
        # ' n ' case use flag 0 or 1 to be used after as position to insert rest
        print("adresse rest after etage : "+adresse_rest)
        if(adresse_rest.find(' n ') > -1):
            flage = 1
        else:
            flage = 0
        clies = cle_liste.copy()
        clies.remove(" etage ")
        clies.remove(" app ")
        for elem in clies :
            value = get_categori(elem, adresse_rest)
            adresse_rest = value[0]
            if(value[1] != ""):
                ladresse.append(elem+value[1])
        if(adresse_rest != ""):
            #print("adresse rest non vide")
            ladresse.insert(flage, adresse_rest)
        return (" ".join(ladresse)+" "+ville, app_value, etage_value)

    else:
        return (addr, "", "")


with open(F_entree, newline='', encoding=encodage_file) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    titles = reader.fieldnames.copy()
    titles.append("app")
    titles.append("etage")
    writing_in(out_file, titles)
    champs = []
    for row in reader:
        for cl in reader.fieldnames:
            champs.append(row[cl])
        addresse_corr = correction(row[ad])
        champs.append(addresse_corr[1]) # to add app
        champs.append(addresse_corr[2])
        # to add etage
        champs[champs.index(row[ad_c])] = addresse_corr[0] #adding corrected adresse
        champs[champs.index(row["ville_corrige"])] = getVille(addresse_corr[0])[1]
        print(champs)
        writing_in(out_file, champs)
        champs = []
