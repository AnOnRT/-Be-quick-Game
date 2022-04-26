import pygame
import pygame_menu
import math
import random
import sys
from sys import stdin
pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

FPS = 60

ENEMY_SPAWN_RATE = 4
ENEMY_MIN_SIZE = 6
ENEMY_MAX_SIZE = 15
ENEMY_MIN_SPEED = 5
ENEMY_MAX_SPEED = 8

LIVE_POINTS_MIN_SIZE = 4
LIVE_POINTS_MAX_SIZE = 15
LIVE_POINTS_MIN_SPEED = 5
LIVE_POINTS_MAX_SPEED = 8

PLAYER_SPEED = 4
PLAYER_SIZE = 15
PLAYER_MAX_UP = 150
PLAYER_BEST_SCORE = [0,1]
PLAYER_MODE_CHECK = False
PLAYER_MODE = ""
newFont1 = pygame.font.Font(r"Lato-Italic.ttf", 25)
txt_mode = newFont1.render("", True, "brown")
checker = True

BG_COLOR = pygame.Color("black")
TEXT_COLOR = pygame.Color("white")
ENEMY_COLOR = pygame.Color("darkred")
PLAYER_COLOR = pygame.Color("darkgreen")

MENU_CHECK = True


class Player:
    def __init__(self):
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.color = PLAYER_COLOR
        self.position = (SCREEN_WIDTH/2, (SCREEN_HEIGHT - (SCREEN_HEIGHT / 10)))

    def draw(self, surface):
        r = self.get_rect()
        pygame.draw.rect(surface, self.color, r)

    def move(self, x, y):
        newX = self.position[0] + x
        newY = self.position[1] + y
        if newX < 0 or newX > SCREEN_WIDTH - PLAYER_SIZE:
            newX = self.position[0]
        if newY > SCREEN_HEIGHT - PLAYER_SIZE or newY < 0:
            newY = self.position[1]

        self.position = (newX, newY)

    def did_hit(self, rect):
        r = self.get_rect()
        return r.colliderect(rect)

    def get_rect(self):
        return pygame.Rect(self.position, (self.size, self.size))



class Enemy:
    def __init__(self):
        self.size = random.randint(ENEMY_MIN_SIZE, ENEMY_MAX_SIZE)
        self.speed = random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
        self.color = ENEMY_COLOR
        self.position = (random.randint(0, SCREEN_WIDTH - self.size), 0 - self.size)

    def draw(self, surface):
        r = self.get_rect()
        pygame.draw.rect(surface, self.color, r)

    def move(self):
        self.position = (self.position[0], self.position[1] + self.speed)


    def is_off_screen(self):
        return self.position[1] > SCREEN_HEIGHT

    def get_rect(self):
        return pygame.Rect(self.position, (self.size, self.size))


class World:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = Player()
        self.enemies = []
        self.gameOver = False
        self.score = 0
        self.enemy_counter = 0
        self.moveUp = False
        self.moveDown = False
        self.moveLeft = False
        self.moveRight = False

    def is_game_over(self):  # For game over screen
        return self.gameOver

    def update(self):
        self.score+=1
        if self.moveUp:
            self.player.move(0, -PLAYER_SPEED)
        if self.moveDown:
            self.player.move(0, PLAYER_SPEED)
        if self.moveLeft:
            self.player.move(-PLAYER_SPEED, 0)
        if self.moveRight:
            self.player.move(PLAYER_SPEED, 0)


        for e in self.enemies:
            e.move()
            if self.player.did_hit(e.get_rect()):
                self.gameOver = True
            if e.is_off_screen():
                self.enemies.remove(e)

        self.enemy_counter+=1

        if self.enemy_counter > ENEMY_SPAWN_RATE:
            self.enemy_counter = 0
            self.enemies.append(Enemy())



    def draw(self, surface):
        self.player.draw(surface)
        for e in self.enemies:
            e.draw(surface)


    def handle_keys(self, event):  # Key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.moveUp = True
            if event.key == pygame.K_DOWN:
                self.moveDown = True
            if event.key == pygame.K_LEFT:
                self.moveLeft = True
            if event.key ==pygame.K_RIGHT:
                self.moveRight = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.moveUp = False
            if event.key == pygame.K_DOWN:
                self.moveDown = False
            if event.key == pygame.K_LEFT:
                self.moveLeft = False
            if event.key ==pygame.K_RIGHT:
                self.moveRight = False


