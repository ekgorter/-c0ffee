__author__ = 'Elias'

############################# Libraries & Functies ############################

# Libraries voor maken en tekenen van graph.
import matplotlib.pyplot as plt
import networkx as nx

# Library om csv files te lezen.
import csv

# Library om kopieen van objecten (classes, lists, etc.) te kunnen maken.
import copy

# Library onderdeel om lijst te sorteren op basis van class instance attributes (= bv. Land.naam, Land.kleur, etc.).
from operator import attrgetter

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

# Functie om een dominerende set nodes te vinden.
def dominating_set(landen):

    # dset is de lijst die gevuld wordt met een dominating set, temp een kopie van de lijst met landen.
    dset = []
    temp = list(landen)

    # Gaat door totdat alle landen zijn verwerkt.
    while len(temp) != 0:

        # Itereert door alle buurlanden van het eerste land in de temp lijst.
        for i in range(len(temp[0].buurlanden)):

            # Maakt temp leeg en vult deze opnieuw met alle landen behalve de buurlanden van het eerste land uit de temp lijst.
            temp[:] = [land for land in temp if not land.naam == temp[0].buurlanden[i]]

        # Haalt het eerste land uit de temp lijst en stopt deze in de dset.
        dset.append(temp.pop(0))

    # Returnt de dset.
    return dset

# Functie om lijst zo te sorteren dat per dominerende node eerst alle buren kleuren krijgen.
def sorteer_per_dnode(dset, landen):

    # Bevat de lijst met landen op de nieuwe manier gesorteerd.
    newlist = []

    # Itereert door alle landen uit de dominerende set.
    for i in range(len(dset)):

        # Zet het huidige land uit de dominerende set in de nieuwe lijst.
        newlist.append(dset[i])

        # Itereert door alle buurlanden van het huidige land uit de dset.
        for j in range(len(dset[i].buurlanden)):

            # Zet de buurlanden van het huidige land uit de dset in de nieuwe lijst onder het huidige land van de dset.
            newlist.append(landen[landen.index([land for land in landen if land.naam == dset[i].buurlanden[j]][0])])

    # Returnt de lijst met de nieuwe volgorde.
    return newlist

#Functie om dominerende set nodes vooraan in gesorteerde lijst te zetten.
def insert_dset(landen, dset):

    # Haalt alle landen die in dset zitten uit de list met landen.
    for i in range(len(landen)):

        landen[:] = [land for land in landen if not land in dset]

    # Pakt steeds de laatste uit de dset en zet hem vooraan in de list met landen, tot dset leeg is.
    while len(dset) != 0:

        landen.insert(0, dset.pop())

    # Returnt de nieuwe list met landen.
    return landen

# Functie om de landen de juiste kleur te geven.
def landen_kleuren(landen, kleuren):

    # Kopie van list met landen.
    templanden = copy.deepcopy(landen)

    # List waar resultaat in komt.
    result = []

    # Ga door totdat alle landen een kleur hebben gekregen.
    while len(result) != len(templanden):

        # Itereert door ieder land.
        for i in range(len(templanden)):

            # Voor ieder land wordt een tijdelijke kopie gemaakt van de lijst met kleuren
            temp = list(kleuren)

            # Bij ieder land wordt door de tuple met de buurlanden van dat land geitereerd.
            for j in range(len(templanden[i].buurlanden)):

                # Als een buurland een bepaalde kleur heeft wordt deze kleur uit de tijdelijke
                # kleuren list verwijderd.
                try:
                    temp.pop(temp.index([land for land in templanden if land.naam == templanden[i].buurlanden[j]][0].kleur))

                # Als een buurland nog geen kleur heeft, of de kleur is al verwijderd, doe dan niks.
                except ValueError:
                    "Do nothing"

            # Dit land krijgt de eerst mogelijke kleur die nog over is in de tijdelijke kleuren list.
            try:
                templanden[i].kleur = temp[0]
                # Voeg land toe aan result list.
                result.append(templanden[i])

            # Als er geen kleuren meer mogelijk zijn.
            except IndexError:
                # Zet dit land vooraan in de list met landen, reset templanden en result en begin opnieuw.
                landen.insert(0, landen.pop(i))
                templanden = copy.deepcopy(landen)
                result = []

    # Returnt list met landen
    return result

