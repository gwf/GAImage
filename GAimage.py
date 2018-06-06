import pygame, pygame.gfxdraw
import math, random

width = 500
height = 500
radius = max(width, height) / 2
running = True

################################################################################

def init(): 
    global canvas
    global target
    random.seed(0)
    pygame.init()
    pygame.display.set_caption("GAimage")
    canvas = pygame.display.set_mode((width, height))
    target = pygame.image.load("daisy.jpg")
    tw = target.get_width()
    th = target.get_height()
    xs = width / tw
    ys = height / th
    s = min(xs, ys)
    nw = math.floor(tw * s)
    nh = math.floor(th * s)
    target = pygame.transform.smoothscale(target, (nw, nh))
    xoff = math.floor((width - nw) / 2)
    yoff = math.floor((height - nh) / 2)
    #canvas.fill((255,255,255,255))
    #canvas.blit(target, (xoff, yoff), None, pygame.BLEND_RGBA_SUB)

################################################################################

def randomCircle():
    return tuple(map(lambda x: random.random(), [None] * 7))    

################################################################################

def drawCircle(circle):
    pygame.gfxdraw.filled_circle(canvas, 
        math.floor(circle[0] * width),
        math.floor(circle[1] * height),
        math.floor(circle[2] * radius),
        pygame.Color(
            math.floor(circle[3] * 256),
            math.floor(circle[4] * 256),
            math.floor(circle[5] * 256),
            math.floor(circle[6] * 256)))

################################################################################

def main():
    global running
    init()
    for i in range(3):
        drawCircle(randomCircle())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

################################################################################

if __name__=="__main__":
    main()

################################################################################
