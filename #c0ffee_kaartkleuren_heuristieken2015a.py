################################################### Header #############################################################
#
# Heuristieken 2015 Universiteit van Amsterdam
#
# Namen: Elias Gorter, Kirsten de Wit, Sangeeta van Beemen
#
# Case: Kaartkleuren
#
# Omschrijving: Drie landkaarten en drie sociale netwerken dienen met zo min mogelijk kleuren ingekleurd te worden,
#               waarbij aangrenzende landen of nodes niet dezelfde kleur mogen hebben.
#
# Algoritme: Constructief, depth-first, compleet, is deterministisch, maakt gebruik van pruning en backtracking. De
#            invoer is een csv bestand. De volgorde van inkleuren is van landen/nodes met meeste aangrenzende landen/
#            nodes naar minste aangrenzende landen/nodes. De uitvoer bestaat uit een weergave van alle aangemaakte
#            objecten van class 'land' met de gegeven kleuren.
#
# Invoer: Een csv bestand waarbij de eerste kolom bestaat uit de nodes van de graaf, gevolgd door de nodes waarmee
#         deze nodes zijn verbonden (bv. 1,4,33,78 <- node = 1 - verbonden met 4,33,78).
#
################################################# Libraries ############################################################

# Library om csv files te lezen.
import csv

# Library om runtime te berekenen.
import time

# Library onderdeel om lijst te sorteren op basis van class instance attributes (= bv. Land.naam, Land.kleur, etc.).
from operator import attrgetter

######################################### Main - Kaartkleur Algoritme ##################################################

# Vul hier het te lezen csv bestand in.
csvBestand = '/Users/Elias/Documents/Programmeren/Programmeertheorie/c0ffee/kaart1_correct.csv'

# De te gebruiken kleuren.
kleuren = ["Rood", "Blauw", "Groen", "Geel"]

def main(csvBestand, kleuren):

    # Voer kaartkleur algoritme uit.
    kaartkleur_algoritme(csvBestand, kleuren)

################################################## Functies ############################################################

# Functie om in te voeren landen uit csv file op te slaan in tuple.
def invoerlanden_uit_csv(csvBestand):

    # Open het csv bestand.
    f = open(csvBestand)

    # Lees het csv bestand.
    csv_f = csv.reader(f)

    # List om landen in op te slaan.
    invoerlanden = []

    # Voeg de waarden uit de eerste kolom in de csv file toe aan de list.
    for row in csv_f:
        invoerlanden.append(int(row[0]))

    # Zet de list om in een tuple.
    invoerlanden = tuple(invoerlanden)

    # Sluit het bestand.
    f.close()

    # Returnt de tuple met landen.
    return invoerlanden

# Functie om dictionary met connecties per land te maken vanuit csv file.
def connecties_uit_csv(csvBestand, invoerlanden):

    # Opent de csv file.
    f = open(csvBestand)

    # Leest de csv file.
    csv_f = csv.reader(f)

    # Tijdelijke list waarin de buurlanden worden opgeslagen.
    temp = []

    # Laat de eerste kolom (de landen) buiten beschouwing, zodat de buurlanden overblijven.
    for row in csv_f:
        temp.append(row[1:])

    # List waarin de buurlanden per land als tuples worden opgeslagen.
    buurlanden = []

    # Zet de buurlanden lists om in tuples.
    for i in temp:
        temp2 = []
        for j in i:
            temp2.append(int(j))
        temp2 = tuple(temp2)
        buurlanden.append(temp2)

    # Dictionary waarin de buurlanden worden gekoppeld aan de landen.
    connecties = {}

    # Koppelt landen aan buurlanden.
    for i in invoerlanden:
        connecties[i] = buurlanden[i - 1]

    # Sluit csv bestand.
    f.close()

    # Returnt de dictionary met connecties.
    return connecties

# Functie om landen te "maken".
def landen_maken(invoerlanden, connecties):

    # Ieder land wordt dit type class waarin de eigenschappen van het land worden opgeslagen.
    # Naam en (aantal)buurlanden zijn gegeven, kleur moet nog worden bepaald.
    class Land:

        def __init__(self, naam, buurlanden, kleur, aantal_connecties):

            self.naam = naam
            self.buurlanden = buurlanden
            self.kleur = kleur
            self.aantal_connecties = aantal_connecties

        def __str__(self):
            return str((self.naam, self.buurlanden, self.kleur, self.aantal_connecties))

    # List om alle landen (van class Land) in op te slaan.
    landen = []

    # Maak voor ieder land een class Land aan en voer de gegeven informatie (naam, buurlanden en aantal connecties)
    # hierbij in. Voeg ieder land toe aan de list "landen".
    for i in range(len(invoerlanden)):
        landen.append(Land(invoerlanden[i], connecties[i+1], 'geen', len(connecties[i+1])))

    # Returnt de list met landen.
    return landen

