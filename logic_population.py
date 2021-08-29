import random as rnd
import time
import yaml
import matplotlib.pyplot as plt

class Mistakes1D:


    def __init__(self, error, population):
        # size of population
        self.population = population
        # change error
        self.chanceError = error
        self.maxIterations = 100000
        # arrangement of cells on the field
        self.field = []
        # coordinates for white and black cells
        self.whiteCoordinates = []
        self.blackCoordinates = []
        # name of yaml data file
        self.nameYAML = "mistakes.yaml"


    def clearField(self):
        """Method for clearing class """
        self.field = []
        self.whiteCoordinates = []
        self.blackCoordinates = []


    def createRandomField(self):
        """Create a random arrangement of cells on the field """
        self.clearField()
        strFiled = f"{'w' * (self.population // 2)}{'b' * (self.population // 2)}"
        self.field = list(strFiled)
        rnd.shuffle(self.field)
        # save coordinates of cells
        for coord, cell in enumerate(self.field):
            if cell == "w":
                self.whiteCoordinates.append(coord)
            else:
                self.blackCoordinates.append(coord)


    def createBadField(self):
        """Create a field with 0 happiness """
        self.clearField()
        for i in range(self.population):
            if i % 2 == 0:
                self.field.append("w")
            else:
                self.field.append("b")
        # save coordinates of cells
        for coord, cell in enumerate(self.field):
            if cell == "w":
                self.whiteCoordinates.append(coord)
            else:
                self.blackCoordinates.append(coord)


    def getRandomCoord(self):
        """Get random coordinates """
        whiteCoord = rnd.choice(self.whiteCoordinates)
        blackCoord = rnd.choice(self.blackCoordinates)
        return whiteCoord, blackCoord


    def getNeighbours(self, coord):
        """Get neighbors by coordinates """
        neighboursCoord = [coord - 1]
        if coord + 1 == self.population:
            neighboursCoord.append(0)
        else:
            neighboursCoord.append(coord + 1)
        neighbours = [self.field[nCoord] for nCoord in neighboursCoord]
        return neighbours


    def getHappinessByCoordAndColor(self, coord, cell):
        """Calculate happiness for a coordinate and type cell
        :param coord: coordinate cell
        :param cell: type cell
        :return: happiness for cell
        """
        happiness = 0
        temporaryNeighbours = self.getNeighbours(coord)
        neighbours = []
        for neighbour in temporaryNeighbours:
            # substitute the values of neighbors
            if rnd.random() < self.chanceError:
                neighbour = "b" if neighbour == "w" else "w"
            neighbours.append(neighbour)
        for neighbour in neighbours:
            if cell == neighbour:
                happiness += 1
        return happiness


    def getFieldHappiness(self):
        """Calculate happiness for field """
        happiness = 0
        for coord, cell in enumerate(self.field):
            neighbours = self.getNeighbours(coord)
            for neighbour in neighbours:
                if cell == neighbour:
                    happiness += 1
        return happiness


    def getMaxHappiness(self):
        return (self.population - 4) * 2 + 4

    def imitateLiveOfPopulation(self):
        """Main method for generating life """
        maxHappiness = 0
        maxFieldHappiness = self.getMaxHappiness()
        iterations = 0
        while (maxFieldHappiness != maxHappiness) and (iterations < self.maxIterations):
            rndWhite, rndBlack = self.getRandomCoord()
            # calculate current happiness for random cells
            nowHappinessW = self.getHappinessByCoordAndColor(rndWhite, "w")
            nowHappinessB = self.getHappinessByCoordAndColor(rndBlack, "b")
            # calculate happiness for cells when changing location
            newHappinessW = self.getHappinessByCoordAndColor(rndBlack, "w")
            newHappinessB = self.getHappinessByCoordAndColor(rndWhite, "b")
            # swap the coordinates if  one cell will receive + happiness
            # another cell will not lose happiness
            if ((newHappinessW - nowHappinessW) >= 1 and (newHappinessB - nowHappinessB >= 0)) \
                    or ((newHappinessB - nowHappinessB) >= 1 and (newHappinessW - nowHappinessW) >= 0):
                self.field[rndWhite], self.field[rndBlack] = self.field[rndBlack], self.field[rndWhite]
                self.whiteCoordinates.remove(rndWhite)
                self.whiteCoordinates.append(rndBlack)
                self.blackCoordinates.remove(rndBlack)
                self.blackCoordinates.append(rndWhite)
            # calculate new filed happiness
            maxHappiness = self.getFieldHappiness()
            iterations += 1
        return iterations


    def testChancesMistakes(self):
        """Method for test chances error """
        chances = [0.001, 0.0015, 0.005, 0.01, 0.015, 0.02, 0.05, 0.075, 0.1, 0.125, 0.175, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
        dictChancesInfo = {}
        for chance in chances:
            self.chanceError = chance
            iterations = []
            for i in range(50):
                print(i)
                self.createBadField()
                iterations.append(self.imitateLiveOfPopulation())
            dictChancesInfo[chance] = sum(iterations) // len(iterations)
            print(f"OK {chance}")
        self.saveResultYAML(dictChancesInfo)


    def saveResultYAML(self, data):
        """Save test data in YAML """
        with open(self.nameYAML, "w", encoding="utf-8") as file:
            yaml.dump(data, file)


    def savePlotByYAML(self):
        """Create plot by YAML data file """
        with open(self.nameYAML, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        xdata = list(data.keys())
        xdata = [f"{x*100}%" for x in xdata]
        ydata = list(data.values())
        plt.bar(xdata, ydata, color='green')
        plt.xlabel("% лжи")
        plt.xticks(size=7, rotation=65)
        plt.ylabel("Итерации")
        plt.title("Зависимость итераций от % лжи")
        plt.savefig("plot.jpeg")


    def generatorImitateLiveOfPopulation(self):
        """Main method for generating life """
        maxHappiness = 0
        maxFieldHappiness = self.getMaxHappiness()
        iterations = 0
        oldHappiness = 0
        while (maxFieldHappiness != maxHappiness) and (iterations < self.maxIterations):
            wasChanged = False
            rndWhite, rndBlack = self.getRandomCoord()
            # calculate current happiness for random cells
            nowHappinessW = self.getHappinessByCoordAndColor(rndWhite, "w")
            nowHappinessB = self.getHappinessByCoordAndColor(rndBlack, "b")
            # calculate happiness for cells when changing location
            newHappinessW = self.getHappinessByCoordAndColor(rndBlack, "w")
            newHappinessB = self.getHappinessByCoordAndColor(rndWhite, "b")
            # swap the coordinates if  one cell will receive + happiness
            # another cell will not lose happiness
            if ((newHappinessW - nowHappinessW) >= 1 and (newHappinessB - nowHappinessB >= 0)) \
                    or ((newHappinessB - nowHappinessB) >= 1 and (newHappinessW - nowHappinessW) >= 0):
                wasChanged = True
                self.field[rndWhite], self.field[rndBlack] = self.field[rndBlack], self.field[rndWhite]
                self.whiteCoordinates.remove(rndWhite)
                self.whiteCoordinates.append(rndBlack)
                self.blackCoordinates.remove(rndBlack)
                self.blackCoordinates.append(rndWhite)
            oldHappiness = maxHappiness
            # calculate new filed happiness
            maxHappiness = self.getFieldHappiness()
            iterations += 1
            yield {"iterations": iterations, "wasChanged": wasChanged, "rndWhite": rndWhite, "rndBlack": rndBlack,
                   "error": self.chanceError,
                   "currentHappiness": maxHappiness, "oldHappiness": oldHappiness,
                   "maxHappiness": maxFieldHappiness}





if __name__ == "__main__":
    # a = Mistakes1D(error=0.125, population=32)
    # a.createBadField()
    # if you want to test errors
    # a.testChancesMistakes()
    # if you want to run imitation
    # a.imitateLiveOfPopulation()
    # if you want to draw a graph
    # a.savePlotByYAML()
    pass


