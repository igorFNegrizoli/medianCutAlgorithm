import math

def is_identical(list_a, list_b):
    if len(list_a) != len(list_b):
        return False
    for i in list_a:
        if i not in list_b:
            return False
    return True

def rTheyAllTheSame(group):
    aux = group[0]
    for i in group:
        if not is_identical(aux, i):
            return False
    return True

def getAmplitude(group, channel):
    minVal = 256
    maxVal = 0
    for i in group:
        if i[channel] > maxVal:
            maxVal = i[channel]
        if i[channel] < minVal:
            minVal = i[channel]
    return maxVal-minVal

def getmaiorAmplitude(group):
    greaterAmp = 0
    greaterCh = 0
    for i in range(3):
        aux = getAmplitude(group, i)
        if aux > greaterAmp:
            greaterAmp = aux
            greaterCh = i
    return greaterCh

def medianSplit(group, channel, limitQuantization):
    cutPos = math.floor(len(group)/2)
    group.sort(key=lambda x: x[channel])
    upCut = cutPos
    downCut = cutPos
    firstHalf = []
    secondHalf = []
    if downCut != 0:  
        while group[downCut-1][channel] == group[cutPos][channel]:
            downCut -= 1
            if downCut == 0:
                break
    if upCut+1 < (len(group)-1):
        while group[upCut+1][channel] == group[cutPos][channel]:
            upCut += 1
            if upCut == (len(group)-1):
                break
    if upCut == downCut:
        firstHalf = group[:cutPos]
        secondHalf = group[cutPos:]
    elif (cutPos - downCut) <= (upCut - cutPos):
        firstHalf = group[:downCut]
        secondHalf = group[downCut:]
    elif (upCut - cutPos) < (cutPos - downCut):
        firstHalf = group[:upCut+1]
        secondHalf = group[upCut+1:]
    else:
        print("Algo errado aconteceu na medianSplit")
        print(downCut, "  ", cutPos, "  ", upCut)

    return firstHalf, secondHalf

def medianCut(image, limitQuantization):
    group = []
    for i in image:
        for j in i:
            group.append(j)
    #para uma quantizacao de n bits setar limitQuantization em (2^n)-1
    groups = []
    groups.append(group)
    auxGroups = []
    globalLen = 1

    flag = True

    while flag:
        for i in groups:
            globalLen += 1
            if globalLen >= limitQuantization:
                auxGroups = groups[:]
                flag = False
                break
            if rTheyAllTheSame(i):
                auxGroups.append(i)
                continue
            if len(i) > 1:
                channel = getmaiorAmplitude(i)
                firstHalf = []
                secondHalf = []
                firstHalf, secondHalf = medianSplit(i, channel, limitQuantization)
                auxGroups.append(firstHalf)
                auxGroups.append(secondHalf)
            else:
                auxGroups.append(i)
        groups = auxGroups[:]
        auxGroups = []
        globalLen = len(groups)
        if globalLen >= limitQuantization:
            return groups
        if oneColorPerGroupCheck(groups):
            return groups
    return groups

def oneColorPerGroupCheck(groups):
    for i in groups:
        if not rTheyAllTheSame(i):
            return False
    return True 

def cmpColors(c1,c2):
    if len(c1) != len(c2):
        print("SHIT")
    for i in range(len(c1)):
        if c1[i] != c2[i]:
            return False
    return True

def isColorInList(color, group):
    for i in group: 
        if cmpColors(i,color):
            return True
    return False

def excludeRepeatedColors(group):
    aux = []
    for i in group:
        if not isColorInList(i,aux):
            aux.append(i)
    return aux

def tuple2list(tupla):
    lista = []
    for i in tupla:
        lista.append(i)
    return lista

def getRepresentative(group):
    freq = {}
    for i in group:
        if tuple(i) in freq.keys():
            freq[tuple(i)] += 1
        else:
            freq[tuple(i)] = 1
    maxOccur = 0
    representative = tuple(group[0])
    for i in freq.keys():
        if freq[tuple(i)] >= maxOccur:
            maxOccur = freq[tuple(i)]
            representative = tuple(i)
    representative = tuple2list(representative)
    return representative

def constructImage(groups, image):
    dicti = {}
    for i in groups:
        representative = getRepresentative(i)
        iAux = excludeRepeatedColors(i)
        for j in iAux:
            dicti[tuple(j)] = representative
    newImage = []
    for i in image:
        newImageRow = []
        for j in i:
            newImageRow.append(dicti[tuple(j)])
        newImage.append(newImageRow)
    return newImage