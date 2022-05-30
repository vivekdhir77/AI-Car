import pygame
from config import ROTATION_RATE, SPEED, MAX_SPEED

def logs(current_generation,Best_car,  nets, cars):
    print("Generation: ", current_generation)
    print("Length: ",len(nets[Best_car].levels))
    print("0 weights: ",nets[Best_car].levels[0].weights)
    print("1 weights: ",nets[Best_car].levels[1].weights)
    print("0 biase: ",nets[Best_car].levels[0].biases)
    print("1 biases: ",nets[Best_car].levels[1].biases)
    print("Reward : ",cars[Best_car].get_reward())
    print("\n\n\n")
    print("-------------------------------------------------------------------------------")

# def move(cars,choice):
def move(cars,nets):
# def move(cars_nets):
    for i in range(len(cars)):
        choice = nets[i].feedForeward(givenInputs = cars[i].get_data(), network =nets[i])
        # print(car.get_data())
        # print(choice)
        if choice[0] == 1 and cars[i].speed!=0:
            cars[i].angle += ROTATION_RATE # Left
        if choice[1] == 1 and cars[i].speed!=0:
            cars[i].angle -= ROTATION_RATE # Right
        if choice[3] == 1:
            if(cars[i].speed  >= 12):
                cars[i].speed -= SPEED # Slow Down
        if choice[2]==1:
            cars[i].speed += SPEED # Speed Up
            cars[i].speed = min(cars[i].speed, MAX_SPEED)
        # if(choice[2]==0 and not cars[i].speed==0):
        #     cars[i].speed -= 1
        #     cars[i].speed = max(0, cars[i].speed);
def keyboard():
    keys = pygame.key.get_pressed()
    moved = False
    choice = [0, 0, 0, 0]
    if keys[pygame.K_a]:
        choice[0] = 1
    if keys[pygame.K_d]:
        choice[1] = 1
    if keys[pygame.K_w]:
        choice[2] = 1
    if keys[pygame.K_s]:
        choice[3] = 1
    return choice

def lerp(A, B, t): # linear interpolation (used for mutation)
    return A+(B-A)*t;