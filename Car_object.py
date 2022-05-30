from config import *
import math
import pygame


class Car:
    def __init__(self):
        # Load Car Sprite and Rotate
        self.sprite = pygame.image.load(CAR).convert() # Convert Speeds Up A Lot
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite 
        self.position = [830, 920] # Starting Position
        self.distance = 0 # Distance Driven
        # self.position = [690, 740] # Starting Position
        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2] # Calculate Center
        self.angle = 0
        self.speed = 0
        self.radars = [] # List For Sensors / Radars
        self.speed_set = SPEED_OUTPUT_NODE # Flag For Default Speed Later on
        self.time = 0
        self.alive = True # Boolean To Check If Car is Crashed

    def update_corners(self):
        length = 0.5 * CAR_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]
    
    def update_Xpos(self): # move into the X-Direction
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed

        #not letting the position overflow putting a check between 20px and 120px
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)

    def update_Ypos(self):
        # move into the Y-Direction
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed


        #not letting the position overflow putting a check between 20px and 120px
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120) 
    
    def update(self, game_map):
    
        if not self.speed_set: # Set The Speed To MAX_SPEED for just focusing on left and right output nodes
            self.speed = MAX_SPEED

        # To get rotated car
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.update_Xpos()
        self.update_Ypos()

        # Increase Distance and Time
        self.distance += self.speed
        self.time += 1

        # Calculating New Center
        self.center = [int(self.position[0]) + CAR_SIZE_X / 2, int(self.position[1]) + CAR_SIZE_Y / 2]

        # Calculating Four Corners
        self.update_corners()
        

        # Check Collisions and clearing radars
        self.check_collision(game_map)
        self.radars.clear()

        # From -90 To 120 With Step-Size 45 Check Radar (5 radars for each car)
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    def check_radar(self, degree, game_map):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # While We Don't Hit BORDER_COLOR AND length < 300 (just a max) -> go further and further
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])


    def get_data(self): # returns distances to border
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = round(1-float(radar[1] / 300),3)
        return return_values

    
    def is_alive(self): # returns if the car is alive or not
        return self.alive
    
    def get_reward(self):
        return self.distance

    def check_collision(self, game_map):
        self.alive = True
        for point in self.corners: # If Any Corner Touches Border Color -> Crash
            # Assumes Rectangle
            # print(point) # debugging
            cur_color = game_map.get_at((int(point[0]), int(point[1])))
            # print(cur_color)
            if cur_color == BORDER_COLOR:
                self.alive = False
                break

    def draw(self, screen):
        screen.blit(self.rotated_sprite, self.position) # Draws car
        self.draw_radar(screen)

    def draw_radar(self, screen): # Draws all sensors
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, RADAR_LINE_COLOR, self.center, position, 1)
            pygame.draw.circle(screen, RADAR_ENDING_COLOR, position, 5)


    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image