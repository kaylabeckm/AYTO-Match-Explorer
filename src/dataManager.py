import csv

nodes = {}
edges = {}
weeks = {}
beams = {}
couples = {}
noMatches = []
confirmedMatches = []
perfectMatches = []
perfectMatchRemovals = {}

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

def loadPerfectMatches():
    with open('res/AYTO-perfectMatches.csv', newline='') as csvPerfectMatch:
        perfectMatchReader = csv.reader(csvPerfectMatch, delimiter=',', quotechar='|')
        next(perfectMatchReader)
        for row in perfectMatchReader:
            pair = (row[0], row[1])
            confirmedMatches.append(pair)


def blackout(matchList):
    localMatches = matchList.copy()
    findContributorsToBlackout(localMatches)
    for doomedPair in localMatches:
        if(doomedPair in perfectMatches):
            print('ERROR REMOVE PERFECT MATCH: these couples cannot all be Perfect Matches')
        addNoMatch(doomedPair)

def fixOverlappingMatches(perfectMatch):
    for couple in couples:
            for partner in perfectMatch:
                if(couple[0] == partner):
                    if(couple != perfectMatch):
                        addNoMatch(couple)
                        perfectMatchRemovals[perfectMatch].append(couple)
                if(couple[1] == partner):
                    if(couple != perfectMatch):
                        addNoMatch(couple)
                        perfectMatchRemovals[perfectMatch].append(couple)

    for week in weeks:
        #print(str(perfectMatch) + str(beams[week]) + ", " + str(len(weeks[week])))
        if (len(weeks[week]) < int(beams[week])):
            print('ERROR FIX OVERLAPPING: these couples cannot all be Perfect Matches')

def addNoMatch(pair):
    noMatches.append(pair)
    removeWeeklyMatch(pair)

def removeWeeklyMatch(pair):
    weekList = couples[pair]
    for week in weekList:
        if(pair in weeks[week]):
            weeks[week].remove(pair)

def reverseMatchRemovals(reversedPair):
    for savedPair in perfectMatchRemovals[reversedPair]:
        if(savedPair in noMatches):
            noMatches.remove(savedPair) #removes only one occurence of the pair in noMatches
            for matchedWeek in couples[savedPair]:
                if (savedPair not in weeks[matchedWeek]):
                    if (matchedWeek in couples[reversedPair]):
                        weeks[matchedWeek].append(savedPair)
    perfectMatchRemovals[reversedPair] = []

def findContributorsToBlackout(matchList):
    for otherPair in perfectMatches:
        for week in couples[otherPair]:
            if(beams[week] == 0):
                perfectMatchRemovals[otherPair].extend(matchList)

def addPerfectMatch(pair):
    matchedWeeks = couples[pair]

    if(pair not in perfectMatches):
        perfectMatches.append(pair)
    if(pair not in perfectMatchRemovals.keys()):
        perfectMatchRemovals[pair] = []

    fixOverlappingMatches(pair)
    for week in matchedWeeks:
        weeks[week].remove(pair)
        
        beamNum = beams[week]
        if(type(beamNum) is str):
            beamNum = int(beams[week])
        beams[week] = beamNum - 1
        if(beams[week] == 0):
            perfectMatchRemovals[pair].extend(weeks[week])
            blackout(perfectMatchRemovals[pair])


def removePerfectMatch(pair):
    matchedWeeks = couples[pair]
    if(pair in perfectMatches):
        perfectMatches.remove(pair)
        reverseMatchRemovals(pair)
        
        for week in matchedWeeks:
            weeks[week].append(pair)

            beamNum = beams[week]
            if(type(beamNum) is str):
                beamNum = int(beams[week])
            beams[week] = beamNum + 1
