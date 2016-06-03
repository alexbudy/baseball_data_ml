import csv
from operator import itemgetter

cutoffYr = 1981 # inclusive

masterDict = {} # playerId -> {playerData}
masterKeys = ['birthYear', 'birthCountry', 'nameFirst', 'nameLast', 'nameGiven',
'weight', 'height', 'bats', 'debut', 'finalGame']
with open('Master.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if (len(row['finalGame']) < 4):
            continue
        yr = row['finalGame'].split('-')[0]
        if (int(yr) >= cutoffYr):
            playerData = {}
            for k in masterKeys:
                playerData[k] = row[k]
        masterDict[row['playerID']] = playerData
            
playerStats = {} # playerId -> {yr: {stats}}
playerStatsKeys = ['G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB']

# all integers in rows
def addStatRows(row1, row2):
    for k in playerStatsKeys:
        row1[k] += row2[k]

    return row1

with open('Batting.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        yr = int(row['yearID'])
        playerId = row['playerID']
        if (yr < cutoffYr):
            continue
        yrStats = {}
        invalidStatRow = False
        for k in playerStatsKeys:
            if (len(row[k]) == 0):
                invalidStatRow = True
                continue
            yrStats[k] = int(row[k])
        
        if (invalidStatRow):
            continue
        
        if ((int(row['stint']) > 1) and (playerId in playerStats) and (yr in playerStats[playerId])):
            prevRow = playerStats[playerId][yr]
            yrStats = addStatRows(prevRow, yrStats)
            

        if (playerId not in playerStats):
            playerStats[playerId] = {}

        playerStats[playerId][yr] = yrStats

fieldingKeys = ['E', 'InnOuts']
posKey = 'POS'
with open('Fielding.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        yr = int(row['yearID'])
        if (yr < cutoffYr):
            continue  
        playerId = row['playerID']
        pos = row[posKey]
        if (playerId not in playerStats or yr not in playerStats[playerId]):
            continue
        
        for k in fieldingKeys:
            fieldingStat = 0
            if (len(row[k]) > 0):
                fieldingStat = int(row[k])

            if (k in playerStats[playerId][yr]):
                playerStats[playerId][yr][k] += fieldingStat
            else:
                playerStats[playerId][yr][k] = fieldingStat

        masterDict[playerId][posKey] = pos

# this function creates a full csv data point row
# includes stats for the player, as well as the players physical stats
# trainingRows -> {yr : {}, yr2 : {}, ...}
def aggregateStats(playerId, trainingRows):
    yrStart = min(trainingRows.keys())
    yrEnd = max(trainingRows.keys())
    aggRow = {}
    for yr, statDict in trainingRows.iteritems():
        for statKey, stat in statDict.iteritems():
            if statKey in aggRow:
                aggRow[statKey] += stat
            else:
                aggRow[statKey] = stat 
    
    for statKey, val in aggRow.iteritems():
        aggRow[statKey] = val/len(trainingRows)

    aggRow['seasons'] = len(trainingRows)
    aggRow['latestAge'] = yrEnd - int(masterDict[playerId]['birthYear'])
    aggRow['weight'] = int(masterDict[playerId]['weight'])    
    aggRow['height'] = int(masterDict[playerId]['height'])    

    # second data point is last available year
    for k, val in trainingRows[yrEnd].iteritems():
        aggRow['last'+k] = val

    return aggRow

# this is the order for the csv file
dataPointsHeader = playerStatsKeys + fieldingKeys + ['seasons', 'latestAge', 'weight', 'height']
for k in playerStatsKeys:
    dataPointsHeader += ['last'+k]

def generateCSVData(dataWriter, labelsWriter, playerId, dataRows):
    sortedYrs = sorted(dataRows.keys()) 
    for idx in xrange(2, len(sortedYrs)+1):
        yrSubset = sortedYrs[0:idx] 
        subsetRows = {key: val for key, val in dataRows.items() if key in yrSubset}
        writeDataRowAndTrainingRow(dataWriter, labelsWriter, playerId, subsetRows)
        

# dataRows is 2 or more rows.  Last row is label row
def writeDataRowAndTrainingRow(dataWriter, labelsWriter, playerId, dataRows):
    yrStart = min(dataRows.keys())
    yrEnd = max(dataRows.keys())
    
    lastRow = dataRows.pop(yrEnd)

    aggStats = aggregateStats(playerId, dataRows)
    if (aggStats['AB'] < 50):  # too few at-bats over data set for significance
        return

    orderedAggStats = []
    for k in dataPointsHeader:
        if k not in aggStats:
            return
        orderedAggStats.append(aggStats[k])

    w.writerow(orderedAggStats)
    w_labels.writerow([lastRow['HR']])


w = csv.writer(open("data.csv", "w"))
w.writerow(dataPointsHeader)

w_labels = csv.writer(open("data_labels.csv", "w"))
w_labels.writerow(["actual_HR_count"])
for playerId, val in playerStats.items():
    if (len(val) < 2): # we need at least two rows (one test, one train)
        continue
    if ((posKey not in masterDict[playerId]) or masterDict[playerId][posKey] == 'P'): # no pitchers
        continue
    
    # at this point we can call aggregateStats to create a data row for a set of stat rows
    generateCSVData(w, w_labels, playerId, val)
    


