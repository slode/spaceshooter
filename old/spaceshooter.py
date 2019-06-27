import pygame, sys
from pygame.locals import *
from entities import *
from menu import *
from putils import *
import time
import datetime
import random

FPS = 30 # frames per second setting

def main():
    pygame.init()
    
    fpsClock = pygame.time.Clock()
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    font = pygame.font.Font(None, 32)
    pygame.display.set_caption('Space Shooter!!')
    if True:
        SCREEN_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        DISPLAYSURF = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN | pygame.DOUBLEBUF, 32)
    else:
        SCREEN_SIZE = (800, 600)
        DISPLAYSURF = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF, 32)

    BACKGROUND = (0, 0, 0)
    #BACKGROUND = (100, 100, 100)
    menu = cMenu(50, 50, 20, 5, 'vertical', 100, DISPLAYSURF,
               [('Start Game', 2, None),
                ('Highscore',  9, None),
                ('Exit',       10, None)])
    menu.set_center(True, True)
    menu.set_alignment('center', 'center')
    
    game = Game(SCREEN_SIZE)
    accel_x = [0.0, 0.0]
    accel_y = [0.0, 0.0]
    shoot = False
    game_state = 0
    rect_list = []
    pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
    time_start = None
    duration = 0.0
    while True: # the main game loop

        DISPLAYSURF.fill(BACKGROUND)
        game.update()
        game.draw(DISPLAYSURF)

        if game_state == 0:
            # Game initialization
            game.reset()
            game_state = 1

        if game_state == 1:
            for event in pygame.event.get():
                if event.type == KEYDOWN or event.type == EVENT_CHANGE_STATE:
                    rect_list, game_state = menu.update(event, game_state)
                    if event.key in [K_ESCAPE]:
                        game_state = 10

                if event.type == QUIT or game_state == 10:
                     pygame.quit()
                     sys.exit()
            menu.draw_buttons()

        elif game_state == 9:
            highscores = []
            with open("highscore.txt", "a+") as f:
                f.seek(0)
                highscores = [a.strip().split("\t") for a in f.readlines()]
            highscores = sorted(highscores, key=lambda x: float(x[1]))
            no_scores = min(len(highscores), 10)
            highscore_text = []
            highscore_text.append("Highscores")
            
            for i in range(no_scores):
                ts = float(highscores[i][0])
                duration = float(highscores[i][1])
                highscore_text.append("{}. {:.2f} seconds on {}".format(
                    i+1, duration, 
                    datetime.datetime.fromtimestamp(ts).strftime('%d. %m %Y')))
            
            textbox(DISPLAYSURF, 
                    highscore_text,
                    position=DISPLAYSURF.get_rect().center,
                    anchor="center")
            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key in [K_SPACE, K_RETURN, K_ESCAPE]:
                        game_state = 1

        elif game_state == 4:
            # game end mode, failure
            textbox(DISPLAYSURF, 
                    ["You lost!"],
                    position=DISPLAYSURF.get_rect().center,
                    anchor="center")

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key in [K_SPACE, K_RETURN, K_ESCAPE]:
                        game_state = 0
            
        elif game_state == 6:
            text = "You finished in {:10.2f} seconds!".format(duration)
                
            textbox(DISPLAYSURF, 
                    [text],
                    position=DISPLAYSURF.get_rect().center,
                    anchor="center")

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key in [K_SPACE, K_RETURN, K_ESCAPE]:
                        game_state = 0

        elif game_state == 2:
            # start game
            shoot = False
            game.start()
            game_state = 3
            time_start = time.time()
            
        elif game_state == 3:
            # game loop
            
            for event in pygame.event.get():
                if event.type == QUIT:
                     pygame.quit()
                     sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        accel_y[0]  = accel_y[0] - 1
                    elif event.key == K_DOWN:
                        accel_y[1]  = accel_y[1] + 1
                    elif event.key == K_LEFT:
                        accel_x[0]  = accel_x[0] - 1
                    elif event.key == K_RIGHT:
                        accel_x[1]  = accel_x[1] + 1
                    elif event.key == K_SPACE:
                        shoot = True
                    elif event.key == K_ESCAPE:
                        game_state = 0
                elif event.type == KEYUP:
                    if event.key == K_UP:
                        accel_y[0]  = 0
                    elif event.key == K_DOWN:
                        accel_y[1]  = 0
                    elif event.key == K_LEFT:
                        accel_x[0]  = 0
                    elif event.key == K_RIGHT:
                        accel_x[1]  = 0
                    elif event.key == K_SPACE:
                        shoot = False

            game.ship.speed_x = game.ship.speed_x + sum(accel_x) * 2.5
            game.ship.speed_y = game.ship.speed_y + sum(accel_y) * 2.5

            if shoot:
                game.ship.shoot()

            duration = time.time() - time_start
            text = "time: {:2.2f} lives: {}".format(duration, game.ship.health)
            textbox(DISPLAYSURF,
                    [text],
                    position=DISPLAYSURF.get_rect().bottomright,
                    anchor="bottomright")

            if game.finished():
                if game.success():
                    game_state = 5
                else:
                    game_state = 4

        elif game_state == 5:
            # game end mode, success
            with open("highscore.txt", "a") as hsfile:
                text = "{}\t{}\n".format(time.time(), duration)
                hsfile.write(text)
            game_state = 6

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == "__main__":
   main()
