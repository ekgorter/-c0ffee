__author__ = 'Elias'

# Alle in te kleuren landen in een tuple.
invoerlanden = (1, 2, 3, 4, 5)

# Dictionary met voor elk land een tuple met de buurlanden van dat land.
connecties = {1: (2, 3, 4, 5), 2: (1, 3), 3: (1, 2, 4), 4: (1, 3, 5), 5: (1, 4)}

# De te gebruiken kleuren.
kleuren = ["Rood", "Blauw", "Groen", "Geel"]

# Ieder land wordt dit type class waarin de eigenschappen van het land worden opgeslagen.
# Naam en buurlanden zijn gegeven, kleur moet nog worden bepaald.
class Land:

    def __init__(self, naam, buurlanden, kleur = 'geen'):

        self.naam = naam
        self.buurlanden = buurlanden
        self.kleur = kleur

    def __str__(self):
        return str((self.naam, self.buurlanden, self.kleur))

# List om alle landen (van class Land) in op te slaan.
landen = []

# Maak voor ieder land een class Land aan en voer de gegeven informatie (naam en buurlanden)
# hierbij in. Voeg ieder land toe aan de list "landen".
for i in range(len(invoerlanden)):
    landen.append(Land(invoerlanden[i], connecties[i+1]))

# Algoritme om landen te kleuren.
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

# Toont ieder land in de terminal.
for i in range(len(landen)):
    print landen[i]



# Code voor het tekenen van een graph:
# TO DO: Deze graph tekenfunctie moet nog gekoppeld worden aan het kaartkleur algoritme,
# heb nu de connecties en kleuren erin ge-hardcoded.

# Libraries voor maken en tekenen van graph.
import matplotlib.pyplot as plt
import networkx as nx

# Functie om graph te tekenen van ingevoerde connecties.
def draw_graph(graph):

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
    kleuren = {1: "rood", 2: "blauw", 3: "groen", 4: "blauw", 5: "groen"}

    # Bepaalt voor iedere node welke kleur-key ze krijgen.
    for node in G.nodes():
        G.node[node]['category'] = kleuren[node]

    # Koppelt de kleur-key aan de kleurcode die de node een kleur geeft.
    color_map = {'rood':'r', 'blauw':'b', 'groen':'g'}

    # Tekent de graph met de gegeven kleuren.
    nx.draw(G, node_color=[color_map[G.node[node]['category']] for node in G])

    # Laat de graph zien op je scherm.
    plt.show()

# De invoer voor de graph functie: tuples met daarin twee nodes die aan elkaar verbonden zijn.
graph = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (3, 4), (4, 5), (1, 4)]

# Aanroepen van de graph functie om een graph te maken.
draw_graph(graph)
