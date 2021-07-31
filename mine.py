# AHMED ASHRAF ABD EL-SALAM
# Minesweeper Game
# V 1.0.0
# 31/7/2021
# Created using PyQt5
#
# The main module
#


from Tile import *

class Ui_MainWindow():

    rowSize = 13
    coulmnSize = 13
    
    checked = []

    showTips = None
    showSettings = None
    box = [[None for i in range(30)] for j in range(30)]
    tile = [[None for i in range(30)] for j in range(30)]
    time = 0
    timer = None
    restartGame = None
    settings = None
    boardSize = None
    howToPlay = None
    mainSpacer = None
    buttonsSpacer = None
    timeElapsed = [None for i in range(4)]
    minesRemaining = [None for i in range(3)]
    
    def setupUi(self, MainWindow):
        'Setting up starting UI elements for user to start interacting with the game'

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Minesweeper")
        
        TileButton.minesLeft = 25
        TileButton.boxesLeft = 144
        
        #Main frame setup
        self.mainSpacer = QtWidgets.QLabel(MainWindow)
        self.mainSpacer.setStyleSheet("border :3px solid black")
        self.colon = QtWidgets.QLabel(MainWindow)
        self.colon.setStyleSheet("border-image : url(Minesweeper/colon.svg)")
        self.timeElapsed[0] = QtWidgets.QLabel(MainWindow)
        self.timeElapsed[1] = QtWidgets.QLabel(MainWindow)
        self.timeElapsed[2] = QtWidgets.QLabel(MainWindow)
        self.timeElapsed[3] = QtWidgets.QLabel(MainWindow)
        self.minesRemaining[0] = QtWidgets.QLabel(MainWindow)
        self.minesRemaining[0].setGeometry(QtCore.QRect(4,3,20,34))
        self.minesRemaining[1] = QtWidgets.QLabel(MainWindow)
        self.minesRemaining[1].setGeometry(QtCore.QRect(25,3,20,34))
        self.minesRemaining[2] = QtWidgets.QLabel(MainWindow)
        self.minesRemaining[2].setGeometry(QtCore.QRect(45,3,20,34))
        self.buttonsSpacer = QtWidgets.QLabel(MainWindow)
        self.buttonsSpacer.setStyleSheet("border :3px solid black;")

        #Settings window setup
        self.settings = QtWidgets.QPushButton(MainWindow)
        self.showSettings = QtWidgets.QLabel()
        self.showSettings.setWindowTitle("Settings")
        self.showSettings.setFixedSize(125,25)
        self.boardSize = QtWidgets.QComboBox(self.showSettings)
        self.boardSize.addItem('Easy 13x13')
        self.boardSize.addItem('Medium 20x20')
        self.boardSize.addItem('Hard 29x29')
        self.settings.clicked.connect(self.showSettings.show)
        self.settings.setStyleSheet("border-image : url(Minesweeper/Minesweeper_settings.svg)")   

        #Restart/Game state button setup 
        self.restartGame = QtWidgets.QPushButton(MainWindow)
        self.restartGame.clicked.connect(self.createNewGame)
        
        #How to play window setup
        self.howToPlay = QtWidgets.QPushButton(MainWindow)
        self.howToPlay.setStyleSheet("border-image : url(Minesweeper/Minesweeper_tips.svg)")
        self.showTips = QtWidgets.QLabel()
        self.showTips.setWindowTitle("How to Play Minesweeper")
        self.showTips.setFixedSize(585,365)
        self.text0 = QtWidgets.QLabel(self.showTips)
        self.text0.setStyleSheet("border-image:url(Minesweeper/Minesweeper_HowToPlay.png)")
        self.text0.setGeometry(QtCore.QRect(0,0,585,100))
        self.text1 = QtWidgets.QLabel(self.showTips)
        self.text1.setStyleSheet("border-image:url(Minesweeper/Minesweeper_HowToPlay2.png)")
        self.text1.setGeometry(QtCore.QRect(0,100,317.5,265))
        self.text2 = QtWidgets.QLabel(self.showTips)
        self.text2.setStyleSheet("border-image:url(Minesweeper/Minesweeper_HowToPlay3.png)")
        self.text2.setGeometry(QtCore.QRect(317.5,100,267.5,265))
        self.howToPlay.clicked.connect(self.showTips.show)

        #Time elapsed counter setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.incrementTime)
        self.createGame()
    
    def createGame(self):
        'Creating an object for every button and another object for handleing the tile'
        TileLabel.isFirstTile = True
        for i in range(self.rowSize):
            for j in range(self.coulmnSize):
                self.tile[i][j] = TileLabel(MainWindow,i,j)
                self.tile[i][j].setGeometry(QtCore.QRect(i*25,(j*25) + 40,25,25))
                self.tile[i][j].show()
                self.tile[i][j].lost.connect(self.gameLost)
                self.tile[i][j].voidFound.connect(self.getAllVoids)
                self.tile[i][j].random.connect(self.randomize)

                self.box[i][j] = TileButton(MainWindow)
                self.box[i][j].setGeometry(QtCore.QRect(i*25,(j*25) + 40,25,25))
                self.box[i][j].show()
                self.box[i][j].clicked.connect(self.tile[i][j].click)
                self.box[i][j].won.connect(self.gameWon)
                self.box[i][j].flag.connect(self.tile[i][j].toggleClickablility)
                self.box[i][j].flag.connect(self.changeMineConuter)

        self.time = 0
        self.timer.start(1000)
        self.changeUI()

    def createNewGame(self):
        'Destroying the old won/lost/restarted game and creating new one'
        for i in range(self.rowSize):
            for j in range(self.coulmnSize):
                self.box[i][j].deleteLater()
                self.tile[i][j].deleteLater()

        self.box = [[None for i in range(30)] for j in range(30)]
        self.tile = [[None for i in range(30)] for j in range(30)]
        self.changeBoardSize()
        self.createGame()

    def randomize(self,xpos,ypos):
        'randomizing mine locations after getting the first tile pressed'

        #First tile positioning and exclusion from the set of tiles to be randomized
        
        yposition = ypos * self.rowSize 
        xposition = xpos
        avoid = yposition + xposition
        
        minesLocations = random.sample((*range(0,avoid-self.rowSize-1) , *range(avoid-self.rowSize+2,avoid-1) , *range(avoid+2,avoid+self.rowSize-1) , *range(avoid+self.rowSize+2,self.rowSize*self.coulmnSize)) , TileButton.minesLeft)
        minesLocationsX = []
        minesLocationsY = []

        for i in minesLocations:
            minesLocationsX.append(i%self.rowSize)
            minesLocationsY.append(i//self.rowSize)

        for i,j in zip(minesLocationsX,minesLocationsY):
            self.tile[i][j].setStyleSheet("border-image : url(Minesweeper/Minesweeper_Mine.png)")
            self.tile[i][j].isMine = True
            self.tile[i][j].num = 10
            for x in range(-1,2):
                for y in range(-1,2):
                    if ((x == 0) and (y == 0)) or (self.tile[i+x][j+y] == None) or (self.tile[i+x][j+y].isMine == True):
                        continue
                    self.tile[i+x][j+y].num += 1
                    s = "border-image : url(Minesweeper/Minesweeper_" + str(self.tile[i+x][j+y].num) + ".svg)"
                    self.tile[i+x][j+y].setStyleSheet(s)
        self.checked = []
        TileLabel.isFirstTile = False

    def getAllVoids(self,a,b):
        'Function to open all tiles adjacent to the empty pressed tile recursively'

        self.checked.append((a,b))

        if self.box[a][b].isVisible() == True:
            self.box[a][b].hide()
            TileButton.boxesLeft -= 1
            if TileButton.boxesLeft == 0:
                self.box[a][b].won.emit()

        for x in range(-1,2):
            for y in range(-1,2):
                
                if (self.tile[a+x][b+y] == None) or ((x == 0) and (y == 0)):
                    continue
                if self.box[a+x][b+y].isVisible() == True:
                    self.box[a+x][b+y].hide()
                    TileButton.boxesLeft -= 1
                    if TileButton.boxesLeft == 0:
                        self.box[a+x][b+y].won.emit()
                if ((self.tile[a+x][b+y].num != 0) and (self.box[a+x][b+y].isVisible() == False)) or ((a+x,b+y) in self.checked): 
                    continue
                if(self.tile[a+x][b+y].num == 0):
                    self.getAllVoids(a+x,b+y)
    
    def gameLost(self):
        self.restartGame.setStyleSheet("border-image: url(Minesweeper/Minesweeper_lost.svg)")
        for i in range(self.rowSize):
            for j in range(self.coulmnSize):
                self.box[i][j].hide()
                self.checked = []
        self.timer.stop()
        self.time = 0
    
    def gameWon(self):
        self.restartGame.setStyleSheet("border-image : url(Minesweeper/Minesweeper_Win.svg)")
        TileButton.minesLeft = 0
        self.changeMineConuter()
        for i in range(self.rowSize):
            for j in range(self.coulmnSize):
                self.box[i][j].setEnabled(False)
                self.box[i][j].setStyleSheet("border-image : url(Minesweeper/Minesweeper_flag.svg)")
        self.timer.stop()
        self.time = 0

    def changeUI(self):
        'Changing UI according to mode (board size)'

        self.mainSpacer.setGeometry(QtCore.QRect(0,0,self.rowSize*25,40))
        self.colon.setGeometry(QtCore.QRect((((self.rowSize - 1)*25)) - 40,3,30,34))
        self.timeElapsed[0].setGeometry(QtCore.QRect((((self.rowSize - 1)*25)) - 60 - 10 ,3,20,34))
        self.timeElapsed[1].setGeometry(QtCore.QRect((((self.rowSize - 1)*25)) - 40 - 10 ,3,20,34))
        self.timeElapsed[2].setGeometry(QtCore.QRect((((self.rowSize - 1)*25)) - 20,3,20,34))
        self.timeElapsed[3].setGeometry(QtCore.QRect((((self.rowSize - 1)*25)),3,20,34))
        self.buttonsSpacer.setGeometry(QtCore.QRect(((self.rowSize/2)*25)-51-3,0,110,40))
        self.settings.setGeometry(QtCore.QRect(((self.rowSize/2)*25) - 51 ,3,34,34))  
        self.restartGame.setGeometry(QtCore.QRect(((self.rowSize/2)*25) - 17 ,3,34,34))
        self.restartGame.setStyleSheet("border-image : url(Minesweeper/Minesweeper_gameOn.svg)")
        self.howToPlay.setGeometry(QtCore.QRect(((self.rowSize/2)*25) + 17 ,3,34,34))
        self.changeMineConuter()
        self.timeElapsed[0].setStyleSheet("border-image : url(Minesweeper/Time_0.svg)")
        self.timeElapsed[1].setStyleSheet("border-image : url(Minesweeper/Time_0.svg)")
        self.timeElapsed[2].setStyleSheet("border-image : url(Minesweeper/Time_0.svg)")
        self.timeElapsed[3].setStyleSheet("border-image : url(Minesweeper/Time_0.svg)")
        MainWindow.setFixedSize(self.rowSize*25,(self.coulmnSize*25) + 40)

    def changeBoardSize(self):
        if self.boardSize.currentText() == 'Easy 13x13':
                self.rowSize = 13
                TileButton.minesLeft = 25
                TileButton.boxesLeft = 144
        elif self.boardSize.currentText() == 'Medium 20x20':
                self.rowSize = 20
                TileButton.minesLeft = 45
                TileButton.boxesLeft = 355
        elif self.boardSize.currentText() == 'Hard 29x29':
                self.rowSize = 29
                TileButton.minesLeft = 200
                TileButton.boxesLeft = 700
        self.coulmnSize = self.rowSize 

    def incrementTime(self):
        s = [None for i in range(4)]
        self.time += 1
        temp = self.time
        s[0] = self.time % 10
        self.time -= s[0]
        s[1] = (self.time % 60) // 10
        self.time -= s[1] * 10
        s[2] = (self.time // 60) % 10
        self.time -= s[2] * 60
        s[3] = self.time // 600
        self.time = temp
        a = "border-image : url(Minesweeper/Time_" + str(s[0]) + ".svg)"
        self.timeElapsed[3].setStyleSheet(a)
        a = "border-image : url(Minesweeper/Time_" + str(s[1]) + ".svg)"
        self.timeElapsed[2].setStyleSheet(a)
        a = "border-image : url(Minesweeper/Time_" + str(s[2]) + ".svg)"
        self.timeElapsed[1].setStyleSheet(a)
        a = "border-image : url(Minesweeper/Time_" + str(s[3]) + ".svg)"
        self.timeElapsed[0].setStyleSheet(a)

    def changeMineConuter(self):
        s = "border-image : url(Minesweeper/Time_" + str(TileButton.minesLeft//100) + ".svg)"
        self.minesRemaining[0].setStyleSheet(s)
        s = "border-image : url(Minesweeper/Time_" + str(((TileButton.minesLeft%100)-(TileButton.minesLeft%10))//10) + ".svg)"
        self.minesRemaining[1].setStyleSheet(s)
        s = "border-image : url(Minesweeper/Time_" + str(TileButton.minesLeft%10) + ".svg)"
        self.minesRemaining[2].setStyleSheet(s)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
