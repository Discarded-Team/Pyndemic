import random
import string
from configparser import ConfigParser
import itertools


class PandemicGame:
    def __init__(self):
        self.startingEpidemics = None
        self.outbreakCount = 0
        self.gameOver = False
        self.gameWon = False
        self.diseaseCubes = {}
        self.cityMap = {}
        self.playerDeck = Deck()
        self.infectDeck = Deck()
        self.infectionRate = None
        self.infectionRates = []
        self.epidemicCount = 0
        self.diseases = {}
        self.players = []
        self.turnNumber = None

    def setupGame(self, settingsLocation):
        City.setCubeColours(settingsLocation)
        self.getInfectionRate(settingsLocation)
        self.getNewCities(settingsLocation)
        self.getNewDecks(settingsLocation)
        self.getNewDiseases(settingsLocation)
        self.setStartingEpidemics(settingsLocation)
        for player in self.players:
            player.setLocation(list(self.cityMap.keys())[0])
        AIcontroller.numberAI = 0

    def setStartingEpidemics(self, settingsLocation):
        parser = ConfigParser()
        parser.read(settingsLocation)
        self.startingEpidemics = int(parser.get('Diseases', 'epidemics'))

    def startGame(self):
        self.shuffleDecks()
        self.initalInfectPhase()
        self.drawInitalHands()
        self.addEpidemics()
        pass

    def addEpidemics(self):
        self.playerDeck.addEpidemics(self.startingEpidemics)

    def addPlayer(self, newPlayer):
        newPlayer.setGame(self)
        newPlayer.setController(AIcontroller(newPlayer))
        self.players.append(newPlayer)

    def drawCard(self, playerDrawing):
        drawnCard = self.playerDeck.takeTopCard()
        if drawnCard.getName() == 'Epidemic':
            self.epidemicPhase()
        else:
            playerDrawing.addCard(drawnCard)

    def shuffleDecks(self):
        self.infectDeck.shuffle()
        self.playerDeck.shuffle()

    def hasXCubeCity(self, x):
        for city in self.cityMap.values():
            if city.getMaxCubes() == x:
                return True
        return False

    def getCountXCubeCity(self, x):
        countXCities = 0
        for city in self.cityMap.values():
            if city.getMaxCubes() == x:
                countXCities = countXCities + 1
        return countXCities

    def infectCity(self, city, colour):
        infectCity = self.cityMap.get(city)
        if infectCity.getCubes(colour) < 3:
            infectCity.addCube(colour)
            self.diseaseCubes[colour] = self.diseaseCubes.get(colour) - 1
        else:
            self.outbreak(city, colour)

    def outbreak(self, city, colour):
        outbreakCity = self.cityMap.get(city)
        self.outbreakCount = self.outbreakCount + 1
        for connectedCity in outbreakCity.getConnections():
            self.infectCity(connectedCity.getName(), colour)
        pass

    def initalInfectPhase(self):
        for x in range(1, 4):
            for y in range(1, 4):
                drawnCard = self.infectDeck.takeTopCard()
                self.infectDeck.addDiscard(drawnCard)
                for z in range(0, y):
                    self.infectCity(drawnCard.getName(), drawnCard.getColour())

    def infectCityPhase(self):
        for x in range(0, int(self.infectionRate)):
            drawnCard = self.infectDeck.takeTopCard()
            self.infectDeck.addDiscard(drawnCard)
            infectCity = self.cityMap.get(drawnCard.getName())
            self.infectCity(infectCity.getName(), infectCity.getColour())

    def startTurn(self, player):
        player.setActionCount(4)
        pass

    def epidemicPhase(self):
        drawnCard = self.infectDeck.takeBottomCard()
        self.infectDeck.addDiscard(drawnCard)
        cityEpidemic = self.cityMap.get(drawnCard.getName())
        for x in range(0, 3):
            self.infectCity(cityEpidemic.getName(), cityEpidemic.getColour())
        self.infectDeck.shuffleDiscardToTop()
        self.incrementEpidemicCount()

    def getNewCities(self, settingsLocation):
        parser = ConfigParser()
        parser.read(settingsLocation)
        numberOfCities = int(parser.get('Cities', 'number'))
        for x in range(1, numberOfCities + 1):
            self.cityMap[parser.get('Cities', "city" + str(x))] = City(parser.get('Cities', "city" + str(x)),
                                                                       parser.get('Colours', "city" + str(x)))
        self.makeCities(settingsLocation)

    def newInfectDeck(self, settingsLocation):
        parser = ConfigParser()
        parser.read(settingsLocation)
        numberOfCards = int(parser.get('Cities', 'number'))
        for x in range(1, numberOfCards + 1):
            self.infectDeck.addCard(Card(parser.get('Cities', "city" + str(x)), parser.get('Colours', "city" + str(x))))

    def newPlayerDeck(self, settingsLocation):
        parser = ConfigParser()
        parser.read(settingsLocation)
        numberOfCards = int(parser.get('Cities', 'number'))
        for x in range(1, numberOfCards + 1):
            self.playerDeck.addCard(Card(parser.get('Cities', "city" + str(x)), parser.get('Colours', "city" + str(x))))

    def getNewDecks(self, settingsLocation):
        self.newInfectDeck(settingsLocation)
        self.newPlayerDeck(settingsLocation)

    def getNewDiseases(self, settingsLocation):
        parser = ConfigParser()
        parser.read(settingsLocation)
        numberOfDisease = int(parser.get('Diseases', 'number'))
        for x in range(1, numberOfDisease + 1):
            self.diseases[parser.get('Diseases', 'disease' + str(x))] = Disease(
                parser.get('Diseases', 'disease' + str(x)))
            self.addDiseaseCubes(parser.get('Diseases', 'disease' + str(x)), int(parser.get('Diseases', 'cubes')))

    def addDiseaseCubes(self, colour, number):
        self.diseaseCubes[colour] = number

    def makeCities(self, settingsLocation):
        parser = ConfigParser()
        parser.read(settingsLocation)
        for city in self.cityMap.items():
            connections = parser.get('Connections', city[0])
            usedlist = list(connections.split("\t"))
            for x in usedlist:
                city[1].addConnection(self.cityMap.get(parser.get('Cities', "city" + x)))
        pass

    def setLabDistances(self):
        citiesWithLabs = []
        for city in self.cityMap.values():
            if city.getLab():
                citiesWithLabs.append(city)
        self.setCitiesDistances(citiesWithLabs)

    def setCitiesDistancesNames(self, cityNames):
        cities = []
        for name in cityNames:
            cities.append(self.cityMap.get(name))
        self.setCitiesDistances(cities)

    def setCitiesDistances(self, cities):
        self.resetDistances()
        for city in cities:
            city.setDistance(0)
        self.updateDistances(cities)

    def setCityDistanceName(self, city):
        cityList = [self.cityMap.get(city)]
        self.setCitiesDistances(cityList)

    def setCityDistance(self, city):
        cityList = [city]
        self.setCitiesDistances(cityList)

    def resetDistances(self):
        for city in self.cityMap.values():
            city.setDistance(999)

    def updateDistances(self, startingCities):
        updatedCities = []
        currentDistance = startingCities[0].getDistance()
        for city in startingCities:
            for connectedCity in city.getConnections():
                if connectedCity.getDistance() == 999:
                    updatedCities.append(connectedCity)
                    connectedCity.setDistance(currentDistance + 1)
        if updatedCities.__len__() > 0:
            self.updateDistances(updatedCities)
        pass

    def incrementEpidemicCount(self):
        self.epidemicCount = self.epidemicCount + 1
        self.infectionRate = self.infectionRates[self.epidemicCount]

    def getInfectionRate(self, settingsLocation):
        parser = ConfigParser()
        parser.read(settingsLocation)
        self.infectionRates = list(parser.get('Diseases', 'rate'))
        self.infectionRate = int(self.infectionRates[0])

    def drawInitalHands(self):
        cardsToDraw = 4
        if self.players.__len__() > 4:
            cardsToDraw = 2
        elif self.players.__len__() == 3:
            cardsToDraw = 3
        for player in self.players:
            for x in range(0, cardsToDraw):
                player.addCard(self.playerDeck.takeTopCard())


