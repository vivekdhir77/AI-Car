WIDTH = 1920
HEIGHT = 1080

CAR_SIZE_X = 35   
CAR_SIZE_Y = 35

BORDER_COLOR = (255, 255, 255, 255) # Color To Crash on Hit
RADAR_LINE_COLOR = (255, 0, 0)
RADAR_ENDING_COLOR = (0, 255, 0)


NN_layers = [5, 6, 4]
SPEED_OUTPUT_NODE = False

BEST_CAR_STORE = True # if true only stores best car in storage and doesn't change storage every generation
DATABASE = 'storage/DATABASE.json'

MAP = 'dataset/map1.png'
CAR = 'imgs/carp.png'
FONT = "Arial"

MUTATION_RATE = 0.3
MAX_GENERATIONS = 100
CHILDREN_CARS = 500

CAR_START_POSITION = [830, 920]
MAX_SPEED = 6
ROTATION_RATE = 4
SPEED = 2

FPS = 60