#Importings
import pygame
from queue import PriorityQueue

#Initialization
pygame.init()
screen_width = 1200
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pathfinding board")
clock = pygame.time.Clock()

#Board
class Board:
    
    def __init__(self,gap,line_width):
        self.gap = gap
        self.total_rows = screen_width//self.gap - 1
        self.total_cols = screen_height//self.gap -1 
        self.drawn = []
        self.start = (1,1)
        self.end = (5,5)
        self.secondscore = 9999
        self.line_width = line_width
    
    def draw_grid(self): #gap = grid square length

        screen.fill((230,230,230))
    
        #Columns
        for i in range(screen_width//self.gap+1):
            pygame.draw.line(screen,"black",(self.gap*i,0),(self.gap*i,screen_height),self.line_width)
        
        #Rows
        for i in range(screen_height//self.gap+1):
            pygame.draw.line(screen,"black",(0,self.gap*i),(screen_width,self.gap*i),self.line_width)
    
    def draw(self):

        mouse_pos = pygame.mouse.get_pos() 
        keys = pygame.key.get_pressed()

        #Start position
        if keys[pygame.K_s]:
            box = (mouse_pos[0]//self.gap,mouse_pos[1]//self.gap)
            if box != self.end and box not in self.drawn:
                self.start = box
        
        #End position
        if keys[pygame.K_e]:
            box = (mouse_pos[0]//self.gap,mouse_pos[1]//self.gap)
            if box != self.start and box not in self.drawn:
                self.end = box
        
        #Start searching
        if keys[pygame.K_SPACE]:
            self.pathfinder()
            

        #Add Blocks
        if pygame.mouse.get_pressed()[0]:
            box = (mouse_pos[0]//self.gap,mouse_pos[1]//self.gap)
            if box not in self.drawn:
                self.drawn.append(box)
        
        #Remove Blocks
        if pygame.mouse.get_pressed()[2]:
            box = mouse_pos[0]//self.gap,mouse_pos[1]//self.gap
            if box in self.drawn:
                self.drawn.remove(box)

        #Draw blocks
        if self.drawn != []:
            for i in self.drawn:
                if i in [self.start,self.end]:
                    self.drawn.remove(i)
                pygame.draw.rect(screen,"black",(i[0]*self.gap,i[1]*self.gap,self.gap,self.gap))

        #Draw Start and End position
        pygame.draw.rect(screen,"red",(self.start[0]*self.gap,self.start[1]*self.gap,self.gap,self.gap))
        pygame.draw.rect(screen,"blue",(self.end[0]*self.gap,self.end[1]*self.gap,self.gap,self.gap))
        
    def check_valid_moves(self,row,col):
        self.neighbour = []
        if row < self.total_rows and not (row+1,col) in self.drawn : #DOWN
            self.neighbour.append([row+1,col])
        if col < self.total_cols and not (row,col+1) in self.drawn: #RIGHT
            self.neighbour.append((row,col+1))
        if row > 0 and not (row-1,col) in self.drawn: #UP
            self.neighbour.append([row-1,col])
        if col > 0 and not (row,col-1) in self.drawn: #LEFT
            self.neighbour.append([row,col-1])
        
        return self.neighbour
    
    def reconstruct_path(self,came_from,current):
        while current in came_from:
            current = came_from[current]
            pygame.draw.rect(screen,"purple",(current[0]*self.gap,current[1]*self.gap,self.gap,self.gap))

    def pathfinder(self):
        open_set = PriorityQueue()
        open_set.put((0, self.start))
        came_from = {}
        g_score = {(cellx , celly): float("inf") for cellx in range(self.total_rows+1) for celly in range(self.total_cols+1)} 
        f_score = g_score.copy()
        g_score[self.start] = 0
        f_score[self.start] = self.distance(self.start,self.end)

        open_set_hash = {self.start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  
            
            current = open_set.get()[1]
            open_set_hash.remove(current)

            if current == self.end:
                self.reconstruct_path(came_from, current)
                return True
            
            for neighbour in self.check_valid_moves(current[0],current[1]):
                temp_g_score = g_score[current] + 1
                neighbour = tuple(neighbour)
                if temp_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = temp_g_score
                    f_score[neighbour] = temp_g_score + self.distance(neighbour,self.end)
                    if neighbour not in open_set_hash:
                        open_set.put((f_score[neighbour],neighbour))
                        open_set_hash.add(neighbour)
                        
                        pygame.draw.rect(screen,"green",(neighbour[0]*self.gap,neighbour[1]*self.gap,self.gap,self.gap))
                    
            pygame.draw.rect(screen,"orange",(current[0]*self.gap,current[1]*self.gap,self.gap,self.gap))

                                         
    
    def distance(self, p1,p2):
        x1,y1 = p1
        x2,y2 = p2
        return abs(x1-x2) + abs(y1-y2)
        
        


board = Board(gap=40,line_width=2)

#Screen display
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
    board.draw_grid()
    board.draw()
    pygame.display.update()
    clock.tick(120)