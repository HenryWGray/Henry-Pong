import pygame
import pygwidgets
import numpy as np
from random import randint

BLACK = (0, 0, 0)
WINDOW_WIDTH=1280
WINDOW_HEIGHT=800
FRAMES_PER_SECOND = 60
clock = pygame.time.Clock()
myFont = pygame.font.SysFont("Georgia", 72)

pygame.init()
pygame.mixer.init()
window=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))


# Variable Definitions
color="white"
object_color="black"
background_item_color = "gray"
posx=WINDOW_WIDTH/2
posy=WINDOW_HEIGHT/2
vel=6
aivel=vel*1.5
velx=3
vely=3
rightx = WINDOW_WIDTH-95
righty = WINDOW_HEIGHT/2-60
leftx = 75
lefty = WINDOW_HEIGHT/2-60
score_right=0
score_left=0
colorset = 1
choice_left = False
choice_right = False
score_expectation_right=0
score_expectation_left=0
monoLooking = {}
bounce_sound = pygame.mixer.Sound("blip.wav.wav")


# Strategies
def basic_ai_left():
    global lefty
    global posy
    global aivel
    if lefty < posy-60:
        if abs(lefty-(posy-60))<aivel:
            lefty=posy-60
        else:
            lefty+=aivel
    elif lefty > posy-60:
        if abs(lefty-(posy-60))<aivel:
            lefty=posy-60
        else:
            lefty-=aivel
def basic_ai_right():
    global righty
    global posy
    global aivel
    if righty < posy-60:
        if abs(righty-(posy-60))<aivel:
            righty=posy-60
        else:
            righty+=aivel
    elif righty > posy-60:
        if abs(righty-(posy-60))<aivel:
            righty=posy-60
        else:
            righty-=aivel
def advanced_ai_left(difficulty):
    global lefty, posy, posx, velx, vely, WINDOW_HEIGHT, WINDOW_WIDTH
    iter=0
    if difficulty == "easy":
        hitpos = 0
        aivel = 3
    elif difficulty == "medium":
        hitpos = 30
        aivel = 4
    elif difficulty == "hard":
        hitpos = 100
        aivel = 6
    else:
        hitpos = 15*difficulty
        aivel = 1+difficulty
    intendedpos=0
    if velx<0:
        time=abs((posx-hitpos)/velx)
        intendedpos=posy+vely*time
        cont=True
        while cont:
            iter+=1
            if intendedpos<0:
                intendedpos=abs(intendedpos)
            if intendedpos>WINDOW_HEIGHT:
                intendedpos=WINDOW_HEIGHT-(intendedpos-WINDOW_HEIGHT-2)
            if intendedpos>=0 and intendedpos<=WINDOW_HEIGHT:
                cont=False
            if iter > 100:
                cont = False
    else:
        intendedpos=WINDOW_HEIGHT/2
    if vely>0:
        intendedpos-=20
    else:
        intendedpos+=20
    if lefty < intendedpos-60:
        if abs(lefty-(intendedpos-60))<aivel:
            lefty=intendedpos-60
        else:
            lefty+=aivel
    elif lefty > intendedpos-60:
        if abs(lefty-(intendedpos-60))<aivel:
            lefty=intendedpos-60
        else:
            lefty-=aivel
def advanced_ai_right(difficulty):
    global righty, posy, posx, velx, vely, WINDOW_HEIGHT, WINDOW_WIDTH
    iter=0
    if difficulty == "easy":
        hitpos = 0
        aivel = 3
    elif difficulty == "medium":
        hitpos = 30
        aivel = 4
    elif difficulty == "hard":
        hitpos = 100
        aivel = 6
    else:
        hitpos = 15*difficulty
        aivel = 1+difficulty
    intendedpos=0
    if velx>0:
        time=abs((WINDOW_WIDTH-hitpos-posx)/velx)
        intendedpos=posy+vely*time
        cont=True
        while cont:
            iter+=1
            if intendedpos<0:
                intendedpos=abs(intendedpos)
            if intendedpos>WINDOW_HEIGHT:
                intendedpos=WINDOW_HEIGHT-(intendedpos-WINDOW_HEIGHT-2)
            if intendedpos>=0 and intendedpos<=WINDOW_HEIGHT:
                cont=False
            if iter > 100:
                cont = False
    else:
        intendedpos=WINDOW_HEIGHT/2
    if vely>0:
        intendedpos-=20
    else:
        intendedpos+=20
    if righty < intendedpos-60:
        if abs(righty-(intendedpos-60))<aivel:
            righty=intendedpos-60
        else:
            righty+=aivel
    elif righty > intendedpos-60:
        if abs(righty-(intendedpos-60))<aivel:
            righty=intendedpos-60
        else:
            righty-=aivel
