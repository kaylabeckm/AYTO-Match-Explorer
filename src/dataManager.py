import csv

nodes = {}
edges = {}
weeks = {}
beams = {}
couples = {}
noMatches = []
perfectMatches = []

def loadData():
    with open('res/AYTO-NODES.csv', newline='') as csvNames:
        namesReader = csv.reader(csvNames, delimiter=',', quotechar='|')
        next(namesReader)
        for row in namesReader:
            nodes[row[0]] = row[1]

    with open('res/ATYO-noMatches.csv', newline='') as csvNoMatch:
        noMatchReader = csv.reader(csvNoMatch, delimiter=',', quotechar='|')
        next(noMatchReader)
        for row in noMatchReader:
            pair = (row[0], row[1])
            noMatches.append(pair)
            couples[pair] = []

    with open('res/AYTO-namedEDGES.csv', newline='') as csvEdges:
        matchesReader = csv.reader(csvEdges, delimiter=',', quotechar='|')
        next(matchesReader)
        week = 1
        weeks[week] = []
        for row in matchesReader:
            weekNum = int(row[2])
            if( weekNum not in beams):
                beams[weekNum] = row[3]
            p1 = row[0]
            p2 = row[1]
            if(p1>p2):
                p1 = row[1]
                p2 = row[0]
            
            if(weekNum != week):
                week += 1
                weeks[week] = []
            pair = (p1, p2)
            weeks[weekNum].append(pair)
            if(pair not in couples):
                couples[pair] = []
            couples[pair].append(weekNum)
    
    for pair in noMatches:
        removeWeeklyMatch(pair)
    for week in beams:
        if(int(beams[week]) == 0):
            blackout(weeks[week])

def blackout(matchList):
    localMatches = matchList.copy()
    for doomedPair in localMatches:
        if(doomedPair in perfectMatches):
            print('ERROR: these couples cannot all be Perfect Matches')
        addNoMatch(doomedPair)

def fixOverlappingMatches(perfectMatch):
    for couple in couples:
            for partner in perfectMatch:
                if(couple[0] == partner):
                    if(couple != perfectMatch):
                        addNoMatch(couple)
                if(couple[1] == partner):
                    if(couple != perfectMatch):
                        addNoMatch(couple)
    for week in weeks:
        #print(str(perfectMatch) + str(beams[week]) + ", " + str(len(weeks[week])))
        if (len(weeks[week]) < int(beams[week])):
            print('ERROR: these couples cannot all be Perfect Matches')

def addNoMatch(pair):
    noMatches.append(pair)
    removeWeeklyMatch(pair)

def removeWeeklyMatch(pair):
    weekList = couples[pair]
    for week in weekList:
        if(pair in weeks[week]):
            weeks[week].remove(pair)

def undoBlackout(week):
    blackoutList = []
    for couple in couples:
        if(week in couples[couple]):
            blackoutList.append(couple)
    for pair in blackoutList:
        if(pair not in perfectMatches):
            weeks[week].append(pair)


def addPerfectMatch(pair):
    matchedWeeks = couples[pair]

    if(pair not in perfectMatches):
        perfectMatches.append(pair)
        for week in matchedWeeks:
            weeks[week].remove(pair)
            
            beamNum = beams[week]
            if(type(beamNum) is str):
                beamNum = int(beams[week])
            beams[week] = beamNum - 1
            if(beams[week] == 0):
                blackout(weeks[week])

        fixOverlappingMatches(pair)

def removePerfectMatch(pair):
    matchedWeeks = couples[pair]
    if(pair in perfectMatches):
        perfectMatches.remove(pair)
        
        for week in matchedWeeks:
            weeks[week].append(pair)

            beamNum = beams[week]
            if(type(beamNum) is str):
                beamNum = int(beams[week])
            beams[week] = beamNum + 1
            if(beams[week] == 1):
                undoBlackout(week)