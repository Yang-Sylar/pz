import sunflower
import zombiebase
import peashooter
import image
import pygame
import data_object
import time
import random
from const import *

class Game(object):
    def __init__(self, ds):
        self.ds = ds
        self.back = image.Image(PATH_BACK, 0, (0, 0), GAME_SIZE, 0)
        self.plants = []
        self.summons = []
        self.zombies = []
        self.hasPlant = []
        self.gold = 100
        self.goldFont = pygame.font.Font(None, 60)
        self.zombieGeneratetime = 0
        for i in range(GRID_COUNT[0]):
            col = []
            for j in range(GRID_COUNT[1]):
                col.append(0)
            self.hasPlant.append(col)

    def renderFont(self):
        textImage = self.goldFont.render("Gold:" + str(self.gold), True, (0, 0, 0))
        self.ds.blit(textImage, (13, 23))

        textImage = self.goldFont.render("Gold:" + str(self.gold), True, (255, 255, 255))
        self.ds.blit(textImage, (10, 20))

    def draw(self):
        self.back.draw(self.ds)
        for plant in self.plants:
            plant.draw(self.ds)
        for summon in self.summons:
            summon.draw(self.ds)
        for zombie in self.zombies:
            zombie.draw(self.ds)
        self.renderFont()

    def update(self):
        self.back.update()
        for plant in self.plants:
            plant.update()
            if plant.hasSummon():
                summ = plant.doSummon()
                self.summons.append(summ)

        for summon in self.summons:
            summon.update()
        for zombie in self.zombies:
            zombie.update()

        if time.time() - self.zombieGeneratetime > ZOMBIE_BORN_CD:
            self.zombieGeneratetime = time.time()
            self.addZombie(ZOMBIE_BORN_X, random.randint(0, GRID_COUNT[1] - 1))
        
        self.checkSummonVSZombie()

    
    def checkSummonVSZombie(self):
        for summon in self.summons:
            for zombie in self.zombies:
                if (summon.isCollide(zombie)):
                    self.fight(summon, zombie)
                    if zombie.hp <= 0:
                        self.zombies.remove(zombie)
                    if summon.hp <= 0:
                        self.summons.remove(summon)
                    return

    def fight(self, a, b):
        while True:
            a.hp -= b.attack
            b.hp -= a.attack
            if b.hp <= 0:
                return True
            if a.hp <= 0:
                return False
        return False

    def getIndexByPos(self, pos):
        x = (pos[0] - LEFT_TOP[0]) // GRID_SIZE[0]
        y = (pos[1] - LEFT_TOP[1]) // GRID_SIZE[1]
        return x, y

    def addZombie(self, x, y):
        pos = (LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1])
        sf = zombiebase.ZombieBase(1, pos)
        self.zombies.append(sf)

    def addSunFlower(self, x, y):
        self.hasPlant[x][y] = 1
        pos = (LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1])
        sf = sunflower.SunFlower(SUNFLOWER_ID, pos)
        self.plants.append(sf)

    def addPeaShooter(self, x, y):
        self.hasPlant[x][y] = 1
        pos = (LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1])
        sf = peashooter.PeaShooter(PEASHOOTER_ID, pos)
        self.plants.append(sf)

    def checkLoot(self, mousePos):
        for summon in self.summons:
            if not summon.canLoot():
                continue
            rect = summon.getRect()

            if rect.collidepoint(mousePos):
                self.summons.remove(summon)
                self.gold += summon.getPrice()
                return True
        
        return False

    def checkAddPlant(self, mousePos, objid):
        x, y = self.getIndexByPos(mousePos)
        if (x < 0 or x >= GRID_COUNT[0] or y < 0 or y >= GRID_COUNT[1]):
            return 
        if self.gold < data_object.data[objid]['PRICE']:
            return 
        if self.hasPlant[x][y] == 1:
            return
        self.gold -= data_object.data[objid]['PRICE']
        if objid == SUNFLOWER_ID:
            self.addSunFlower(x, y)
        elif objid == PEASHOOTER_ID:
            self.addPeaShooter(x, y)

    def mouseClickHandler(self, btn):
        mousePos = pygame.mouse.get_pos()
        if self.checkLoot(mousePos):
            return 
        
        if btn == 1:
            self.checkAddPlant(mousePos, SUNFLOWER_ID)
        elif btn == 3:
            self.checkAddPlant(mousePos, PEASHOOTER_ID)