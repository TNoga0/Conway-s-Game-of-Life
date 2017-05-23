import numpy as np
import time

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


print "Gra w zycie:\n"
rows = raw_input("Podaj ilosc wierszy tablicy z gra:\n")
cols = raw_input("Podaj ilosc kolumn tablicy z gra:\n")
generations = raw_input("Podaj ilosc pokolen:\n")

Life = Game(rows,cols)
Life.initialfillmatrix()
Life.printMatrix()
for i in range(int(generations)):
    Life.playGame()
    time.sleep(0.4)
    Life.printMatrix()
Life.printToFile()

