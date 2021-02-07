import pygame
import random
from threading import Timer
import threading
import time
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

pipes = []
vel = 0.35
gravity = 0.0062
up = 60
newPipe_timer = 1.8
birdMovement = 0
music = False

ballColor = (48, 49, 49)
pipeColor = (71, 50, 50)
bgColor = (109, 110, 110)
scoreColor = (0, 0, 0)

green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (60, 60, 60)

bgSound = pygame.mixer.Sound(".\datas\BgSong.wav")
jumpSound = pygame.mixer.Sound(".\datas\jump.wav")
windSound = pygame.mixer.Sound(".\datas\windy.wav")
theme1 = pygame.image.load(".\datas\intro1.png")
theme2 = pygame.image.load(".\datas\intro2.png")
icon = pygame.image.load(".\datas\icony.png")

jumpSound.set_volume(0.7)
myfont = pygame.font.SysFont("comicsansms", 28)
musicfont = pygame.font.SysFont("comicsansms", 21)

pygame.display.set_icon(icon)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncy Ball")

# Pipe Class


class Pipe(object):
    def __init__(self):
        self.x = 810
        self.y = 0
        self.height = random.randrange(200, HEIGHT - 200)
        self.width = 60
        self.spacing = 174
        self.pipeOpening = 36

    def draw(self, win):
        pygame.draw.rect(
            win, pipeColor, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(
            win,
            pipeColor,
            (self.x - 2, self.y + self.height, self.width + 4, self.pipeOpening),
        )

        pygame.draw.rect(
            win,
            pipeColor,
            (self.x - 2, self.height + self.spacing,
             self.width + 4, self.pipeOpening,),
        )
        pygame.draw.rect(
            win,
            pipeColor,
            (
                self.x,
                self.height + self.spacing + self.pipeOpening,
                self.width,
                HEIGHT - self.height - self.spacing,
            ),
        )

    def update(self):
        self.x -= vel


# Bird Class
class Bird(object):
    def __init__(self):
        self.x = 150
        self.y = HEIGHT / 2
        self.radius = 50
        self.movement = 0

    def draw(self, win):
        pygame.draw.ellipse(
            win, ballColor, (self.x, self.y, self.radius, self.radius))

    def update(self):
        self.movement += gravity
        self.y += self.movement
        if self.y > HEIGHT - self.radius:
            self.y = HEIGHT - self.radius

        if self.y < 0:
            self.y = 0

    def hit(self, obj):
        return (
            self.y < obj.height + obj.pipeOpening
            or self.y > (obj.height + obj.spacing + obj.pipeOpening - self.radius - 7)
        ) and (self.x + self.radius > obj.x and self.x < obj.x + obj.width)

    def scores(self, score):
        label = myfont.render("Score: " + str(score), True, scoreColor)
        screen.blit(label, (20, 10))


# Adding pipes to the list every 1.3 sec
def create_Pipe():
    threading.Timer(newPipe_timer, create_Pipe).start()
    pipes.append(Pipe())


def message(msg, color, y, font_size):
    font = pygame.font.SysFont("Segoe UI Semibold", font_size)
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2) + y))
    screen.blit(text, text_rect)


# Intro Screen
def gameIntro():
    btn1 = pygame.transform.scale(theme1, (200, 150))
    btn2 = pygame.transform.scale(theme2, (200, 150))
    global music

    intro = True
    while intro:
        mouses = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        screen.fill((109, 110, 110))

        if 150 + 210 > mouses[0] > 150 and 400 + 160 > mouses[1] > 395:
            pygame.draw.rect(screen, black, (145, 395, 210, 160))
            if click[0] == 1:
                global pipeColor, ballColor, bgColor, scoreColor
                pipeColor = (92, 155, 155)
                ballColor = (198, 220, 220)
                bgColor = (24, 84, 84)
                scoreColor = (255, 255, 255)
                intro = False
                gameLoop()

        else:
            pygame.draw.rect(screen, gray, (145, 395, 210, 160))

        if 450 + 210 > mouses[0] > 450 and 400 + 160 > mouses[1] > 395:
            pygame.draw.rect(screen, black, (445, 395, 210, 160))
            if click[0] == 1:
                pipeColor = (100, 100, 100)
                ballColor = (215, 215, 215)
                bgColor = (195, 137, 137)
                scoreColor = (255, 255, 255)
                intro = False
                gameLoop()
        else:
            pygame.draw.rect(screen, gray, (445, 395, 210, 160))

        screen.blit(btn1, (150, 400))
        screen.blit(btn2, (450, 400))

        if 750 + 20 > mouses[0] > 750 and 23 + 20 > mouses[1] > 23:
            pygame.draw.rect(screen, (200, 200, 200), (750, 23, 20, 20))
            if click[0]:
                music = not music
        else:
            pygame.draw.rect(screen, (160, 160, 160), (750, 23, 20, 20))

        if music == True:
            pygame.draw.ellipse(screen, black, (755, 28, 10, 10))

        label = musicfont.render("Music: ", True, black)
        screen.blit(label, (682, 15))

        message("Bouncy Ball", black, -120, 92)
        message("Press 'SPACE' to start", white, -10, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                    gameLoop()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


pipes.clear()
create_Pipe()
# GameLoop


def gameLoop():
    pipes.clear()
    gameExit = False
    gameOver = False
    score = 0

    windSound.play(-1)
    bgSound.play(-1)
    if music:
        bgSound.set_volume(0.2)
        windSound.set_volume(1)
    else:
        bgSound.set_volume(0)
        windSound.set_volume(0)

    bird = Bird()

    while not gameExit:
        while gameOver == True:
            # screen.blit(bg, (0, 0))
            mouses = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            pipes.clear()
            screen.fill(bgColor)
            message("Game Over", scoreColor, -90, 95)
            message("Score: " + str(score), black, 10, 62)
            message("Press 'C' to continue", black, 120, 40)

            if 300+200 > mouses[0] > 300 and 460+46 > mouses[1] > 460:
                pygame.draw.rect(screen, (85, 85, 85), (300, 460, 200, 46))
                if click[0]:
                    gameIntro()
            else:
                pygame.draw.rect(screen, (70, 70, 70), (300, 460, 200, 46))
            label = myfont.render("Main Menu ", True, black)
            screen.blit(label, (330, 464))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_c:
                        gameExit = True
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                gameExit = True
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jumpSound.play()
                    bird.movement = 0
                    bird.movement -= 1.0

        screen.fill(bgColor)

        bird.draw(screen)
        bird.update()

        for i in range(len(pipes) - 1, -1, -1):
            pipes[i].draw(screen)
            pipes[i].update()

            if (
                bird.x > pipes[i].x + pipes[i].width
                and bird.x < pipes[i].x + pipes[i].width + 0.6
            ):
                if not bird.hit(pipes[i]):
                    score += 1
            bird.scores(score)

            if bird.hit(pipes[i]):
                gameOver = True
                bgSound.stop()
                windSound.stop()
                break
            if pipes[i].x < -60:
                pipes.pop(i)

        pygame.display.update()


gameIntro()
gameLoop()

pygame.quit()
quit()