class Disease:
    def __init__(self, colour):
        self.colour = colour
        self.cured = False

    def getCured(self):
        return self.cured

    def setCured(self, newStatus):
        self.cured = newStatus


class Card:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def getName(self):
        return self.name

    def getColour(self):
        return self.colour


class City:
    cubeColours = []

    def __init__(self, name, colour):
        self.name = name
        self.hasLab = False
        self.colour = colour
        self.cubes = {}
        self.setCityColours(City.cubeColours)
        self.distance = 999
        self.connectedCities = []

    def getColour(self):
        return self.colour

    def getCountConnections(self):
        return self.connectedCities.__len__()

    def getConnectedCity(self, connection):
        return self.connectedCities[connection - 1]

    def setCityColours(self, cubeColours):
        for colour in cubeColours:
            self.cubes[colour] = 0

    def removeCube(self, colour):
        self.cubes[colour] = self.cubes[colour] - 1

    def addCube(self, colour):
        self.cubes[colour] = self.cubes[colour] + 1

    def getLab(self):
        return self.hasLab

    def buildLab(self):
        if not self.hasLab:
            self.hasLab = True
            return True
        else:
            return False

    def addConnection(self, newConnection):
        self.connectedCities.append(newConnection)

    def getConnections(self):
        return self.connectedCities

    def getName(self):
        return self.name

    def removeAllCubes(self, colour):
        self.cubes[colour] = 0

    def getMaxCubes(self):
        toReturn = 0
        for cubeCount in self.cubes.values():
            if cubeCount > toReturn:
                toReturn = cubeCount
        return toReturn

    def getCubes(self, colour):
        return self.cubes[colour]

    def getDistance(self):
        return self.distance

    def setDistance(self, newDistance):
        self.distance = newDistance

    @classmethod
    def setCubeColours(cls, settingsLocation):
        parser = ConfigParser()
        parser.read(settingsLocation)
        cls.cubeColours = parser.get('Colours', 'colours').split(',')


