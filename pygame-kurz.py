from pygame import display, draw, time, event
import pygame
from random import randrange

RAINDROP_LIMIT = 25
SCREEN_X_MAX = 800
SCREEN_Y_MAX = 600
raindrops = []
screen = display.set_mode([SCREEN_X_MAX, SCREEN_Y_MAX])
clock = time.Clock()

# Until key is pressed
while event.poll().type != pygame.KEYDOWN:

    # Clear screen
    screen.fill([0,0,0])

    # Define new droplet
    new_center = [randrange(100, SCREEN_X_MAX-100), randrange(100, SCREEN_Y_MAX-100)]
    new_color = [randrange(0,255) for _ in range(3)]
    raindrops.append([new_center, new_color, 0])

    # Remove big droplets
    raindrops = [x for x in raindrops if x[2] <= RAINDROP_LIMIT]

    # Enlarge and draw remaining droplets
    for i in range(len(raindrops)):
        raindrops[i][2] += 1
        draw.circle(screen, raindrops[i][1], raindrops[i][0], raindrops[i][2], 1)

    clock.tick(60)
    display.flip()