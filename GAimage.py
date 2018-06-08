import pygame, pygame.gfxdraw
import numpy, math, random

width = 200
height = 200
radius = max(width, height) / 2

numGroups = 10
numShapes = 200
numCoords = 7

population = None
running = True
canvas = None

################################################################################

def init_graphics():
    global canvas
    pygame.init()
    pygame.display.set_caption("GAimage")
    canvas = pygame.display.set_mode((width, height))
    canvas.fill((0, 0, 0, 255))

################################################################################

def init_target():
    global target, targetArray
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
    target = pygame.Surface((width, height)).convert()
    target.fill((0, 0, 0,255))
    target.blit(image, (xoff, yoff))
    targetArray = numpy.fromstring(target.get_view('0').raw, dtype=numpy.int8)

################################################################################

def random_circle():
    return list(map(lambda x: random.random(), [None] * numCoords))    

################################################################################

def init_population():
    global population
    #random.seed(0)    
    population = []
    for i in range(numGroups):
        genes = []
        for j in range(numShapes):
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
    img.fill((0, 0, 0, 255))
    for j in range(numShapes):
        draw_circle(population[index][j], img)
    return img
    
################################################################################

def compute_image_fitness(img):
    imageArray = numpy.fromstring(img.get_view('0').raw, dtype=numpy.int8)
    diff = targetArray - imageArray
    return abs(diff).sum()
    
################################################################################

def compute_population_fitness():
    total = 0
    scores = []
    for i in range(numGroups):
        img = render_image(i)
        score = compute_image_fitness(img)
        scores.append((score, i))
    scores.sort()
    return scores        

################################################################################

def mutate_shape(shape):
    newShape = []
    for i in range(numCoords):
        newCoord = shape[i]
        if (random.random() < 0.01):
            newCoord += random.random() * 0.1
            newCoord = max(0, min(1-10E-17, newCoord))
        newShape.append(newCoord)
    return newShape

################################################################################

def mutate_group(group):
    nextGroup = []
    newOrder = list(range(len(group)))
    if (random.random() < 0.25):
        random.shuffle(newOrder)
    for i in range(len(group)):
        shape = mutate_shape(group[newOrder[i]])
        nextGroup.append(shape)
    return nextGroup

################################################################################

def evolve_population(scores):
    global population
    nextGen = []
    numKeep = max(1, int(numGroups / 10))
    for i in range(numKeep):
        nextGen.append(population[scores[i][1]])
    for i in range(numKeep, numGroups):
        nextGen.append(mutate_group(population[random.randrange(0, numKeep)]))
    population = nextGen

################################################################################

def main():
    init()
    global running, canvas
    while running:
        scores = compute_population_fitness()
        print(scores[0], scores[-1])
        canvas.blit(render_image(scores[0][1]), (0,0))
        evolve_population(scores)
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

################################################################################

if __name__=="__main__":
    main()

################################################################################
