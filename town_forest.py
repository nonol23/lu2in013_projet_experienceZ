# BY Noriane LABIAD & Elodie ZHANG

import sys
import datetime
from random import *
import math
import time
import pygame
from pygame.locals import *

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
###
### PARAMETERS: simulation
###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# all values are for initialisation. May change during runtime.
nbTrees = 100 #350
nbGrass = 800 #15
nbZombies = 5
nbScientists = 15
nbSurvivors = 15
nbPig = 15
nbRabbit = 15
nbSheep = 15
nbWolf = 10  
nbAnimalZ = 0
nbStores = 10
nbLabo = 3
nbCloud = 50
temperature = 10

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
###
### PARAMETERS: rendering
###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# display screen dimensions
screenWidth = 1400 # 1400
screenHeight = 900 #900

# world dimensions (ie. nb of cells in total)
worldWidth = 64#64
worldHeight = 64#64

# set surface of displayed tiles (ie. nb of cells that are rendered) -- must be superior to worldWidth and worldHeight
viewWidth = 64 #32
viewHeight = 64 #32

scaleMultiplier = 0.20 # re-scaling of loaded images

objectMapLevels = 20 # number of levels for the objectMap. This determines how many objects you can pile upon one another.

# set scope of displayed tiles
xViewOffset = 0
yViewOffset = 0

addNoise = False

maxFps = 30 # set up maximum number of frames-per-second

verbose = False # display message in console on/off
verboseFps = True # display FPS every once in a while

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
###
### setting up Pygame/SDL
###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

pygame.init()
#pygame.key.set_repeat(5,5)
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screenWidth, screenHeight), DOUBLEBUF)
pygame.display.set_caption('TownForest City')

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
###
### CORE/USER: Image management
###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def loadImage(filename):
    global tileTotalWidthOriginal,tileTotalHeightOriginal,scaleMultiplier
    image = pygame.image.load(filename).convert_alpha()
    image = pygame.transform.scale(image, (int(tileTotalWidthOriginal*scaleMultiplier), int(tileTotalHeightOriginal*scaleMultiplier)))
    return image

def loadAllImages():
    global tileType, objectType, agentType, buildingType, spatialType

    tileType = []
    objectType = []
    agentType = []
    buildingType = []
    spatialType = []

    tileType.append(loadImage('assets/basic111x128/platformerTile_48_ret.png')) # grass
    tileType.append(loadImage('assets/basic111x128/platformerTile_33.png')) # brick
    tileType.append(loadImage('assets/basic111x128/platformerTile_12.png')) # neige
    tileType.append(loadImage('assets/basic111x128/platformerTile_09.png')) # neige

    objectType.append(None) # default -- never drawn
    objectType.append(loadImage('assets/basic111x128/tree1.png')) # normal tree
    objectType.append(loadImage('assets/basic111x128/fire.png')) # burning tree
    objectType.append(loadImage('assets/basic111x128/snowtree.png')) # arbre enneige
    objectType.append(loadImage('assets/basic111x128/corpse.png')) #cadavre animal
    objectType.append(loadImage('assets/basic111x128/corpse_z.png')) #cadavre zombie

    agentType.append(None) # default -- never drawn
    agentType.append(loadImage('assets/basic111x128/girl.png')) # human
    agentType.append(loadImage('assets/basic111x128/zombie.png')) # zombie
    agentType.append(loadImage('assets/basic111x128/rabbit.png')) # lapin
    agentType.append(loadImage('assets/basic111x128/pig.png')) # cochon
    agentType.append(loadImage('assets/basic111x128/sheep.png')) # mouton
    agentType.append(loadImage('assets/basic111x128/wolf.png')) # loup
    agentType.append(loadImage('assets/basic111x128/scientist.png')) # scientifique
    agentType.append(loadImage('assets/basic111x128/animal_z.png')) # animal zombie
    
    buildingType.append(None)
    buildingType.append(loadImage('assets/basic111x128/cafe_a.png')) # store
    buildingType.append(loadImage('assets/basic111x128/hospital_a.png')) # hopital
    buildingType.append(loadImage('assets/basic111x128/decor.png')) # decor1
    buildingType.append(loadImage('assets/basic111x128/grass.png')) # herbe
    buildingType.append(loadImage('assets/basic111x128/fire2.png')) # little fire
    buildingType.append(loadImage('assets/basic111x128/building_small_gray_a.png')) # decor1
    buildingType.append(loadImage('assets/basic111x128/buildingTiles_045.png')) # decor1
    buildingType.append(loadImage('assets/basic111x128/building_small_gray_a_damaged.png')) # decor1
    buildingType.append(loadImage('assets/basic111x128/building_small_red_a_damaged.png')) # decor1
    buildingType.append(loadImage('assets/basic111x128/hospital_a_damaged.png')) # decor1
    buildingType.append(loadImage('assets/basic111x128/cafe_a_damaged.png')) # decor1
    buildingType.append(loadImage('assets/basic111x128/Trash.png')) # decor1
    
    
    spatialType.append(None)
    spatialType.append(loadImage('assets/basic111x128/cloud.png')) # nuage
    spatialType.append(loadImage('assets/basic111x128/rain.png')) # pluie
    spatialType.append(loadImage('assets/basic111x128/snow.png')) # neige

def resetImages():#for tiles
    global tileTotalWidth, tileTotalHeight, tileTotalWidthOriginal, tileTotalHeightOriginal, scaleMultiplier, heightMultiplier, tileVisibleHeight
    tileTotalWidth = tileTotalWidthOriginal * scaleMultiplier  # width of tile image, as stored in memory
    tileTotalHeight = tileTotalHeightOriginal * scaleMultiplier # height of tile image, as stored in memory
    tileVisibleHeight = tileVisibleHeightOriginal * scaleMultiplier # height "visible" part of the image, as stored in memory
    heightMultiplier = tileTotalHeight/2 # should be less than (or equal to) tileTotalHeight
    loadAllImages()
    return

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
###
### CORE: objects parameters
###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# spritesheet-specific -- as stored on the disk ==> !!! here, assume 128x111 with 64 pixels upper-surface !!!
# Values will be updated *after* image loading and *before* display starts
tileTotalWidthOriginal = 111  # width of tile image
tileTotalHeightOriginal = 128 # height of tile image
tileVisibleHeightOriginal = 64 # height "visible" part of the image, i.e. top part without subterranean part

###

tileType = []
objectType = []
agentType = []
buildingType = []
spatialType = []

noObjectId = noAgentId = 0
###

# re-scale reference image size -- must be done *after* loading sprites
resetImages()

###

terrainMap = [x[:] for x in [[0] * worldWidth] * worldHeight]
heightMap  = [x[:] for x in [[0] * worldWidth] * worldHeight]
objectMap = [ [ [ 0 for i in range(worldWidth) ] for j in range(worldHeight) ] for k in range(objectMapLevels) ]
agentMap   = [x[:] for x in [[0] * worldWidth] * worldHeight]
buildingMap = [ [ [ 0 for i in range(worldWidth) ] for j in range(worldHeight) ] for k in range(objectMapLevels) ]
spatialMap = [ [ [ 0 for i in range(worldWidth) ] for j in range(worldHeight) ] for k in range(objectMapLevels) ]

###

# set initial position for display on screen
xScreenOffset = screenWidth/2 - tileTotalWidth/2
yScreenOffset = 3*tileTotalHeight # border. Could be 0.

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### CORE: get/set methods
###
###

def getWorldWidth():
    return worldWidth

def getWorldHeight():
    return worldHeight

def getViewWidth():
    return viewWidth

def getViewHeight():
    return viewHeight

def getTerrainAt(x,y):
    return terrainMap[y][x]

def setTerrainAt(x,y,type):
    terrainMap[y][x] = type

def getHeightAt(x,y):
    return heightMap[y][x]

def setHeightAt(x,y,height):
    heightMap[y][x] = height

def getObjectAt(x,y,level=0):
    if level < objectMapLevels:
        return objectMap[level][y][x]
    else:
        print ("[ERROR] getObjectMap(.) -- Cannot return object. Level does not exist.")
        return 0

def setObjectAt(x,y,type,level=0): # negative values are possible: invisible but tangible objects (ie. no display, collision)
    if level < objectMapLevels:
        objectMap[level][y][x] = type
    else:
        print ("[ERROR] setObjectMap(.) -- Cannot set object. Level does not exist.")
        return 0

def getAgentAt(x,y):
    return agentMap[y][x]

def setAgentAt(x,y,type):
    agentMap[y][x] = type
    
def getBuildingAt(x,y,level=0):
    if level < objectMapLevels:
        return buildingMap[level][y][x]
    else:
        print ("[ERROR] getObjectMap(.) -- Cannot return object. Level does not exist.")
        return 0

def setBuildingAt(x,y,type,level=0): # negative values are possible: invisible but tangible objects (ie. no display, collision)
    if level < objectMapLevels:
        buildingMap[level][y][x] = type
    else:
        print ("[ERROR] setObjectMap(.) -- Cannot set object. Level does not exist.")
        return 0
    
def getSpatialAt(x,y,level):
    return spatialMap[level][y][x]
    

def setSpatialAt(x,y,type,level): # negative values are possible: invisible but tangible objects (ie. no display, collision)
    if level < objectMapLevels:
        spatialMap[level][y][x] = type
    else:
        print ("[ERROR] setObjectMap(.) -- Cannot set object. Level does not exist.")
        return 0

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### CORE: rendering
###
###

