import csv


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
with open('Batting.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        yr = int(row['yearID'])
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
        
        if (int(row['stint']) > 1):
            prevRow = playerStats[row['playerID']][yr]
            for k in playerStatsKeys:
                prevRow[k] += yrStats[k]
            
            yrStats = prevRow

        if (row['playerID'] not in playerStats):
            playerStats[row['playerID']] = {}

        playerStats[row['playerID']][yr] = yrStats

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
        
        if ('InnOuts' in playerStats[playerId][yr]):
            playerStats[playerId][yr]['InnOuts'] += row['InnOuts']
        else:
            playerStats[playerId][yr]['InnOuts'] = row['InnOuts']

        if ('E' in playerStats[playerId][yr]):
            playerStats[playerId][yr]['E'] += row['E']
        else:
            playerStats[playerId][yr]['E'] = row['E']

        masterDict[playerId][posKey] = pos

# trainingRows -> {yr : {}, yr2 : {}, ...}
# testRow -> {yr : {}}
def aggregateStats(trainingRows, testRow):
    print(trainingRows)
    yrStart = min(trainingRows.keys())
    yrEnd = max(trainingRows.keys())
    aggRow = {}
    for yr, statDict in trainingRows.iteritems():
        print(yr)
        print(statDict)
        for statKey, stat in statDict.iteritems():
            if statKey in aggRow:
                aggRow[statKey] += stat
            else:
                aggRow[statKey] = stat 
    return aggRow

w = csv.writer(open("out.csv", "w"))
for key, val in playerStats.items():
    w.writerow([key, aggregateStats(val, None)])



