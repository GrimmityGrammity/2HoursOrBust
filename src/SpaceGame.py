import pygame
from pygame.locals import *
import random
import time

def main():
    # Init screen
    pygame.init()

    # Define some colours
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 200, 0)
    BRIGHT_GREEN = (0, 255, 0)
    RED = (200, 0, 0)
    BRIGHT_RED = (255, 0, 0)

    display_width = 1240
    display_height = 720
    ship_width = 38

    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('2HoursOrBust')
    clock = pygame.time.Clock()

    # Fill Background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BLACK)

    # Image shit
    shipImg = pygame.image.load('spaceship.png')
    astroidImg = pygame.image.load('rock.png')

    def astroids_avoided(count):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Dodged:" + str(count), True, WHITE)
        screen.blit(text, (0,0))

    def astroids(x, y, w, h, colour):
        pygame.transform.scale(astroidImg, (int(w),int(h)))
        screen.blit(astroidImg, (x,y))
        # pygame.draw.rect(screen, colour, [x,y,w,h])

    def ship(x,y):
        screen.blit(shipImg, (x,y))

    def text_objects(text, font):
        text_surface = font.render(text, True, WHITE)
        return text_surface, text_surface.get_rect()

    def message_display(text):
        largeText = pygame.font.Font(None, 115)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.centerx = background.get_rect().centerx
        screen.blit(TextSurf, TextRect)

        pygame.display.update()

    def crash():
        message_display("You crashed, faggot!")
        time.sleep(2)
        game_loop()

    def button(msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        print(click)

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))

        smallText = pygame.font.Font(None, 20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(textSurf, textRect)

    def game_intro():

        intro = True

        while intro:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            screen.fill(BLACK)
            largeText = pygame.font.Font(None, 115)
            TextSurf, TextRect = text_objects("2HoursOrBust The Game", largeText)
            TextRect.center = ((display_width/2),(display_height/2))
            screen.blit(TextSurf,TextRect)

            mouse = pygame.mouse.get_pos()

            if display_width / 4 + 100 > mouse[0] > display_width / 4 and 450 + 50 > mouse[1] > 450:
                pygame.draw.rect(screen, BRIGHT_GREEN, (display_width / 4, 450, 100, 50))
            else:
                pygame.draw.rect(screen, GREEN, (display_width / 4, 450, 100, 50))

            pygame.draw.rect(screen, RED, ((display_width/4)*3, 450, 100, 50))

            button("GO!", display_width/4, 450, 100, 50, GREEN, BRIGHT_GREEN, game_loop)
            button("Quit", (display_width/4)*3, 450, 100, 50, RED, BRIGHT_RED, quitgame)

            pygame.display.update()
            clock.tick(15)

    def quitgame():
        pygame.quit()
        quit()

    def game_loop():
        # Event loop

        # Ship shit
        x = (display_width * 0.45)
        y = (display_height * 0.8)
        delta_x = 0
        ship_speed = 4
        dead = False

        #### Astroid shit #####
        astroid_startx = random.randrange(0, display_width)
        astroid_starty = -500
        astroid_speed = 7
        astroid_width = 100
        astroid_height = 100

        avoided = 0
        astroid_count = 1

        while not dead:
            for event in pygame.event.get():
                if event.type == QUIT:
                    dead = True

                # Move the ship left/right
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        delta_x += -5
                    elif event.key == pygame.K_RIGHT:
                        delta_x += 5
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        delta_x = 0

            x += delta_x

            screen.blit(background, (0,0))

            #### Render Objects ####
            astroids(astroid_startx, astroid_starty, astroid_width, astroid_height, RED)
            astroid_starty += astroid_speed

            ship(x, y)
            astroids_avoided(avoided)


            if astroid_starty > display_height:
                astroid_starty = 0 - astroid_height
                astroid_startx = random.randrange(0, display_width)
                # Deal with score
                avoided += 1
                # astroid_width += (avoided *1.2)
                astroid_speed += 1

            if x > display_width - ship_width or x < 0:
                crash()

            if y < astroid_starty + astroid_height:
                print("y crossover")
                if x > astroid_startx and x < astroid_startx + astroid_width or x + ship_width > astroid_startx and x + ship_width < astroid_startx + astroid_width:
                    print("x crossover")
                    crash()

            pygame.display.flip()
            clock.tick(60)

    game_intro()
    game_loop()
    quitgame()

if __name__ == '__main__': main()