import pygame
import math
import random
from Projectile import Projectile

class Weapon():
    def __init__(self):
        self.lastShot = 0
    
    def shoot():
        pass
    
    @staticmethod
    def normalize_vector(vector):
        if vector == [0, 0]:
            return [0, 0]    
        pythagoras = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
        return (vector[0] / pythagoras, vector[1] / pythagoras)
    
    @staticmethod
    def rotate_vector(vector, theta):
        resultVector = (vector[0] * math.cos(theta)
                        - vector[1] * math.sin(theta),
                        vector[0] * math.sin(theta)
                        + vector[1] * math.cos(theta))
        return resultVector

class Sniper(Weapon):
    def __init__(self):
        super().__init__()
        self.weaponCooldown = 400
    
    def shoot(self, user, mousePos):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastShot > self.weaponCooldown:
            direction = (mousePos[0] - user.pos[0], mousePos[1] - user.pos[1]) \
                if mousePos != user.pos else (1, 1)
            self.lastShot = currentTime
            user.projectiles.add(Projectile((user.pos[0] + 15, user.pos[1] + 15),
                                            super().normalize_vector(direction),
                                            10, 4000, (0, 0, 255)))

            sound = pygame.mixer.Sound("pistol.wav")
            pygame.mixer.Sound.play(sound)
            
class Shotgun(Weapon):
    def __init__(self):
        super().__init__()
        self.weaponCooldown = 750
        self.spreadArc = 90
        self.projectilesCount = 7
        
    def shoot(self, user, mousePos):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastShot > self.weaponCooldown:
            direction = (mousePos[0] - user.pos[0], mousePos[1] - user.pos[1]) \
                if mousePos != user.pos else (1, 1)
            self.lastShot = currentTime
            arcDifference = self.spreadArc / (self.projectilesCount - 1)
            for proj in range(self.projectilesCount):
                theta = math.radians(arcDifference*proj - self.spreadArc/2)
                projDir = super().rotate_vector(direction, theta)
                user.projectiles.add(Projectile((user.pos[0] + 15, user.pos[1] + 15),
                                                super().normalize_vector(projDir),
                                                7, 500, (232, 144, 42)))

            sound = pygame.mixer.Sound("shotgun.wav")
            pygame.mixer.Sound.play(sound)
                
class MachineGun(Weapon):
    def __init__(self):
        super().__init__()
        self.weaponCooldown = 50
        self.spreadArc = 30
        
    def shoot(self, user, mousePos):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastShot > self.weaponCooldown:
            direction = (mousePos[0] - user.pos[0], mousePos[1] - user.pos[1]) \
                if mousePos != user.pos else (1, 1)
            self.lastShot = currentTime
            theta = math.radians(random.random()*self.spreadArc - self.spreadArc/2)
            projDir = super().rotate_vector(direction, theta)   
            user.projectiles.add(Projectile((user.pos[0] + 15, user.pos[1] + 15),
                                            super().normalize_vector(projDir),
                                            8, 1200, (200, 20, 255)))

            sound = pygame.mixer.Sound("machinegun.wav")
            pygame.mixer.Sound.play(sound)
