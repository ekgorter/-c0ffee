################################################### Header #############################################################
#
# Heuristieken 2015 Universiteit van Amsterdam
#
# Namen: Elias Gorter, Kirsten de Wit, Sangeeta van Beemen
#
# Case: Kaartkleuren (Harmony Search Algoritme)
#
# Omschrijving: Drie landkaarten en drie sociale netwerken dienen met zo min mogelijk kleuren ingekleurd te worden,
#               waarbij aangrenzende landen of nodes niet dezelfde kleur mogen hebben.
#
# Algoritme: Harmony Search Algoritme. Er wordt een geheugen bijgehouden van een bepaalde grootte (HMS) met daarin de
#            oplossingen met de hoogste fitheidsscore. De fitheidsscore is gebaseerd op het aantal conflicten, hoe lager
#            hoe beter. Voor iedere in te kleuren eenheid bestaat de kans (HMCR) dat er een kleur wordt gekozen die de
#            eenheid had in een van de oplossingen in het geheugen. Anders wordt er random een beschikbare kleur
#            gekozen. Als er een kleur wordt gekozen uit het geheugen, bestaat de kans (PAR) dat deze nog wordt
#            aangepast. Aan de volledige inkleuring wordt een fitheidsscore toegekend; als deze beter is dan de
#            slechtste in het geheugen, dan wordt deze in plaats daarvan in het geheugen geplaatst. Als er een oplossing
#            met fitheidsscore 0 wordt gevonden, dan is een optimale oplossing gevonden.
#
# Invoer: Een csv bestand waarbij de eerste kolom bestaat uit de nodes van de graaf, gevolgd door de nodes waarmee
#         deze nodes zijn verbonden (bv. 1,4,33,78 <- node = 1 - verbonden met 4,33,78).
#
########################################################################################################################

############################################ Invoerdata #################################################

# Vul hier het te lezen csv bestand in.
csvBestand = '/Users/Elias/Documents/Programmeren/Programmeertheorie/test.csv'

# Aantal te gebruiken kleuren.
kleuren = 4

# Max aantal ingekleurde vectors.
maxvectors = 6000000

# Harmony Memory Size (HMS).
HMS = 10

# Harmony Memory Consideration Rate (HMCR).
HMCR = 0.90

# Pitch Adjustment Rate (PAR).
PAR = 0.15

#################################### Harmony Search Algoritme #############################################

def main(csvBestand, kleuren, maxvectors, HMS, HMCR, PAR):

    # Alle in te kleuren landen in een tuple uit csv file gehaald.
    invoerlanden = invoerlanden_uit_csv(csvBestand)

    # Dictionary met voor elk land een tuple met de buurlanden van dat land, uit csv gehaald.
    connecties = connecties_uit_csv(csvBestand, invoerlanden)

    # Start tijdmeting.
    start_time = time.time()

    # Maakt connectie matrix uit gegevens csv bestand.
    matrix = connectie_matrix(invoerlanden, connecties)

    # Vult memory met opgegeven aantal random ingekleurde vectors.
    memory = vul_memory(HMS, invoerlanden)

    # Telt hoeveel vectors tot nu toe zijn ingekleurd.
    vectorcount = 0

    # Stop met kleuren wanneer het maximaal toegestane aantal in te kleuren vectors is bereikt.
    while vectorcount < maxvectors:

        # Genereer nieuwe vector, aan de hand van Harmony Search regels.
        nieuwevector = nieuwe_vector(invoerlanden, HMS, memory, HMCR, PAR, kleuren)

        # Tel aantal gemaakte vectors.
        vectorcount += 1

        # Als nieuwe vector beter is dan slechtste uit geheugen, vervang deze dan.
        vervang_memory(nieuwevector, memory, matrix)

        # Als optimaal ingekleurde kaart is gevonden.
        if vector_score(nieuwevector, matrix) == 0:

            # Geef optimale inkleuring kaart.
            print 'kaart oplossing: ', nieuwevector

            # Stop het algoritme.
            break

    # Stop tijdmeting.
    runtime = (time.time() - start_time)

    # Laat zien hoeveel ingekleurde kaarten nodig waren om oplossing te vinden.
    print 'aantal ingekleurde vectors: ', vectorcount

    print 'runtime:', runtime

######################################### Libraries #############################################

# Library om csv files te lezen.
import csv

# Library om random getallen te genereren.
import random

# Library om runtime te berekenen.
import time

######################################### Functies ##############################################

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

# Functie om connectie matrix te maken van kaart of netwerk.
def connectie_matrix(invoerlanden, connecties):

    # De te vullen matrix (2-dimensionale array)
    matrix = []

    # Vult de rijen van de matrix.
    for i in range(len(invoerlanden)):

        # Lijst voor iedere rij van matrix.
        temp = []

        # Vult de kolommen van de matrix.
        for j in range(len(invoerlanden)):

            # Als de huidige rij en kolom aan elkaar grenzen, zet dan een 1 neer.
            if invoerlanden[j] in connecties[i + 1]:

                temp.append(1)

            # Zet anders een 0 neer (als ze niet aan elkaar grenzen).
            else:

                temp.append(0)

        # Voeg deze rij aan de matrix toe.
        matrix.append(temp)

    # Returnt de matrix.
    return matrix