def run():
    global PLAYER_BEST_SCORE, ENEMY_SPAWN_RATE, PLAYER_MODE
    pygame.init()

    clock = pygame.time.Clock()  # Counting time after running the game
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My game project")

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    world = World()

    font = pygame.font.SysFont("monospace", 42)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == ord("r"):
                world.reset()
            elif event.type == pygame.KEYDOWN and event.key == ord("m"):
                MENU_CHECK = True
                running = False
                menu()
            else:

                world.handle_keys(event)

        clock.tick(FPS)

        surface.fill(BG_COLOR)

        world.draw(surface)

        screen.blit(surface, (0, 0))
        font = pygame.font.Font(r"Lato-Italic.ttf", 20)
        text1 = font.render("Score {0}".format(world.score), 1, TEXT_COLOR)
        text = font.render("Mode: " + PLAYER_MODE, 1, TEXT_COLOR)

        screen.blit(text, (5, 10))
        screen.blit(text1, (25, 30))


        if not world.is_game_over():
            world.update()



        if world.is_game_over():

            font = pygame.font.Font(r"Lato-Italic.ttf", 25)
            go = font.render("Game Over", 1, TEXT_COLOR)
            screen.blit(go, (SCREEN_WIDTH / 3 + 30, SCREEN_HEIGHT / 3))

            sw = font.render("Your score was " + str(world.score), 1, TEXT_COLOR)
            screen.blit(sw, (SCREEN_WIDTH / 2 - 105, SCREEN_HEIGHT / 3 + 50))

            hr = font.render("Hit R to Reset", 1, TEXT_COLOR)
            screen.blit(hr, (SCREEN_WIDTH / 3 + 25, SCREEN_HEIGHT / 2 + 45))

            hm = font.render("Hit M to go Menu section", 1, TEXT_COLOR)
            screen.blit(hm, (SCREEN_WIDTH / 3 - 30, SCREEN_HEIGHT / 2 + 95))

        pygame.display.update()
        b_s = PLAYER_BEST_SCORE[0]
        PLAYER_BEST_SCORE[0] = max(PLAYER_BEST_SCORE[0], world.score)
        if PLAYER_BEST_SCORE != b_s:
            PLAYER_BEST_SCORE[1] = PLAYER_MODE




