import pygame
import math



class CircleCell:
    """Class for one cell on the screen """
    def __init__(self, degree):
        self.typeCircle = "w"
        self.index = 0
        self.choosed = False
        self.radius = 20
        self.area = 250
        self.x = 300
        self.y = 300
        self.oneCellDegree = degree
        self.colorChoosed = (4, 12, 181)


    def draw(self, screen):
        """Draw one cell """
        color = (105, 105, 105) if self.typeCircle == "w" else (240, 233, 224)
        # calculate the new coordinates of the point
        x = self.x + math.sin(self.index*self.oneCellDegree*math.pi/180) * self.area
        y = self.y + math.cos(self.index * self.oneCellDegree*math.pi/180) * self.area
        pygame.draw.circle(screen, color, (x, y), self.radius)
        # if an entity is selected, then we make a point in the center
        if self.choosed:
            pygame.draw.circle(screen, self.colorChoosed, (x, y), self.radius-10)


class DisplayInfo:
    """Class for displaying information """
    def __init__(self):
        self.fontText = pygame.font.SysFont('arial', 25)
        self.fontData = pygame.font.SysFont('arial', 15)
        self.x = 600
        self.y = 50


    def draw(self, screen, iterations=0, oldHappinness=32, newHappinness=38, maxHappinness=60, population=32, error=0):
        """Draw all info on the screen """
        status = ""
        if newHappinness == maxHappinness:
            status = "Счастье максимально"
        elif oldHappinness < newHappinness:
            status = "Счастье увеличилось"
        elif oldHappinness > newHappinness:
            status = "Счастье уменьшилось"
        elif oldHappinness == newHappinness:
            status = "Счастье не изменилось"

        screen.blit(self.fontText.render(f"Итераций: {iterations}", True, (0, 0, 0)), (self.x, self.y))
        screen.blit(self.fontText.render(f"Счастье: {newHappinness} (из {maxHappinness})", True, (0, 0, 0)), (self.x, self.y+45))
        screen.blit(self.fontText.render(f"Популяция: {population}", True, (0, 0, 0)), (self.x, self.y+90))
        screen.blit(self.fontText.render(f"Шанс ошибки: {error*100}%", True, (0, 0, 0)), (self.x, self.y+135))
        screen.blit(self.fontText.render(status, True, (0, 0, 0)), (self.x, self.y+180))