def random_ai_left(alternate = False):
    global choice_left, velx, score_left, score_right, score_expectation_left
    if not choice_left:
        choice_left = randint(0,6)
    if alternate:
        if score_left+score_right != score_expectation_left:
            choice_left = randint(0,6)
            score_expectation_left = score_left+score_right
            print(f"Left AI Swapped to {choice_left}")
    if choice_left < 2:
        basic_ai_left()
    elif choice_left == 2:
        advanced_ai_left("easy")
    elif choice_left == 3:
        advanced_ai_left("medium")
    elif choice_left == 4:
        advanced_ai_left("hard")
    else:
        if velx < 15:
            advanced_ai_left('medium')
        else:
            advanced_ai_left("hard")
def random_ai_right(alternate = False):
    global choice_right, velx, score_right, score_left, score_expectation_right
    if not choice_right:
        choice_right = randint(0,6)
    if alternate:
        if score_left+score_right != score_expectation_right:
            choice_right = randint(0,6)
            score_expectation_right = score_left+score_right
            print(f"Right AI Swapped to {choice_right}")
    if choice_right < 2:
        basic_ai_right()
    elif choice_right == 2:
        advanced_ai_right("easy")
    elif choice_right == 3:
        advanced_ai_right("medium")
    elif choice_right == 4:
        advanced_ai_right("hard")
    else:
        if velx < 15:
            advanced_ai_right('medium')
        else:
            advanced_ai_right("hard")


# Basic Systems
class button():
    def __init__(self,posx,posy,width,height,colorup,colordown,type,text=None,textcolor="black"):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.colorup = colorup
        self.colordown = colordown
        self.color = colorup
        self.type = type
        self.found = False
        self.text = text
        self.textcolor = textcolor
    def isPressed(self):
        if self.type == "presser":
            if pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pos()[0] > self.posx and pygame.mouse.get_pos()[0] < self.posx+self.width and pygame.mouse.get_pos()[1] > self.posy and pygame.mouse.get_pos()[1] < self.posy+self.height:
                self.color=self.colordown
                return(True)
            else:
                self.color=self.colorup
                return(False)
        elif self.type == "tapper":
            if pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pos()[0] > self.posx and pygame.mouse.get_pos()[0] < self.posx+self.width and pygame.mouse.get_pos()[1] > self.posy and pygame.mouse.get_pos()[1] < self.posy+self.height:
                self.found = True
                return(True)
            else:
                if self.found == True:
                    if self.color == self.colordown:
                        self.color = self.colorup
                    else:
                        self.color = self.colordown
                self.found = False
                return(False)
    def update(self):
        if self.type == "presser":
            if pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pos()[0] > self.posx and pygame.mouse.get_pos()[0] < self.posx+self.width and pygame.mouse.get_pos()[1] > self.posy and pygame.mouse.get_pos()[1] < self.posy+self.height:
                self.color=self.colordown
            else:
                self.color=self.colorup
        elif self.type == "tapper":
            if pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pos()[0] > self.posx and pygame.mouse.get_pos()[0] < self.posx+self.width and pygame.mouse.get_pos()[1] > self.posy and pygame.mouse.get_pos()[1] < self.posy+self.height:
                self.found = True
            else:
                if self.found == True:
                    if self.color == self.colordown:
                        self.color = self.colorup
                    else:
                        self.color = self.colordown
                self.found = False
        self.render()
    def render(self):
        pygame.draw.rect(window,self.color,pygame.Rect(self.posx,self.posy,self.width,self.height))
        if self.text is not None:
            font = pygame.font.SysFont("Georgia", int(self.height/2))
            dText = font.render(self.text, 1, self.textcolor)
            window.blit(dText, ((self.posx+self.width/2-len(self.text)*int(self.height/8)), (self.posy+self.height/4)))
def monoPresser(object):
    global monoLooking
    if object not in monoLooking.keys():
        monoLooking[object] = False
    if object.isPressed() and not monoLooking[object]:
        monoLooking[object] = True
        return(True)
    elif not object.isPressed() and monoLooking[object]:
        monoLooking[object] = False
        return(False)
    else:
        return(False)
def reset():
    global posx, posy, velx, vely, WINDOW_HEIGHT, WINDOW_WIDTH
    posx=WINDOW_WIDTH/2
    posy=WINDOW_HEIGHT/2
    velx=3*abs(velx)/velx
    vely=randint(-3000,3000)/1000
