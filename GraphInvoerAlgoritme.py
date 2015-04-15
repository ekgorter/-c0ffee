__author__ = 'Elias'

def graph_invoer(connecties):

    uitvoer = []

    for i in range(len(connecties)):
        for j in range(len(connecties[i+1])):
            uitvoer.append([i+1, connecties[i+1][j]])

    for i in uitvoer:
        if i[0] > i[1]:
            i[0], i[1] = i[1], i[0]

    temp = []

    for i in uitvoer:
        if i not in temp:
            temp.append(i)

    uitvoer = temp

    temp = []

    for i in uitvoer:
        temp.append((i[0], i[1]))

    uitvoer = temp

    return uitvoer

connecties = {1: (2, 3, 4, 5), 2: (1, 3), 3: (1, 2, 4), 4: (1, 3, 5), 5: (1, 4)}

uitvoer = graph_invoer(connecties)

print uitvoer
