import pygame
import json
from Car_object import *
from FeedForeward import *
from utils import *

def run_simulation(total_generations):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont(FONT, 30)
    alive_font = pygame.font.SysFont(FONT, 20)
    game_map = pygame.image.load(MAP).convert() # Convert Speeds Up A Lot

    cars = [Car() for i in range(CHILDREN_CARS)]
    nets = [NN(NN_layers) for i in range(CHILDREN_CARS)]
    
    for current_generation in range(total_generations):
        
        counter = 0 # timer for each generation
        ded = []
        while True:
            for event in pygame.event.get(): # Exit On Quit Event
                if event.type == pygame.QUIT:
                    sys.exit(0)

            # choice  = keyboard()
            move(cars, nets) # moves cars based on neural network choices
            
            still_alive = 0 # counts no of alive cars
            
            for i in range(len(cars)):
                if cars[i].is_alive() and (i not in ded):
                    still_alive += 1
                    cars[i].update(game_map)
                else:
                    ded.append(i)

            if still_alive == 0:
                break

            counter += 1
            if counter == 1000: # Stop After About 20 Seconds
                break

            # Draw Map And All Cars That Are Alive
            screen.blit(game_map, (0, 0))
            for i in range(len(cars)):
                if cars[i].is_alive():
                    cars[i].draw(screen) # draws all alive cars
            

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
            clock.tick(FPS) # 60 FPS
        
        Best_car = 0;# finding the best car index to store in the database
        reward = cars[0].get_reward()
        for i in range(len(cars)):
            if(cars[i].get_reward()>reward):
                reward = cars[i].get_reward()
                Best_car = i
        
        
        data_dict = { # JSONifying BEST CAR data to store in database
            "Length": len(nets[Best_car].levels),
            "weights": [nets[Best_car].levels[0].weights, nets[Best_car].levels[1].weights],
            "biases": [nets[Best_car].levels[0].biases,nets[Best_car].levels[1].biases],
            "inputs": [nets[Best_car].levels[0].inputs,nets[Best_car].levels[1].inputs],
            "reward": cars[Best_car].get_reward()
        }

        
        if BEST_CAR_STORE:
            old_reward = -1
            try:
                f = open(DATABASE)
                data = json.load(f)
                old_reward = data['reward']
            except:
                with open(DATABASE, "w") as f:
                    json.dump(data_dict, f)
                f.close()
            if(cars[Best_car].get_reward()>old_reward):
                with open(DATABASE, "w") as f:
                    json.dump(data_dict, f)
                f.close()
        else:
            with open(DATABASE, "w") as f:
                json.dump(data_dict, f)
            f.close()
        logs(current_generation,Best_car, nets, cars)

        cars = []
        nets = []
        for i in range(CHILDREN_CARS):
            cars.append(Car())
            nets.append(NN(NN_layers))

        # genetic algorithm part (Mutation, Crossover)
        # Here we are only doing mutation for all cars except first 10 cars
        for i in range(10,CHILDREN_CARS): 
            nets[i].mutate(nets[i], MUTATION_RATE)
        