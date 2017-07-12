import numpy as np
import time
from PyQt4 import QtGui, QtCore
import sys

#klasa z glownym oknem i akcjami
class Window(QtGui.QMainWindow):

    filepath = "default.txt"

    def __init__(self):
        super(Window,self).__init__()
        self.setGeometry(100,100,700,500)
        self.setWindowTitle("Conway's Game of Life")

        exitAct = QtGui.QAction("&Quit", self)
        exitAct.setShortcut("Crtl+Q")
        exitAct.setStatusTip('Leave program')
        exitAct.triggered.connect(self.closemyapp)

        aboutAct = QtGui.QAction("&About", self)
        aboutAct.triggered.connect(self.aboutapp)

        instrAct = QtGui.QAction("&Instructions", self)
        instrAct.triggered.connect(self.instructionswindow)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&Menu')
        fileMenu.addAction(instrAct)
        fileMenu.addAction(aboutAct)
        fileMenu.addAction(exitAct)

        self.home()

    def instructionswindow(self):
        QtGui.QMessageBox.about(self,"How-to","In the proper fields, input the following data:\n"
                                "-number of rows and columns of the game board\n"
                                "-number of generations\n"
                                "-choose the file with input data\n"
                                "Output file will be generated automatically after the simulation")

    def home(self):
        mainWidget = QtGui.QWidget()  #stworzenie widgetu z layoutem

        self.Life = Game(Game.rows, Game.cols)

        self.table = QtGui.QTableWidget()  #stworzenie widgetu z tabela
        self.table.setRowCount(Game.rows)
        self.table.setColumnCount(Game.cols)

        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

        #tworzenie widegtow z menu glownego:

        self.rowz = QtGui.QSpinBox()   #by uzywac wartosci z boxa musi byc self.
        self.rowz.setMinimum(1)
        self.rowz.setMaximum(20)
        self.rowz.setValue(10)
        self.rowz.setFont(QtGui.QFont("Arial",10))
        self.rowz.valueChanged.connect(self.updateboard_menu)

        self.colz = QtGui.QSpinBox()
        self.colz.setMinimum(1)
        self.colz.setMaximum(20)
        self.colz.setValue(10)
        self.colz.setFont(QtGui.QFont("Arial", 10))
        self.colz.valueChanged.connect(self.updateboard_menu)

        self.generationz = QtGui.QSpinBox()
        self.generationz.setMinimum(1)
        self.generationz.setMaximum(50)
        self.generationz.setValue(1)
        self.generationz.setFont(QtGui.QFont("Arial", 10))
        self.generationz.valueChanged.connect(self.updateboard_menu)

        self.formy = QtGui.QFormLayout()  #do poukladania pionowo inputboxow

        labRows = QtGui.QLabel("Number of rows:")
        labCols = QtGui.QLabel("Number of columns:")
        labGen = QtGui.QLabel("Number of generations:")

        startButton = QtGui.QPushButton()
        startButton.setText("Run the simulation")
        startButton.clicked.connect(self.startnewgame)

        fileButton = QtGui.QPushButton()
        fileButton.setText("Input file:")
        fileButton.clicked.connect(self.openfile)

        self.path = QtGui.QLineEdit()

        self.formy.addRow(labRows,self.rowz)
        self.formy.addRow(labCols,self.colz)
        self.formy.addRow(labGen,self.generationz)
        self.formy.addRow(fileButton,self.path)
        self.formy.addRow(startButton)

        tabelka = QtGui.QVBoxLayout()
        tabelka.addWidget(self.table)
       # tabelka.setSizeConstraint(self.table.sizeHint())

        hbox = QtGui.QHBoxLayout()  #hbox (layout) do poukladania widgetow
        hbox.addLayout(self.formy)
        hbox.addLayout(tabelka)

        mainWidget.setLayout(hbox)   #wrzucenie glownego widgeta do boxa
        mainWidget.show()

        hbox.setSizeConstraint(self.table.sizeHintForColumn(Game.cols))
        self.setCentralWidget(mainWidget)
        self.show()


    def closemyapp(self):
        wybor = QtGui.QMessageBox.question(self,'Quit',"Are you sure?",QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if wybor == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def aboutapp(self):
        str1 = "Author : T. Noga"
        str2 = "2017"
        str3 = "Made for and with educational purposes"
        QtGui.QMessageBox.about(self,"About","\t"+str1+"\n"+str3+"\n"+str2)

    def startnewgame(self):
        #wylaczenie dzialania inputow zeby nie pozmieniac nic w czasie symulacji
        self.path.setDisabled(True)
        self.rowz.setDisabled(True)
        self.colz.setDisabled(True)
        self.generationz.setDisabled(True)

        self.Life.initialfillmatrix()
        for i in range(int(self.generationz.value())):
            self.updateboard_game()
            self.Life.playGame()
            #time.sleep(0.4)
            self.updateboard_game()
            self.Life.printToFile()

        self.path.setDisabled(False)
        self.rowz.setDisabled(False)
        self.colz.setDisabled(False)
        self.generationz.setDisabled(False)

    def openfile(self):
        self.clearboard_game()
        self.Life.clearmatrix()
        self.name = QtGui.QFileDialog.getOpenFileName(self,'Select the initial data file')
        self.file = open(self.name,'r')
        Window.filepath = self.name
        self.path.setText(self.name)
        self.Life.initialfillmatrix()

        for w in range(Game.rows):  #wpisanie komorek do wspolrzednych z danych we.
            for k in range(Game.cols):
                self.table.setItem(w,k,QtGui.QTableWidgetItem(self.Life.matrix[w][k]))

        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()


    def updateboard_menu(self):
        #przepisanie wartosci ze spinboxa to klasy game
        Game.rows = self.rowz.value()
        Game.cols = self.colz.value()
        #aktualizacja rzmiaru tablicy
        self.table.setRowCount(Game.rows)
        self.table.setColumnCount(Game.cols)
        #dopasowanie rozmiaru komorki do zawartosci
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

    def board_isempty(self):
        for w in range(Game.rows):
            for k in range(Game.cols):
                if self.table.item(w,k) == "O":
                    return False
        return True

    def clearboard_game(self):
        for w in range(Game.rows):  #wpisanie komorek do wspolrzednych z danych we.
            for k in range(Game.cols):
                self.table.setItem(w,k,QtGui.QTableWidgetItem(""))

    def updateboard_game(self):
        for w in range(Game.rows):  #wpisanie komorek do wspolrzednych z danych we.
            for k in range(Game.cols):
                self.table.setItem(w,k,QtGui.QTableWidgetItem(self.Life.matrix[w][k]))


#klasa z tablica do gry i metodami odpowiedzialnymi za jej przebieg
class Game:

    # defaultowy rozmiar tablicy z gra
    rows = 10
    cols = 10

    def __init__(self):
        self.matrix = [[" " for x in range(int(self.rows))] for y in range(int(self.cols))] #deklaracja macierzy 2x2

    #stworzenie customowej tablicy do "gry"
    def __init__(self,rows,cols):
        self.rows = int(rows)
        self.cols = int(cols)
        self.matrix = [[" " for x in range(self.rows)] for y in range(self.cols)] #deklaracja macierzy 2x2

    def clearmatrix(self):
        for w in range(self.rows):
            for k in range(self.cols):
                self.matrix[w][k]=" "

    #wypelnienie komorkami tablicy po uprzednim wczytaniu z pliku
    def initialfillmatrix(self):
        # otwarcie plikow z danymi we-/wy-
        self.wejscie = open('%s' %Window.filepath, 'r')   #musi byc tak otwarte bo inaczej miksowania nie puszcza python
        with open('%s' %Window.filepath, 'r') as input_file:      #with zamiast przypisania przez open bo jest pewnosc poprawnego zamkniecia i python inaczej nie pusci petli
            for linia in input_file:
                 # zczytanie pojedynczej linii
                 linia = self.wejscie.readline()
                 # wspolrzedne o stalej konwencji, wiec mozliwy zapis na konkretnych indeksach
                 xx = linia[0:2]
                 yy = linia[3:5]
                 #konwersja na int zeby mozna bylo indeksowac elementy macierzy
                 xx = int(xx)
                 yy = int(yy)
                 self.matrix[xx][yy] = "O"
                 if 'str' in linia:
                     break

    def printMatrix(self):
        print np.matrix(self.matrix)

    def at(self,matrix,w,k):
        if w<0 | w>self.rows | k<0 | k>self.cols:
            return -1
        else:
            return matrix[w][k]

    def printToFile(self):
        wyjscie = open("danewy.txt","w")
        for x in range(int(self.rows)):     #"przejazd" po calej macierzy i wypisanie wspolrzednych do pliku danewy
            for y in range(int(self.cols)):
                if self.matrix[x][y] == "O":
                    if x<10:
                        wyjscie.write("0")
                        wyjscie.write(str(x))
                    else:
                        wyjscie.write(str(x))
                    wyjscie.write(" ")
                    if y<10:
                        wyjscie.write("0")
                        wyjscie.write(str(y))
                    else:
                        wyjscie.write(str(y))
                    wyjscie.write("\n")

    def playGame(self):

        #nalezy przepisac elementy recznie zamiast kopiowac macierz zwyklym przypisaniem
        #bo leci 'wskaznik' i dzialamy na zmienionej macierzy - tl;dr -> przestaje dzialac
        backupmatrix = [[" " for x in range(int(self.rows))] for y in range(int(self.cols))]
        for w in range(self.rows-1):
            for k in range(self.cols-1):
                backupmatrix[w][k] = self.matrix[w][k]

        for w in range(self.rows-1):
            for k in range(self.cols-1):
                neighbors = 0
                if self.at(backupmatrix,w-1,k+1) == "O": neighbors+=1
                if self.at(backupmatrix, w - 1, k) == "O": neighbors += 1
                if self.at(backupmatrix, w - 1, k-1) == "O": neighbors += 1
                if self.at(backupmatrix, w, k + 1) == "O": neighbors += 1
                if self.at(backupmatrix, w, k - 1) == "O": neighbors += 1
                if self.at(backupmatrix, w + 1, k + 1) == "O": neighbors += 1
                if self.at(backupmatrix, w + 1, k) == "O": neighbors += 1
                if self.at(backupmatrix, w + 1, k - 1) == "O": neighbors += 1

                if (self.at(backupmatrix,w,k) == "O") and (neighbors<2 or neighbors>3):
                    self.matrix[w][k]=" "
                elif (self.at(backupmatrix,w,k)== " ") and neighbors == 3:
                    self.matrix[w][k] = "O"


def run_app():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())

run_app()