class Deck:
    def __init__(self):
        self.cards = []
        self.discard = []

    def takeTopCard(self):
        return self.cards.pop(0)

    def takeBottomCard(self):
        self.cards.reverse()
        toReturn = self.cards.pop(0)
        self.cards.reverse()
        return toReturn

    def addCard(self, newCard):
        self.cards.append(newCard)

    def addDiscard(self, discardedCard):
        self.discard.append(discardedCard)

    def getDiscardCount(self):
        return self.discard.__len__()

    def shuffleDiscardToTop(self):
        random.shuffle(self.discard)
        self.cards.reverse()
        for card in self.discard:
            toUse = self.discard.pop(0)
            self.cards.append(toUse)
        self.cards.reverse()

    def shuffle(self):
        random.shuffle(self.cards)

    def addEpidemics(self, numberEpidemics):
        cardPiles = {}
        for x in range (0, numberEpidemics):
            cardPiles[x] = []
        random.shuffle(self.cards)
        while self.cards.__len__()>0:
            for x in range(0, numberEpidemics):
                cardToAdd = self.cards.pop()
                cardPiles.get(x).append(cardToAdd)
        for x in range(0, numberEpidemics):
            cardPiles.get(x).append(Card("Epidemic", "All"))
            random.shuffle(cardPiles.get(x))
        for x in range(0, numberEpidemics):
            while cardPiles.get(x).__len__() > 0:
                cardToAdd = cardPiles.get(x).pop()
                self.cards.append(cardToAdd)


