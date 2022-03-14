
from ast import Num
from site import venv
import pygame
from pygame.locals import *


pygame.init()

clock = pygame.time.Clock()
fps=60


screen_width=600
screen_height=600

screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Platformer")

# define game variables
tile_size=30

# load images
bg_img=pygame.image.load("img/arkaplan.png")

# bu grid küçük kareler çiziyor|||
# def draw_grid():
#     for line in range(0,20):
#         pygame.draw.line(screen,(255,255,255),(0,line * tile_size),(screen_width, line*tile_size))
#         pygame.draw.line(screen,(255,255,255),(line * tile_size , 0 ),(line* tile_size,screen_height))

## yukarısı kareler olusturuyor 
class Player():# karakteri oynatan sınıf 
    def __init__(self,x,y):
        self.images_right =[]
        self.images_left = []
        self.index=0
        self.counter=0
        for num in range(1, 5):
            img_right= pygame.image.load(f'img//Player/karakter{num}.png')
            img_right = pygame.transform.scale(img_right,(30,30))
            img_left = pygame.transform.flip(img_right, True,False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
            
        self.image = self.images_right[self.index]     
        self.rect=self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.vel_y=0
        self.jumped=False
        self.direction=0
        
    def update(self,game_over):  
        dx=0
        dy=0
        walk_coldown=5
        if game_over == 0:
            
            #Klavye kontrolü
            key=pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped==False:
                self.vel_y= -5
                self.jumped==True
            if key[pygame.K_SPACE]== False:
                self.jumped == False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1 
                self.direction=1
            if key[pygame.K_LEFT]== False and key[pygame.K_RIGHT] == False:
                self.counter=0
                self.index=0
                self.image= self.images_right[self.index]
                if self.direction==1:
                    self.image=self.images_right[self.index]
                if self.direction== -1 :
                    self.image=self.images_left[self.index]  
            
            #animasyon işleme karakter 
            if self.counter > walk_coldown: 
                self.counter=0
                self.index +=1
                if self.index >= len(self.images_right):
                    self.index=0
                if self.direction==1:
                    self.image=self.images_right[self.index]
                if self.direction== -1 :
                    self.image=self.images_left[self.index]    
            
            # yerçekimi ekle
            self.vel_y +=1
            if self.vel_y > 10:
                self.vel_y = 10 
            dy += self.vel_y    
            
            
            # çarpışma kontrolü tespit etme
            for tile in wold.tile_list:
                # x ekseni çarpışma kontrolü
                if tile[1].colliderect(self.rect.x + dx , self.rect.y , self.width, self.height):
                    dx=0
                #y eksenin çarpışması tespit etme 
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #yerin altındaki atşlama kontrolü
                    if self.vel_y<0:
                        dy=tile[1].bottom-self.rect.top
                        self.vel_y=0
                    # düşme kontrolü
                    elif self.vel_y >= 0:
                        dy=tile[1].top-self.rect.bottom
                        self.vel_y=0
                        
                        
            # düsman için  kontrol yapma
            if pygame.sprite.spritecollide(self,düsman_group,False):
                game_over=-1
            # lav için kontrol etme
            if pygame.sprite.spritecollide(self,lav_group,False):
                game_over=-1          
            
            # karakter kordinat güncellemesi
            
            self.rect.x += dx
            self.rect.y += dy 
            
            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                dy=0
                
        #karakteri ekrana ciziyor
        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen,(255,255,255),self.rect,1)        
        
        return game_over
        
           
            
        
        

        
class World():
    def __init__(self,data):
        self.tile_list=[]
        #resim yukleme alani
        dirt_img=pygame.image.load("img/dirt.png")
        cimen_img=pygame.image.load("img/grass.png")
        
        
        row_count=0
        for row in data:
            col_count=0
            for tile in row:
                if tile ==1:
                    img = pygame.transform.scale(dirt_img,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(cimen_img,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)    
                if tile ==3:
                    düsman=Enemy(col_count*tile_size, row_count*tile_size-20)
                    düsman_group.add(düsman)
                if tile ==6:
                    lav=Lava(col_count*tile_size, row_count*tile_size + (tile_size //2))
                    lav_group.add(lav)
                    
                col_count +=1
            row_count += 1   
                    
              
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
            pygame.draw.rect(screen,(255,255,255), tile[1],2 )
            
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/düsman.png") 
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y     
        self.move_direction=1
        self.move_counter=0
        
    def update(self):
        self.rect.x += self.move_direction   
        self.move_counter += 1
        if abs(self.move_counter) > 20:
            self.move_direction *= -1
            self.move_counter *= -1
            
class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load("img/Lav.png") 
        self.image=pygame.transform.scale(img,(tile_size,tile_size//2))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y     
        self.move_direction=1
        self.move_counter=0
               
        
        
# aşağıdaki veri seti map yerlesim kısmıdır                
world_data= [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


run=True
player=Player(50,screen_height-105)
düsman_group=pygame.sprite.Group()
lav_group=pygame.sprite.Group()
wold=World(world_data)
while run:
    clock.tick(fps)
    screen.blit(bg_img,(0,0))
    
    wold.draw()
    
    düsman_group.update()
    düsman_group.draw(screen)
    lav_group.draw(screen)
    game_over = player.update(game_over)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()        
            
pygame.quit()
            
            