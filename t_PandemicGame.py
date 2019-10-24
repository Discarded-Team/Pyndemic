import unittest
from PandemicGame import PandemicGame, PandemicPlayer


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.settingsLocation = 'testSettings.cfg'
        self.player1 = PandemicPlayer('Evie')
        self.player2 = PandemicPlayer('Amelia')
        self.pg = PandemicGame()
        self.pg.addPlayer(self.player1)
        self.pg.addPlayer(self.player2)
        self.pg.setupGame(self.settingsLocation)

    def test_AddEpidemics(self):
        self.pg.addEpidemics()
        self.assertFalse(self.pg.hasXCubeCity(3))
        for x in range(0,11):
            self.pg.drawCard(self.player1)
        self.assertEqual(1, self.pg.epidemicCount)
        self.assertTrue(self.pg.hasXCubeCity(3))

    def test_CompleteRound(self):
        self.pg.initalInfectPhase()
        self.pg.drawInitalHands()
        self.assertEqual(3, self.pg.cityMap.get('Cambridge').getCubes('Blue'))
        self.assertEqual(3, self.pg.cityMap.get('Bristol').getCubes('Blue'))
        self.pg.CompleteRound()
        self.assertEqual(0, self.pg.cityMap.get('Cambridge').getCubes('Blue'))
        self.assertEqual('Cambridge', self.player1.getLocation().getName())
        self.assertEqual(0, self.pg.cityMap.get('Bristol').getCubes('Blue'))
        self.assertEqual('Bristol', self.player1.getLocation().getName())

    def test_AddPlayer(self):
        self.assertEqual(self.pg, self.player1.getGame())

    def test_addDiseaseCubes(self):
        self.assertEqual(30, self.pg.diseaseCubes.get('Red'))
        self.assertEqual(30, self.pg.diseaseCubes.get('Blue'))

    def test_SetupGame(self):
        self.london = self.pg.cityMap.get('London')
        self.newyork = self.pg.cityMap.get('New York')
        self.topPlayerCard = self.pg.playerDeck.takeTopCard()
        self.topInfectCard = self.pg.infectDeck.takeTopCard()
        self.assertEqual(30, self.pg.diseaseCubes.get('Red'))
        self.assertEqual(30, self.pg.diseaseCubes.get('Blue'))
        self.assertEqual('Evie', self.pg.players[0].getName())
        self.assertEqual('Amelia', self.pg.players[1].getName())
        self.assertEqual(False, self.pg.gameWon)
        self.assertEqual(False, self.pg.gameOver)
        self.assertEqual('London', self.london.getName())
        self.assertEqual(6, self.london.getConnections().__len__())
        self.assertEqual('Blue', self.london.getColour())
        self.assertEqual('New York', self.newyork.getName())
        self.assertEqual(3, self.newyork.getConnections().__len__())
        self.assertEqual('Yellow', self.newyork.getColour())
        self.assertEqual(2, self.pg.infectionRate)
        self.assertEqual(0, self.pg.epidemicCount)
        self.assertEqual(0, self.pg.outbreakCount)
        self.assertEqual('London', self.topPlayerCard.getName())
        self.assertEqual('London', self.topInfectCard.getName())
        self.assertEqual('Blue', self.topPlayerCard.getColour())
        self.assertEqual('Blue', self.topInfectCard.getColour())
        self.assertEqual('London', self.pg.players[0].getLocation().getName())
        self.assertEqual('London', self.pg.players[1].getLocation().getName())

    def test_GetNewDecks(self):
        self.pg.getNewDecks(self.settingsLocation)
        topPlayerCard = self.pg.playerDeck.takeTopCard()
        topInfectCard = self.pg.infectDeck.takeTopCard()
        self.assertEqual('London', topPlayerCard.getName())
        self.assertEqual('London', topInfectCard.getName())

    def test_AddCard(self):
        topPlayerCard = self.pg.playerDeck.takeTopCard()
        self.player1.addCard(topPlayerCard)
        self.assertEqual(1, self.player1.getHandSize())
        self.assertTrue(self.player1.handContains('London'))

    def test_GetNewCities(self):
        self.pg.getNewCities(self.settingsLocation)
        city1 = self.pg.cityMap.get('London')
        self.assertEqual(6, city1.getCountConnections())
        self.assertEqual('Blue', city1.getColour())
        self.assertEqual('Washington', city1.getConnectedCity(4).getName())

    def test_InfectCity(self):
        self.pg.infectCity('London', 'Blue')
        self.assertEqual(1, self.pg.cityMap.get('London').getCubes('Blue'))

    def test_InfectCityPhase(self):
        self.pg.infectCityPhase()
        self.assertEqual(1, self.pg.cityMap.get('London').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Oxford').getCubes('Blue'))
        self.assertEqual(2, self.pg.infectDeck.getDiscardCount())
        self.assertEqual('London', self.pg.infectDeck.discard[0].getName())
        self.assertEqual(28, self.pg.diseaseCubes.get('Blue'))

    def test_getInfectionRate(self):
        self.assertEqual(2, self.pg.infectionRate)

    def test_EpidemicPhase(self):
        self.pg.epidemicPhase()
        self.assertEqual(3, self.pg.cityMap.get('Belgorod').getCubes('Black'))
        topInfectCard = self.pg.infectDeck.takeTopCard()
        self.assertEqual('Belgorod', topInfectCard.getName())
        self.assertEqual('Black', topInfectCard.getColour())
        self.assertEqual(1, self.pg.epidemicCount)
        self.assertEqual(0, self.pg.infectDeck.getDiscardCount())

    def test_OutbreakTrigger(self):
        for x in range(0, 4):
            self.pg.infectCity('London', 'Blue')
        self.assertEqual(3, self.pg.cityMap.get('London').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Oxford').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Cambridge').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Brighton').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Washington').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Bejing').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Moscow').getCubes('Blue'))
        self.assertEqual(1, self.pg.outbreakCount)

    def test_Outbreak(self):
        self.pg.outbreak('London', 'Blue')
        self.assertEqual(1, self.pg.cityMap.get('Oxford').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Cambridge').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Brighton').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Washington').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Bejing').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Moscow').getCubes('Blue'))

    def test_Shuffle(self):
        self.assertEqual('London', self.pg.infectDeck.takeTopCard().getName())
        self.assertEqual('London', self.pg.playerDeck.takeTopCard().getName())
        self.pg.playerDeck.shuffle()
        self.pg.infectDeck.shuffle()
        self.assertNotEqual('Oxford', self.pg.infectDeck.takeTopCard().getName())
        self.assertNotEqual('Oxford', self.pg.playerDeck.takeTopCard().getName())

    def test_StartGame(self):
        self.pg.startGame()
        self.topPlayerCard = self.pg.playerDeck.takeTopCard()
        self.topInfectCard = self.pg.infectDeck.takeTopCard()
        self.assertEqual(9, self.pg.infectDeck.getDiscardCount())
        self.assertEqual(0, self.pg.playerDeck.getDiscardCount())
        self.assertTrue(self.pg.hasXCubeCity(3))
        self.assertEqual(3, self.pg.getCountXCubeCity(3))
        self.assertTrue(self.pg.hasXCubeCity(2))
        self.assertEqual(3, self.pg.getCountXCubeCity(2))
        self.assertTrue(self.pg.hasXCubeCity(1))
        self.assertEqual(3, self.pg.getCountXCubeCity(1))
        self.assertEqual(4, self.player1.getHand().__len__())
        self.assertEqual(4, self.player2.getHand().__len__())
        self.assertNotEqual('London', self.topPlayerCard.getName())
        self.assertNotEqual('London', self.topInfectCard.getName())
        for x in range (0, 10):
            self.pg.drawCard(self.player1)
        self.assertEqual(1, self.pg.epidemicCount)

    def test_getMaxCubes(self):
        self.pg.infectCity('London', 'Blue')
        self.pg.infectCity('New York', 'Blue')
        self.pg.infectCity('New York', 'Blue')
        self.pg.infectCity('Moscow', 'Red')
        self.pg.infectCity('Moscow', 'Red')
        self.pg.infectCity('Moscow', 'Red')
        self.pg.infectCity('Moscow', 'Blue')
        self.assertEqual(1, self.pg.cityMap.get('London').getMaxCubes())
        self.assertEqual(2, self.pg.cityMap.get('New York').getMaxCubes())
        self.assertEqual(3, self.pg.cityMap.get('Moscow').getMaxCubes())

    def test_InitalInfectPhase(self):
        self.pg.initalInfectPhase()
        self.assertEqual(1, self.pg.cityMap.get('London').getCubes('Blue'))
        self.assertEqual(2, self.pg.cityMap.get('Oxford').getCubes('Blue'))
        self.assertEqual(3, self.pg.cityMap.get('Cambridge').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Brighton').getCubes('Blue'))
        self.assertEqual(2, self.pg.cityMap.get('Southampton').getCubes('Blue'))
        self.assertEqual(3, self.pg.cityMap.get('Bristol').getCubes('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('Plymouth').getCubes('Blue'))
        self.assertEqual(2, self.pg.cityMap.get('Liverpool').getCubes('Blue'))
        self.assertEqual(3, self.pg.cityMap.get('Manchester').getCubes('Blue'))
        self.assertEqual(9, self.pg.infectDeck.getDiscardCount())
        self.assertEqual(12, self.pg.diseaseCubes.get('Blue'))

    def test_DrawInitialHands(self):
        self.pg.startGame()

    def test_DrawCard(self):
        self.pg.drawCard(self.player1)
        self.assertEqual('London', self.player1.getHand()[0].getName())

    def test_CheckCureDisease(self):
        for x in range(0, 9):
            self.pg.drawCard(self.player1)
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.assertEqual(4, self.player1.actionCount)
        self.assertEqual(True, self.player1.buildLab())
        self.assertTrue(
            self.player1.checkCureDisease('Oxford', 'Cambridge', 'Brighton', 'Southampton', 'Bristol'))
        self.assertFalse(
            self.player1.checkCureDisease('Brighton', 'Liverpool', 'Brighton', 'Southampton', 'Manchester'))
        self.assertFalse(
            self.player1.checkCureDisease('Brighton', 'Liverpool', 'New York', 'Southampton', 'Manchester'))

    def test_CureDisease(self):
        self.assertFalse(self.pg.diseases.get('Blue').getCured())
        for x in range(0, 15):
            self.pg.drawCard(self.player1)
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.assertEqual(4, self.player1.actionCount)
        self.assertTrue( self.player1.buildLab())
        self.assertTrue(self.player1.cureDisease('Cambridge', 'Liverpool', 'Brighton', 'Southampton', 'Manchester'))
        self.assertTrue(self.pg.diseases.get('Blue').getCured())
        self.assertEqual(2, self.player1.actionCount)

    def test_CheckShareKnowledge(self):
        self.player1.setLocation('London')
        self.player2.setLocation('London')
        self.pg.startTurn(self.player1)
        self.pg.drawCard(self.player1)
        self.assertTrue(self.player1.checkShareKnowledge('London', self.player2))
        self.player2.setLocation('New York')
        self.assertFalse(self.player1.checkShareKnowledge('London', self.player2))

    def test_ShareKnowledge(self):
        self.player1.setLocation('London')
        self.player2.setLocation('London')
        self.pg.startTurn(self.player1)
        self.pg.drawCard(self.player1)
        self.assertEqual(True, self.player1.shareKnowledge('London', self.player2))
        self.assertEqual('London', self.player2.getHand()[0].getName())
        self.assertEqual(3, self.player1.actionCount)

    def test_CheckTreatDisease(self):
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.pg.infectCity('London', 'Blue')
        self.pg.infectCity('London', 'Blue')
        self.assertTrue(self.player1.checkTreatDisease('Blue'))
        self.assertFalse(self.player1.checkTreatDisease('Red'))

    def test_TreatDiseaseNoCure(self):
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.pg.infectCity('London', 'Blue')
        self.pg.infectCity('London', 'Blue')
        self.assertEqual(2, self.pg.cityMap.get('London').getCubes('Blue'))
        self.assertEqual(4, self.player1.actionCount)
        self.assertEqual(True, self.player1.treatDisease('Blue'))
        self.assertEqual(1, self.pg.cityMap.get('London').getCubes('Blue'))
        self.assertEqual(3, self.player1.actionCount)
        self.assertEqual(False, self.player1.treatDisease('Red'))
        self.assertEqual(1, self.pg.cityMap.get('London').getCubes('Blue'))
        self.assertEqual(3, self.player1.actionCount)

    def test_GetNewDiseaes(self):
        self.assertFalse(self.pg.diseases.get('Blue').getCured())
        self.assertFalse(self.pg.diseases.get('Red').getCured())
        self.pg.diseases.get('Blue').setCured(True)
        self.assertTrue(self.pg.diseases.get('Blue').getCured())

    def test_TreatDiseaseCure(self):
        self.pg.diseases.get('Blue').setCured(True)
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.pg.infectCity('London', 'Blue')
        self.pg.infectCity('London', 'Blue')
        self.assertEqual(2, self.pg.cityMap.get('London').getCubes('Blue'))
        self.assertEqual(4, self.player1.actionCount)
        self.assertEqual(True, self.player1.treatDisease('Blue'))
        self.assertEqual(0, self.pg.cityMap.get('London').getCubes('Blue'))
        self.assertEqual(3, self.player1.actionCount)
        self.assertEqual(False, self.player1.treatDisease('Red'))
        self.assertEqual(0, self.pg.cityMap.get('London').getCubes('Blue'))
        self.assertEqual(3, self.player1.actionCount)

    def test_CheckCharterFlight(self):
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.pg.drawCard(self.player1)
        self.assertEqual(4, self.player1.actionCount)
        self.assertTrue(self.player1.checkCharterFlight('London', 'Texas'))

    def test_CharterFlight(self):
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.pg.drawCard(self.player1)
        self.assertEqual(4, self.player1.actionCount)
        self.assertEqual(True, self.player1.charterFlight('London', 'New York'))
        self.assertEqual(1, self.pg.playerDeck.getDiscardCount())
        self.assertEqual('London', self.pg.playerDeck.discard[0].getName())
        self.assertEqual('New York', self.player1.getLocation().getName())
        self.assertEqual(3, self.player1.actionCount)
        self.assertEqual(self.player1.charterFlight('New York', 'Brighton'), False)
        self.assertEqual(1, self.pg.playerDeck.getDiscardCount())
        self.assertEqual('London', self.pg.playerDeck.discard[0].getName())
        self.assertEqual(3, self.player1.actionCount)
        self.assertEqual('New York', self.player1.getLocation().getName())

    def test_CheckShuttleFlight(self):
        for x in range(0, 30):
            self.pg.drawCard(self.player1)
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.assertEqual(True, self.player1.buildLab())
        self.player1.setLocation('New York')
        self.assertEqual(True, self.player1.buildLab())
        self.assertTrue(self.player1.checkShuttleFlight('New York', 'London'))

    def test_ShuttleFlight(self):
        for x in range(0, 30):
            self.pg.drawCard(self.player1)
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.pg.drawCard(self.player1)
        self.assertEqual(True, self.player1.buildLab())
        self.player1.setLocation('New York')
        self.assertEqual(True, self.player1.buildLab())
        self.assertEqual(True, self.player1.shuttleFlight('New York', 'London'))
        self.assertEqual(1, self.player1.actionCount)
        self.assertEqual('London', self.player1.getLocation().getName())

    def test_CheckBuildLab(self):
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.pg.drawCard(self.player1)
        self.assertFalse(self.pg.cityMap.get('London').hasLab)
        self.assertEqual(4, self.player1.actionCount)
        self.assertTrue(self.player1.checkBuildLab())

    def test_BuildLab(self):
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.pg.drawCard(self.player1)
        self.assertFalse(self.pg.cityMap.get('London').hasLab)
        self.assertEqual(4, self.player1.actionCount)
        self.assertEqual(True, self.player1.buildLab())
        self.assertEqual(3, self.player1.actionCount)
        self.assertTrue(self.pg.cityMap.get('London').getLab())
        self.assertEqual(1, self.pg.playerDeck.getDiscardCount())
        self.assertEqual('London', self.pg.playerDeck.discard[0].getName())

    def test_CheckDirectFlight(self):
        self.player1.setLocation('Jinan')
        self.pg.startTurn(self.player1)
        self.pg.drawCard(self.player1)
        self.assertEqual(4, self.player1.actionCount)
        self.assertTrue(self.player1.handContains('London'))
        self.assertTrue(self.player1.checkDirectFlight('Jinan', 'London'), True)

    def test_DirectFlight(self):
        self.player1.setLocation('Moscow')
        self.pg.startTurn(self.player1)
        self.pg.drawCard(self.player1)
        self.assertEqual(4, self.player1.actionCount)
        self.assertEqual('Moscow', self.player1.getLocation().getName())
        self.assertTrue(self.player1.directFlight('Moscow', 'London'))
        self.assertEqual(1, self.pg.playerDeck.getDiscardCount())
        self.assertEqual('London', self.player1.getLocation().getName())
        self.assertEqual('London', self.pg.playerDeck.discard[0].getName())
        self.assertEqual(3, self.player1.actionCount)
        self.assertEqual(self.player1.directFlight('Texas', 'New York'), False)
        self.assertEqual(1, self.pg.playerDeck.getDiscardCount())
        self.assertEqual('London', self.pg.playerDeck.discard[0].getName())
        self.assertEqual('London', self.player1.getLocation().getName())
        self.assertEqual(3, self.player1.actionCount)

    def test_CheckStandardMove(self):
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.assertEqual(4, self.player1.actionCount)
        self.assertTrue(self.player1.checkStandardMove('London', 'Brighton'))

    def test_StandardMove(self):
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.assertEqual(4, self.player1.actionCount)
        self.assertTrue(self.player1.standardMove('London', 'Brighton'))
        self.assertEqual(3, self.player1.actionCount)
        self.assertEqual('Brighton', self.player1.getLocation().getName())
        self.assertFalse(self.player1.standardMove('New York', 'London'))
        self.assertEqual(3, self.player1.actionCount)
        self.assertEqual('Brighton', self.player1.getLocation().getName())
        self.assertFalse(self.player1.standardMove('Brighton', 'New York'))
        self.assertEqual(3, self.player1.actionCount)
        self.assertEqual('Brighton', self.player1.getLocation().getName())
        self.assertTrue(self.player1.standardMove('Brighton', 'Southampton'))
        self.assertEqual(2, self.player1.actionCount)
        self.assertEqual('Southampton', self.player1.getLocation().getName())

    def test_CheckLongMove(self):
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.assertEqual(4, self.player1.actionCount)
        self.assertTrue(self.player1.checkLongMove('London', 'Plymouth'))
        self.assertTrue(self.player1.checkLongMove('London', 'Baoding'))
        self.assertFalse(self.player1.checkLongMove('Plymouth', 'Baoding'))
        self.assertFalse(self.player1.checkLongMove('Baoding', 'London'))

    def test_LongMove(self):
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.assertEqual(4, self.player1.actionCount)
        self.assertTrue(self.player1.longMove('London', 'Plymouth'))
        self.assertEqual(1, self.player1.actionCount)
        self.assertEqual('Plymouth', self.player1.getLocation().getName())
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.assertEqual(4, self.player1.actionCount)
        self.assertTrue(self.player1.longMove('London', 'Oxford'))
        self.assertEqual(3, self.player1.actionCount)
        self.assertEqual('Oxford', self.player1.getLocation().getName())
        self.player1.setLocation('Moscow')
        self.pg.startTurn(self.player1)
        self.assertEqual(4, self.player1.actionCount)
        self.assertTrue(self.player1.longMove('Moscow', 'Detroit'))
        self.assertEqual(2, self.player1.actionCount)
        self.assertEqual('Detroit', self.player1.getLocation().getName())

    def test_MakeCities(self):
        self.assertEqual('London', self.pg.cityMap.get('London').getName())
        self.assertEqual(40, self.pg.cityMap.__len__())
        self.assertEqual('Yellow', self.pg.cityMap.get('Washington').getColour())

    def test_HandContains(self):
        self.pg.drawCard(self.player1)
        self.assertTrue(self.player1.handContains('London'))
        self.assertFalse(self.player1.handContains('New York'))

    def test_DiscardCard(self):
        self.pg.drawCard(self.player1)
        self.assertEqual(1, self.player1.getHandSize())
        self.assertEqual(True, self.player1.discardCard('London'))
        self.assertEqual(0, self.player1.getHandSize())
        self.assertEqual(1, self.pg.playerDeck.discard.__len__())
        self.assertEqual('London', self.pg.playerDeck.discard[0].getName())

    def test_AIcontroller(self):
        self.assertEqual('AIcontroller1', self.player1.getController().getName())

    def test_AI_CurePossible(self):
        for x in range(0, 9):
            self.pg.drawCard(self.player1)
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.assertEqual(4, self.player1.actionCount)
        self.assertEqual(True, self.player1.buildLab())
        self.assertTrue(self.player1.getController().curePossible())

    def test_AI_BuildLabSensible(self):
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.pg.drawCard(self.player1)
        self.assertFalse(self.pg.cityMap.get('London').hasLab)
        self.assertEqual(4, self.player1.actionCount)
        self.assertEqual(True, self.player1.buildLab())
        self.player1.setLocation('Jacksonville')
        for x in range(0, 21):
            self.pg.drawCard(self.player1)
        self.assertEqual(6, self.player1.getDistanceFromLab())
        self.assertTrue(self.player1.handContains('Jacksonville'))
        self.assertTrue(self.player1.getController().buildLabSensible())

    def test_ResetDistances(self):
        self.pg.resetDistances()
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.pg.drawCard(self.player1)
        self.assertEqual(True, self.player1.buildLab())
        self.assertEqual(999, self.pg.cityMap.get('London').getDistance())
        self.assertEqual(999, self.pg.cityMap.get('Moscow').getDistance())
        self.pg.setLabDistances()
        self.assertNotEqual(999, self.pg.cityMap.get('London').getDistance())
        self.assertNotEqual(999, self.pg.cityMap.get('Moscow').getDistance())
        self.pg.resetDistances()
        self.assertEqual(999, self.pg.cityMap.get('London').getDistance())
        self.assertEqual(999, self.pg.cityMap.get('Moscow').getDistance())

    def test_RemoveAllCubes(self):
        self.pg.infectCity('Leeds', 'Yellow')
        self.pg.infectCity('Leeds', 'Yellow')
        self.assertEqual(2, self.pg.cityMap.get('Leeds').getCubes('Yellow'))
        self.pg.cityMap.get('Leeds').removeAllCubes('Yellow')
        self.assertEqual(0, self.pg.cityMap.get('Leeds').getCubes('Yellow'))
        self.pg.infectCity('Bristol', 'Red')
        self.assertEqual(1, self.pg.cityMap.get('Bristol').getCubes('Red'))
        self.pg.cityMap.get('Bristol').removeAllCubes('Red')
        self.assertEqual(0, self.pg.cityMap.get('Bristol').getCubes('Red'))

    def test_SetCityDistanceName(self):
        self.pg.setCityDistanceName('Leeds')
        self.assertEqual(2, self.pg.cityMap.get('London').getDistance())
        self.assertEqual(3, self.pg.cityMap.get('Moscow').getDistance())

    def test_SetDistanceCitiesName(self):
        cities = ['Leeds', 'Atlanta', 'Moscow']
        self.pg.setCitiesDistancesNames(cities)
        self.assertEqual(1, self.pg.cityMap.get('London').getDistance())
        self.assertEqual(0, self.pg.cityMap.get('Moscow').getDistance())

    def test_setDistanceLabs(self):
        for x in range(0, 21):
            self.pg.drawCard(self.player1)
        self.player1.setLocation('London')
        self.pg.startTurn(self.player1)
        self.assertEqual(True, self.player1.buildLab())
        self.player1.setLocation('New York')
        self.pg.drawCard(self.player1)
        self.assertEqual(True, self.player1.buildLab())
        self.player1.setLocation('Jinan')
        self.pg.setLabDistances()
        self.assertEqual(0, self.pg.cityMap.get('London').getDistance())
        self.assertEqual(1, self.pg.cityMap.get('Moscow').getDistance())
        self.assertEqual(3, self.player1.getDistanceFromLab())

    def test_getInputs(self):
        print("Checking test inputs at start of game")
        testInputs = self.player1.getInputs()
        print("Checking first 40 inputs (0-39) for city cubes are all 0")
        for x in range(0, 40):
            self.assertEqual(testInputs[x],0)
        print("Checking inputs (40-46 for player1 potential cards are all 0")
        for x in range(40, 46):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs (47-53 for player2 potential cards are all 0")
        for x in range(47, 53):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs (54-60 for player3 potential cards are all 0")
        for x in range(54, 60):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs (61-68 for player4 potential cards are all 0")
        for x in range(61, 68):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs for player cards in discard are all 0")
        for x in range(69, 109):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs for infect cards in discard are all 0")
        for x in range(110, 150):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs for epidemic cards in game is 0")
        self.assertEqual(0, testInputs[151])
        print("Checking inputs for epidemic drawn in game is 0")
        self.assertEqual(0, testInputs[152])
        print("Checking inputs for outbreaks in game is 0")
        self.assertEqual(0, testInputs[152])
        print("Checking inputs for infection rate is 2")
        self.assertEqual(2, testInputs[152])
        print("Checking location for each player is set to London")
        self.assertEqual(0.975, testInputs[153])
        print("Checking the number of research stations in London is set to 1")
        self.assertEqual(1, testInputs[158])
        print("Checking number of research stations in each location is to 0")
        for x in range(159, 199):
            self.assertEqual(testInputs[x], 0.975)
        print("checking each disease is set to uncured")
        for x in range(200, 203):
            self.assertEqual(testInputs[x], 0)
        print("checking the availability of each non movement option (cure disease, treat disease, share knowledge, "
              "buildResaerch) is set to 0")
        for x in range(204, 207):
            self.assertEqual(testInputs[x], 0)
        print("checking the availability of each movement option (standard, direct, charter, shuttle) is set correctly")
        print("standard possible")
        for x in range(208, 248):
            self.assertEqual(testInputs[x], 0)
        print("standard not possible")
        for x in range(208, 248):
            self.assertEqual(testInputs[x], 0)
        print("direct")
        for x in range(249, 289):
            self.assertEqual(testInputs[x], 0)
        print("charter")
        for x in range(249, 289):
            self.assertEqual(testInputs[x], 0)
        print("shuttle")
        for x in range(249, 289):
            self.assertEqual(testInputs[x], 0)
        print("checking available actions for each player is set to 0")
        self.assertEqual(0, testInputs[300])
        self.assertEqual(0, testInputs[301])

        self.pg.drawInitalHands()
        self.pg.initalInfectPhase()
        self.pg.startTurn(self.player1)

        print("Checking test inputs after game Start during player 1 turn")
        testInputs = self.player1.getInputs()
        print("Checking first 40 inputs (0-39) for city cubes are all correct")
        self.assertEqual(0.25, testInputs[0])
        self.assertEqual(0.25, testInputs[3])
        self.assertEqual(0.25, testInputs[6])
        self.assertEqual(0.50, testInputs[1])
        self.assertEqual(0.50, testInputs[4])
        self.assertEqual(0.50, testInputs[7])
        self.assertEqual(0.75, testInputs[2])
        self.assertEqual(0.75, testInputs[5])
        self.assertEqual(0.75, testInputs[8])
        for x in range(9, 40):
            self.assertEqual(testInputs[x],0)
        print("Checking inputs (40-46 for player1 potential cards are all 0")
        self.assertEqual(0.975, testInputs[41])
        self.assertEqual(0.95, testInputs[42])
        self.assertEqual(0.925, testInputs[43])
        self.assertEqual(0.9, testInputs[44])
        for x in range(45, 53):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs (47-53 for player2 potential cards are all 0")
        for x in range(47, 53):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs (54-60 for player3 potential cards are all 0")
        for x in range(54, 60):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs (61-68 for player4 potential cards are all 0")
        for x in range(61, 68):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs for player cards in discard are all 0")
        for x in range(69, 109):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs for infect cards in discard are all 0")
        for x in range(110, 150):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs for epidemic cards in game is 0")
        self.assertEqual(0, testInputs[151])
        print("Checking inputs for epidemic drawn in game is 0")
        self.assertEqual(0, testInputs[152])
        print("Checking inputs for outbreaks in game is 0")
        self.assertEqual(0, testInputs[152])
        print("Checking inputs for infection rate is 2")
        self.assertEqual(0, testInputs[152])
        print("Checking location for each player is set to London")
        for x in range(153, 158):
            self.assertEqual(testInputs[x], 0.975)
        print("Checking number of research stations in each location is to 0.75")
        for x in range(159, 199):
            self.assertEqual(0, testInputs[x])
        print("checking each disease is set to uncured")
        for x in range(200, 203):
            self.assertEqual(testInputs[x], 0)
        print("checking the availability of each non movement option (cure disease, treat disease, share knowledge, "
              "buildResaerch) is set to 0")
        for x in range(204, 207):
            self.assertEqual(testInputs[x], 0)
        print("checking the availability of each movement option (standard, direct, charter, shuttle) is set correctly")
        print("standard possible")
        for x in range(208, 248):
            self.assertEqual(testInputs[x], 0)
        print("standard not possible")
        for x in range(208, 248):
            self.assertEqual(testInputs[x], 0)
        print("direct")
        for x in range(249, 289):
            self.assertEqual(testInputs[x], 0)
        print("charter")
        for x in range(249, 289):
            self.assertEqual(testInputs[x], 0)
        print("shuttle")
        for x in range(249, 289):
            self.assertEqual(testInputs[x], 0)
        print("checking available actions for each player is set to 0")
        self.assertEqual(0, testInputs[300])
        self.assertEqual(0, testInputs[301])




if __name__ == '__main__':
    unittest.main()
