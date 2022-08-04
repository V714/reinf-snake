
import pygame
pygame.font.init()
import numpy

class DisplayText:
    def __init__(self):
        
        self.WIDTH = 640
        self.HEIGHT = 900
        self.REWARD = 0
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("TEXT")

        self.LINE = (100, 100, 255)
        self.font = pygame.font.Font('Poppins.ttf', 20)

    def draw_text(self, reward, score, n_games,train):
        training = False
        if train:
            self.REWARD = 0
            training = True
        else:
            self.REWARD += reward

        text_surface1 = self.font.render(f'Reward: {self.REWARD}', False, self.LINE)
        text_surface2 = self.font.render(f'Score: {score}', False, self.LINE)
        text_surface3 = self.font.render(f'Game: {n_games}', False, self.LINE)
        text_surface4 = self.font.render(f'Training: {training}', False, self.LINE)
        self.WIN.blit(text_surface1, (320, 500))
        self.WIN.blit(text_surface2, (320, 530))
        self.WIN.blit(text_surface3, (320, 560))
        self.WIN.blit(text_surface4, (320, 620))

        pygame.display.update()


class Display:
    def __init__(self):
        self.WIDTH = 640
        self.HEIGHT = 900
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("NN")

        self.BG_COLOR = (0, 0, 0)
        self.NEURON = (100, 100, 100)
        self.NEURON_ACTIVATED = (100, 255, 100)
        self.LINE = (30, 30, 155)
        self.my_font = pygame.font.SysFont('Comic Sans MS', 20)


    def draw_window(self,inp,hs1,out):

        neurons = []
        pos = 600
        for i in inp:
            neurons.append((30, pos, i,0))
            pos += 10
        pos = 380
        for i in hs1:
            neurons.append((70, pos, i, 1))
            pos += 10
        pos = 620
        for i in out:
            neurons.append((150, pos, i, 2))
            pos += 10
        
        for i in neurons:
            if i[3] == 0:
                for i2 in neurons:
                    if i2[3] == 1:
                        pygame.draw.line(self.WIN, self.LINE,
                                         (i[0], i[1]), (i2[0], i2[1]))

            if i[3] == 1:
                for i2 in neurons:
                    if i2[3] == 2:
                        pygame.draw.line(self.WIN, self.LINE,
                                         (i[0], i[1]), (i2[0], i2[1]))

        for i in neurons:
            pygame.draw.circle(self.WIN,self.NEURON_ACTIVATED if i[2]>0 else self.NEURON,(i[0],i[1]),3)
            
        pygame.draw.line(self.WIN, (255,255,000),(0,360),(640,360))
        pygame.display.update()



if __name__ == "__main__":
    NN = Display()
    run = True
    input = [0,0,0,1,0,1,0]
    hs1 = [0.12,0.43,0,1,0.,1,0]
    hs2 = [0.62,0.43,0,1,0.,1,0]
    output = [0,0,1,0]
    while run:
        NN.draw_window(input,hs1,hs2,output)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
