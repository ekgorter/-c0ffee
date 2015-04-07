__author__ = 'Elias'

landen = (1, 2, 3, 4, 5)

connecties = {1: (2, 3, 4, 5), 2: (1, 3), 3: (1, 2, 4), 4: (1, 3, 5), 5: (1, 4)}

kleur = ["Rood", "Blauw", "Groen", "Geel"]

resultaat = {1: "Geen", 2: "Geen", 3: "Geen", 4: "Geen", 5: "Geen"}


temp = []

for land in landen:
    if land == 1:
        resultaat[1] = kleur[0]

print resultaat




