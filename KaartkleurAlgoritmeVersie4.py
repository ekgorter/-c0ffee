__author__ = 'Elias'

############################# Libraries & Functies ############################

# Libraries voor maken en tekenen van graph.
import matplotlib.pyplot as plt
import networkx as nx

# Library om csv files te lezen.
import csv

from operator import itemgetter, attrgetter, methodcaller

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

    # Maak voor ieder land een class Land aan en voer de gegeven informatie (naam en buurlanden)
    # hierbij in. Voeg ieder land toe aan de list "landen".
    for i in range(len(invoerlanden)):
        landen.append(Land(invoerlanden[i], connecties[i+1], 'geen', len(connecties[i+1])))

    # Returnt de list met landen.
    return landen

# Functie om landen te sorteren op basis van aantal connecties.
def sorteer_landen(landen):

    # Sorteert de lijst met landen van hoog naar laag op basis van de aantal_connecties eigenschap.
    landen = sorted(landen, key=attrgetter('aantal_connecties'), reverse = True)

    # Returnt de gesorteerde lijst met landen.
    return landen

# Functie om de landen de juiste kleur te geven.
def landen_kleuren(landen, kleuren):

    # Itereert door ieder land.
    for i in range(len(landen)):

        # Voor ieder land wordt een tijdelijke kopie gemaakt van de lijst met kleuren
        temp = list(kleuren)

        # Bij ieder land wordt door de tuple met de buurlanden van dat land geitereerd.
        for j in range(len(landen[i].buurlanden)):

            # Als een buurland een bepaalde kleur heeft wordt deze kleur uit de tijdelijke
            # kleuren list verwijderd.
            try:
                temp.pop(temp.index(landen[landen[i].buurlanden[j] - 1].kleur))

            # Als een buurland nog geen kleur heeft, of de kleur is al verwijderd, doe dan niks.
            except ValueError:
                "Do nothing"

        # Dit land krijgt de eerst mogelijke kleur die nog over is in de tijdelijke kleuren list.
        landen[i].kleur = temp[0]

    # Returnt list met landen
    return landen

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
csvBestand = '/Users/Elias/Documents/Programmeren/Programmeertheorie/kaart2spiraal.csv'

# Alle in te kleuren landen in een tuple uit csv file gehaald.
invoerlanden = invoerlanden_uit_csv(csvBestand)

# Dictionary met voor elk land een tuple met de buurlanden van dat land, uit csv gehaald.
connecties = connecties_uit_csv(csvBestand, invoerlanden)

# De te gebruiken kleuren.
kleuren = ["Rood", "Blauw", "Groen", "Geel"]


########################### Aanroepen functies ###############################

# Maakt de landen van de class Land met naam en connecties, nog zonder kleur.
landen = landen_maken(invoerlanden, connecties)

# Sorteert landen op aantal connecties van hoog naar laag.
landen = sorteer_landen(landen)

# Geeft de landen een kleur
landen = landen_kleuren(landen, kleuren)

# Toont ieder land in de terminal.
for i in range(len(landen)):
    print landen[i]

# Maakt de connecties dictionary geschikt om in te voeren in de graph teken functie.
#graphInvoer = graph_invoer(connecties)

# Tekent een graph
#draw_graph(graphInvoer, landen)



