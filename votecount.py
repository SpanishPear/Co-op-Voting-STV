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
        self.votes = 0

        for position in positionsApplied:
            self.positionsApplied[position] = []


    
    def getName(self):
        return self.name

    def addVote(self, position, ballot):
        #print(self.name, "adding vote")
        if position in self.positionsApplied:
            self.positionsApplied[position].append(ballot)


    def transferAdd(self, numVotes):
        #print('i', self.getName(), 'have', self.votes)

        self.votes += numVotes
        #print('i', self.getName(), 'now have', self.votes)






    def buildProportion(self, position, quota):
        if position in self.positionsApplied:
            ballotList = self.positionsApplied[position]
            freq = {}
            for b in ballotList:
                secondPref = b.getVote(1)

                if secondPref not in freq:
                    freq[secondPref] = 1
                else:
                    freq[secondPref] += 1
        
        return freq


        



    def transferVotes(self, position, quota, surplus=False):
        #print('transfering')
        if position in self.positionsApplied:
            freq = self.buildProportion(position, quota)


            for secondPref in freq:
                if (surplus):
                    #print('surplus')
                    total = self.tallyVotes(position)
                    surplus = total - quota
                    #print("there are", freq[secondPref], "votes to", secondPref.getName(), "i,", self.getName(), "have a total of", total, "surplus is", surplus)
                    f = round(freq[secondPref]/total)
                    #print("fract is", f)

                    fractionThing = round((freq[secondPref] / total) * surplus)
                    #print('giving', secondPref.getName(), fractionThing, "votes")
                    
                    secondPref.transferAdd(fractionThing)
                
                else:
                    #print('hi i am', self.getName(), "transferring", freq[secondPref], "votes to", secondPref.getName(),)
                    secondPref.transferAdd(freq[secondPref])
                    
                    #print(secondPref.tallyVotes(position))

    

    def getPositionsApplied(self):
        return self.positionsApplied






    def tallyVotes(self, position):
        ##could break

        if (not self.votes):
            if position in self.positionsApplied:
                #print("hi")
                self.votes = len(self.positionsApplied[position])
        
        return self.votes

        
       

        




class election:
    def __init__(self, candidateList, rolesList, needToWin, ballotsList):
        self.roles = {}
        self.check = needToWin
        self.ballotsList = ballotsList
        self.candidateList = candidateList

        self.winners = {}
        self.losers = {}

        for r in rolesList:
            self.roles[r] = []
            self.winners[r] = []
            self.losers[r] = []

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
    

    def removeCandidate(self, c, position, quota, surplus=False):
        #print(self.roles[position])
        if c in self.roles[position]:
            c.transferVotes(position, quota, surplus)
            self.roles[position].remove(c)
            if (surplus):
                self.winners[position].append(c.getName())
            else:
                self.losers[position].append(c.getName())



    def applyVotes(self,ballotList):
        for i in ballotList:
            i.applyVote()


    def getMaxVotes(self, position):
        m = self.roles[position][0]
        maxVotes = m.tallyVotes(position)
        for c in self.roles[position]:
            if (c.tallyVotes(position) > maxVotes):
                maxVotes = c.tallyVotes(position)
                m = c
        return m


    def getMinVotes(self, position):
        m = self.roles[position][0]
        minVotes = m.tallyVotes(position)
        for c in self.roles[position]:
            if (c.tallyVotes(position) < minVotes):
                minVotes = c.tallyVotes(position)
                m = c
        
        return m



    def tally(self, position, surplusList, transferList):
        quota = self.check[position]
        print('quota is',quota)
        print()

        ballots = self.getBallots(position)
        self.applyVotes(ballots)

        for c in self.roles[position]:
            c.tallyVotes(position)

        
        while (len(self.roles[position]) > 1):

            #print(self.roles[position])
            maxCandidate = self.getMaxVotes(position)
            maxVotes = maxCandidate.tallyVotes(position)
            minCandidate = self.getMinVotes(position)

            for c in self.roles[position]:
                print(c.getName(), 'has', c.tallyVotes(position))

            if (maxVotes < quota):
                self.removeCandidate(minCandidate, position, quota)
                print("\n\n\n")
            else:
                self.removeCandidate(maxCandidate, position, quota, True)
                minCandidate = self.getMinVotes(position)
                print("the", position, "of Co-op soc ", 2020 + 1, "is", maxCandidate.getName(), "with", maxVotes, "the min candidate removed was", minCandidate.getName(), "\n\n")
                self.removeCandidate(minCandidate, position, quota)
        
        
        luckyLast = self.roles[position][0].getName()


        print("order:", self.winners[position], [luckyLast], self.losers[position])

                

        

        


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

for i in range(8):
    b = ballot('pres', [choc, straw, ph,ph,ph])
    ballotList.append(b)


for i in range(4):
    b = ballot('pres', [choc, burg,ph,ph,ph])
    ballotList.append(b)

b = ballot('pres', [straw, ph,ph,ph,ph])
ballotList.append(b)
b = ballot('pres', [burg, ph,ph,ph,ph])
ballotList.append(b)


candidateList = [orange, pear, choc, straw, burg, ph]
e = election(candidateList, rolesList, n2w, ballotList)
#print(choc.positionsApplied['pres'])

e.tally('pres', [], [])

#print(orange)

#ian Ng: i'm applying for pres, vp, arc
#{ian ng : [roles]}





