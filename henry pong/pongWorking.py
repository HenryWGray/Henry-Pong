# class ball():
#     def __init__(self, window, posx, posy, velx, vely, radius, color):
#         self.window = window
#         self.posx = posx
#         self.posy = posy
#         self.velx = velx
#         self.vely = vely
#         self.radius = radius
#         self.color = color
#     def overlap(self, objectC):
#         if self.posx+self.radius >= objectC.posx and self.posx-self.radius <= objectC.posx+objectC.width:
#             overlapX = True
#         if self.posx+self.radius >= objectC.posy and self.posx-self.radius <= objectC.posy+objectC.height:
#             overlapY = True
#         if overlapX and overlapY:
#             return(True)
#     def bounce(self):
#         global WINDOW_WIDTH, WINDOW_HEIGHT, left_paddle, right_paddle, bounce_sound_wall, bounce_sound_paddle
#         if self.posy > WINDOW_HEIGHT-self.radius:
#             self.posy = WINDOW_HEIGHT-self.radius
#             self.vely = -abs(self.vely)
#         elif self.posy < self.radius:
#             self.posy = self.radius
#             self.vely = abs(self.vely)
#         if self.overlap(right_paddle) and self.velx > 0:
#             pygame.mixer.Sound.play(bounce_sound_paddle)
#             self.velx = -(abs(self.velx) + 1)
#             self.vely = abs(self.velx)*-np.sin((-(self.posy+self.radius)+(right_paddle.posy+right_paddle.height/2))*np.pi/180) + self.vely
#         if self.overlap(left_paddle) and self.velx < 0:
#             pygame.mixer.Sound.play(bounce_sound_paddle)
#             self.velx = (abs(self.velx) + 1)
#             self.vely = abs(self.velx)*-np.sin((-(self.posy+self.radius)+(left_paddle.posy+left_paddle.height/2))*np.pi/180) + self.vely
#         if self.posx + self.radius > WINDOW_WIDTH:
#             left_paddle.score += 1
#             self.reset()
#         elif self.posx - self.radius <= 0:
#             right_paddle.score += 1
#             self.reset()
#     def reset(self):
#         global WINDOW_HEIGHT, WINDOW_WIDTH
#         self.posx=WINDOW_WIDTH/2
#         self.posy=WINDOW_HEIGHT/2
#         self.velx=3*abs(self.velx)/self.velx
#         self.vely=randint(-3000,3000)/1000
#     def update(self):
#         self.bounce()
#         self.posx = self.posx+self.velx
#         self.posy = self.posy+self.vely
#         self.render()
#     def render(self):
#         pygame.draw.circle(self.window,self.color,(self.posx,self.posy),self.radius)


# class paddle():
#     def __init__(self, window, posx, posy, velocity, width, height, color, strat, score, difficulty = "medium"):
#         self.window = window
#         self.posx = posx
#         self.posy = posy
#         self.vel = velocity
#         self.width = width
#         self.height = height
#         self.color = color
#         self.strat = strat
#         self.score = score
#         self.diff = difficulty
#     def update(self, ball):
#         global WINDOW_HEIGHT
#         if self.strat == "player":
#             self.player()
#         elif self.strat == "basic_ai":
#             self.basic_ai(ball)
#         elif self.strat == "advanced_ai":
#             self.advanced_ai(ball, self.diff)
#         if self.posy>WINDOW_HEIGHT-self.height:
#             self.posy=WINDOW_HEIGHT-self.height
#         elif self.posy<0:
#             self.posy=0
#         self.render()
#     def player(self):
#         global keys
#         self.posy += (keys[pygame.K_DOWN]-keys[pygame.K_UP])*self.vel
#     def basic_ai(self, following):
#         if self.posy < following.posy-self.height/2:
#             if abs(self.posy-(following.posy-self.height/2))<self.vel:
#                 self.posy=following.posy-self.height/2
#             else:
#                 self.posy+=self.vel
#         elif self.posy > following.posy-self.height/2:
#             if abs(self.posy-(following.posy-self.height/2))<self.vel:
#                 self.posy=following.posy-self.height/2
#             else:
#                 self.posy-=self.vel
#     def advanced_ai(self, following, difficulty):
#         global WINDOW_HEIGHT, WINDOW_WIDTH
#         iter=0
#         if difficulty == "easy":
#             hitpos = 0
#             aivel = 3
#         elif difficulty == "medium":
#             hitpos = 30
#             aivel = 4
#         elif difficulty == "hard":
#             hitpos = 100
#             aivel = 6
#         else:
#             hitpos = 15*difficulty
#             aivel = 1+difficulty
#         intendedpos=0
#         if (self.posx-following.posx)/following.velx>0:
#             time=abs((following.posx-hitpos)/following.velx)
#             intendedpos=following.posy+following.vely*time
#             cont=True
#             while cont:
#                 iter+=1
#                 if intendedpos<0:
#                     intendedpos=abs(intendedpos)
#                 if intendedpos>WINDOW_HEIGHT:
#                     intendedpos=WINDOW_HEIGHT-(intendedpos-WINDOW_HEIGHT-2)
#                 if intendedpos>=0 and intendedpos<=WINDOW_HEIGHT:
#                     cont=False
#                 if iter > 100:
#                     cont = False
#         else:
#             intendedpos=WINDOW_HEIGHT/2
#         if following.vely>0:
#             intendedpos-=20
#         else:
#             intendedpos+=20
#         if self.posy < intendedpos-self.height/2:
#             if abs(self.posy-(intendedpos-self.height/2))<self.vel:
#                 self.posy=intendedpos-self.height/2
#             else:
#                 self.posy+=self.vel
#         elif self.posy > intendedpos-self.height/2:
#             if abs(self.posy-(intendedpos-self.height/2))<self.vel:
#                 self.posy=intendedpos-self.height/2
#             else:
#                 self.posy-=self.vel
#     def render(self):
#         pygame.draw.rect(self.window,self.color,pygame.Rect(self.posx,self.posy,self.width,self.height))
class slider():
    def __init__(self, window, posx, posy, colorback, colorfront, lengthSlider, widthSlider, moverRadius, moverStatus):
        self.colorS = colorback
        self.colorM = colorfront
        self.lengthSlider = lengthSlider
        self.widthSlider = widthSlider
        self.moverRadius = moverRadius
        self.moverStatus = moverStatus
        self.posx = posx
        self.posy = posy
        self.clicking = False
        self.moverPosition = self.moverStatus/100*self.lengthSlider
    def isMoving(self):
        if pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pos()[0]-(self.posx+self.moverPosition)+pygame.mouse.get_pos()[1]-self.posy<self.moverRadius and pygame.mouse.get_pos()[0]-(self.posx+self.moverPosition)+pygame.mouse.get_pos()[1]-self.posy>-self.moverRadius and not self.clicking:
            self.clicking = True
        elif pygame.mouse.get_pressed()[0] == False:
            self.clicking = False
        if self.clicking:
            self.moverPosition = pygame.mouse.get_pos()[0]-self.posx
            self.moverStatus = self.moverPosition/self.lengthSlider*100
    def update(self):
        self.render()
    def render(self):
        pygame.draw.rect(self.window,self.colorS,pygame.Rect(self.posx,self.posy,self.lengthSlider,self.widthSlider))
        pygame.draw.circle(self.window,self.colorM,(self.posx+self.moverPosition,self.posy),self.moverRadius)


import pygame
window=pygame.display.set_mode((0,0), pygame.FULLSCREEN)

pygame.draw.circle(window,"blue",(150,150),40)
pygame.draw.circle(window,"yellow",(150,150),20)
pygame.display.update()