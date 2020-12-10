import pygame
from pygame import mixer    # this will help us handle sounds
from pygame.locals import *
import random
import math

# initialize the game
pygame.init()

clicked = False

# create the game screen
screen = pygame.display.set_mode((800, 600))

# Set the window caption and icon
pygame.display.set_caption("Space Invaders") 
icon = pygame.image.load('imgs/rocket.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load("imgs/background2.png")

# background sound. we use mixer.music for a background sound
mixer.music.load("sounds/bg.wav")
mixer.music.play(-1) # this will play the .wav file on loop

# load the laser sound
laserSound = mixer.Sound("sounds/laser.wav")

# load the collision sound
collisionSound = mixer.Sound("sounds/explosion1.wav")

# load player iamge
playerImg = pygame.image.load("imgs/rocket.png")
# myPlayer class
class myPlayer(object):
    def __init__(self, x, y):   # this is like a constructor
        self.playerX = x              # 'self' makes 'x' an attribute of the class
        self.playerY = y              # 'self' makes 'y' an attribute of the class
        self.velocity = 3     # 'self' makes 'velocity' an attribute of the class
    # display the player 
    def movePlayer(self, x, y):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            if x < 800-60:
                x+=self.velocity
        if keys[pygame.K_a]:
            if x > -4:
                x-=self.velocity
        screen.blit(playerImg, (x, y))
        self.playerX = x   # update the x attribute of the object
        self.playerY = y   # update teh y attribute of the object

# load alien image
alienImg = pygame.image.load("imgs/alien.png")
# alien class
class alien(object):
    def __init__(self, x, y, vel):   # this is like a constructor
        self.alienX = x              # 'self' makes 'x' an attribute of the class
        self.alienY = y              # 'self' makes 'y' an attribute of the class
        self.velocity = vel         # 'self' makes 'velocity' an attribute of the class
        self.direction = True
        self.yDelta = 55
    # display the player 
    def moveAlien(self, x, y):
        if x < 800-60 and x > -4:
            if self.direction == True:
                x += self.velocity
            else:
                x -= self.velocity
        if x >= 800-60: # when we reach the border the alien will change direction
            self.direction = False
            y += self.yDelta
            x-=self.velocity
        if x <= -4:     # when we reach the border the alien will change direction
            self.direction = True
            y += self.yDelta
            x+=self.velocity
        screen.blit(alienImg, (x, y))
        self.alienX = x
        self.alienY = y
    def __del__(self):
        print("alien deleted")

# laser
laserImg = pygame.image.load("imgs/laser.png")
#laser class
class laser(object):
    def __init__(self, x, y):
        self.laserX = x
        self.laserY = y
        self.ready = True
    def shootLaser(self):
        if self.ready == False:
            self.laserY-=5
            screen.blit(laserImg, (self.laserX, self.laserY))
            if self.laserY < -5:
                self.ready = True
        elif pygame.mouse.get_pressed()[0]:
            self.laserX = spaceship.playerX+16
            self.laserY = spaceship.playerY-16
            self.ready = False
            laserSound.play()
            screen.blit(laserImg, (spaceship.playerX+16, spaceship.playerY-16))
        else:
            self.laserX = 0
            self.laserY = 0

# button class for when the game is over
class button(object):
    button_col = (25, 190, 255)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = (255, 255, 255)
    width = 200
    height = 40
    def __init__(self, x, y, text):
        self.posx = x
        self.posy = y
        self.text = text
    def draw(self):
        global clicked
        action = False
        pos = pygame.mouse.get_pos()
        button_rect = Rect(self.posx, self.posy, self.width, self.height)
        pygame.draw.rect(screen, self.button_col, button_rect)   
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.hover_col, button_rect)   
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
                pygame.draw.rect(screen, (0,0,0), button_rect)   
            else:
                pygame.draw.rect(screen, self.click_col, button_rect)
        # add shading to the button
        pygame.draw.line(screen, (255, 255, 255), (self.posx, self.posy), (self.posx + self.width, self.posy), 2)
        pygame.draw.line(screen, (255, 255, 255), (self.posx, self.posy), (self.posx, self.posy + self.height), 2)
        pygame.draw.line(screen, (0, 0, 0), (self.posx, self.posy + self.height), (self.posx + self.width, self.posy + self.height), 2)
        pygame.draw.line(screen, (0, 0, 0), (self.posx + self.width, self.posy), (self.posx + self.width, self.posy + self.height), 2)

        # add text
        text_img = font.render(self.text, True, self.text_col)
        screen.blit(text_img, (self.posx+13, self.posy + 5))
        return action