# Functie om een geschikte invoer list te maken voor graph teken functie.
def graph_invoer(connecties):

    # List waarin geschikte invoer komt te staan.
    uitvoer = []

    # Maakt list van alle connecties in paren van 2 (van het type list ipv tuple).
    for i in range(len(connecties)):
        for j in range(len(connecties[i+1])):
            uitvoer.append([i+1, connecties[i+1][j]])

    # Maakt dubbele connecties gelijk in vorm, zodat ze makkelijk vergeleken kunnen worden.
    for i in uitvoer:
        if i[0] > i[1]:
            i[0], i[1] = i[1], i[0]

    # Tijdelijke list om dubbele connecties eruit te filteren.
    temp = []

    # Filtert dubbele connecties uit de list.
    for i in uitvoer:
        if i not in temp:
            temp.append(i)

    # Vervangt de list met dubbele connecties door de gefilterde list.
    uitvoer = temp

    # Tijdelijke list om connecties om te zetten in tuples.
    temp = []

    # Zet de connecties om in tuples.
    for i in uitvoer:
        temp.append((i[0], i[1]))

    # Zet de nieuwe tuple list in de uitvoer.
    uitvoer = temp

    # Returnt de list met connecties als tuples.
    return uitvoer

# Functie om graph te tekenen van ingevoerde connecties.
def draw_graph(graph, landen):

    # Haalt alle benodigde nodes uit ingevoerde connecties.
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # Maakt nieuwe graph aan.
    G = nx.Graph()

    # Maakt alle nodes.
    for node in nodes:
        G.add_node(node)

    # Maakt alle lijnen tussen nodes (connecties).
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # Dictionary met de kleur die ieder land moet krijgen.
    kleuren = {}

    # Vult de kleuren dictionary met de kleuren die het kaartkleur algoritme heeft gegeven.
    for i in range(len(landen)):
        kleuren[landen[i].naam] = landen[i].kleur

    # Bepaalt voor iedere node welke kleur-key ze krijgen.
    for node in G.nodes():
        G.node[node]['category'] = kleuren[node]

    # Koppelt de kleur-key aan de kleurcode die de node een kleur geeft.
    color_map = {'Rood':'r', 'Blauw':'b', 'Groen':'g', 'Geel':'y'}

    # Tekent de graph met de gegeven kleuren.
    nx.draw(G, node_color=[color_map[G.node[node]['category']] for node in G])

    # Laat de graph zien op je scherm.
    plt.show()


############################ Invoerdata #################################

# LET OP: Op dit moment werkt de graph teken functie alleen wanneer de uitkomst
#           van het kaartkleur algoritme handmatig wordt ingevoerd.

# Vul hier het te lezen csv bestand in.
csvBestand = '/Users/Elias/Documents/Programmeren/Programmeertheorie/kaart3.csv'

# Alle in te kleuren landen in een tuple uit csv file gehaald.
invoerlanden = invoerlanden_uit_csv(csvBestand)

# Dictionary met voor elk land een tuple met de buurlanden van dat land, uit csv gehaald.
connecties = connecties_uit_csv(csvBestand, invoerlanden)

# De te gebruiken kleuren.
kleuren = ["Rood", "Blauw", "Groen", "Geel", "Paars"]


########################### Aanroepen functies ###############################

# Maakt de landen van de class Land met naam en connecties, nog zonder kleur.
landen = landen_maken(invoerlanden, connecties)

# Sorteert landen op aantal connecties van hoog naar laag.
landen = sorteer_landen(landen)

# Haalt een dominating set uit de lijst met landen.
dset = dominating_set(landen)

for i in range(len(dset)):
    print dset[i]

# Sorteert de lijst zodat per dominerende node eerst alle buren worden gekleurd.
#landen = sorteer_per_dnode(dset, landen)

# Zet de dominating set vooraan in de landenlijst.
#landen = insert_dset(landen, dset)

# Geeft de landen een kleur
resultaat = landen_kleuren(landen, kleuren)

# Toont ieder land in de terminal.
for i in range(len(resultaat)):
    print resultaat[i]

# Maakt de connecties dictionary geschikt om in te voeren in de graph teken functie.
#graphInvoer = graph_invoer(connecties)

# Tekent een graph
#draw_graph(graphInvoer, resultaat)