def render( it = 0 , time_of_day = 0):
    global xViewOffset, yViewOffset
    if 8 <= time_of_day < 20:
        pygame.draw.rect(screen, (135, 206, 235), (0, 0, screenWidth, screenHeight), 0) # overkill - can be optimized. (most sprites are already "naturally" overwritten)
    else :
        pygame.draw.rect(screen, (5, 1, 74), (0, 0, screenWidth, screenHeight), 0)
    #pygame.display.update()

    for y in range(getViewHeight()):
        for x in range(getViewWidth()):
            # assume: north-is-upper-right

            xTile = ( xViewOffset + x + getWorldWidth() ) % getWorldWidth()
            yTile = ( yViewOffset + y + getWorldHeight() ) % getWorldHeight()

            heightNoise = 0
            if addNoise == True: # add sinusoidtileType.append(loadImage('assets/basic111x128/Stone.png')) # betonal noise on height positions
                if it%int(math.pi*2*199) < int(math.pi*199):
                    # v1.
                    heightNoise = math.sin(it/23+yTile) * math.sin(it/7+xTile) * heightMultiplier/10 + math.cos(it/17+yTile+xTile) * math.cos(it/31+yTile) * heightMultiplier
                    heightNoise = math.sin(it/199) * heightNoise
                else:
                    # v2self.speed = 2.
                    heightNoise = math.sin(it/13+yTile*19) * math.cos(it/17+xTile*41) * heightMultiplier
                    heightNoise = math.sin(it/199) * heightNoise

            height = getHeightAt( xTile , yTile ) * heightMultiplier + heightNoise

            xScreen = xScreenOffset + x * tileTotalWidth / 2 - y * tileTotalWidth / 2
            yScreen = yScreenOffset + y * tileVisibleHeight / 2 + x * tileVisibleHeight / 2 - height

            ######   AFFICHAGE SOL
            if neiger:#temperature <= 0 :
                screen.blit( tileType[2] , (xScreen, yScreen))
            else : 
                if(y<getViewHeight()//2) :
                    screen.blit( tileType[0] , (xScreen, yScreen)) # display terrain
                else:
                    screen.blit( tileType[1] , (xScreen, yScreen)) # display terrain
            #######
            for level in range(objectMapLevels):
                if getObjectAt( xTile , yTile , level)  > 0: # object on terrain?
                    screen.blit( objectType[ getObjectAt( xTile , yTile, level) ] , (xScreen, yScreen - heightMultiplier*(level+1) ))
                    
                if getBuildingAt( xTile , yTile , level)  > 0: # object on terrain?
                    screen.blit( buildingType[ getBuildingAt( xTile , yTile, level) ] , (xScreen, yScreen - heightMultiplier*(level+1) ))

            if getAgentAt( xTile, yTile ) != 0: # agent on terrain?
                screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))
                
            ####affichage nuage
            for level in range(objectMapLevels):
                if getSpatialAt( xTile , yTile , level)  > 0: # object on terrain?
                    screen.blit( spatialType[ getSpatialAt( xTile , yTile, level) ] , (xScreen, yScreen - heightMultiplier*(level+1) ))

    return

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### Agents
###
###

#### agents 
agents = []
zombie_l = []
animalZ_l = []
human_l = []
scientists_l = []
survivors_l = []
animal_l = []
rabbit_l = []
pig_l = []
sheep_l = []
wolf_l = []
dead_a_l = []
dead_z_l = []
nb_food = 0

##### environnement
stores_l = []
groceries_l = []
laboratory_l = []
decorx = []
decory = []
cloud_l = []
rain_l = []
snow_l = []
grass_l = []
tree_l = []
trash_l = []

