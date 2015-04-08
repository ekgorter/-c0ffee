__author__ = 'Elias'

landen = (1, 2, 3, 4, 5)

connecties = {1: (2, 3, 4, 5), 2: (1, 3), 3: (1, 2, 4), 4: (1, 3, 5), 5: (1, 4)}

kleur = ["Rood", "Blauw", "Groen", "Geel"]

resultaat = {1: "Geen", 2: "Geen", 3: "Geen", 4: "Geen", 5: "Geen"}

temp = []
temp2 = 1

for land in landen:
    if land == 1:
        resultaat[temp2] = kleur[0]
    elif land != 1:
        buurlanden = connecties[land]
        for buurland in buurlanden:
            temp = kleur
            kleurland = resultaat[buurland]
            print kleurland
            print temp
            # Als het land er in voorkomt weghalen en anders niet
            for kleurland in temp:
                temp.remove(kleurland)
                print temp
            resultaat[temp2] = kleur[0]
            temp2 += 1
            print temp2

print resultaat




