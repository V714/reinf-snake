import enum
import os
from traitlets import Undefined
import pygame
import random
from enum import Enum

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Snake:
    def __init__(self):
        self.WIDTH = 640
        self.HEIGHT= 360
        self.WIN = pygame.display.set_mode((self.WIDTH,900))
        pygame.display.set_caption("SNAAAKE")

        self.BG_COLOR = (22,22,22)
        self.SNAKE_HEAD_COLOR = (100,100,252)
        self.SNAKE_TAIL_COLOR = (66,66,222)
        self.FOOD_COLOR = (180,22,22)
        self.TILE_COLOR = (22,22,180)
        self.TILE_SIZE = 20
        self.SNAKE_SPEED = 2

        self.W_TILES = (self.WIDTH / self.TILE_SIZE) - 1
        self.H_TILES = (self.HEIGHT / self.TILE_SIZE) - 1

        self.MAX_POINTS = self.H_TILES*self.W_TILES
        self.MAX_IDLE = 300
        self.IDLE = 0

        self.SNAKE_TAIL = []
        self.SNAKE_POS = (0,0)
        self.SNAKE_DIRECTION = Direction.UP
        self.FOOD_POS = (0,0)
        self.SCORE = 0
        self.SNAKE_FOOD_DISTANCE = 0
        self.reset()

        self.REWARD = 0
        self.GAMEOVER = False

    def random_pos(self,player=False):
        if player:
            return (random.randint(5,self.W_TILES-5),random.randint(5,self.H_TILES-5))
        return (random.randint(0,self.W_TILES),random.randint(0,self.H_TILES))

    def reset(self):
        snake_pos = self.random_pos(True)
        food_pos = self.random_pos()
        while snake_pos == food_pos:
            food_pos = self.random_pos()

        self.SNAKE_DIRECTION = Direction.UP
        self.SNAKE_POS = snake_pos
        self.FOOD_POS = food_pos
        self.SCORE = 0
        self.SNAKE_FOOD_DISTANCE = abs(self.SNAKE_POS[0] - self.FOOD_POS[0]) + abs(self.SNAKE_POS[1] - self.FOOD_POS[1])
        self.SNAKE_TAIL = [] # (snake_pos[0],snake_pos[1]+1),(snake_pos[0],snake_pos[1]+2)
        self.IDLE = 0
        self.GAMEOVER = False

    def handle_key(self,key):
        if key[pygame.K_a] and self.SNAKE_DIRECTION != Direction.LEFT:
            self.SNAKE_DIRECTION = Direction.LEFT
        elif key[pygame.K_d] and self.SNAKE_DIRECTION != Direction.RIGHT:
            self.SNAKE_DIRECTION = Direction.RIGHT
        elif key[pygame.K_w] and self.SNAKE_DIRECTION != Direction.UP:
            self.SNAKE_DIRECTION = Direction.UP
        elif key[pygame.K_s] and self.SNAKE_DIRECTION != Direction.DOWN:
            self.SNAKE_DIRECTION = Direction.DOWN
    
    def handle_action(self,action):
        if action == [0,0,0,1]:
            self.SNAKE_DIRECTION = Direction.LEFT
        elif action == [0,1,0,0]:
            self.SNAKE_DIRECTION = Direction.RIGHT
        elif action == [1,0,0,0]:
            self.SNAKE_DIRECTION = Direction.UP
        elif action == [0,0,1,0]:
            self.SNAKE_DIRECTION = Direction.DOWN
    
    def handle_movement(self):
        self.IDLE += 1
        for i in range(len(self.SNAKE_TAIL)-1,-1,-1):
            if i>0:
                self.SNAKE_TAIL[i] = self.SNAKE_TAIL[i-1]
            else:
                self.SNAKE_TAIL[0] = self.SNAKE_POS

        old_distance = self.SNAKE_FOOD_DISTANCE


        if self.SNAKE_DIRECTION == Direction.LEFT:
            self.SNAKE_POS = (self.SNAKE_POS[0]-1,self.SNAKE_POS[1])
        elif self.SNAKE_DIRECTION == Direction.RIGHT:
            self.SNAKE_POS = (self.SNAKE_POS[0]+1,self.SNAKE_POS[1])
        elif self.SNAKE_DIRECTION == Direction.DOWN:
            self.SNAKE_POS = (self.SNAKE_POS[0],self.SNAKE_POS[1]+1)
        elif self.SNAKE_DIRECTION == Direction.UP:
            self.SNAKE_POS = (self.SNAKE_POS[0],self.SNAKE_POS[1]-1)
        
        new_distance = abs(self.SNAKE_POS[0] - self.FOOD_POS[0]) + abs(self.SNAKE_POS[1] - self.FOOD_POS[1])
        
        if new_distance < old_distance:
            self.SNAKE_FOOD_DISTANCE = new_distance
            self.REWARD = 1


        if self.SNAKE_POS[0] < 0 or self.SNAKE_POS[0] > self.W_TILES or self.SNAKE_POS[1] < 0 or self.SNAKE_POS[1] > self.H_TILES:
            self.game_over()


    def eat(self):
        self.IDLE = 0
        food_pos = self.random_pos()
        while food_pos in self.SNAKE_TAIL:
            food_pos = self.random_pos()
        self.FOOD_POS = food_pos
        self.SNAKE_FOOD_DISTANCE = abs(self.SNAKE_POS[0] - self.FOOD_POS[0]) + abs(self.SNAKE_POS[1] - self.FOOD_POS[1])
        
        self.REWARD = 10
        self.SCORE += 1
        if self.SNAKE_DIRECTION == Direction.UP:
            self.SNAKE_TAIL.append((self.SNAKE_POS[0],self.SNAKE_POS[1]-1))
        elif self.SNAKE_DIRECTION == Direction.DOWN:
            self.SNAKE_TAIL.append((self.SNAKE_POS[0],self.SNAKE_POS[1]+1))
        elif self.SNAKE_DIRECTION == Direction.RIGHT:
            self.SNAKE_TAIL.append((self.SNAKE_POS[0]-1,self.SNAKE_POS[1]))
        elif self.SNAKE_DIRECTION == Direction.LEFT:
            self.SNAKE_TAIL.append((self.SNAKE_POS[0]+1,self.SNAKE_POS[1]))

    def check_collisions(self):
        if self.SNAKE_POS == self.FOOD_POS:
            self.eat()
        if self.SNAKE_POS in self.SNAKE_TAIL:
            self.game_over() 
        if self.IDLE > self.MAX_IDLE:
            self.game_over()

    def game_over(self):
        self.REWARD = -10
        self.GAMEOVER = True

    def draw_window(self):
        self.WIN.fill(self.BG_COLOR)

        # Uncomment for tiles grid
        """ for x in range(0,self.WIDTH,self.TILE_SIZE): # TILE GRID
            for y in range(0,self.HEIGHT,self.TILE_SIZE):
                pygame.draw.rect(self.WIN,self.TILE_COLOR, pygame.Rect(x,y,self.TILE_SIZE,self.TILE_SIZE),1)
        """
        pygame.draw.rect(self.WIN,self.SNAKE_HEAD_COLOR,pygame.Rect(self.SNAKE_POS[0]*self.TILE_SIZE,self.SNAKE_POS[1]*self.TILE_SIZE,self.TILE_SIZE,self.TILE_SIZE)) # SNAKE HEAD 
        pygame.draw.rect(self.WIN,self.FOOD_COLOR,pygame.Rect(self.FOOD_POS[0]*self.TILE_SIZE,self.FOOD_POS[1]*self.TILE_SIZE,self.TILE_SIZE,self.TILE_SIZE)) # SNAKE HEAD 
        for i in self.SNAKE_TAIL:
            pygame.draw.rect(self.WIN,self.SNAKE_TAIL_COLOR,pygame.Rect(i[0]*self.TILE_SIZE,i[1]*self.TILE_SIZE,self.TILE_SIZE,self.TILE_SIZE)) # SNAKE HEAD 
            
        pygame.display.update()

    def debug(self):
        direction = 0.0
        if self.SNAKE_DIRECTION == Direction.RIGHT:
            direction = 0.333
        elif self.SNAKE_DIRECTION == Direction.DOWN:
            direction = 0.666
        elif self.SNAKE_DIRECTION == Direction.LEFT:
            direction = 1.0
        
        
        return {"snake": (self.SNAKE_POS[0]/self.W_TILES,self.SNAKE_POS[1]/self.H_TILES),
                "food": (self.FOOD_POS[0]/self.W_TILES,self.FOOD_POS[1]/self.H_TILES),
                "score": self.SCORE/self.MAX_POINTS,
                "direction": direction
                }
    
    def debug_big(self): #576
        data = []
        for y in range(int(self.H_TILES+1)):
            for x in range(int(self.W_TILES+1)):
                if (x,y) == self.FOOD_POS:
                    data.append(1.0)
                elif (x,y) == self.SNAKE_POS:
                    data.append(0.6666)
                elif (x,y) in self.SNAKE_TAIL:
                    data.append(0.3333)
                else:
                    data.append(0.0)
        return data

    def debug_small(self):  # 576
        data = [
            int(self.SNAKE_POS[0] > self.FOOD_POS[0]),
            int(self.SNAKE_POS[0] < self.FOOD_POS[0]),
            int(self.SNAKE_POS[1] < self.FOOD_POS[1]),
            int(self.SNAKE_POS[1] > self.FOOD_POS[1]),
            int(self.SNAKE_POS[0]+1 > self.W_TILES or (self.SNAKE_POS[0]+1, self.SNAKE_POS[1]) in self.SNAKE_TAIL),
            int(self.SNAKE_POS[1]+1 > self.H_TILES or (self.SNAKE_POS[0],self.SNAKE_POS[1]+1) in self.SNAKE_TAIL),
            int(self.SNAKE_POS[0]-1 < 0 or (self.SNAKE_POS[0]-1, self.SNAKE_POS[1]) in self.SNAKE_TAIL),
            int(self.SNAKE_POS[1]-1 < 0 or (self.SNAKE_POS[0], self.SNAKE_POS[1]-1) in self.SNAKE_TAIL)]
        return data

    def give_reward(self):
        reward = self.REWARD
        self.REWARD = 0
        return reward

    def play_step(self,action):
        if self.GAMEOVER:
            self.reset()
        self.handle_action(action)
        self.handle_movement()
        self.check_collisions()
        if not self.GAMEOVER:
            self.draw_window()
        return self.give_reward(),self.GAMEOVER,self.SCORE

if __name__ == "__main__":
    newGame = Snake()
    
    clock = pygame.time.Clock()
    run = True
    while run:
        action=[0,0,0,0]
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            action=[0,0,0,1]
        elif key[pygame.K_d]:
            action=[0,1,0,0]
        elif key[pygame.K_w]:
            action=[1,0,0,0]
        elif key[pygame.K_s]:
            action=[0,0,1,0]

        print(newGame.play_step(action))
        clock.tick(newGame.SNAKE_SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()