def menu():
    global MENU_CHECK, ENEMY_SPAWN_RATE, PLAYER_BEST_SCORE, PLAYER_MODE, PLAYER_MODE_CHECK, txt_mode, checker
    pygame.init()


    res = (SCREEN_WIDTH, SCREEN_HEIGHT) #Game menu resolution

    screen1 = pygame.display.set_mode(res)
    screen2 = pygame.display.set_mode(res)

    color = TEXT_COLOR

    color_light = (170,170,170)

    color_dark = pygame.Color("darkgreen")

    newFont = pygame.font.Font(r"Lato-Italic.ttf", 25)
    headerFont = pygame.font.Font(r"Lato-Bold.ttf", 40)

    txt_header = headerFont.render("Welcome to Art's Game", True, color)
    if PLAYER_MODE_CHECK == True:
        txt_score = newFont.render(f"Your best score is {PLAYER_BEST_SCORE[0]} in the {PLAYER_MODE} mode", True, "blue")
    else:
        txt_score = newFont.render(f"Your best score is {PLAYER_BEST_SCORE[0]}", True, "blue")
    txt_play = newFont.render("Play", True, color)
    txt_easy = newFont.render("Easy", True, color)
    txt_medium = newFont.render("Medium", True, color)
    txt_hard = newFont.render("Hard", True, color)
    txt_quit = newFont.render("Quit", True, color)



    def logo_animation():
        logo = pygame.image.load(r"Art's Game_logo.png")
        logo = pygame.transform.scale(logo, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen1.fill(BG_COLOR)
        for i in range(-200,600):
            t=False
            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()

                    if (0 <= mouse[0] <= SCREEN_WIDTH) and (0 <= mouse[1] <= SCREEN_HEIGHT):
                        t = True
            if t == True:
                break

            screen1.blit(logo, (0, i))
            pygame.display.update()
            screen1.fill(BG_COLOR)

    if MENU_CHECK == True:
        logo_animation()
        MENU_CHECK = False

    check=True

    while check==True:

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.QUIT
                check = False


            if ev.type == pygame.MOUSEBUTTONDOWN:


                if (SCREEN_WIDTH / 2 - 80<= mouse[0] <= SCREEN_WIDTH / 2 + 60) and (SCREEN_HEIGHT / 3 <= mouse[1] <= SCREEN_HEIGHT / 3 + 40):
                    if PLAYER_MODE != "":
                        pygame.QUIT
                        check = False
                        PLAYER_MODE_CHECK = True
                        run()

                elif (SCREEN_WIDTH / 2 - 80 <= mouse[0] <= SCREEN_WIDTH / 2 + 60) and (SCREEN_HEIGHT / 3 + 100 <= mouse[1] <= SCREEN_HEIGHT / 3 + 140):

                    ENEMY_SPAWN_RATE = 3.5
                    PLAYER_MODE_CHECK = True
                    PLAYER_MODE = "Medium"
                    txt_mode = newFont.render("You have chosen " + PLAYER_MODE + " mode", True, "brown")
                    if checker == False:
                        screen2.blit(txt_mode, (SCREEN_WIDTH / 3 - 60, SCREEN_HEIGHT / 3 + 250))
                        checker = True
                    else:
                        screen2.fill((0,0,1))
                        screen2.blit(txt_mode, (SCREEN_WIDTH / 3 - 60, SCREEN_HEIGHT / 3 + 250))

                elif (SCREEN_WIDTH / 2 - 80 <= mouse[0] <= SCREEN_WIDTH / 2 + 60) and (SCREEN_HEIGHT / 3 + 50 <= mouse[1] <= SCREEN_HEIGHT / 3 + 90):

                    ENEMY_SPAWN_RATE = 5
                    PLAYER_MODE_CHECK = True
                    PLAYER_MODE = "Easy"

                    txt_mode = newFont.render("You have chosen " + PLAYER_MODE + " mode", True, "brown")
                    screen1.blit(txt_mode, (SCREEN_WIDTH / 3 - 60, SCREEN_HEIGHT / 3 + 250))
                    if checker == False:
                        screen2.blit(txt_mode, (SCREEN_WIDTH / 3 - 60, SCREEN_HEIGHT / 3 + 250))
                        checker = True
                    else:
                        screen2.fill((0,0,1))
                        screen2.blit(txt_mode, (SCREEN_WIDTH / 3 - 60, SCREEN_HEIGHT / 3 + 250))

                elif (SCREEN_WIDTH / 2 - 80 <= mouse[0] <= SCREEN_WIDTH / 2 + 60) and (SCREEN_HEIGHT / 3 + 150 <= mouse[1] <= SCREEN_HEIGHT / 3 + 190):
                    # pygame.QUIT
                    # check = False
                    PLAYER_MODE = "Hard"
                    PLAYER_MODE_CHECK = True
                    ENEMY_SPAWN_RATE = 2
                    txt_mode = newFont.render("You have chosen " + PLAYER_MODE + " mode", True, "brown")

                    if checker == False:
                        screen2.blit(txt_mode, (SCREEN_WIDTH / 3 - 60, SCREEN_HEIGHT / 3 + 250))
                        checker = True
                    else:
                        screen2.fill((0,0,1))
                        screen2.blit(txt_mode, (SCREEN_WIDTH / 3 - 60, SCREEN_HEIGHT / 3 + 250))

                elif (SCREEN_WIDTH / 2 - 80 <= mouse[0] <= SCREEN_WIDTH / 2 + 60) and (SCREEN_HEIGHT / 3 + 200 <= mouse[1] <= SCREEN_HEIGHT / 3 + 240):
                    pygame.QUIT
                    check = False

        pygame.draw.rect(screen1, "red", [SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 3, 140, 40])
        pygame.draw.rect(screen1, color_dark, [SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 3 + 50, 140, 40])
        pygame.draw.rect(screen1, color_dark, [SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 3 + 100, 140, 40])
        pygame.draw.rect(screen1, color_dark, [SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 3 + 150, 140, 40])
        pygame.draw.rect(screen1, color_dark, [SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 3 + 200, 140, 40])

        screen1.blit(txt_header, txt_header.get_rect(center=(SCREEN_WIDTH // 2, 50)))
        screen1.blit(txt_score, (SCREEN_WIDTH / 4 - 50, SCREEN_HEIGHT / 5))
        screen1.blit(txt_play, (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 3))
        screen1.blit(txt_easy, (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 3 + 50))
        screen1.blit(txt_medium, (SCREEN_WIDTH / 2 - 53, SCREEN_HEIGHT / 3 + 100))
        screen1.blit(txt_hard, (SCREEN_WIDTH / 2 - 35, SCREEN_HEIGHT / 3 + 150))
        screen1.blit(txt_quit, (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 3 + 200))
        screen1.blit(txt_mode, (SCREEN_WIDTH / 3 - 60, SCREEN_HEIGHT / 3 + 250))


        mouse = pygame.mouse.get_pos()

        if (SCREEN_WIDTH / 2 - 80 <= mouse[0] <= SCREEN_WIDTH / 2 + 60) and (SCREEN_HEIGHT / 3 <= mouse[1] <= SCREEN_HEIGHT / 3 + 40):
            pygame.draw.rect(screen1, color_light, [SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 3, 140, 40])
            screen1.blit(txt_play, (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 3))

        elif (SCREEN_WIDTH / 2 - 80 <= mouse[0] <= SCREEN_WIDTH / 2 + 60) and (SCREEN_HEIGHT / 3 + 100<= mouse[1] <= SCREEN_HEIGHT / 3 + 140):
            pygame.draw.rect(screen1, color_light, [SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 3 + 100, 140, 40])
            screen1.blit(txt_medium, (SCREEN_WIDTH / 2 - 53, SCREEN_HEIGHT / 3 + 100))

        elif (SCREEN_WIDTH / 2 - 80 <= mouse[0] <= SCREEN_WIDTH / 2 + 60) and (SCREEN_HEIGHT / 3 + 50 <= mouse[1] <= SCREEN_HEIGHT / 3 + 90):
            pygame.draw.rect(screen1, color_light, [SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 3 + 50, 140, 40])
            screen1.blit(txt_easy, (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 3 + 50))

        elif (SCREEN_WIDTH / 2 - 80 <= mouse[0] <= SCREEN_WIDTH / 2 + 60) and (SCREEN_HEIGHT / 3 + 150 <= mouse[1] <= SCREEN_HEIGHT / 3 + 190):
            pygame.draw.rect(screen1, color_light, [SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 3 + 150, 140, 40])
            screen1.blit(txt_hard, (SCREEN_WIDTH / 2 - 35,  SCREEN_HEIGHT / 3 + 150))

        elif (SCREEN_WIDTH / 2 - 80 <= mouse[0] <= SCREEN_WIDTH / 2 + 60) and (SCREEN_HEIGHT / 3 + 200 <= mouse[1] <= SCREEN_HEIGHT / 3 + 240):
            pygame.draw.rect(screen1, color_light, [SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 3 + 200, 140, 40])
            screen1.blit(txt_quit, (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 3 + 200))

        pygame.display.update()


    pygame.QUIT

menu()