# Functie om landen te sorteren op basis van aantal connecties.
def sorteer_landen(landen):

    # Sorteert de lijst met landen van hoog naar laag op basis van de aantal_connecties eigenschap.
    landen = sorted(landen, key = attrgetter('aantal_connecties'), reverse = True)

    # Returnt de gesorteerde lijst met landen.
    return landen

# Functie om de landen de juiste kleur te geven.
def landen_kleuren(landen, kleuren):

    # List waar resultaat in komt.
    result = []
    # Begin bij het eerste land in de landen list.
    i = 0
    # Houdt aantal backtracks bij.
    backtracks = 0

     # Itereert door ieder land.
    while i in range(len(landen)):

        # Voor ieder land wordt een tijdelijke kopie gemaakt van de lijst met kleuren
        temp = list(kleuren)

        # Bij ieder land wordt door de tuple met de buurlanden van dat land geitereerd.
        for j in range(len(landen[i].buurlanden)):

            # Als een buurland een bepaalde kleur heeft wordt deze kleur uit de tijdelijke
            # kleuren list verwijderd.
            try:
                temp.pop(temp.index([land for land in landen if land.naam == landen[i].buurlanden[j]][0].kleur))

            # Als een buurland nog geen kleur heeft, of de kleur is al verwijderd, doe dan niks.
            except ValueError:
                "Do nothing"

        # Als het huidige land al een kleur heeft, verwijder dan alle kleuren t/m deze kleur uit de kleuren list.
        if landen[i].kleur != 'geen':
            tempindex = temp.index(landen[i].kleur) + 1
            del temp[:tempindex]

        # Dit land krijgt de eerst mogelijke kleur die nog over is in de tijdelijke kleuren list.
        try:
            landen[i].kleur = temp[0]

            # Voeg land toe aan result list.
            result.append(landen[i])

            # Ga naar volgende land.
            i += 1

        # Als er geen kleuren meer mogelijk zijn.
        except IndexError:
            # Als er helemaal naar het eerste land gebacktrackt is, en daar zijn geen kleuren meer mogelijk.
            if i == 0:
                return ["Geen oplossing mogelijk"], backtracks

            # Verwijder de kleur van het huidige land, als deze al een kleur heeft.
            if landen[i].kleur != 'geen':
                landen[i].kleur = 'geen'

            # Ga naar het vorige land (backtrack).
            i -= 1

            # Houdt aantal backtracks bij.
            backtracks += 1

    # Returnt list met landen
    return result, backtracks

# Haalt landen die dubbel in de resultaten lijst staan uit die lijst.
def verwijder_duplicaten(resultaat):
    seen = set()
    seen_add = seen.add
    return [ x for x in resultaat if not (x in seen or seen_add(x))]

# Voert alle functies uit en toont resultaat.
def kaartkleur_algoritme(csvBestand, kleuren):

    # Start tijdmeting.
    start_time = time.time()

    # Alle in te kleuren landen/nodes in een tuple uit csv file gehaald.
    invoerlanden = invoerlanden_uit_csv(csvBestand)

    # Dictionary met voor elk land/node een tuple met de buurlanden/nodes van dat land/node, uit csv gehaald.
    connecties = connecties_uit_csv(csvBestand, invoerlanden)

    # Maakt de landen/nodes van de class Land met naam en connecties, nog zonder kleur.
    landen = landen_maken(invoerlanden, connecties)

    # Sorteert landen/nodes op aantal connecties van hoog naar laag.
    landen = sorteer_landen(landen)

    # Kleurt de landen/nodes in.
    resultaat, backtracks = landen_kleuren(landen, kleuren)

    # Stop tijdmeting.
    runtime = (time.time() - start_time)

    # Haalt landen die dubbel in de resultaten lijst staan uit die lijst.
    resultaat = verwijder_duplicaten(resultaat)

    # Toont ieder land in de terminal.
    print 'Result:'
    for i in range(len(resultaat)):
        print resultaat[i]

    # Toont runtime in terminal.
    print 'Runtime:'
    print runtime, 'seconds'

    # Toont aantal backtracks in terminal.
    print 'Backtracks:'
    print backtracks

# Voert main uit.
if __name__ == '__main__':
    main(csvBestand, kleuren)