def bounce():
    global righty, WINDOW_HEIGHT, WINDOW_WIDTH, lefty, leftx, rightx, posy, posx, velx, vely, score_right, score_left
    if righty>WINDOW_HEIGHT-120:
        righty=WINDOW_HEIGHT-120
    elif righty<0:
        righty=0
    if posy>=WINDOW_HEIGHT-20:
        vely = -abs(vely)
        pygame.mixer.Sound.play(bounce_sound)
    elif posy<=20:
        vely = abs(vely)
        pygame.mixer.Sound.play(bounce_sound)
    if posx>=WINDOW_WIDTH-20:
        score_left+=1
        reset()
        if (score_right+score_left)%3==0:
            alternate()
    if posx<=20:
        score_right+=1
        reset()
        if (score_right+score_left)%3==0:
            alternate()
    if (posx>rightx-20 and posx<rightx+40) and (posy+20>righty and posy-20<righty+120) and (velx>0):
        velx = -abs(velx+1)
        vely = abs(velx)*-np.sin((-(posy+20)+(righty+60))*np.pi/180) + vely
        pygame.mixer.Sound.play(bounce_sound)
    if (posx>leftx-20 and posx<leftx+40) and (posy+10>lefty and posy-10<lefty+120) and (velx<0):
        velx = abs(velx)+1
        vely = abs(velx)*-np.sin((-(posy+20)+(lefty+60))*np.pi/180) + vely
        pygame.mixer.Sound.play(bounce_sound)
def alternate():
    global color, object_color, colorset, background_item_color
    colorset+=1
    if colorset>10:
        colorset=1
    if colorset==1:
        color="white"
        object_color="black"
        background_item_color = "gray"
    elif colorset==2:
        color="black"
        object_color="white"
        background_item_color = "gray"
    elif colorset==3:
        color="mediumpurple4"
        object_color = "mediumseagreen"
        background_item_color = "mediumpurple1"
    elif colorset==4:
        color = "mediumseagreen"
        object_color = "mediumpurple4"
        background_item_color = "mediumspringgreen"
    elif colorset == 5:
        color="red4"
        object_color="yellow"
        background_item_color = "orangered"
    elif colorset == 6:
        color = "yellow"
        object_color = "orangered"
        background_item_color = "red4"
    elif colorset == 7:
        color = "paleturquoise3"
        object_color = "palevioletred"
        background_item_color = "paleturquoise1"
    elif colorset == 8:
        color = "palevioletred"
        object_color = "paleturquoise3"
        background_item_color = "palevioletred1"
    elif colorset == 9:
        color = "green"
        object_color = "yellow"
        background_item_color = "yellowgreen"
    elif colorset == 10:
        color = "yellow"
        object_color = "green"
        background_item_color = "orangered"
def score_display():
    global score_left, score_right, myFont, object_color
    scoreDisplayRight = myFont.render(str(score_right), 1, object_color)
    window.blit(scoreDisplayRight, (WINDOW_WIDTH/2+150, 30))
    scoreDisplayLeft = myFont.render(str(score_left), 1, object_color)
    window.blit(scoreDisplayLeft, (WINDOW_WIDTH/2-150-45, 30))


# Player controls
def player_right():
    global righty
    righty += (keys[pygame.K_DOWN]-keys[pygame.K_UP])*vel
def player_left():
    global lefty
    lefty += (keys[pygame.K_s]-keys[pygame.K_w])*vel


# Object declarations
color_button = button(25,WINDOW_HEIGHT-75,200,50,object_color,background_item_color,"presser",text="Change Color",textcolor=color)
random_left_button = button(25,WINDOW_HEIGHT-145,200,50,object_color,background_item_color,"presser",text="Random Left",textcolor=color)
random_right_button = button(25,WINDOW_HEIGHT-215,200,50,object_color,background_item_color,"presser",text="Random Right",textcolor=color)


while True:
    window.fill(color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                alternate()
    keys=pygame.key.get_pressed()
    # basic_ai_right()
    random_ai_left(alternate=False)
    # basic_ai_left()
    # random_ai_right(alternate=False)
    # player_left()
    player_right()
    bounce()
    score_display()
    if lefty>WINDOW_HEIGHT-120:
        lefty=WINDOW_HEIGHT-120
    elif lefty<0:
        lefty=0
    posx += velx
    posy += vely
    if monoPresser(color_button):
        alternate()
    if monoPresser(random_left_button):
        choice_left = randint(0,6)
    if monoPresser(random_right_button):
        choice_right = randint(0,6)
    color_button.colorup = background_item_color
    color_button.colordown = object_color
    color_button.textcolor = color
    random_right_button.colorup = background_item_color
    random_right_button.colordown = object_color
    random_right_button.textcolor = color
    random_left_button.colorup = background_item_color
    random_left_button.colordown = object_color
    random_left_button.textcolor = color
    pygame.draw.rect(window,background_item_color,pygame.Rect(WINDOW_WIDTH/2,-10,5,WINDOW_HEIGHT+20))
    color_button.update()
    random_left_button.update()
    random_right_button.update()
    pygame.draw.circle(window,object_color,(posx,posy),20)
    pygame.draw.rect(window,object_color,pygame.Rect(rightx,righty,20,120))
    pygame.draw.rect(window,object_color,pygame.Rect(leftx,lefty,20,120))

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)
    