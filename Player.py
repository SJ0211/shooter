import pygame
import math
import Weapon

from pygame import RLEACCEL

player_weapon1 = pygame.image.load("pistol.png")
player_weapon2 = pygame.image.load("shotgun.png")
player_weapon3 = pygame.image.load("machinegun.png")
PLAYERCOLOR = (1,   1,   1)

def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]    
    pythagoras = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
    return (vector[0] / pythagoras, vector[1] / pythagoras)

class Player(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()
    def __init__(self, screenSize):
        super().__init__()
        self.image = pygame.image.load("player-left.png")
        #self.image.set_colorkey((PLAYERCOLOR), RLEACCEL)
        self.rect = self.image.get_rect(x=screenSize[0]//2,
                                        y=screenSize[1]//2)
        
        self.pos = [screenSize[0] // 2, screenSize[1] // 2]
        self.health = 10
        self.alive = True
        self.movementVector = [0, 0]
        self.movementSpeed = 5
        self.availableWeapons = [Weapon.Sniper(),
                                 Weapon.Shotgun(),
                                 Weapon.MachineGun()]
        self.equippedWeapon = self.availableWeapons[0]

    def move(self, screenSize, tDelta):
        self.movementVector = normalize_vector(self.movementVector)
        newPos = (self.pos[0] + self.movementVector[0]*self.movementSpeed*tDelta,
                  self.pos[1] + self.movementVector[1]*self.movementSpeed*tDelta)
        if newPos[0] < 0:
            self.pos[0] = 0
        elif newPos[0] > screenSize[0] - self.rect.width:
            self.pos[0] = screenSize[0] - self.rect.width
        else:
            self.pos[0] = newPos[0]

        if newPos[1] < 0:
            self.pos[1] = 0
        elif newPos[1] > screenSize[1]-self.rect.height:
            self.pos[1] = screenSize[1]-self.rect.width
        else:
            self.pos[1] = newPos[1]
        
        self.rect.topleft = self.pos
        self.movementVector = [0, 0]
        
    def shoot(self, mousePos):
        self.equippedWeapon.shoot(self, mousePos)
        
    def render(self, surface):

        surface.blit(self.image, self.pos)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        x, y = self.rect.center
        rel_x, rel_y = mouse_x - x, mouse_y - y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        if self.availableWeapons.index(self.equippedWeapon) == 0:
            player_weapon_copy = pygame.transform.rotate(player_weapon1, angle)
        elif self.availableWeapons.index(self.equippedWeapon) == 1:
            player_weapon_copy = pygame.transform.rotate(player_weapon2, angle)
        elif self.availableWeapons.index(self.equippedWeapon) == 2:
            player_weapon_copy = pygame.transform.rotate(player_weapon3, angle)
        else:
            print("something went wrong")
        surface.blit(player_weapon_copy, (x - int(player_weapon_copy.get_width() / 2),
                                            y + 10 - int(player_weapon_copy.get_height() / 2)))

