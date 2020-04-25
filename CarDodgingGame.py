# Modules and packages

import pygame
from time import sleep
import random


# Classes

class player():
    def __init__(self, road, height):
        self.width = 50
        self.height = self.width * 2
        self.x = road[0]
        self.y = height - self.height - self.height
        self.car = pygame.transform.scale(
            pygame.image.load("car1.png"), (self.width, self.height))

    def draw(self, window):
        window.blit(self.car, (self.x, self.y))

    def move(self, road, hit):
        if self.x == road[0] and hit == 1:
            self.x = road[1]
        elif self.x == road[1] and hit == 0:
            self.x = road[0]


class road():
    def __init__(self, width, height, car_width):
        self.slot_width = car_width
        self.road_0 = width // 2 - self.slot_width - 20
        self.road_1 = width // 2 + 20
        self.road = [self.road_0, self.road_1]
        self.height = height
        self.width = 10

    def draw(self, window, color, width):
        ho = 2*self.slot_width + 40 + 30 + 20
        pygame.draw.rect(window, (40, 43, 42), (self.road_0 -
                                                self.width-15, 0, ho, self.height))
        pygame.draw.rect(window, color, (self.road_0 -
                                         self.width - 15, 0, self.width, self.height))
        pygame.draw.rect(window, color, (self.road_1 +
                                         self.slot_width + 15, 0, self.width, self.height))
        pygame.draw.rect(window, (255, 255, 255), (width/2 - 1,
                                                   0, 2, self.height))


class enemy():
    def __init__(self, road, car, speed=0.6):
        self.width = car.width
        self.height = car.height
        self.name = 'car'+str(random.randint(2, 8))+'.png'
        self.car = pygame.transform.scale(
            pygame.image.load(self.name), (self.width, self.height))
        self.x = road[random.randint(0, 1)]
        self.y = - self.height
        self.speed = speed
        self.acceleration = 0.0003

    def draw(self, window):
        window.blit(self.car, (self.x, self.y))

    def move(self, height):
        self.y += self.speed
        self.speed += self.acceleration


# Variables
width = 600
height = 800
fps = pygame.time.Clock()
hit = 0
enem_num = -1
border_color = (255, 0, 0)  # #990000
background_color = (0, 0, 0)  # #000000
text_color = (153, 21, 54)  # #991536
score = 0

pygame.init()
window = pygame.display.set_mode((width, height))


game_running = True
pause = False
car_width = 50
ro = road(width, height, car_width)
player1 = player(ro.road, height)
enemmy = []

# Functions


def enemies(enemmy, road, player, height, enem_num):
    if len(enemmy) == 0 and enem_num < 1:
        enem = enemy(road, player)
        enem_num += 1
        enemmy.append(enem)
    elif enemmy[0].y > height/2 and enem_num < 1:
        enem = enemy(road, player, enemmy[0].speed)
        enem_num += 1
        enemmy.append(enem)

    return enem_num


def draw_enemies(window, enemmy):
    for enem in enemmy:
        enem.draw(window)


def move_enemies(enemmy, height, enem_num, score):
    for enem in enemmy:
        if enem.y > height:
            enemmy.remove(enem)
            enem_num = 0
            score += 1
        enem.move(height)
    return enem_num, score


def game_over(player, enemmy):
    for enem in enemmy:
        if player.x == enem.x and (player.y < enem.y < player.y + enem.height or player.y < enem.y + enem.height < player.y + enem.height):
            return False
    return True


def text_to_screen_score(window, score, pos, text):
    font = pygame.font.SysFont(None, 50)
    stext = text + str(score)
    score_text = font.render(stext, True, text_color)
    window.blit(score_text, pos)
    pygame.display.update()


# Main code

while game_running:
    window.fill(background_color)
    if not pause:
        enem_num, score = move_enemies(enemmy, height, enem_num, score)
        enem_num = enemies(enemmy, ro.road, player1, height, enem_num)
        player1.move(ro.road, hit)

    ro.draw(window, border_color, width)
    draw_enemies(window, enemmy)
    player1.draw(window)

    game_running = game_over(player1, enemmy)
    ###controls###
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not pause:
                hit = 1

            if event.key == pygame.K_LEFT and not pause:
                hit = 0

            if event.key == pygame.K_SPACE:
                pause = not pause

    ##############
    text_to_screen_score(window, score, (20, 20), "")
    pygame.display.update()

window.fill(background_color)
text_to_screen_score(window, score, (20, 100), "your score is: ")

sleep(5)

pygame.quit()
