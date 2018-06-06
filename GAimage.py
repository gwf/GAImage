import pygame, pygame.gfxdraw
import math, random

width = 100
height = 100
radius = max(width, height) / 2
popSize = 10
geneLen = 50
population = None
running = True

################################################################################

def init_graphics():
    global canvas
    pygame.init()
    pygame.display.set_caption("GAimage")
    canvas = pygame.display.set_mode((width, height))
    canvas.fill((0, 0, 0,255))

################################################################################

def init_target():
    global target
    image = pygame.image.load("daisy.jpg")
    tw = image.get_width()
    th = image.get_height()
    xs = width / tw
    ys = height / th
    scale = min(xs, ys)
    nw = math.floor(tw * scale)
    nh = math.floor(th * scale)
    image = pygame.transform.smoothscale(image, (nw, nh))
    xoff = math.floor((width - nw) / 2)
    yoff = math.floor((height - nh) / 2)
    target = pygame.Surface((width, height))
    target.fill((0, 0, 0,255))
    target.blit(image, (xoff, yoff))

################################################################################

def random_circle():
    return tuple(map(lambda x: random.random(), [None] * 7))    

################################################################################

def init_population():
    global population
    random.seed(0)    
    population = []
    for i in range(popSize):
        genes = []
        for j in range(geneLen):
            genes.append(random_circle())
        population.append(genes)

################################################################################

def init(): 
    init_graphics()
    init_target()
    init_population()

################################################################################

def draw_circle(circle, surface):
    pygame.gfxdraw.filled_circle(surface, 
        math.floor(circle[0] * width),
        math.floor(circle[1] * height),
        math.floor(circle[2] * radius),
        pygame.Color(
            math.floor(circle[3] * 256),
            math.floor(circle[4] * 256),
            math.floor(circle[5] * 256),
            math.floor(circle[6] * 256)))

################################################################################

def render_image(index):
    img = pygame.Surface((width, height))
    img.fill((0, 0, 0,255))
    for j in range(geneLen):
        draw_circle(population[index][j], img)
    return img
    
################################################################################

def compute_image_fitness(img):
    fitness = 0
    targetBytes = target.get_view('0').raw
    imageBytes = img.get_view('0').raw
    assert(len(targetBytes) == len(imageBytes))
    for j in range(len(targetBytes)):
        large = max(imageBytes[j], targetBytes[j])
        small = min(imageBytes[j], targetBytes[j])
        fitness += large - small
    return fitness
    
################################################################################

def compute_population_fitness():
    sumAll = 0
    scores = []
    for i in range(popSize):
        img = render_image(i)
        score = compute_image_fitness(img)
        scores.append((score, i))
    scores.sort(reverse=True)
    return scores        

################################################################################

def main():
    init()
    scores = compute_population_fitness()
    print(scores)

    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

################################################################################

if __name__=="__main__":
    main()

################################################################################