class PandemicPlayer:
    def __init__(self, name):
        self.game = None
        self.location = None
        self.actionCount = 0
        self.hand = []
        self.name = name
        self.controller = None

    def getName(self):
        return self.name

    def getDistanceFromLab(self):
        self.game.setLabDistances()
        return self.location.getDistance()

    def setController(self, newController):
        self.controller = newController

    def setActionCount(self, x):
        self.actionCount = x

    def getHand(self):
        return self.hand

    def getCard(self, cardName):
        for card in self.hand:
            if card.getName() == cardName:
                return card

    def setGame(self, game):
        self.game = game

    def getGame(self):
        return self.game

    def getLocation(self):
        return self.location

    def setLocation(self, newLocation):
        self.location = self.game.cityMap.get(newLocation)

    def checkCharterFlight(self, location, destination):
        if (self.actionCount > 0) & (self.location.getName() == location):
            if self.handContains(location):
                return True
        return False

    def charterFlight(self, location, destination):
        if self.checkCharterFlight(location, destination):
            self.discardCard(location)
            self.setLocation(destination)
            self.actionCount = self.actionCount - 1
            return True
        return False

    def checkDirectFlight(self, location, destination):
        if self.actionCount > 0:
            if self.handContains(destination):
                if self.location.getName() == location:
                    return True
        return False

    def directFlight(self, location, destination):
        if self.checkDirectFlight(location, destination):
            self.discardCard(destination)
            self.setLocation(destination)
            self.actionCount = self.actionCount - 1
            return True
        return False

    def checkBuildLab(self):
        if self.actionCount > 0:
            if self.handContains(self.location.getName()):
                if not self.location.getLab():
                    return True
        return False

    def buildLab(self):
        if self.checkBuildLab():
            self.discardCard(self.location.getName())
            self.location.buildLab()
            self.actionCount = self.actionCount - 1
            return True
        return False

    def checkShuttleFlight(self, location, destination):
        if self.actionCount > 0:
            if location == self.location.getName():
                if self.location.getLab():
                    if self.game.cityMap.get(destination).getLab():
                        return True
        return False

    def shuttleFlight(self, location, destination):
        if self.checkShuttleFlight(location, destination):
            self.setLocation(destination)
            self.actionCount = self.actionCount - 1
            return True
        return False

    def checkTreatDisease(self, colour):
        if self.actionCount > 0:
            if self.location.getCubes(colour) > 0:
                return True
        return False

    def treatDisease(self, colour):
        if self.checkTreatDisease(colour):
            if self.game.diseases.get(colour).getCured():
                self.location.removeAllCubes(colour)
            else:
                self.location.removeCube(colour)
            self.actionCount = self.actionCount - 1
            return True
        return False

    def checkCureDisease(self, card1, card2, card3, card4, card5):
        settry = {self.getCard(card1), self.getCard(card2), self.getCard(card3),
                  self.getCard(card4), self.getCard(card5)}
        if settry.__len__() == 5:
            if self.actionCount > 0:
                if self.handContains(card1) & self.handContains(card2) & self.handContains(card3) & self.handContains(
                        card4) & self.handContains(card5) and self.location.getLab():
                    return True
        return False

    def cureDisease(self, card1, card2, card3, card4, card5):
        if self.checkCureDisease(card1, card2, card3, card4, card5):
            self.game.diseases.get(self.getCard(card1).getColour()).setCured(True)
            self.actionCount = self.actionCount - 1
            return True
        return False

    def checkShareKnowledge(self, card, player):
        if self.actionCount > 0:
            if self.location.getName() == player.getLocation().getName():
                if self.location.getName() == card:
                    return True
        return False

    def shareKnowledge(self, card, player):
        if self.checkShareKnowledge(card, player):
            for heldCard in self.hand:
                if heldCard.getName() == card:
                    player.addCard(heldCard)
                    self.hand.remove(heldCard)
            self.actionCount = self.actionCount - 1
            return True
        return False

    def addCard(self, newCard):
        self.hand.append(newCard)

    def discardCard(self, toDiscard):
        if self.handContains(toDiscard):
            for card in self.hand:
                if card.getName() == toDiscard:
                    self.game.playerDeck.addDiscard(card)
                    self.hand.remove(card)
                    return True
        return False

    def getHandSize(self):
        return self.hand.__len__()

    def handContains(self, cardName):
        for card in self.hand:
            if card.getName() == cardName:
                return True
        return False

    def getController(self):
        return self.controller

    def checkStandardMove(self, location, destination):
        self.game.setCityDistanceName(destination)
        if self.location.getName() == location:
            if self.actionCount > 1:
                if self.location.getDistance() == 1:
                    return True
        return False

    def standardMove(self, location, destination):
        if self.checkStandardMove(location, destination):
            self.setLocation(destination)
            self.actionCount = self.actionCount - 1
            return True
        return False

    def checkLongMove(self, location, destination):
        self.game.setCityDistanceName(destination)
        if self.location.getDistance() < self.actionCount:
            if self.location.getName() == location:
                return True
        return False

    def longMove(self, location, destination):
        if self.checkLongMove(location, destination):
            self.actionCount = self.actionCount - self.location.getDistance()
            self.setLocation(destination)
            return True
        return False

    def getInputs(self):
        pass


class AIcontroller:
    numberAI = 0

    def __init__(self, player):
        AIcontroller.numberAI = AIcontroller.numberAI + 1
        self.name = "AIcontroller" + str(AIcontroller.numberAI)
        self.player = player
        self.distanceToBuild = 5

    def getName(self):
        return self.name

    def curePossible(self):
        handCombinations = self.handCombinations(self.player.getHand())
        for hand in handCombinations:
            if self.player.checkCureDisease(hand[0], hand[1], hand[2], hand[3], hand[4]):
                return True
        return False

    def handCombinations(self, currentHand):
        cardNames = []
        for card in currentHand:
            cardNames.append(card.getName())
        if currentHand.__len__() > 4:
            possibleHands = itertools.combinations(cardNames, 5)
        return possibleHands

    def buildLabSensible(self):
        self.player.game.setLabDistances()
        if self.player.getDistanceFromLab() > self.distanceToBuild:
            if self.player.handContains(self.player.getLocation().getName()):
                return True
        return False
