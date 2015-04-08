__author__ = 'Elias'

landen = (1, 2, 3, 4, 5)

connecties = {1: (2, 3, 4, 5), 2: (1, 3), 3: (1, 2, 4), 4: (1, 3, 5), 5: (1, 4)}

kleur = ["Rood", "Blauw", "Groen", "Geel"]

resultaat = {1: "Geen", 2: "Geen", 3: "Geen", 4: "Geen", 5: "Geen"}

temp = []
land = 1

for land in landen:
    if land == 1:
        resultaat[land] = kleur[0]
    elif land != 1:
        buurlanden = connecties[land]
        for buurland in buurlanden:
            temp = kleur
            kleurlanden = resultaat[buurland]
            # print kleurlanden
            # print temp
            # Als de kleur in de lijst voorkomt weghalen en anders niet
            if temp == kleurlanden:
                temp.remove(kleurlanden)
            # print temp
        resultaat[land] = temp[0]
    land += 1
        #print temp2

print resultaat




