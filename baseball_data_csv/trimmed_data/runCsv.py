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
            
playerStats = {} # playerId -> {yr: {stats}}
playerStatsKeys = ['G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB']
with open('Batting.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        yr = int(row['yearID'])
        if (yr < cutoffYr):
            continue
        yrStats = {}
        for k in playerStatsKeys:
            yrStats[k] = row[k]

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

        playerStats[playerId][yr][posKey] = row[posKey]


w = csv.writer(open("out.csv", "w"))
for key, val in playerStats.items():
    w.writerow([key, val])

