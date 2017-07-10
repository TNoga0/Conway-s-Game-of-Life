import numpy as np
import time
from PyQt4 import QtGui, QtCore
import sys

#klasa z glownym oknem i akcjami
class Window(QtGui.QMainWindow):

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

        # newAct = QtGui.QAction("&New Game", self)
        # newAct.setShortcut("Ctrl+N")
        # newAct.setStatusTip('Start a new simulation')
        # newAct.triggered.connect(self.gamewindow)

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

        Life = Game(Game.rows, Game.cols)
        Life.initialfillmatrix()

        table = QtGui.QTableWidget()  #stworzenie widgetu z tabela
        table.setRowCount(Game.rows)
        table.setColumnCount(Game.cols)

        # header = table.horizontalHeader()
        # for w in range(10):
        table.resizeRowsToContents()
        table.resizeColumnsToContents()

        for w in range(Game.rows):  #wpisanie komorek do wspolrzednych z danych we.
            for k in range(Game.cols):
                table.setItem(w,k,QtGui.QTableWidgetItem(Life.matrix[w][k]))

        #tworzenie widegtow z menu glownego:

        self.rowz = QtGui.QSpinBox()   #by uzywac wartosci z boxa musi byc
        self.rowz.setMinimum(1)
        self.rowz.setMaximum(20)
        self.rowz.setValue(10)
        self.rowz.setFont(QtGui.QFont("Arial",10))
        self.rowz.valueChanged.connect(self.rowzinput)

        self.colz = QtGui.QSpinBox()
        self.colz.setMinimum(1)
        self.colz.setMaximum(20)
        self.colz.setValue(10)
        self.colz.setFont(QtGui.QFont("Arial", 10))
        self.colz.valueChanged.connect(self.colzinput)

        formy = QtGui.QFormLayout()  #do poukladania pionowo inputboxow
        formy.addWidget(self.rowz)
        formy.addWidget(self.colz)


        hbox = QtGui.QHBoxLayout()  #hbox (layout) do poukladania widgetow
        hbox.addLayout(formy)
        hbox.addWidget(table)

        mainWidget.setLayout(hbox)   #wrzucenie glownego widgeta do boxa
        mainWidget.show()

        self.setCentralWidget(mainWidget)

        self.show()

    def rowzinput(self):
        Game.rows = self.rowz.value()
        print Game.rows

    def colzinput(self):
        Game.cols = self.colz.value()
        print Game.cols

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
        Life = Game(Game.rows,Game.cols)
        Life.initialfillmatrix()
        Life.printMatrix()
        for i in range(4):
            Life.playGame()
            time.sleep(0.4)
            Life.printMatrix()
        Life.printToFile()


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


    #wypelnienie komorkami tablicy po uprzednim wczytaniu z pliku
    def initialfillmatrix(self):
        # otwarcie plikow z danymi we-/wy-
        wejscie = open("danewe.txt", "r")   #musi byc tak otwarte bo inaczej miksowania nie puszcza python
        with open("danewe.txt", "r") as input_file:      #with zamiast przypisania przez open bo jest pewnosc poprawnego zamkniecia i python inaczej nie pusci petli
            for linia in input_file:
                 # zczytanie pojedynczej linii
                 linia = wejscie.readline()
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
        backupmatrix = [[" " for x in range(int(self.rows))]for y in range(int(self.cols))]
        for w in range(self.rows):
            for k in range(self.cols):
                if self.matrix[w][k] == "O":
                    counter = 0  #do zliczania ilu sasiadow ma komorka
                    if w >= 1 and k >= 1 and w<=self.rows-2 and k <= self.cols-2:
                        if self.matrix[w-1][k+1] == "O":
                            counter=counter+1
                        if self.matrix[w-1][k] == "O":
                            counter=counter+1
                        if self.matrix[w-1][k-1] == "O":
                            counter=counter+1
                        if self.matrix[w][k+1] == "O":
                            counter=counter+1
                        if self.matrix[w][k-1] == "O":
                            counter=counter+1
                        if self.matrix[w+1][k+1] == "O":
                            counter=counter+1
                        if self.matrix[w+1][k] == "O":
                            counter=counter+1
                        if self.matrix[w+1][k-1] == "O":
                            counter=counter+1
                    if w==0 and k==0:
                        if self.matrix[w+1][k+1] == "O":
                            counter = counter + 1
                        if self.matrix[w][k+1] == "O":
                            counter = counter + 1
                        if self.matrix[w+1][k] == "O":
                            counter = counter + 1
                    if w==self.rows-1 and k==self.cols-1:
                        if self.matrix[w-1][k-1] == "O":
                            counter = counter + 1
                        if self.matrix[w][k-1] == "O":
                            counter = counter + 1
                        if self.matrix[w-1][k] == "O":
                            counter = counter + 1
                    if w==0 and k==self.cols-1:
                        if self.matrix[w+1][k-1] == "O":
                            counter = counter + 1
                        if self.matrix[w+1][k] == "O":
                            counter = counter + 1
                        if self.matrix[w][k-1] == "O":
                            counter = counter + 1
                    if w==self.rows-1 and k==0:
                        if self.matrix[w][k+1] == "O":
                            counter = counter + 1
                        if self.matrix[w-1][k] == "O":
                            counter = counter + 1
                        if self.matrix[w-1][k+1] == "O":
                            counter = counter + 1
                    if counter == 0 or counter == 1:
                        backupmatrix[w][k] = " "
                    if counter == 2:
                        backupmatrix[w][k] = "O"
                    if counter >= 3:
                        backupmatrix[w][k] = " "
                elif backupmatrix[w][k] == " ":
                    counter = 0  # do zliczania ilu sasiadow ma komorka
                    if w >= 1 and k >= 1 and w <= self.rows - 2 and k <= self.cols - 2:
                        if self.matrix[w - 1][k + 1] == "O":
                            counter = counter + 1
                        if self.matrix[w - 1][k] == "O":
                            counter = counter + 1
                        if self.matrix[w - 1][k - 1] == "O":
                            counter = counter + 1
                        if self.matrix[w][k + 1] == "O":
                            counter = counter + 1
                        if self.matrix[w][k - 1] == "O":
                            counter = counter + 1
                        if self.matrix[w + 1][k + 1] == "O":
                            counter = counter + 1
                        if self.matrix[w + 1][k] == "O":
                            counter = counter + 1
                        if self.matrix[w + 1][k - 1] == "O":
                            counter = counter + 1
                    if w == 0 and k == 0:
                        if self.matrix[w + 1][k + 1] == "O":
                            counter = counter + 1
                        if self.matrix[w][k + 1] == "O":
                            counter = counter + 1
                        if self.matrix[w + 1][k] == "O":
                            counter = counter + 1
                    if w == self.rows - 1 and k == self.cols - 1:
                        if self.matrix[w - 1][k - 1] == "O":
                            counter = counter + 1
                        if self.matrix[w][k - 1] == "O":
                            counter = counter + 1
                        if self.matrix[w - 1][k] == "O":
                            counter = counter + 1
                    if w == 0 and k == self.cols - 1:
                        if self.matrix[w+1][k - 1] == "O":
                            counter = counter + 1
                        if self.matrix[w+1][k] == "O":
                            counter = counter + 1
                        if self.matrix[w][k-1] == "O":
                            counter = counter + 1
                    if w == self.rows - 1 and k == 0:
                        if self.matrix[w][k+1] == "O":
                            counter = counter + 1
                        if self.matrix[w-1][k] == "O":
                            counter = counter + 1
                        if self.matrix[w-1][k+1] == "O":
                            counter = counter + 1
                    if counter == 3:
                        backupmatrix[w][k] = "O"
        self.matrix = backupmatrix   #przepisanie tablicy


def run_app():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())


# print "Gra w zycie:\n"
# rows = raw_input("Podaj ilosc wierszy tablicy z gra:\n")
# cols = raw_input("Podaj ilosc kolumn tablicy z gra:\n")
# generations = raw_input("Podaj ilosc pokolen:\n")

run_app()

# Life = Game(rows,cols)
# Life.initialfillmatrix()
# Life.printMatrix()
# for i in range(int(generations)):
#     Life.playGame()
#     time.sleep(0.4)
#     Life.printMatrix()
# Life.printToFile()