# Functie om random vector te maken.
def random_vector_maken(invoerlanden):

    # De te vullen vector.
    vector = []

    # Vult de vector met een random waarde tussen 1 en 4 (inclusief) voor ieder land.
    for i in range(len(invoerlanden)):

        vector.append(random.randrange(1, kleuren + 1))

    # Returnt de vector
    return vector

# Functie om memory te vullen met random vectors.
def vul_memory(HMS, invoerlanden):

    # List met alle random ingekleurde vectors.
    memory = []

    # Vult de memory met random ingekleurde vectors t/m het opgegeven aantal.
    for vector in range(HMS):

        memory.append(random_vector_maken(invoerlanden))

    # Returnt het gevulde memory.
    return memory

# Functie om nieuwe vector te genereren, met kans op gebruik van geheugen en pitch aanpassing.
def nieuwe_vector(invoerlanden, HMS, memory, HMCR, PAR, kleuren):

    # De te vullen vector.
    vector = []

    # Geeft iedere regio in de vector een kleur, random of met gebruik van geheugen/pitch aanpassing.
    for regio in range(len(invoerlanden)):

        # Bepaalt of kleur uit geheugen wordt gekozen.
        if random.random() < HMCR:

            # Random kleur uit geheugen.
            kleur = memory[random.randrange(HMS)][regio]

            # Kans op pitch aanpassing.
            kleur = pitch_aanpassing(kleur, PAR, kleuren)

            # Geef regio in vector deze kleur.
            vector.append(kleur)

        # Als geen kleur uit het geheugen wordt gekozen, dan wordt een random kleur gegeven.
        else:

            vector.append(random.randrange(1, kleuren + 1))

    # Returnt de vector
    return vector

# Functie om te bepalen of pitch wordt aangepast, en in welke richting.
def pitch_aanpassing(kleur, PAR, kleuren):

    # Bepaalt of pitch wordt aangepast, aan de hand van pitch aanpassings ratio.
    if random.random() < PAR:

        # Keuzemogelijkheden voor aanpassen naar links of naar rechts.
        keuze = ('links', 'rechts')

        # Wanneer naar rechts wordt gekozen.
        if random.choice(keuze) == 'rechts':

            # Schuif een kleur naar rechts.
            kleur += 1

            # Als je niet verder naar rechts kunt, schuif dan helemaal naar links.
            if kleur == kleuren + 1:

                kleur = 1

        # Wanneer naar links wordt gekozen.
        else:

            # Schuif een kleur naar links.
            kleur -= 1

            # Als je niet verder naar links kunt, schuif dan helemaal naar rechts.
            if kleur == 0:

                kleur = kleuren

    # Returnt eventueel aangepaste kleur.
    return kleur

# Functie om score toe te kennen aan een vector, hoe lager de score hoe beter.
def vector_score(vector, matrix):

    # Uiteindelijke score.
    score = 0

    # Itereert over helft matrix.
    k = 0

    for i in range(len(matrix)):

        for j in range(k, len(matrix)):

            # Als landen aan elkaar grenzen.
            if matrix[i][j] == 1:

                # Als deze landen dezelfde kleur hebben.
                if vector[i] == vector[j]:

                    # Verhoog de score met 1.
                    score += 1

        # Zorgt ervoor dat over de helft van de matrix wordt geitereerd, zodat alle grenzen slechts 1 keer worden gecheckt.
        k += 1

    # Returnt score
    return score

# Functie berekent (een van) de vector(s) in het geheugen met de slechtste score.
def slechtste_in_memory(memory, matrix):

    # List met alle scores voor de vectors in de memory.
    scores = []

    # Berekent de score voor iedere vector in de memory en zet deze in scores.
    for vector in range(HMS):

        scores.append(vector_score(memory[vector], matrix))

    # Geeft de vector uit het geheugen met (een van) de hoogste score(s) uit de lijst met scores.
    for score in range(HMS):

        if scores[score] == max(scores):

            return score

            # Zorgt dat er maar 1 vector met hoogste score wordt gereturnd, als er meerdere zijn.
            break

# Functie om nieuw ingekleurde vector in memory te plaatsen als deze beter is dan de slechtste in de memory.
def vervang_memory(nieuwevector, memory, matrix):

    # Als de nieuwe vector beter is dan de slechtste uit de memory, vervang deze slechtste dan met de nieuwe vector.
    if vector_score(nieuwevector, matrix) < vector_score(memory[slechtste_in_memory(memory, matrix)], matrix):

        memory.remove(memory[slechtste_in_memory(memory, matrix)])
        memory.append(nieuwevector)

# Voert main uit.
if __name__ == '__main__':
    main(csvBestand, kleuren, maxvectors, HMS, HMCR, PAR)