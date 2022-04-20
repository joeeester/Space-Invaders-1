import pygame
from pygame.locals import *
import sprites
import random

clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

rows = 5
cols = 5
enemy_cooldown = 1000
last_enemy_shot = pygame.time.get_ticks()

red = (255, 0, 0)
green = (0, 255, 0)


bg = pygame.image.load("bg.jpg")

bgy=0
def draw_bg():
  global bgy
  screen.blit(bg, (0, bgy))
  screen.blit(bg, (0, bgy-1000))
  bgy+=1
  if bgy>1000:
    bgy=0
 

class player(pygame.sprite.Sprite):
  def __init__(self,x,y, health):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("spaceships/player.png")
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]
    self.health_start = health
    self.health_remaining = health
    self.last_shot = pygame.time.get_ticks()

  def update(self):

    speed = 8

    cooldown = 500

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and self.rect.left > 0:
      self.rect.x -= speed
    if key[pygame.K_RIGHT] and self.rect.right < screen_width:
      self.rect.x += speed

    time_now = pygame.time.get_ticks()
      
    if key[pygame.K_SPACE] and time_now -self.last_shot > cooldown:
      bullet = Bullets(self.rect.      
     centerx, self.rect.top)
      bullet_group.add(bullet)
      self.last_shot = time_now

    self.mask = pygame.mask.from_surface(self.image)

    
    pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
    if self.health_remaining > 0:
       pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width* (self.health_remaining / self.health_start)),  15))

class Bullets(pygame.sprite.Sprite):
  def __init__(self,x,y,):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("spaceships/bullet.png")
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]

  def update(self):
    self.rect.y -= 5
    if self.rect.bottom < 0:
      self.kill()
    if pygame.sprite.spritecollide(self, enemy_group, True):
      self.kill()

class Enemy(pygame.sprite.Sprite):
  def __init__(self,x,y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("spaceships/enemy.png")
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]
    self.move_counter = 0
    self.move_direction = 1
  
  def update(self):
    self.rect.x += self.move_direction
    self.move_counter += 1
    if abs(self.move_counter) > 75:
      self.move_direction *=  -1
      self.move_counter *= self.move_direction
  

class Enemy_Bullets(pygame.sprite.Sprite):
  def __init__(self,x,y,):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("spaceships/enemybullet.png")
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]

  def update(self):
    self.rect.y += 2
    if self.rect.top > screen_height:
      self.kill()
    if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):

      spaceship.health_remaining -= 1





spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()

def create_enemy():
  for row in range(rows):
    for item in range(cols):
      enemy = Enemy(100 + item * 100, 100 + row * 70)
      enemy_group.add(enemy)

create_enemy()


spaceship = player(int(screen_width / 2), screen_height - 100, 3)
enemies=[]

spaceship_group.add(spaceship)

run = True
while run:

  clock.tick(fps)

  draw_bg()

  time_now = pygame.time.get_ticks()

  if time_now - last_enemy_shot > enemy_cooldown and len(enemy_bullet_group) < 5 and len(enemy_group) > 0:
    attacking_enemy = random.choice(enemy_group.sprites())
    enemy_bullet = Enemy_Bullets(attacking_enemy.rect.centerx, attacking_enemy.rect.bottom)
    enemy_bullet_group.add(enemy_bullet)
    last_enemy_shot = time_now
    
    

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  spaceship.update()
  bullet_group.update()
  enemy_group.update()
  enemy_bullet_group.update()
  
  spaceship_group.draw(screen)
  bullet_group.draw(screen)
  enemy_group.draw(screen)
  enemy_bullet_group.draw(screen)
  
  pygame.display.update()
pygame.quit()  
