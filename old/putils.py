import pygame
from pygame.locals import *


def anchorbox(position, box, anchor="topleft"):
    if anchor == "center":
        position = (
            position[0] - box[0] // 2,
            position[1] - box[1] // 2)
    elif anchor == "topright":
        position = (
            position[0] - box[0],
            position[1])
    elif anchor == "bottomright":
        position = (
            position[0] - box[0],
            position[1] - box[1])
    elif anchor == "bottomleft":
        position = (
            position[0],
            position[1] - box[1])
    return position

def textbox(surface, lines, position=(0,0), text_color=(255,255,255), anchor="topleft"):
    
    font = pygame.font.Font(None, 32)
    labels = []
    widths = []
    heights = []

    for line in lines:
        label = font.render(line, True, text_color)
        labels.append(label)
        widths.append(label.get_width())
        heights.append(label.get_height())

    textbox = pygame.Surface((max(widths), sum(heights)), 0, 32)
    x = y = 0
    for label, height in zip(labels, heights):
        textbox.blit(label, (x, y))
        y = y + height

    position = anchorbox(position, textbox.get_size(), anchor)
    surface.blit(textbox, position)
