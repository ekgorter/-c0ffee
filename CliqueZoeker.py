__author__ = 'Elias'

############################################# Libraries ###############################################

# Libraries voor maken en tekenen van graph.
import networkx as nx

# Library om csv files te lezen.
import csv

############################################ Functies ##################################################

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

# Functie om een geschikte invoer list te maken voor graph functies.
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

# Functie om maximale cliques te vinden.
def clique_zoeker(graph):

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

    # Zoekt naar alle cliques.
    clique = nx.find_cliques(G)

    # Plaatst alle gevonden cliques in een lijst.
    result = list(clique)

    # Haalt de grootste clique uit de lijst.
    result = max(result,key=len)

    # Returnt de grootste clique.
    return result

############################ Invoerdata #################################

# Vul hier het te lezen csv bestand in.
csvBestand = '/Users/Elias/Documents/Programmeren/Programmeertheorie/test.csv'

# Alle in te kleuren landen in een tuple uit csv file gehaald.
invoerlanden = invoerlanden_uit_csv(csvBestand)

# Dictionary met voor elk land een tuple met de buurlanden van dat land, uit csv gehaald.
connecties = connecties_uit_csv(csvBestand, invoerlanden)

########################### Aanroepen functies ###############################

# Maakt de connecties dictionary geschikt om in te voeren in de graph teken functie.
graphInvoer = graph_invoer(connecties)

# Geeft de grootste clique weer.
clique = clique_zoeker(graphInvoer)

print 'clique:', clique