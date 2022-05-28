import math
import pygame
import json
from Car_object import *
from FeedForeward import *
database = 'database.json'
from utils import *


current_generation = 0 # Generation counter
CHILDREN_CARS = 500


def run_simulation(total_generations):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    game_map = pygame.image.load('map1.png').convert() # Convert Speeds Up A Lot

    cars = []
    nets = []
    for i in range(CHILDREN_CARS):
        cars.append(Car())
        nets.append(NN([5, 6, 4]))
        
    
    for current_generation in range(total_generations):
        
        counter = 0
        ded = []
        while True:

            for event in pygame.event.get(): # Exit On Quit Event
                if event.type == pygame.QUIT:
                    sys.exit(0)

            choice  = keyboard()
            move(cars, nets)
            
            still_alive = 0
            
            for i in range(len(cars)):
                if cars[i].is_alive() and (i not in ded):
                    still_alive += 1
                    cars[i].update(game_map)
                else:
                    ded.append(i)

            if still_alive == 0:
                break

            counter += 1
            if counter == 20*30: # Stop After About 20 Seconds
                break

            # Draw Map And All Cars That Are Alive
            screen.blit(game_map, (0, 0))
            for i in range(len(cars)):
                if cars[i].is_alive():
                    cars[i].draw(screen)
            

            # Display Info
            text = generation_font.render("Generation: " + str(current_generation), True, (0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (900, 450)
            screen.blit(text, text_rect)

            text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (900, 490)
            screen.blit(text, text_rect)

            pygame.display.flip()
            clock.tick(60) # 60 FPS
        
        Best_car = 0;
        reward = cars[0].get_reward()
        for i in range(len(cars)):
            if(cars[i].get_reward()>reward):
                reward = cars[i].get_reward()
                Best_car = i
        
        
        data_dict = {
            "Length": len(nets[Best_car].levels),
            "weights": [nets[Best_car].levels[0].weights, nets[Best_car].levels[1].weights],
            "biases": [nets[Best_car].levels[0].biases,nets[Best_car].levels[1].biases],
            "inputs": [nets[Best_car].levels[0].inputs,nets[Best_car].levels[1].inputs]
        }
        with open(database, "w") as f:
            json.dump(data_dict, f)
        f.close()

        logs(current_generation,Best_car, nets)

        cars = []
        nets = []
        for i in range(CHILDREN_CARS):
            cars.append(Car())
            nets.append(NN([5, 6, 4]))
            # cars[-1].speed = 28
        for i in range(10,CHILDREN_CARS):
            nets[i].mutate(nets[i], 0.15)
        
if __name__ == "__main__":
    run_simulation(100)

    