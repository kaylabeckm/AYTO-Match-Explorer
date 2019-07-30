import dataManager

def init():
    dataManager.loadData()

def getNodes():
    return dataManager.nodes

def getName(id):
    return dataManager.nodes[id]

def getBeams():
    return dataManager.beams

def getMatchesPerWeek():
    return dataManager.weeks

def getCumulativeCouples():
    return dataManager.couples

def getNoMatches():
    return dataManager.noMatches

def getPerfectMatches():
    return dataManager.perfectMatches

def togglePerfectMatch(pair):
    matches = getPerfectMatches()
    if(pair in matches):
        dataManager.removePerfectMatch(pair)
        return False
    else:
        dataManager.addPerfectMatch(pair)
        return True