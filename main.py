import pygame
from logic_population import Mistakes1D
from game_obj import CircleCell, DisplayInfo
import os
import imageio

pygame.init()

def matchPopulationWithGameObjs(settlement, fieldsGameObj):
    """match cells in population with screen objects """
    for i, cell in enumerate(settlement.field):
        fieldsGameObj[i].typeCircle = cell
        fieldsGameObj[i].index = i

def createScreenshot(screen, i):
    """Create screenshot """
    fname = f"screenshots/{i}.png"
    pygame.image.save(screen, fname)

def createGIFfromPyGame(fps):
    """Create gif from screenshot folder """
    folder = os.listdir("screenshots")[:-1]
    with imageio.get_writer('gifka.gif', mode='I', fps=fps) as writer:
        for i, fname in enumerate(folder):
            if i % 10 == 0: print(i)
            fname = f"screenshots/{fname}"
            image = imageio.imread(fname)
            writer.append_data(image)


def main():
    # pygame settings
    BG = (255, 255, 255)
    run = True
    screen = pygame.display.set_mode((900, 600))
    clock = pygame.time.Clock()
    # display info
    displayInfo = DisplayInfo()
    # population
    settlement = Mistakes1D(error=0.1, population=32)
    settlement.createBadField()
    # game info
    degree = 360/settlement.population
    fieldsGameObj = [CircleCell(degree) for _ in range(settlement.population)]
    matchPopulationWithGameObjs(settlement, fieldsGameObj)
    generator = settlement.generatorImitateLiveOfPopulation()
    settlementInfo = {}
    needScreenshot = False
    steps = 0
    while run:
        steps += 1

        screen.fill(BG)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        for gameObj in fieldsGameObj:
            gameObj.choosed = False
        # next generation step
        try:
            settlementInfo = next(generator)
            fieldsGameObj[settlementInfo["rndWhite"]].choosed = True
            fieldsGameObj[settlementInfo["rndBlack"]].choosed = True
            matchPopulationWithGameObjs(settlement, fieldsGameObj)
        except:
            # end of generation
            pass
        # draw all object
        for gameObj in fieldsGameObj:
            gameObj.draw(screen)
        displayInfo.draw(screen, settlementInfo["iterations"], settlementInfo["oldHappiness"],
                         settlementInfo["currentHappiness"], settlementInfo["maxHappiness"], settlement.population,
                         settlementInfo["error"])
        pygame.display.update()
        # if need screenshots
        if needScreenshot:
            createScreenshot(screen, steps)
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
    # createGIFfromPyGame(fps=60)