class Zombie:
    
    def __init__(self, pos_x, pos_y) : #constructeur de la classe zombie
        self.health = randint(50,90) #points de vie
        self.health_max = 100 #plafond des points de vie
        self.attack = 20 #points d'attaque
        self.speed = 3 #niveau de vitesse
        self.cooldown_attack = 0 #cooldown apres une attaque
        self.type = 2 #le type de l'agent
        self.image = pygame.image.load('assets/basic111x128/zombie.png') #le png
        if((pos_x == None) and (pos_y == None)) : #on veut un zombie
            self.reset() #donne des coordonnees aleatoires
        else : #un humain est devenu zombie donc les coordonnées passer en param sont les anciennes de l'humain
            self.x = pos_x
            self.y = pos_y
        return
            
    def getX(self) : 
        return self.x
    
    def getY(self) :
        return self.y
    
        

    def death(self) : #mort lorsque l'humain le tue
        if self.health <= 0 : 
            dead_z_l.append(self) #on l'ajoute a la liste de zombie mort
            zombie_l.remove(self) #on retire le zombie de la liste de zombie
            setObjectAt(self.x,self.y,5,0) #on fait apparaitre le cadavre 
            
        return


    def attack_human(self,human) : #fonction d'attaque sur les humains
        if self.cooldown_attack == 0 : #si il n'a pas attaquer recemment il peut attaquer
            if random() < 0.6 : #60% de chance d'attaquer
                human.health -= self.attack
                self.cooldown_attack = 50 #plus le droit d'attaquer pendant un certain nombre d'iteration
                #human.death_h()
            return 
        return
    
    def attack_animal(self,animal) :  #fonction d'attaque sur les animaux
         if self.cooldown_attack == 0 :
            if random() < 0.3 :
                animal.health -= self.attack
                self.cooldown_attack = 50
                #animal.death_a_to_az()
            return 
            

    def healing(self, pos_x, pos_y) : #guerison lorsque le sérum sera prêt
        human_l.append(Human(pos_x,pos_y)) #redeviens humain
        zombie_l.remove(self) 
        return


    def mutation(self) : #mutation lorsque le nombre d'humains est 4 fois plus elever
        if len(human_l)/4 >= len(zombie_l) :
            self.speed = 6
            self.attack = 50
        else :
            self.speed = 3
            self.attack = 20


    def follow_human(self): #fonction de poursuite d'humain
        for h in human_l: #on parcourt la liste d'humain
            if h.getX() == self.getX() and h.getY() == self.getY(): #si ils se trouvent sur la mm case ils s'attaquent
                h.attack_zombie(self)
                self.attack_human(h)
                h.death_h()
                self.death()
                if self.cooldown_attack > 0 : #on decremente
                    self.cooldown_attack -= 1
                return
            else:
                if abs(h.getX() - self.getX()) <= 4 and abs(h.getY() - self.getY()) <= 4 : #verifie si l'humain est a un perimetre de 4 cases
                    if abs(h.getX() - self.getX()) <= 4: #verifie si l'humain est a une distance de 4 cases sur x
                        if h.getX() != self.getX() : #si X diff du zombie on avance sur X
                            if random() < (self.speed)/10 : 
                                if h.getX() < self.getX():
                                    xNew = (self.x - 1 + getWorldWidth()) % getWorldWidth()
                                    yNew = self.y
                                elif h.getX() > self.getX():
                                    xNew = (self.x + 1 + getWorldWidth() ) % getWorldWidth()
                                    yNew = self.y
                                if(getObjectAt(xNew,yNew)==0) : #ne bouge pas si se cogne à un objet
                                    setAgentAt(self.x,self.y,0)
                                    self.x = xNew
                                    self.y = yNew
                                    setAgentAt(self.x,self.y,self.type)
                                if self.cooldown_attack > 0 : #on decremente
                                    self.cooldown_attack -= 1
                                return 
                        else : #sinon on va sur Y
                            if h.getY() != self.getY() : #si Y diff du zombie on avance sur Y
                                if random() < (self.speed)/10 : 
                                    if h.getY() < self.getY():
                                        yNew = (self.y - 1 + getWorldHeight()) % getWorldHeight()
                                        xNew = self.x
                                    elif h.getY() > self.getY():
                                        yNew = (self.y + 1 + getWorldHeight()) % getWorldHeight()
                                        xNew = self.x
                                    if(getObjectAt(xNew,yNew)==0) : #ne bouge pas si se cogne à un objet
                                        setAgentAt(self.x,self.y,0)
                                        self.x = xNew
                                        self.y = yNew
                                        setAgentAt(self.x,self.y,self.type)
                                    if self.cooldown_attack > 0 : #on decremente
                                        self.cooldown_attack -= 1
                                    return   

        self.move() #si aucun humain n'est trouvé dans le champ de vision, se déplacer aléatoirement
        return
       


    def raining(self) : #si il pleut le zombie est plus lent
        if pleuvoir :
            self.speed = 1
            self.attack = 20
        else : 
            self.speed = 3
            self.attack = 20           

    def move(self) : #fonction reprise en partie, fonction de mouvement
        xNew = self.x
        yNew = self.y 
        if random() < (self.speed/10) :
            if random() < 0.8 : #80% de chance d'aller tout droit, les zombies ont une vision rétréci
                xNew = ( self.x + [-1,+1][randint(0,1)] + getWorldWidth() ) % getWorldWidth()
            else : 
                yNew = ( self.y + [-1,+1][randint(0,1)] + getWorldHeight() ) % getWorldHeight()
        if(getObjectAt(xNew,yNew)==0) : #ne bouge pas si se cogne à un objet
                setAgentAt(self.x,self.y,0)
                self.x = xNew
                self.y = yNew
                setAgentAt(self.x,self.y,self.type)
        return 


    def reset(self): #fonction reprise, elle donne des coordonnees aleatoires
        self.x = randint(0,getWorldWidth()-1)
        self.y = randint(getWorldWidth()//2,getWorldWidth()-1)
        while getTerrainAt(self.x,self.y) != 0 or getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
            self.x = randint(0,getWorldWidth()-1)
            self.y = randint(getWorldWidth()//2,getWorldWidth()-1)
        setAgentAt(self.x,self.y,self.type)
        return


class Human: 
    
    def __init__(self, pos_x, pos_y) :  #constructeur 
        self.health = randint(10,60) #attribut des pdv entre 10 et 60 a l'initialisation
        self.health_max = 100 #pdv max
        self.speed = 5 #vitesse
        self.attack = 20 #points d'attaque
        self.cooldown = 0 #cooldown pour la reproduction
        self.cooldown_attack = 0 #cooldown pour l'attaque
        self.type = 1 #type de l'agent
        self.image = pygame.image.load('assets/basic111x128/girl.png') #le png
        if (pos_x == None) and (pos_y == None) : #si pas de coordonnees
            self.reset() #coordonnees donner aleatoirement
        else : #sinon cela veut dire qu'on veut un zombie qui redevient humain donc les coordonnées en param sont les anciennes du zombie 
            self.x = pos_x                
            self.y = pos_y
        
            
    def death_h(self) : #fonction de mort
        if self.health <= 0 : 
            if isinstance(self,Survivor) :
                self.death_sv() 
            if isinstance(self, Scientist) :
                self.death_sc()
        return
            
    def reproduce_human(self) : #fonction de reproduction
        if self.cooldown == 0 : 
            for h in human_l : #on parcourt la liste'dhumain
                if self is h and h.cooldown == 0 : #si ils sont de la meme instance 
                    if h!= self and h.getX()==self.getX() and h.getY()==self.getY() : #et sur la mm case
                        if random() < 0.1 : #10% de chance de se reproduire
                            if isinstance(h,Survivor) : 
                                new = Survivor(self.getX(), self.getY())
                                human_l.append(new)
                                survivors_l.append(new)
                                #mets tout les cooldown a 100, pour eviter qu'ils se reproduisent infiniment
                                new.cooldown = 100
                                self.cooldown = 100
                                h.cooldown = 100
                                return
                            if isinstance(h,Scientist) : 
                                new = Scientist(self.getX(), self.getY())
                                human_l.append(new)
                                scientists_l.append(new)
                                new.cooldown = 100
                                self.cooldown = 100
                                h.cooldown = 100
                                return
        return
                
        
    def attack_zombie(self, zombie) :  #fonction d'attaque les zombies 
        if self.cooldown_attack == 0 : 
            if random() < 0.6 : #60% de chance d'attaquer un zombie 
                zombie.health -= self.attack
                self.cooldown_attack = 100 #ne peut pas attaquer pendant certains nombre d'iteration
                #zombie.death()
                return
        return
        

            
    def attack_animal(self,animal) : #fonction d'attaque des animaux
        if self.health < 50 :  #ne peut les attaquer que si ses pdv sont inferieur 50
            if random() < 0.6 : 
                animal.health = animal.health - self.attack 
                #animal.death()
        else : 
            if random() <0.3 :
                animal.health = animal.health - self.attack
        return
    
    def attack_wolf(self,wolf) : #fonction d'attaque pour le loup
        if random() < 0.15 : 
            wolf.health = wolf.health - self.attack      
        return
     
             
    def getX(self) : 
        return self.x
    
    def getY(self) :
        return self.y
         
    def eat(self, animal, groceries) : #manger un animal ou un produit de la superette
        if animal == None : #produit de la superette
            if self.health < self.health_max : #si les pdv ne sont pas au max on ajoute les points de la nourriture
                self.health = self.health + groceries
                if self.health >= self.health_max : #sinon on n'ajoute rien
                    self.health = self.health_max
                return
        if groceries == None : #animal
            if animal.health <= 0: #les pdv sont a 0 => l'animal est mort
                if self.health < self.health_max : #l'animal est mangé
                    self.health = self.health + animal.point
                    if self.health >= self.health_max : #sinon on ne fait rien
                        self.health = self.health_max
                        return
        return 


    def piller(self, s): #piller les superettes
        if self.health < self.health_max : #on mange un produit
            if self.getX() == s.getX() and self.getY() == s.getY() and s.groceries_l != []: #si l'humain se trouve sur la meme case qu'une superette
                self.eat(None, s.groceries_l[len(groceries_l)]) #l'humain mange le dernier de la liste
                s.groceries_l.pop()  #enlève le dernier de la liste
        return 


    def winter(self) : #en hiver les humains deviennent plus lent
        if temperature <= 0 : 
            self.health = self.health - 1
            self.speed = 1
        else :
            self.speed = 5
            
    

    def move(self) : #fonction en partie reprise, fonction de mouvements
        xNew = self.x
        yNew = self.y
        if nb_food == 0 : #il n'y a plus de nourriture en ville donc ils vont dans la foret pour les animaux
            if yNew > (getWorldHeight()//2) -1 :
                yNew = ( self.y + (-1) + getWorldHeight() ) % getWorldHeight()
            else :
                if random() < (self.speed/10) : #vitesse
                    if random() < 0.5 : #probabilité de 40% d'avancer sur x
                        xNew = ( self.x + [-1,+1][randint(0,1)] + getWorldWidth() ) % getWorldWidth() 
                    else : 
                        yNew = ( self.y + [-1,+1][randint(0,1)] + getWorldHeight()) % getWorldHeight()
            
                else : 
                    xNew = self.x
                    yNew = self.y
        else : 
            if random() < (self.speed/10) :
                if random() < 0.5 : #probabilité de 50% d'avancer sur x
                    xNew = ( self.x + [-1,+1][randint(0,1)] + getWorldWidth() ) % getWorldWidth() 
                else : 
                    yNew = ( self.y + [-1,+1][randint(0,1)] + getWorldHeight() ) % getWorldHeight()
            else : 
                xNew = self.x
                yNew = self.y

        if(getObjectAt(xNew,yNew)==0) : #ne bouge pas si se cogne à un objet
            setAgentAt(self.x,self.y,0)
            self.x = xNew
            self.y = yNew
            setAgentAt(self.x,self.y,self.type) 
    
        if self.cooldown > 0 : #decremente le cooldown de la reproduction
            self.cooldown = self.cooldown - 1 

        if self.cooldown_attack > 0 : #decremente le cooldown de l'attaquer
            self.cooldown_attack -= 1

        return


    def reset(self): #fonction reprise
        self.x = randint(0,getWorldWidth()-1)
        self.y = randint(getWorldWidth()/2,getWorldWidth()-1)
        while getTerrainAt(self.x,self.y) != 0 or getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
            self.x = randint(0,getWorldWidth()-1)
            self.y = randint(getWorldWidth()/2,getWorldWidth()-1)
        setAgentAt(self.x,self.y,self.type)
        return


class Survivor(Human) : #classe survivants herite de la classe Human

        def __init__(self, pos_x, pos_y) : #constructeur
            super().__init__(pos_x, pos_y) #appelle le constructeur de Human
            self.type = 1 #type de l'agent
            self.image = pygame.image.load('assets/basic111x128/girl.png')
            self.attack = 40 #les survivants ont une capacite d'attaque plus elever que les scientifiques

        
        def death_sv(self): #fonction de mort
            if self.health <= 0:
                if self in human_l: #on verifie que c'est dans la liste avant pour ne pas provoquer d'erreur
                    human_l.remove(self)
                if self in survivors_l:
                    survivors_l.remove(self)
                zombie_l.append(Zombie(self.getX(), self.getY())) #il devient un zombie des qu'il meurt


        def run_to_store(self) : #fonction pour aller vers les superettes
            if self.health < self.health_max :
                for s in stores_l : #on parcourt la liste des superettes
                    if s.groceries_l != [] : 
                        if abs(s.getX() - self.getX()) <= 5 and abs(s.getY() - self.getY()) <=5 : #verifie si la superette est dans un perimetre de 5 cases 
                            if abs(s.getX() - self.getX()) <= 5: #verifie si la superette est a une distance de 5 cases sur x
                                if s.getX() != self.getX() : #si X diff de la superette on avance sur x
                                    if s.getX() < self.getX():
                                        xNew = (self.x - 1 + getWorldWidth()) % getWorldWidth()
                                        yNew = self.y
                                    elif s.getX() > self.getX():
                                        xNew = (self.x + 1 + getWorldWidth() ) % getWorldWidth()
                                        yNew = self.y
                                    if(getObjectAt(xNew,yNew)==0) : #ne bouge pas si se cogne à un objet
                                        setAgentAt(self.x,self.y,0)
                                        self.x = xNew
                                        self.y = yNew
                                        setAgentAt(self.x,self.y,self.type)
                                        
                                    if self.cooldown > 0 : #decremente le cooldown de la reproduction
                                        self.cooldown = self.cooldown - 1 

                                    if self.cooldown_attack > 0 : #decremente le cooldown de l'attaquer
                                        self.cooldown_attack -= 1
                                    return
                                
                                else : #sinon on va sur Y
                                    if s.getY() != self.getY() : #si Y diff de la superette
                                        if s.getY() < self.getY():
                                            yNew = (self.y - 1 + getWorldHeight()) % getWorldHeight()
                                            xNew = self.x
                                        elif s.getY() > self.getY():
                                            yNew = (self.y + 1 + getWorldHeight()) % getWorldHeight()
                                            xNew = self.x
                                        if(getObjectAt(xNew,yNew)==0) : #ne bouge pas si se cogne à un objet
                                            setAgentAt(self.x,self.y,0)
                                            self.x = xNew
                                            self.y = yNew
                                            setAgentAt(self.x,self.y,self.type)
                                            
                                        if self.cooldown > 0 : #decremente le cooldown de la reproduction
                                            self.cooldown = self.cooldown - 1 

                                        if self.cooldown_attack > 0 : #decremente le cooldown de l'attaquer
                                            self.cooldown_attack -= 1
                                            
                                        return 



            self.move() #si aucune superette n'est trouvé on avance aleatoirement
            return


class Scientist(Human) : #classe scientifique qui herite de Human

    def __init__(self, pos_x, pos_y) : #constructeur
        super().__init__(pos_x, pos_y) #appelle le constructeur de Human
        self.type = 7 #le type de l'agent
        self.image = pygame.image.load('assets/basic111x128/scientist.png') #le png
        self.antidote = 0 #nombre d'antidote que le scientifique possede
        self.cooldown_antidote = 0 #cooldown pour la creation d'antidote

    
    def death_sc(self): #fonction de la mort du scientifique
        if self.health <= 0:
            if self in human_l:
                human_l.remove(self)
            if self in survivors_l:
                scientists_l.remove(self)
            zombie_l.append(Zombie(self.getX(), self.getY()))



    def make_antidote(self): #fonction pour faire l'antidote
        #shuffle(laboratory_l)
        if self.cooldown_antidote == 0 :
            for labo in laboratory_l : #on parcourt la liste des labos
                if self.getX() == labo.getX() and self.getY() == labo.getY() : #si se trouvent sur la mm case
                    if self.antidote == 0 : #le scientifique n'a pas d'antidote sur lui
                        if random() < 0.05 : #alors il a 5% de chance d'en faire un car il n'a pas d'exemple
                            self.antidote += 5 #il en fabrique 5
                            self.cooldown_antidote = 300
                    else : #si il a des antidotes sur lui
                        if random() < 0.15 : #il a 15%de chance d'en faire un car il a un exemple
                            self.antidote +=2 #il en fait 2 
                            self.cooldown_antidote = 300
        return
    
    def give_antidote(self) : #administre l'antidote
        if self.antidote > 0 : #si il en a sur lui
            for z in zombie_l : #on parcourt la liste de zombies
                if self.getX() == z.getX() and self.getY() == z.getY(): #si se trouve sur la mm case 
                    self.antidote -=1
                    z.healing(z.getX(),z.getY()) #guerit le zombie


    def run_to_lab(self): #fonction de deplacement vers les labo 
        if self.cooldown_antidote == 0 :
            for l in laboratory_l: 
                if l.getX() == self.getX() and l.getY() == self.getY(): #si se trouve sur la mm case, fabrique un antidote et bouge
                    self.make_antidote()
                    self.move()
                    
                    return
                else:
                    if abs(l.getX() - self.getX()) <= 7 and abs(l.getY() - self.getY()) <=7 :
                        if abs(l.getX() - self.getX()) <= 7: #verifie si le labo est a une distance de 7 cases 
                            if l.getX() != self.getX() : #si X diff du labo, on avance sur x
                                if l.getX() < self.getX():
                                    xNew = (self.x - 1 + getWorldWidth()) % getWorldWidth()
                                    yNew = self.y
                                elif l.getX() > self.getX():
                                    xNew = (self.x + 1 + getWorldWidth() ) % getWorldWidth()
                                    yNew = self.y
                                if(getObjectAt(xNew,yNew)==0) : #ne bouge pas si se cogne à un objet
                                    setAgentAt(self.x,self.y,0)
                                    self.x = xNew
                                    self.y = yNew
                                    setAgentAt(self.x,self.y,self.type)
                                 
                                if self.cooldown > 0 : #decremente le cooldown de la reproduction
                                    self.cooldown = self.cooldown - 1    
                                
                                if self.cooldown_antidote > 0 : #decremente le cooldown de la preparation
                                    self.cooldown_antidote -= 1
                                return
                            else : #si on va sur Y
                                if l.getY() != self.getY() : #si Y diff du labo
                                    if l.getY() < self.getY():
                                        yNew = (self.y - 1 + getWorldHeight()) % getWorldHeight()
                                        xNew = self.x
                                    elif l.getY() > self.getY():
                                        yNew = (self.y + 1 + getWorldHeight()) % getWorldHeight()
                                        xNew = self.x
                                    if(getObjectAt(xNew,yNew)==0) : #ne bouge pas si se cogne à un objet
                                        setAgentAt(self.x,self.y,0)
                                        self.x = xNew
                                        self.y = yNew
                                        setAgentAt(self.x,self.y,self.type)
                                        
                                    if self.cooldown > 0 : #decremente le cooldown de la reproduction
                                        self.cooldown = self.cooldown - 1 
                                        
                                    if self.cooldown_antidote > 0 : #decremente le cooldown de la preparation
                                        self.cooldown_antidote -= 1
                                    return 



        self.move() #si aucun labo n'est trouvé dans le champ de vision, se déplacer aléatoirement
        return

        

 
class Animal : 
    
    def __init__(self) :  #constructeur
        self.health = 25 #pdv
        self.health_max = 50 #pdv max
        self.cooldown = 0 #cooldown de la reproduction
        self.cooldown_attack = 0 #cooldown de l'attaque
        self.attack = 0 #point d'attaque initialement
        self.speed = 2 #vitesse initiale

    def reset(self): #fonction reprise, coordonnees aleatoires
        self.x = randint(0,getWorldWidth()-1)
        self.y = randint(0,(getWorldWidth()//2)-1)
        while getTerrainAt(self.x,self.y) != 0 or getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
            self.x = randint(0,getWorldWidth()-1)
            self.y = randint(0,(getWorldWidth()//2)-1)
        setAgentAt(self.x,self.y,self.type)
        
        return
    
    def getX(self) : 
        return self.x
    
    def getY(self) :
        return self.y
            
    
    def attack_human(self, human) : #fonction d'attaque
        if random() < 0.15 : #15% de chance d'attaquer l'humain 
            human.health -= self.attack
            self.cooldown_attack = 250                
            #human.death_h()
        return
    
    
    def death_a(self) : #mort lorsque l'humain le tue et le mange
        if self.health <= 0 :
            if isinstance(self,Wolf) :
                self.death_wolf()
                return
            if isinstance(self,Rabbit) :
                self.death_rabbit()
                return
            if isinstance(self,Sheep) :
                self.death_sheep()
                return
            if isinstance(self,Pig) :
                self.death_pig()
                return    
        return
    
    def death_a_to_az(self) : #mort lorsqu'il est attaqué par un zombie, il en devient un aussi
        if isinstance(self,Wolf) :
            self.death_wolf_z()
            return
        if isinstance(self,Rabbit) :
            self.death_rabbit_z()
            return
        if isinstance(self,Sheep) :
            self.death_sheep_z()
            return
        if isinstance(self,Pig) :
            self.death_pig_z()
            return 


    def move(self) : #fonction en partie reprise, fonction de mouvement
        xNew = self.x
        yNew = self.y 
        if random() < self.speed/10: #pourcentage de chance d'avancer different pour chaque animal
            if random() < 0.5 :
                xNew = ( self.x + [-1,+1][randint(0,1)] + getWorldWidth() ) % getWorldWidth()
            else :
                yNew = ( self.y + [-1,+1][randint(0,1)] + (getWorldHeight()//2) +1 ) % (getWorldHeight()//2) 
        else :
            xNew = self.x
            yNew = self.y 

        if getObjectAt(xNew,yNew) == 0: # dont move if collide with object (note that negative values means cell cannot be walked on)
            setAgentAt(self.x,self.y,0)
            self.x = xNew
            self.y = yNew
            setAgentAt(self.x,self.y,self.type)
            
        if self.cooldown > 0 : #decremente le cooldown de la reproduction
            self.cooldown = self.cooldown - 1

        if self.cooldown_attack > 0 : #decremente le cooldown de l'attaque 
            self.cooldown_attack = self.cooldown_attack - 1

        return

    def run_from_human(self) : #fonction pour fuir les humains
        for h in human_l : 
            if abs(h.getX() - self.getX()) <= 3 and abs(h.getY() - self.getY()) <= 3 : #verifie si l'humain est a un perimetre de 3 cases
                if abs(h.getX() - self.getX()) <= 3: #verifie si l'humain est a une distance de 3 cases sur x
                    if h.getX() != self.getX() : #si X diff de l'humain, on avance sur X
                        if h.getX() < self.getX():
                            xNew = (self.x + 2 + getWorldWidth()) % getWorldWidth()
                            yNew = self.y
                        elif h.getX() > self.getX():
                            xNew = (self.x - 2 + getWorldWidth() ) % getWorldWidth()
                            yNew = self.y
                        if(getObjectAt(xNew,yNew)==0) : #ne bouge pas si se cogne à un objet
                            setAgentAt(self.x,self.y,0)
                            self.x = xNew
                            self.y = yNew
                            setAgentAt(self.x,self.y,self.type)
                        if self.cooldown > 0 : #decremente le cooldown de la reproduction
                            self.cooldown = self.cooldown - 1

                        if self.cooldown_attack > 0 : #decremente le cooldown de l'attaque 
                            self.cooldown_attack = self.cooldown_attack - 1
                            
                        return 
                    
                    else : #sinon on va sur Y
                        if h.getY() != self.getY() : #si Y diff de l'animal, on avance sur Y
                            if h.getY() < self.getY():
                                yNew = (self.y + 2 + getWorldHeight()) % getWorldHeight()
                                xNew = self.x
                            elif h.getY() > self.getY():
                                yNew = (self.y - 2 + getWorldHeight()) % getWorldHeight()
                                xNew = self.x
                            if(getObjectAt(xNew,yNew)==0) : #ne bouge pas si se cogne à un objet
                                setAgentAt(self.x,self.y,0)
                                self.x = xNew
                                self.y = yNew
                                setAgentAt(self.x,self.y,self.type)
                                
                            if self.cooldown > 0 : #decremente le cooldown de la reproduction
                                self.cooldown = self.cooldown - 1

                            if self.cooldown_attack > 0 : #decremente le cooldown de l'attaque 
                                self.cooldown_attack = self.cooldown_attack - 1 
                                
                            return   

        self.move() #si aucun humain n'est trouvé dans le champ de vision, se déplacer aléatoirement
        return

    def run_to_human(self) : #avance vers les humains
        if self.cooldown_attack == 0 :
            for h in human_l : 
                if abs(h.getX() - self.getX()) <= 3 and abs(h.getY() - self.getY()) <= 3 : #verifie si l'humain est a un perimetre de 3 cases
                    if abs(h.getX() - self.getX()) <= 3: #verifie si l'humain est a une distance de 3 cases 
                        if h.getX() != self.getX() : #si X diff de l'humain, on avance sur x  
                            if h.getX() < self.getX():
                                xNew = (self.x - 1 + getWorldWidth()) % getWorldWidth()
                                yNew = self.y
                            elif h.getX() > self.getX():
                                xNew = (self.x + 1 + getWorldWidth() ) % getWorldWidth()
                                yNew = self.y
                            if(getObjectAt(xNew,yNew)==0) : #ne bouge pas si se cogne à un objet
                                setAgentAt(self.x,self.y,0)
                                self.x = xNew
                                self.y = yNew
                                setAgentAt(self.x,self.y,self.type)
                                
                            if self.cooldown > 0 : #decremente le cooldown de la reproduction
                                self.cooldown = self.cooldown - 1

                            if self.cooldown_attack > 0 : #decremente le cooldown de l'attaque 
                                self.cooldown_attack = self.cooldown_attack - 1 
                                
                            return 
                        else : #sinon on avance sur Y
                            if h.getY() != self.getY() : #si Y diff de l'humain, on avance sur Y
                                if h.getY() < self.getY():
                                    yNew = (self.y - 1 + getWorldHeight()) % getWorldHeight()
                                    xNew = self.x
                                elif h.getY() > self.getY():
                                    yNew = (self.y + 1 + getWorldHeight()) % getWorldHeight()
                                    xNew = self.x
                                if(getObjectAt(xNew,yNew)==0) : #ne bouge pas si se cogne à un objet
                                    setAgentAt(self.x,self.y,0)
                                    self.x = xNew
                                    self.y = yNew
                                    setAgentAt(self.x,self.y,self.type)
                                    
                                if self.cooldown > 0 : #decremente le cooldown de la reproduction
                                    self.cooldown = self.cooldown - 1

                                if self.cooldown_attack > 0 : #decremente le cooldown de l'attaque 
                                    self.cooldown_attack = self.cooldown_attack - 1 
                                    
                                return  



        self.move() #si aucun humain n'est trouvé dans le champ de vision, se déplacer aléatoirement
        return


class Rabbit(Animal) : #classe lapin qui herite de la classe Animal

    def __init__(self, pos_x, pos_y) : #constructeur
        super().__init__() #appel au constructeur de Animal
        self.type = 3 #type de l'agent
        self.speed = 5 #vitesse
        self.image = pygame.image.load('assets/basic111x128/rabbit.png') #png
        self.point = randint(0,10) #point qu'il donne si on le mange
        self.attack = 0 #points d'attaque
        if pos_x == None and pos_y==None : #coordonnees aleatoires si pas de parametres
            self.reset()
        else : 
            self.x = pos_x
            self.y = pos_y
        
    def reproduce(self) : #fonction de reproduction
        if self.cooldown == 0 : 
            for r in rabbit_l :
                if r!= self and r.getX()==self.getX() and r.getY()==self.getY() and r.cooldown == 0: #si sur la mm case
                    if random() < 1 : #30% de chance de se reproduire
                        new = Rabbit(self.getX(), self.getY())
                        rabbit_l.append(new)
                        animal_l.append(new)
                        #on met le cooldown a 100, les lapins se reproduisent souvent
                        new.cooldown = 100
                        self.cooldown = 100
                        r.cooldown = 100
                    return
            return
        return
    
    def death_rabbit(self) : #mort du lapin par un humain
        #on verifie qu'il est dans les listes pour eviter de provoquer une erreur
        if self in animal_l :
            animal_l.remove(self) 
        if self in rabbit_l :
            rabbit_l.remove(self)
            
        dead_a_l.append(self) #on l'ajoute a la liste des animaux morts
        setObjectAt(self.x,self.y,4,0) #on met son cadavre
        
    def death_rabbit_z(self) : #mort du lapin par un zombie
        if self in animal_l :
            animal_l.remove(self) 
        if self in rabbit_l :
            rabbit_l.remove(self)
            
        animalZ_l.append(Animal_Zombie(self.getX(), self.getY())) #il devient un animal zombie

class Pig(Animal) : #classe cochon qui herite de Animal

    def __init__(self, pos_x, pos_y) : #constructeur
        super().__init__() #appel au constructeur de Animal
        self.type = 4 #type de l'agent
        self.speed = 2 #vitesse
        self.image = pygame.image.load('assets/basic111x128/pig.png') #png
        self.point = randint(10,20) #point qu'il donne
        self.attack = 5 #points d'attaque
        if pos_x == None and pos_y==None : 
            self.reset() #coordonnees aleatoires
        else : 
            self.x = pos_x
            self.y = pos_y
            
    def reproduce(self) : #fonction de reproduction
        if self.cooldown == 0 : 
            for p in pig_l :
                if p!= self and p.getX()==self.getX() and p.getY()==self.getY() and p.cooldown == 0: #sur la mm case
                    if random() < 0.5 : #20% de chance de se reproduire
                        new = Pig(self.getX(), self.getY())
                        pig_l.append(new)
                        animal_l.append(new)
                        new.cooldown = 300
                        self.cooldown = 300
                        p.cooldown = 300
                    return
            return
        return
    
    def death_pig(self) : #mort du cochon par un humain
        if self in animal_l :
            animal_l.remove(self) 
        if self in pig_l :
            pig_l.remove(self)
            
        dead_a_l.append(self) #on l'ajoute a la liste des animaux morts
        setObjectAt(self.x,self.y,4,0) #on met son cadavre
        
    def death_pig_z(self) : #mort du cochon par un zombie
        if self in animal_l :
            animal_l.remove(self) 
        if self in pig_l :
            pig_l.remove(self)
            
        animalZ_l.append(Animal_Zombie(self.getX(), self.getY())) #il devient un animal zombie

class Sheep(Animal) : #classe mouton qui herite de Animal

    def __init__(self, pos_x, pos_y) : #constructeur
        super().__init__() #appel au constructeur de Animal
        self.type = 5 #type de l'agent
        self.speed = 3 #vitesse
        self.image = pygame.image.load('assets/basic111x128/sheep.png') #png
        self.point = randint(20,30) #point qu'il donne
        self.attack = 10 #points d'attaque
        if pos_x == None and pos_y==None :
            self.reset() #coordonnees aleatoires
        else : 
            self.x = pos_x
            self.y = pos_y
            
    def reproduce(self) :  #fonction de reproduction
        if self.cooldown == 0 : 
            for s in sheep_l :
                if s!= self and s.getX()==self.getX() and s.getY()==self.getY() and s.cooldown == 0: #sur la mm case
                    if random() < 0.4 : #20% de chance de se reproduire
                        new = Sheep(self.getX(), self.getY())
                        sheep_l.append(new)
                        animal_l.append(new)
                        new.cooldown = 300
                        self.cooldown = 300
                        s.cooldown = 300
                    return
            return
        return 
    
    def death_sheep(self) : #mort du mouton par un humain
        if self in animal_l :
            animal_l.remove(self) 
        if self in sheep_l :
            sheep_l.remove(self)
            
        dead_a_l.append(self) #on l'ajoute a la liste des animaux morts
        setObjectAt(self.x,self.y,4,0) #on met son cadavre
        
        
    def death_sheep_z(self) : #mort du mouton par un zombie
        if self in animal_l :
            animal_l.remove(self) 
        if self in sheep_l :
            sheep_l.remove(self)
            
        animalZ_l.append(Animal_Zombie(self.getX(), self.getY())) #il devient un animal zombie

class Wolf(Animal) :  #classe loup qui herite de Animal
               
    def __init__(self, pos_x, pos_y) : #constructeur
        super().__init__() #appel au constructeur de Animal
        self.type = 6 #type de l'agent
        self.speed = 4 #vitesse
        self.attack = 10 #points d'attaque
        self.point = 30 #point qu'il donne
        self.image = pygame.image.load('assets/basic111x128/wolf.png') #png
        if pos_x == None and pos_y==None :
            self.reset() #coordonnees aleatoires
        else : 
            self.x = pos_x
            self.y = pos_y
            
    def reproduce(self) : #fonction de reproduction
        if self.cooldown == 0 : 
            for w in wolf_l :
                if w!= self and w.getX()==self.getX() and w.getY()==self.getY() and w.cooldown == 0: 
                    if random() < 0.15 : #15% de chance de se reproduire
                        new = Wolf(self.getX(), self.getY())
                        wolf_l.append(new)
                        animal_l.append(new)
                        new.cooldown = 300
                        self.cooldown = 300
                        w.cooldown = 300
                    return
            return
        return
    
    def death_wolf(self) : #mort du loup par un humain
        if self in animal_l :
            animal_l.remove(self) 
        if self in wolf_l :
            wolf_l.remove(self)
            
        dead_a_l.append(self) #on l'ajoute a la liste des animaux morts
        setObjectAt(self.x,self.y,4,0) #on met le cadavre
        
    def death_wolf_z(self) : #mort du loup par un zombie
        if self in animal_l :
            animal_l.remove(self) 
        if self in wolf_l :
            wolf_l.remove(self)
            
        animalZ_l.append(Animal_Zombie(self.getX(), self.getY())) #il devient un animal zombie
    
    def attack_human_w(self, human) : #fonction d'attaque de l'humain
        if self.cooldown_attack <= 0 : 
            if random() < 0.40 : #40% de chance de l'attaquer
                human.health = human.health - self.attack
                self.cooldown_attack = 250
                #human.death_h()
        return


    def attack_animal(self,animal) : #focntion d'attaque sur les autres animaux
        if self.health < 50 : #peut les attaquer seulement si ses pdv sont inferieur a 50
            if isinstance(animal,Wolf) : #ne peut pas attaquer un autre loup
                return
            else : 
                if animal.getX()==self.getX() and animal.getY()==self.getY() : #si sur la mm case
                    if random() < 0.5: #50% de chance d'attaquer
                        self.health = self.health + a.point
                        animal.health = 0 #l'animal meurt direct
                        #a.death()
                        self.cooldown_attack = 250
                    if self.health > self.health_max :
                        self.health = self.health_max
        return 
    
    def attack_zombie(self,zombie) : #fonction d'attaque sur les zombies
        if self.cooldown_attack <= 0 : 
            if random() < 0.2 : #20% de chance d'attaquer
                zombie.health = zombie.health - self.attack
                self.cooldown_attack = 250
                #zombie.death()



class Animal_Zombie(Zombie,Animal) : #classe animal zombie qui herite de Animal et de Zombie
    
    def __init__(self, pos_x, pos_y) : #constructeur
        self.health = 40 #pdv
        self.health_max = 50 #pdv max
        self.speed = 3 #vitesse
        self.type = 8 #type de l'agent
        self.attack = 10
        self.image = pygame.image.load('assets/basic111x128/animal_z.png') #png
        if((pos_x == None) and (pos_y == None)) : #on veut un animal zombie
            self.reset() #coordonnees aleatoires
        else : #un animal est devenu zombie
            self.x = pos_x
            self.y = pos_y
        return

    def attack_h(self,human) : #fonction d'attaque sur l'humain
        if random() < 0.5 :    #50% de chance d'attaquer un humain
            human.health = human.health - 15
            #human.death_h()

        return


    def attack_a(self,animal) : #fonction d'attaque sur les animaux 
        if random() < 0.5 :    #50% de chance d'attaquer un animal 
            animal.health = animal.health - 25

        return
    
    def reset(self): #focntion reprise
        Animal.reset(self)

    def death(self) : #fonction de mort 
        if self.health <= 0 :
            animalZ_l.remove(self) 
            dead_z_l.append(self) #on l'ajoute a la liste des zombies morts
            setObjectAt(self.x,self.y,5,0) #on met le cadavre d'un zombie
            
        return
        
    def move(self) : #fonction reprise en partie, pour les mouvements
        Zombie.move(self) #se deplace comme un zombie
    
########################################
########################################
############ Environnement #############
        
class Tree:     #classe Arbre 
    def __init__(self,pos_x,pos_y):
        self.x = pos_x
        self.y = pos_y
        #possède 3 etats
        self.isBurned = False #avait ete bruler
        self.regenerate = False #entrain de repousser
        self.B = False #entrain de bruler
        self.it = 0
        self.cooldown = 400
    
    def getX(self) : 
        return self.x
    
    def getY(self) :
        return self.y
    
    def burn(self,x,y):
        # s'il n'est pas dans l'etat repoussé et l'etat deja brûle alors il peut bruler 
        if self.regenerate == False and self.isBurned == False:
            self.isBurned = True
            self.B = True
            setObjectAt(x,y,2)
        return
        
    #Fonction qui permet de repousser l'arbre
    def repousse(self):
        if self.B == True :
            self.it += 1
            # l'arbre a fini de bruler,  l'image du feu disparait
            if self.it >= 100 and self.it < self.cooldown:
                self.isBurned = False
                self.regenerate = True
                setObjectAt(self.x,self.y,noAgentId)
            #puis l'image de l'arbre réapparait après son cool down
            elif self.it == self.cooldown:
                setObjectAt(self.x,self.y,1)
                self.regenerate = False
                self.B == False
                self.it = 0
        return
    
    #permet de mettre une image d'arbre
    def Tree(self):
        if self.B == False :
            setObjectAt(self.x,self.y,1)
    
    #foncyion reset pour les boutons     
    def reset(self):
        self.isBurned = False
        self.regenerate = False
        self.B = False
        self.it = 0
        setObjectAt(self.x,self.y,1)
        
class Grass: #classe herbe
    def __init__(self,pos_x,pos_y):
        self.x = pos_x
        self.y = pos_y
        self.type = 4
        self.point = 1
        self.cooldown = 300
        self.it = 0
        self.estMange = False #etat manger
        self.isBurned = False #etat brule
        self.regenerate = False #etat repousser
        self.wasBurned = False
        
    def getX(self) : 
        return self.x
    
    def getY(self) :
        return self.y
    
    # se faire manger par un animal, animal doit être un lapin, un cochon ou un mouton, pour pouvoir manger l'herbe
    def eaten(self, Animal):
        #verification de la présence de l'herbe en etat intact
        if self.estMange == False and self.regenerate == False and self.isBurned == False:
            #verification de la classe de l'animal
            if (isinstance(Animal, Rabbit) or isinstance(Animal, Sheep) or isinstance(Animal, Pig)) and Animal.health < Animal.health_max:
                if self.getX() == Animal.getX() and self.getY() == Animal.getY():
                    self.estMange = True
                    setBuildingAt(self.x,self.y,noAgentId)
                    if Animal.health + self.point > Animal.health_max:
                        Animal.health = Animal.health_max
                    else:
                        Animal.health += self.point
        return
    
    #Fonction qui permet de repousser l'herbe
    def repousse(self):
        if self.estMange == True :
            if self.it == self.cooldown :
                setBuildingAt(self.x,self.y,self.type)
                self.regenerate = False
                self.estMange = False
                self.it = 0
            self.it += 1
        if self.wasBurned == True : 
            
            if self.it >= 100 and self.it < self.cooldown:
                #print("er",self.it,"\n")
                self.isBurned = False
                self.regenerate = True
                setBuildingAt(self.x,self.y,noAgentId)
            elif self.it == self.cooldown :
                #print("ICI\n")
                setBuildingAt(self.x,self.y,self.type)
                self.regenerate = False
                self.estMange = False
                self.wasBurned = False
                self.it = 0
            self.it += 1
        return
    
    #fonction brûler
    def burn(self,x,y):
        if self.estMange == False and self.regenerate == False and self.isBurned == False:
            self.isBurned = True
            self.wasBurned = True
            setBuildingAt(x,y,noAgentId)
            setBuildingAt(x,y,5)
        return
    
    #### A revoir avec Norianne
    def beingBurned(self, Animal):
        if self.isBurned == True:
            if self.getX() == Animal.getX() and self.getY() == Animal.getY():
                Animal.health -= 2
            if Animal.health < 0 :
                Animal.death()
        return

#########batiment#####

class Building: #classe Batiment
    def __init__(self,pos_x,pos_y):
        self.x = pos_x
        self.y = pos_y
        
    def getX(self) : 
        return self.x
    
    def getY(self) :
        return self.y


class Laboratory(Building): #Classe Laboratoire qui hérite de Building
    
    def __init__(self,pos_x,pos_y):
        super().__init__(pos_x,pos_y)
        self.image = pygame.image.load('assets/basic111x128/hospital_a.png') #un laboratoire
    
                
class Stores(Building): #Classe Stores qui hérite de Building
    def __init__(self,pos_x,pos_y):
        super().__init__(pos_x,pos_y)
        self.image = pygame.image.load('assets/basic111x128/cafe_a.png') #un magasin
        self.x = pos_x
        self.y = pos_y
        self.groceries_l = []

    #initialise une source de nourriture
    def initStore(self) :
        for i in range (5):
            self.groceries_l.append(randint(1,30))
        return
    
    def getGroceries(self) :
        return self.groceries_l
        
        
class Decor(Building): #Classe Décor qui hérite de Building
    
    def __init__(self,pos_x,pos_y):
        super().__init__(pos_x,pos_y)
        self.image = pygame.image.load('assets/basic111x128/decor.png') #un laboratoire
    
            
#####METEO#######

class Cloud: # Classe Nuage
    def __init__(self):
        self.type = 1
        self.image = pygame.image.load('assets/basic111x128/cloud.png') #un nuage
        self.reset()
        
    def getX(self) : 
        return self.x
    
    def getY(self) :
        return self.y      
    
    def move(self):
        xNew = self.x
        yNew = self.y
        if random() < 0.01:
            xNew = (self.x + [-1,+1][randint(0,1)] + getWorldWidth()) % getWorldWidth() # Déplacement horizontal aléatoire
        else:
            yNew = (self.y + [0,+1][randint(0,1)] + getWorldHeight()) % getWorldHeight() # Déplacement vertical aléatoire
    
        setSpatialAt(self.x, self.y, 0, objectMapLevels-1)  # Marquer l'emplacement actuel comme vide
        self.x = xNew  # Mettre à jour la nouvelle position en x
        self.y = yNew  # Mettre à jour la nouvelle position en y
        setSpatialAt(self.x, self.y, self.type, objectMapLevels-1)  # Marquer la nouvelle position avec le type du nuage
        return
            
    def reset(self):
        self.x = randint(0,getWorldWidth()-1)
        self.y = randint(0,getWorldWidth()-1)
        while getSpatialAt(self.x,self.y,11) != 0 or getObjectAt(self.x,self.y) != 0 :
            self.x = randint(0,getWorldWidth()-1)
            self.y = randint(0,getWorldWidth()-1)
        setSpatialAt(self.x,self.y,self.type,objectMapLevels-1)
        return

class Weather: #Classe Weather
    def __init__(self, cloud):
        self.x = cloud.getX()  # Même position x que le nuage
        self.y = cloud.getY()  # Même position y que le nuage
        self.z = objectMapLevels-2  # Position z initiale (altitude)
        self.cloud = cloud  # Référence au nuage associé
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getZ(self):
        return self.z
    
    def reset(self):
        # Réinitialiser les coordonnées de la pluie en fonction du nuage associé
        self.x = self.cloud.getX()
        self.y = self.cloud.getY()
        self.z = objectMapLevels - 2  
        return  

class Rain(Weather): #Classe Pluie qui a hérité de Weather
    def __init__(self, cloud):
        super().__init__(cloud)
        self.type = 2
        self.image = pygame.image.load('assets/basic111x128/rain.png') # Image de la pluie
        self.speed = 2
    
    def move(self):
        xNew = self.x
        yNew = self.y
        zNew = self.z
        if random() < 1:
            # Vérifier si la pluie a atteint une certaine hauteur minimale
            if self.z == 0:
                setSpatialAt(self.x, self.y, 0, self.z)
                self.reset()  # Réinitialiser la position de la pluie
            self.z = self.z - 1  # Modifier la coordonnée z de la pluie

        setSpatialAt(self.x, self.y, 0, self.z+1)  # Marquer l'emplacement actuel comme vide
        self.x = self.cloud.getX()  # Mettre à jour la nouvelle position en x
        self.y = self.cloud.getY()  # Mettre à jour la nouvelle position en y
        setSpatialAt(self.x, self.y, self.type, self.z)  # Marquer la nouvelle position avec le type du nuage
        return
     
#Fonction pour faire disparaitre la pluie
def noRain():
    for r in rain_l:
        setSpatialAt(r.x, r.y, 0, r.z)
    return
        
class Snow(Weather): #Classe Pluie qui a hérité de Weather
    def __init__(self, cloud):
        super().__init__(cloud)
        self.type = 3
        self.image = pygame.image.load('assets/basic111x128/snow.png') # Image de la pluie
        self.speed = 1
    
    def move(self):
        xNew = self.x
        yNew = self.y
        zNew = self.z
        if random() < 1:
            # Vérifier si la pluie a atteint une certaine hauteur minimale
            if self.z == 0:
                setSpatialAt(self.x, self.y, 0, self.z)
                self.reset()  # Réinitialiser la position de la pluie
            self.z = self.z - 1  # Modifier la coordonnée z de la pluie

        setSpatialAt(self.x, self.y, 0, self.z+1)  # Marquer l'emplacement actuel comme vide
        self.x = self.cloud.getX()  # Mettre à jour la nouvelle position en x
        self.y = self.cloud.getY()  # Mettre à jour la nouvelle position en y
        setSpatialAt(self.x, self.y, self.type, self.z)  # Marquer la nouvelle position avec le type du nuage
        return
    
#Fonction pour faire disparaitre la neige
def noSnow():
    for s in snow_l:
        setSpatialAt(s.x, s.y, 0, s.z)
    return

###########################################
########## Phenomene ####################

#Fonction pour remplacer l'image des arbres par des sapins lorsqu'il neige
def snowTree():
    for t in tree_l:
        setObjectAt(t.x,t.y,3) 
        
#Fonction pour provoquer un incendie
#Brule le premier arbre de la map
def incendie():
    #if random() < 0.25 and temperature > 50 :
        for x in range(getWorldHeight()):
            for y in range(getWorldHeight()//2):
                if getObjectAt(x,y) != 0:
                    for t in tree_l:
                        if t.getX() == x and t.getY() == y:
                            t.burn(x,y)
                    return
               
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### Initialise world
###
###

#Pour calculer la distance entre deux points de manière torique
def distance_entre_points(x1, y1, x2, y2, world_width, world_height):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dx = min(dx, world_width - dx)
    dy = min(dy, world_height - dy)
    return (dx ** 2 + dy ** 2) ** 0.5

rayon_minimal = 5  # Rayon minimal entre chaque laboratoire

#initialisation du monde
def initWorld():
    global nbTrees, nbBurningTrees, agents, nb_food


    for i in range(nbCloud):#nuage, la pluie, la neige
        c = Cloud()
        cloud_l.append(c)
        r = Rain(c)
        rain_l.append(r)
        s = Snow(c)
        snow_l.append(s)
    
    #arbre
    for i in range(nbTrees):
        x = randint(0, getWorldWidth()-1)
        y = randint(0,getWorldHeight()//2 -2)
        while getTerrainAt(x,y) != 0 or getObjectAt(x,y) != 0:
            x = randint(0,getWorldWidth()-1)
            y = randint(0,getWorldHeight()//2 -2)
        t = Tree(x,y)
        tree_l.append(t)
        setObjectAt(x,y,1)
    
    ####### A NE PAS SUPPRIMER
    #for i in range(nbGrass): #herbe
    #    x = randint(0, getWorldWidth()-1)
    #    y = randint(0,getWorldHeight()//2 -1)
    #    while getTerrainAt(x,y) != 0 or getObjectAt(x,y) != 0:
    #        x = randint(0,getWorldWidth()-1)
    #        y = randint(0,getWorldHeight()//2 -1)
    #    g = Grass(x,y)
    #    grass_l.append(g)
    #    setBuildingAt(g.x,g.y,g.type)
        
    for x in range(getWorldWidth()): #herbe
        for y in range(getWorldHeight()//2):
            g = Grass(x,y)
            grass_l.append(g)
            setBuildingAt(g.x,g.y,g.type)
    
    for _ in range(nbLabo):#laboratoire
        x = randint(0, getWorldWidth()-1)
        y = randint(getWorldHeight() // 2, getWorldHeight() - 1)
        while any(distance_entre_points(x, y, labo.x, labo.y, getWorldWidth(), getWorldHeight()) < rayon_minimal for labo in laboratory_l):
            x = randint(0, getWorldWidth() - 1)
            y = randint(getWorldHeight() // 2, getWorldHeight() - 1)
        laboratory_l.append(Laboratory(x, y))
        setBuildingAt(x, y, 2)
    
    #Decor
    y = 63
    l = 7 
    for j in range(5): 
        for i in range(30):
            x = randint(0, getWorldWidth()-1)
            while getTerrainAt(x,y) != 0 or getBuildingAt(x,y) != 0:
                x = randint(0,getWorldWidth()-1)
            decorx.append(Decor(x,y))
            setBuildingAt(x,y,7)
            setBuildingAt(x,y,7,1)
            setBuildingAt(x,y,7,2)
        y -= l
        
    x = 0  
    for j in range (9):
        for i in range(10):
            y = randint(getWorldHeight()//2 ,getWorldHeight()-1)
            while getTerrainAt(x,y) != 0 or getBuildingAt(x,y) != 0:
                y = randint(getWorldHeight()//2 ,getWorldHeight()-1)
                decory.append(Decor(x,y))
            setBuildingAt(x,y,6)
            setBuildingAt(x,y,6,1)
            setBuildingAt(x,y,6,2)
        x += l
        
    #les magasins
    for i in range(nbStores):
        x = randint(0, getWorldWidth()-1)
        y = randint(getWorldHeight()//2 ,getWorldHeight()-1)
        while getTerrainAt(x,y) != 0 or getBuildingAt(x,y) != 0:
            x = randint(0,getWorldWidth()-1)
            y = randint(getWorldHeight()//2 ,getWorldHeight()-1)
        s = Stores(x,y)
        s.initStore()
        stores_l.append(s)
        setBuildingAt(x,y,1)
        
    #les sacs poubelles
    for i in range(nbStores):
        x = randint(0, getWorldWidth()-1)
        y = randint(getWorldHeight()//2 ,getWorldHeight()-1)
        while getTerrainAt(x,y) != 0 or getBuildingAt(x,y) != 0:
            x = randint(0,getWorldWidth()-1)
            y = randint(getWorldHeight()//2 ,getWorldHeight()-1)
        trash_l.append(Decor(x,y))
    
    return


#pour changer les images des immeubles pour que ce soit plus délabré
def intD(it):
    if it > 800:
        for l in laboratory_l:
            setBuildingAt(l.x,l.y,10)
            
        for s in stores_l:
            setBuildingAt(s.x,s.y,11)
            
        for dx in decorx:
            setBuildingAt(dx.x,dx.y,9)
            setBuildingAt(dx.x,dx.y,9,1)
            setBuildingAt(dx.x,dx.y,9,2)
            
        for dy in decory:
            setBuildingAt(dy.x,dy.y,8)
            setBuildingAt(dy.x,dy.y,8,1)
            setBuildingAt(dy.x,dy.y,8,2)
            
        for t in trash_l:
            setBuildingAt(t.x,t.y,12)
            
    return

### ### ### ### ###

def initAgents(): #initialisation des agents

    for i in range(nbZombies):
        zombie_l.append(Zombie(None,None))

    for i in range(nbSurvivors) :
        sv = Survivor(None,None)
        human_l.append(sv)
        survivors_l.append(sv)
        
    for i in range(nbScientists) :
        sc = Scientist(None,None)
        human_l.append(sc)
        scientists_l.append(sc)

    for i in range(nbPig) :
        p = Pig(None,None)
        animal_l.append(p)
        pig_l.append(p)
        
    for i in range(nbRabbit) : 
        r = Rabbit(None,None)
        animal_l.append(r)
        rabbit_l.append(r)
        
    for i in range(nbSheep) :
        s = Sheep(None,None)
        animal_l.append(s)
        sheep_l.append(s)
    
    for i in range(nbWolf) :
        w = Wolf(None,None)
        animal_l.append(w)
        wolf_l.append(w)

    for i in range(nbAnimalZ) :
        animalZ_l.append(Animal_Zombie(None,None))

    return

### ### ### ### ###

#pour propager les flammes
def stepFire( it = 0):
    if it % (maxFps/10) == 0:
        for x in range(worldWidth):
            for y in range(worldHeight//2):
                if getBuildingAt(x,y) == 4: #verifie si c de l'herbe
                    for dx in range(-2, 3):  # Boucle pour les voisins horizontaux dans un rayon de 2
                        for dy in range(-2, 3):  # Boucle pour les voisins verticaux dans un rayon de 2
                            # Coordonnées du voisin (torique)
                            nx = (x + dx) % worldWidth
                            ny = (y + dy) % worldHeight
                            if (getBuildingAt(nx,ny) == 5 or getObjectAt(nx,ny) == 2) and random() < 0.05 : #si voisin est enflammé
                                for g in grass_l:
                                    if g.getX() == x and g.getY() == y:
                                        g.burn(x,y)
                if getObjectAt(x,y) == 1:
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        # Coordonnées du voisin (torique)
                        nx = (x + dx) % worldWidth
                        ny = (y + dy) % worldHeight
                        for t in tree_l:
                            if getBuildingAt(nx,ny) == 5 or getObjectAt(nx,ny) == 2: #si voisin est enflammé
                                if t.getX() == x and t.getY() == y:
                                    t.burn(x,y)

### ### ### ### ###


def stepZombies( it = 0) : #move zombies
    if it % (maxFps/10) == 0:
        shuffle(zombie_l)
        for z in zombie_l:
            z.follow_human() #fonction de deplacement pour suivre les humains
            z.raining() #fonction si il pleut
            z.mutation() #fonction de mutation
    return

def stepSurvivors( it = 0) : #move survivors
    if it % (maxFps/10) == 0:
        shuffle(survivors_l)
        for s in survivors_l:
            s.run_to_store() #fonction de deplacement 
    return

def stepScientists( it = 0) : #move scientist
    if it % (maxFps/10) == 0:
        shuffle(scientists_l)
        for s in scientists_l:
            s.run_to_lab() #fonction de deplacement
    return

def stepAnimal( it = 0) : #move animals
    if it % (maxFps/10) == 0:
        shuffle(animal_l)
        for a in animal_l:
            if isinstance(a,Wolf):
                a.run_to_human() #fonction de deplacement des loups
            else :
                a.run_from_human() #fonction de deplacement des autres animaux
    return

def stepAnimal_Z(it = 0) : #move animals zombies
    if it % (maxFps/10) == 0:
        shuffle(animalZ_l)
        for az in animalZ_l:
            az.move() #fonction de deplacement
    return
    

def stepCloud( it = 0) : #move cloud
    if it % (maxFps/10) == 0:
        shuffle(cloud_l)
        for c in cloud_l:
            c.move()
    return

def stepRain( it = 0) : #move rain
    if it % (maxFps/10) == 0:
        shuffle(rain_l)
        for r in rain_l:
            r.move()
    return

def stepSnow( it = 0) : #move snow
    if it % (maxFps/10) == 0:
        shuffle(snow_l)
        for s in snow_l:
            s.move()
    return

def dead(it = 0) : 
    for d in dead_a_l : #cadavre animal
        if it % 360 == 0: #le cadavre reste pendant 360 iterations
            dead_a_l.remove(d) #on le retire de la liste
            setObjectAt(d.x, d.y, 0, 0) #on le retire

    for d in dead_z_l : #cadavre zombie
        if it % 360 == 0: #le cadavre reste pendant 360 iterations
            dead_z_l.remove(d)
            setObjectAt(d.x, d.y, 0, 0)

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### MAIN
###
###

timestamp = datetime.datetime.now().timestamp()

loadAllImages()

initWorld()
initAgents()

print ("initWorld:",datetime.datetime.now().timestamp()-timestamp,"second(s)")
timeStampStart = timeStamp = datetime.datetime.now().timestamp()

#initialisation des itérations pour le monde
it = itStamp = 0
snow_iterations = 0 
rain_iterations = 0
incendie_iterations = 0
fire_iterations = 0

#meteo
chaud = False
normal = False
froid = False
pleuvoir = False
neiger = False
fire = False

# Variables pour le cycle jour-nuit
time_of_day = 0  # Heure du jour (0-23)
transition_speed = 0.1  # Vitesse de transition (plus la valeur est petite, plus la transition est lente)

##################### pour ecrire dans le fichier
fichier = open("data.txt", "a")
fichier.write("it Temperature NbHumain NbZombie NbLoup NbLapin NbCochon NbMouton\n")


while True :

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:#pour quitter la fenetre
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_s and not( pygame.key.get_mods() & pygame.KMOD_SHIFT ) : #pour dézoomer
                scaleMultiplier = scaleMultiplier - 0.01
                resetImages()
                if verbose:
                    print ("scaleMultiplier is ",scaleMultiplier)
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_SHIFT: #pour zoomer
                scaleMultiplier = scaleMultiplier + 0.01
                resetImages()
                if verbose:
                    print ("scaleMultiplier is ",scaleMultiplier)
            elif event.key == pygame.K_a: #baisser température
                froid = True
                chaud = False
                normal = False
            elif event.key == pygame.K_z:# augmenter temperature
                froid = False
                chaud = True
                normal = False
                incendie_iterations = 0
                fire_iterations = 0
            elif event.key == pygame.K_e:#mettre temperature à normal
                froid = False
                chaud = False
                normal = True
                pleuvoir = False
                neiger = False
                fire = False
                incendie_iterations = 0
                fire_iterations = 0
                snow_iterations = 0 
                rain_iterations = 0
            elif event.key == pygame.K_r: #pour faire pleuvoir
                pleuvoir = True
                neiger = False
                fire = False
                normal = False
            elif event.key == pygame.K_t:#pour faire neiger
                pleuvoir = False
                neiger = True
                fire = False
                normal = False
            elif event.key == pygame.K_y:#pour faire un incendie
                pleuvoir = False
                neiger = False
                fire = True
                incendie_iterations = 0
                fire_iterations = 0
                normal = False

    if it != 0 and it % 100 == 0 and verboseFps:
        print ("[fps] ", ( it - itStamp ) / ( datetime.datetime.now().timestamp()-timeStamp ) )
        timeStamp = datetime.datetime.now().timestamp()
        itStamp = it

    # Mise à jour de l'heure du jour (simulée)
    time_of_day = (time_of_day + transition_speed) % 24
    
    jour = (it // 240) +1
    render(it,time_of_day)
    intD(it)
    
    #on parcourt les listes et on lance nos fonctions

    for a in animal_l :
        a.reproduce()
        for g in grass_l:
            g.eaten(a)
            
    for g in grass_l :
        g.repousse()
        
    for t in tree_l :
        t.repousse()
        t.Tree()


    nb_food = 0
    for s in stores_l : 
        nb_food = nb_food + len(s.getGroceries())


    for a in animal_l :
        a.reproduce()
        for w in wolf_l : 
            w.attack_animal(a)
            a.death_a()
            if a not in animal_l: 
                break 
            
        for h in human_l: 
            if a.getX() == h.getX() and a.getY() == h.getY() :
                if isinstance(a,Wolf) : 
                    a.attack_human_w(h)
                    h.attack_wolf(a)
                    h.eat(a,None)
                    a.death_a()
                    h.death_h()
                    if a not in animal_l :
                        break
                else :
                    h.attack_animal(a)
                    h.eat(a,None)
                    h.death_h()
                    a.death_a()
                    if a not in animal_l :
                        break
                    
        for z in zombie_l :
            if a.getX() == z.getX() and a.getY() == z.getY() :
                if isinstance(a,Wolf) : 
                    z.attack_animal(a)
                    a.attack_zombie(z)
                    a.death_a_to_az()
                    z.death()
                    if a not in animal_l :
                        break
                else :
                    z.attack_animal(a)
                    a.death_a_to_az()
                    if a not in animal_l :
                        break
                
                
    for h in human_l : 
        h.reproduce_human()
    
        for s in stores_l : 
            h.piller(s)
                
        for z in zombie_l :
            if z.getX() == h.getX() and z.getY() == h.getY() :
                h.attack_zombie(z)
                z.attack_human(h)
                h.death_h()
                z.death()
                if h not in human_l: 
                    break 
                
                    
    for az in animalZ_l : 
        for h in human_l: 
            if az.getX() == h.getX() and az.getY() == h.getY() :
                az.attack_h(h)
                h.attack_zombie(az)
                h.death_h()
                az.death()
                if az not in animalZ_l :
                    break

        for a in animal_l:
            if isinstance(a,Wolf) :
               if az.getX() == a.getX() and az.getY() == a.getY() :
                    az.attack_a(a)
                    a.attack_zombie(az)
                    a.death_a_to_az()
                    az.death()
                    if a not in animal_l :
                        break 
                
            else :
                if az.getX() == a.getX() and az.getY() == a.getY() :
                    az.attack_a(a)
                    a.death_a_to_az()
                    if a not in animal_l :
                        break
        

    for s in scientists_l :
        if isinstance(s,Scientist) :
            #s.make_antidote()  
            s.give_antidote() 


    nb_antidote = 0
    for s in scientists_l : 
        if isinstance(s,Scientist) :
            nb_antidote = nb_antidote + s.antidote    
        

    stepZombies(it)
    stepSurvivors(it)
    stepScientists(it)
    stepAnimal(it)
    stepCloud(it)
    stepAnimal_Z(it)

    ######### A METTRE ICI les choses de pluies, de neige et de feu 
    snowing = random()
    if froid and temperature > -30 :
        temperature -= random()
    
    if chaud and temperature < 60 :
        temperature += random()
        
    if temperature < 0 or neiger:
        if pleuvoir:
            pleuvoir = False
            noRain()
            rain_iterations = 0
        if neiger and snow_iterations < 200:
            stepSnow(it)
            snow_iterations += 1
            fire = False
            for t in tree_l :
                t.reset()
            snowTree()
            fire_iterations = 0
            incendie_iterations = 0
            rain_iterations = 0
        # Si le nombre d'itérations de neige atteint 100, arrêter de faire neiger
        if snow_iterations >= 200:
            neiger = False
            snow_iterations = 0  # Réinitialiser le compteur d'itérations de neige
            noSnow()
        if neiger == False:
            snow_iterations = 0
            noSnow()
            if snowing < 0.01:
                neiger = True
            
    if pleuvoir == True :
        stepRain(it)
        noSnow()
        fire = False
        for t in tree_l :
            t.reset()
        fire_iterations = 0
        incendie_iterations = 0
        snow_iterations = 0
    if pleuvoir and rain_iterations < 200:
        rain_iterations += 1
    if rain_iterations >= 200:
        pleuvoir = False
        rain_iterations = 0  
        noRain()
    if pleuvoir == False:
        rain_iterations = 0  
        noRain()
        if snowing < 0.0005:
            pleuvoir = True
        
    if temperature < -30 :
        froid = False
        
    if fire and fire_iterations < 400:
        snow_iterations = 0
        noSnow()
        if incendie_iterations < 300:
            incendie()
            incendie_iterations += 1
            stepFire(it)
        fire_iterations += 1
    if fire_iterations == 300:
        for t in tree_l :
            t.reset()
    if fire_iterations == 400:
        fire_iterations = 0
        incendie_iterations = 0
        fire = False
        
    nb_pop = len(zombie_l) + len(rabbit_l) + len(wolf_l) + len(sheep_l) + len(pig_l) + len(scientists_l) + len(survivors_l) + len(animalZ_l)
    if nb_pop > 90 :
        if temperature < 60 :
            temperature += 0.01
    if nb_pop < 90 :
        if temperature > 10 :
            temperature -= 0.01
        
    if temperature > 50:
        if random() < 0.8 :
            fire = True
        
    if normal:
        temperature = 20
        for t in tree_l :
            t.reset()
    #######################################################
    
    dead(it)
    
    # Couleur du texte
    textColor = (255, 255, 255)

    # Police et taille de la police
    font = pygame.font.Font(None, 25)
    text = "nb iteration : "+ str(it)
    text_surface = font.render(text , True, textColor)
    text_rect = text_surface.get_rect(topleft=(0, 0))
    screen.blit(text_surface, text_rect)
    
    # Message : Heure 
    text_time = "Heure : {:.2f}".format(time_of_day)
    text_surface_time = font.render(text_time, True, textColor)
    text_rect_time = text_surface_time.get_rect(topleft=(0, 20)) 
    screen.blit(text_surface_time, text_rect_time)

    # Message : Jour 
    text_time = "Jour : " + str(jour)
    text_surface_time = font.render(text_time, True, textColor)
    text_rect_time = text_surface_time.get_rect(topleft=(0, 40)) 
    screen.blit(text_surface_time, text_rect_time)
    
    # Message : Temperature
    text_creature_count = "Temperature : {:.2f} 'C".format(temperature)
    text_surface_creature_count = font.render(text_creature_count, True, textColor)
    text_rect_creature_count = text_surface_creature_count.get_rect(topleft=(0, 60))  
    screen.blit(text_surface_creature_count, text_rect_creature_count)
    
    # Message : Nombre de zombies
    text_creature_count = "nb zombie : " + str(len(zombie_l)+len(animalZ_l))
    text_surface_creature_count = font.render(text_creature_count, True, textColor)
    text_rect_creature_count = text_surface_creature_count.get_rect(topleft=(0, 100))  
    screen.blit(text_surface_creature_count, text_rect_creature_count)
    
    # Message : Nombre d'humain
    text_creature_count = "nb humain : " + str(len(scientists_l)+len(survivors_l))
    text_surface_creature_count = font.render(text_creature_count, True, textColor)
    text_rect_creature_count = text_surface_creature_count.get_rect(topleft=(0, 120)) 
    screen.blit(text_surface_creature_count, text_rect_creature_count)
    
    # Message : Nombre de lapin
    text_creature_count = "nb lapin: " + str(len(rabbit_l))
    text_surface_creature_count = font.render(text_creature_count, True, textColor)
    text_rect_creature_count = text_surface_creature_count.get_rect(topleft=(0, 140))  
    screen.blit(text_surface_creature_count, text_rect_creature_count)
    
    # Message : Nombre de loup
    text_creature_count = "nb loup : " + str(len(wolf_l))
    text_surface_creature_count = font.render(text_creature_count, True, textColor)
    text_rect_creature_count = text_surface_creature_count.get_rect(topleft=(0, 160))  
    screen.blit(text_surface_creature_count, text_rect_creature_count)
    
    # Message : Nombre de mouton
    text_creature_count = "nb mouton : " + str(len(sheep_l))
    text_surface_creature_count = font.render(text_creature_count, True, textColor)
    text_rect_creature_count = text_surface_creature_count.get_rect(topleft=(0, 180))  
    screen.blit(text_surface_creature_count, text_rect_creature_count)
    
    # Message : Nombre de cochon
    text_creature_count = "nb cochon : " + str(len(pig_l))
    text_surface_creature_count = font.render(text_creature_count, True, textColor)
    text_rect_creature_count = text_surface_creature_count.get_rect(topleft=(0, 200))  
    screen.blit(text_surface_creature_count, text_rect_creature_count)

     # Message : Nombre de nourriture
    text_creature_count = "nb food : " + str(nb_food)
    text_surface_creature_count = font.render(text_creature_count, True, textColor)
    text_rect_creature_count = text_surface_creature_count.get_rect(topleft=(0, 220))  
    screen.blit(text_surface_creature_count, text_rect_creature_count)
    
    # Message : Nombre d'antidote
    text_creature_count = "nb antidote: " + str(nb_antidote)
    text_surface_creature_count = font.render(text_creature_count, True, textColor)
    text_rect_creature_count = text_surface_creature_count.get_rect(topleft=(0, 240))  
    screen.blit(text_surface_creature_count, text_rect_creature_count)

    # Message : Nombre d'iteration de la neige
    text_creature_count = "nb snow it: " + str(snow_iterations)
    text_surface_creature_count = font.render(text_creature_count, True, textColor)
    text_rect_creature_count = text_surface_creature_count.get_rect(topleft=(0, 260))  
    screen.blit(text_surface_creature_count, text_rect_creature_count)
    
    # Message : Nombre d'iteration de la pluie
    text_creature_count = "nb rain it: " + str(rain_iterations)
    text_surface_creature_count = font.render(text_creature_count, True, textColor)
    text_rect_creature_count = text_surface_creature_count.get_rect(topleft=(0, 280))  
    screen.blit(text_surface_creature_count, text_rect_creature_count)
    
    # Message : Nombre d'iteration que dure le feu
    text_creature_count = "nb fire it: " + str(fire_iterations)
    text_surface_creature_count = font.render(text_creature_count, True, textColor)
    text_rect_creature_count = text_surface_creature_count.get_rect(topleft=(0, 300))  
    screen.blit(text_surface_creature_count, text_rect_creature_count)
    
    pygame.display.flip()
    fpsClock.tick(maxFps) # recommended: 30 fps
    
    fichier.write(f"{it} {temperature} {len(scientists_l) + len(survivors_l)} {len(zombie_l) + len(animalZ_l)} {len(wolf_l)} {len(rabbit_l)} {len(pig_l)} {len(sheep_l)}\n")

    it += 1
fichier.close()
fps = it / ( datetime.datetime.now().timestamp()-timeStampStart )
print ("[Quit] (", fps,"frames per second )")

pygame.quit()
sys.exit()