import datetime
import copy

class ballot:
    def __init__(self, seat : str, preferences : list):
        self.seat = seat
        self.preferences = preferences

    def getVote(self, n):
        '''returns a candidate'''
        #get first
        return self.preferences[n]

    def applyVote(self):
        cand = self.getVote(0)
        #print('applying vote to', cand.getName())
        cand.addVote(self.seat, self)
    
    def popVote(self):
        self.preferences.pop(0)

    def getSeat(self):
        return self.seat





class candidate:
    def __init__(self, name : str, positionsApplied : list):
        self.name = name
        self.positionsApplied = {}

        for position in positionsApplied:
            self.positionsApplied[position] = []


    
    def getName(self):
        return self.name

    def addVote(self, position, ballot):
        #print(self.name, "adding vote")
        if position in self.positionsApplied:
            self.positionsApplied[position].append(ballot)


    def transferVotes(self, position, quota):
        if position in self.positionsApplied:
            for b in self.positionsApplied[position]:
                
                b.popVote()
                b.applyVote()
    

    def getPositionsApplied(self):
        return self.positionsApplied


    def tallyVotes(self, position):
        if position in self.positionsApplied:
            #print("look at me:" , (self.positionsApplied[position]))
            return len(self.positionsApplied[position])
        
        return 0
        




class election:
    def __init__(self, candidateList, rolesList, needToWin, ballotsList):
        self.roles = {}
        self.check = needToWin
        self.ballotsList = ballotsList
        self.candidateList = candidateList
        for r in rolesList:
            self.roles[r] = []

        for c in candidateList:
            #print("adding", c.getName(), c.getPositionsApplied())
            for p in c.getPositionsApplied():
                self.roles[p].append(c)
  


    def getBallots(self, seat):
        return [i for i in self.ballotsList if i.getSeat() == seat]
   

    def getCandidate(self,name):
        for c in self.candidateList:
            if c.getName() == name:
                return c
    

    def removeCandidate(self, c, position, quota):
        #print(self.roles[position])
        if c in self.roles[position]:
            c.transferVotes(position, quota)
            self.roles[position].remove(c)


    def applyVotes(self,ballotList):
        for i in ballotList:
            i.applyVote()


    def tally(self, position, exclusionList):
        quota = self.check[position]
        print('quota is',quota)
        print()

        ballots = self.getBallots(position)
        self.applyVotes(ballots)

        for c in exclusionList:
            self.removeCandidate(c, position, quota)
            #print('removing', c.getName())

    

        maxCandidate = self.roles[position][0]

        maxVotes = maxCandidate.tallyVotes(position)
        minCandidate = self.roles[position][0]
        minVotes = maxVotes

        
        while (maxVotes < quota and len(self.roles[position]) > 1):

            #print(self.roles[position])
            maxCandidate = self.roles[position][0]

            maxVotes = maxCandidate.tallyVotes(position)
            minCandidate = self.roles[position][0]
            minVotes = maxVotes


            for c in self.roles[position]:
                votes = c.tallyVotes(position)
                print(c.getName(), 'has', votes)

                if (votes > maxVotes):
                    maxVotes = votes
                    maxCandidate = c
                
                if (votes < minVotes):
                    minVotes = votes
                    minCandidate = c
            
            if (maxVotes < quota):
                #print('removing', minCandidate.getName())
                self.removeCandidate(minCandidate, position, quota)
                print("\n\n\n")
            
        print("the", position, "of Co-op soc ", 2020 + 1, "is", maxCandidate.getName(), "with", maxVotes)




orange = candidate('orange', ['pres'])
pear = candidate('pear', ['pres'])
choc = candidate('choc', ['pres'])
straw = candidate('straw', ['pres'])
burg = candidate('burg', ['pres'])
ph = candidate('ph', [])            
n2w = {'pres' : 6}
rolesList = ['pres']
ballotList = []
for i in range(4):
    b = ballot('pres', [orange, ph,ph,ph,ph])
    ballotList.append(b)

for i in range(2):
    b = ballot('pres', [pear, orange,ph,ph,ph])
    ballotList.append(b)

for i in range(2):
    b = ballot('pres', [choc, straw, ph,ph,ph])
    ballotList.append(b)


for i in range(3):
    b = ballot('pres', [choc, burg,ph,ph,ph])
    ballotList.append(b)

b = ballot('pres', [straw, ph,ph,ph,ph])
ballotList.append(b)
b = ballot('pres', [burg, ph,ph,ph,ph])
ballotList.append(b)


candidateList = [orange, pear, choc, straw, burg, ph]
e = election(candidateList, rolesList, n2w, ballotList)
#print(choc.positionsApplied['pres'])

e.tally('pres', [])

#ian Ng: i'm applying for pres, vp, arc
#{ian ng : [roles]}