# handle the quit event
def checkQuit():
    for event in pygame.event.get():    # this will get all of our events
        if event.type == pygame.QUIT:   # if the event type is QUIT. leave the gameloop
            return False
    return True

def collision(p1X, p1Y, p2X, p2Y):
    dist = (p1X - p2X+15) * (p1X - p2X+15) + (p1Y - p2Y) * (p1Y - p2Y) # (p1x - p2x)^2 + (p1y - p2y)^2
    dist = math.sqrt(dist) # [(p1x - p2x)^2 + (p1y - p2y)^2]^(0.5)

    # if within this range we have made a collision
    if dist < 27:
        collisionSound.play()
        return True
    return False

# show the score
def showScore(score, y, text):
    text = font.render(text + ": " + str(score), True, (255, 255, 255))
    screen.blit(text, (10, y))

# game over message
def gameover():
    font = pygame.font.Font('freesansbold.ttf', 64)
    text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text, (180, 200))
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    return True
    
#---mainloop---#
# Score variables
score = 0
highscore = 0
font = pygame.font.Font('freesansbold.ttf', 32)
# keep track of number of aliens
numAliens = 1
# keep track of the hits we make
hit = list()
# we will create an instance of our player class
spaceship = myPlayer(370, 480)
# we will create an instance of our alien class
aliens = list()
alienVel = 1.5
aliens.append(alien(random.randint(0, 800-64), random.randint(50, 150), alienVel))
# we will create an instance of our laser class
laser = laser(0,0)
# we will create an instance of our button classs
playAgain = button(285, 300, "Play Again")
# we need this forever loop so that our program does not end right away
GameLoop = True
again = False
gg = False
while GameLoop:
    # change the background screen colour
    screen.fill((128, 193, 255)) # we want to do this first in the loop so we do not cover any icons 
    screen.blit(background, (0,0))

    # check if the quit event has occured
    GameLoop = checkQuit() 

    # show the game score
    showScore(score, 10, "Score")
    showScore(highscore, 40, "Highscore") 
    
    # display the player on the screen and update the position
    spaceship.movePlayer(spaceship.playerX, spaceship.playerY)
    laser.shootLaser()
    for i in range(len(aliens)):
        aliens[i].moveAlien(aliens[i].alienX, aliens[i].alienY)
        if aliens[i].alienY > 470:
            if score > highscore:
                highscore = score
            gg = gameover()
            pygame.mixer.music.pause()
        if collision(aliens[i].alienX, aliens[i].alienY, laser.laserX, laser.laserY):
            laser.ready = True
            laser.shootLaser()  # update the laser
            score+=100
            print(score)
            if len(aliens) > 0:
                hit.append(i)   # build our list of aliens we have hit
    for i in hit:               # loop through our list of hits so we can remove those aliens. 
        aliens.remove(aliens[i])
        print(len(aliens))
    hit = list()
    if len(aliens) <= 0:
        numAliens += 1
        alienVel += 0.5
        for i in range(numAliens):
            aliens.append(alien(random.randint(0, 800-64), random.randint(50, 150), alienVel))
            aliens[i].moveAlien(aliens[i].alienX, aliens[i].alienY)
    if gg:
        again = playAgain.draw()
    if again:
        score = 0
        numAliens = 1
        aliens = list()
        alienVel = 1.5
        aliens.append(alien(random.randint(0, 800-64), random.randint(50, 150), alienVel))
        pygame.mixer.music.unpause()
        del playAgain
        playAgain = button(285, 300, "Play Again")
        
        again = False
        gg = False
    pygame.display.update() # update the display
pygame.quit()