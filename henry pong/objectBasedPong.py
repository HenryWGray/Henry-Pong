import pygame
import pygwidgets
import numpy as np
from random import randint

BLACK = (0, 0, 0)
FRAMES_PER_SECOND = 60
clock = pygame.time.Clock()
myFont = pygame.font.SysFont("Georgia", 72)

pygame.init()
pygame.mixer.init()
window=pygame.display.set_mode((0,0), pygame.FULLSCREEN)

WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_desktop_sizes()[0]


# Variable Definitions
color="white"
object_color="black"
background_item_color = "gray"
posx=WINDOW_WIDTH/2
posy=WINDOW_HEIGHT/2
velx=3
vely=3
colorset = 1
choice_left = False
choice_right = False
score_expectation_right=0
score_expectation_left=0
monoLooking = {}
bounce_sound_paddle = pygame.mixer.Sound("blip.wav.wav")
bounce_sound_wall = pygame.mixer.Sound("wallblip.wav")
score_noise = pygame.mixer.Sound("score.wav")
state_left = False
state_right = False
state_ball = False


# Strategies
class ball():
    def __init__(self, window, posx, posy, velx, vely, radius, color):
        self.window = window
        self.posx = posx
        self.posy = posy
        self.velx = velx
        self.vely = vely
        self.radius = radius
        self.color = color
    def overlap(self, objectC):
        overlapX, overlapY = False, False
        if self.posx+self.radius >= objectC.posx and self.posx-self.radius <= objectC.posx+objectC.width:
            overlapX = True
        if self.posy+self.radius >= objectC.posy and self.posy-self.radius <= objectC.posy+objectC.height:
            overlapY = True
        if overlapX and overlapY:
            return(True)
    def bounce(self):
        global WINDOW_WIDTH, WINDOW_HEIGHT, left_paddle, right_paddle, bounce_sound_wall, bounce_sound_paddle
        if self.posy > WINDOW_HEIGHT-self.radius:
            pygame.mixer.Sound.play(bounce_sound_wall)
            self.posy = WINDOW_HEIGHT-self.radius
            self.vely = -abs(self.vely)
        elif self.posy < self.radius:
            pygame.mixer.Sound.play(bounce_sound_wall)
            self.posy = self.radius
            self.vely = abs(self.vely)
        if self.overlap(right_paddle) and self.velx > 0:
            pygame.mixer.Sound.play(bounce_sound_paddle)
            self.velx = -(abs(self.velx) + 1)
            self.vely = abs(self.velx)*-np.sin((-(self.posy+self.radius)+(right_paddle.posy+right_paddle.height/2))*np.pi/180) + self.vely
        if self.overlap(left_paddle) and self.velx < 0:
            pygame.mixer.Sound.play(bounce_sound_paddle)
            self.velx = (abs(self.velx) + 1)
            self.vely = abs(self.velx)*-np.sin((-(self.posy+self.radius)+(left_paddle.posy+left_paddle.height/2))*np.pi/180) + self.vely
        if self.posx + self.radius > WINDOW_WIDTH:
            left_paddle.score += 1
            pygame.mixer.Sound.play(score_noise)
            self.reset()
        elif self.posx - self.radius <= 0:
            right_paddle.score += 1
            pygame.mixer.Sound.play(score_noise)
            self.reset()
    def reset(self):
        global WINDOW_HEIGHT, WINDOW_WIDTH
        self.posx=WINDOW_WIDTH/2
        self.posy=WINDOW_HEIGHT/2
        self.velx=3*abs(self.velx)/self.velx
        self.vely=randint(-3000,3000)/1000
    def update(self):
        self.bounce()
        self.posx = self.posx+self.velx
        self.posy = self.posy+self.vely
        self.render()
    def render(self):
        pygame.draw.circle(self.window,self.color,(self.posx,self.posy),self.radius)


class paddle():
    def __init__(self, window, posx, posy, velocity, width, height, color, strat, score = 0, difficulty = "medium", controls = "a"):
        self.window = window
        self.posx = posx
        self.posy = posy
        self.vel = velocity
        self.width = width
        self.height = height
        self.color = color
        self.strat = strat
        self.score = score
        self.diff = difficulty
        self.controls = controls
    def update(self, ball):
        global WINDOW_HEIGHT
        if self.strat == "player":
            self.player()
        elif self.strat == "basic_ai":
            self.basic_ai(ball)
        elif self.strat == "advanced_ai":
            self.advanced_ai(ball, self.diff)
        if self.posy>WINDOW_HEIGHT-self.height:
            self.posy=WINDOW_HEIGHT-self.height
        elif self.posy<0:
            self.posy=0
        self.render()
    def player(self):
        global keys
        if self.controls == "a":
            self.posy += (keys[pygame.K_DOWN]-keys[pygame.K_UP])*self.vel
        elif self.controls == "w":
            self.posy += (keys[pygame.K_s]-keys[pygame.K_w])*self.vel
    def basic_ai(self, following):
        if self.posy < following.posy-self.height/2:
            if abs(self.posy-(following.posy-self.height/2))<self.vel:
                self.posy=following.posy-self.height/2
            else:
                self.posy+=self.vel
        elif self.posy > following.posy-self.height/2:
            if abs(self.posy-(following.posy-self.height/2))<self.vel:
                self.posy=following.posy-self.height/2
            else:
                self.posy-=self.vel
    def advanced_ai(self, following, difficulty):
        global WINDOW_HEIGHT, WINDOW_WIDTH
        iter=0
        bounce=0
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
        if (self.posx-following.posx)/following.velx>0:
            if self.posx > WINDOW_WIDTH/2:
                if difficulty == "hard":
                    hitpos = WINDOW_WIDTH-self.posx
                time=abs((WINDOW_WIDTH-hitpos-following.posx-following.radius)/following.velx)
            else:
                if difficulty == "hard":
                    hitpos = self.posx+self.width
                time=abs((following.posx-hitpos-following.radius)/following.velx)
            intendedpos=following.posy+following.vely*time
            cont=True
            while cont:
                iter+=1
                if intendedpos<0:
                    intendedpos=abs(intendedpos)
                    bounce+=1
                if intendedpos>WINDOW_HEIGHT-following.radius:
                    intendedpos=WINDOW_HEIGHT-2*following.radius-(intendedpos-WINDOW_HEIGHT-2)
                    bounce+=1
                if intendedpos>=0 and intendedpos<=WINDOW_HEIGHT:
                    cont=False
                if iter > 100:
                    cont = False
        else:
            intendedpos=WINDOW_HEIGHT/2
        if following.vely*((-1)**(bounce))>0:
            if abs(following.vely)/abs(following.velx) < 0.7:
                intendedpos-=self.height/4
            elif abs(following.vely)/abs(following.velx) > 1.25:
                intendedpos+=self.height/4
        else:
            if abs(following.vely)/abs(following.velx) < 0.7:
                intendedpos+=self.height/4
            elif abs(following.vely)/abs(following.velx) > 1.25:
                intendedpos-=self.height/4
        if self.posy+self.height/2 < intendedpos:
            if abs(self.posy+self.height/2-(intendedpos))<self.vel:
                self.posy=intendedpos-self.height/2
            else:
                self.posy+=self.vel
        elif self.posy+self.height/2 > intendedpos:
            if abs(self.posy+self.height/2-(intendedpos))<self.vel:
                self.posy=intendedpos-self.height/2
            else:
                self.posy-=self.vel
    def render(self):
        pygame.draw.rect(self.window,self.color,pygame.Rect(self.posx,self.posy,self.width,self.height))


# Basic Systems
class slider():
    def __init__(self, window, posx, posy, colorback, colorfront, lengthSlider, widthSlider, moverRadius, moverStatus):
        self.window = window
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
            if self.moverPosition>self.lengthSlider:
                self.moverPosition = self.lengthSlider
            elif self.moverPosition<0:
                self.moverPosition = 0
            self.moverStatus = self.moverPosition/self.lengthSlider*100
    def update(self):
        self.isMoving()
        self.render()
    def render(self):
        pygame.draw.rect(self.window,self.colorS,pygame.Rect(self.posx,self.posy,self.lengthSlider,self.widthSlider))
        pygame.draw.circle(self.window,self.colorM,(self.posx+self.moverPosition,self.posy+self.widthSlider/2),self.moverRadius)
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
    global left_paddle, right_paddle, myFont, object_color, score_expectation_left, score_expectation_right
    scoreDisplayRight = myFont.render(str(right_paddle.score), 1, object_color)
    window.blit(scoreDisplayRight, (WINDOW_WIDTH/2+150, 30))
    scoreDisplayLeft = myFont.render(str(left_paddle.score), 1, object_color)
    window.blit(scoreDisplayLeft, (WINDOW_WIDTH/2-150-45, 30))
    if left_paddle.score + right_paddle.score > score_expectation_left+score_expectation_right+3:
        alternate()
        score_expectation_right = right_paddle.score
        score_expectation_left = left_paddle.score
def set_color(color, object_color, background_item_color):
    color_button.colorup = background_item_color
    color_button.colordown = object_color
    color_button.textcolor = color
    selection_right_button.colorup = background_item_color
    selection_right_button.colordown = object_color
    selection_right_button.textcolor = color
    selection_left_button.colorup = background_item_color
    selection_left_button.colordown = object_color
    selection_left_button.textcolor = color
    main_ball.color = object_color
    left_paddle.color = object_color
    right_paddle.color = object_color
    basic_ai_left_button.colorup = background_item_color
    medium_ai_left_button.colorup = background_item_color
    hard_ai_left_button.colorup = background_item_color
    random_ai_left_button.colorup = background_item_color
    player_left_button.colorup = background_item_color
    basic_ai_right_button.colorup = background_item_color
    medium_ai_right_button.colorup = background_item_color
    hard_ai_right_button.colorup = background_item_color
    random_ai_right_button.colorup = background_item_color
    player_right_button.colorup = background_item_color
    selection_ball_button.colorup = background_item_color
    ball_size_slider.colorS = background_item_color

    basic_ai_left_button.colordown = object_color
    medium_ai_left_button.colordown = object_color
    hard_ai_left_button.colordown = object_color
    random_ai_left_button.colordown = object_color
    player_left_button.colordown = object_color
    basic_ai_right_button.colordown = object_color
    medium_ai_right_button.colordown = object_color
    hard_ai_right_button.colordown = object_color
    random_ai_right_button.colordown = object_color
    player_right_button.colordown = object_color
    selection_ball_button.colordown = object_color
    ball_size_slider.colorM = object_color

    basic_ai_left_button.textcolor = color
    medium_ai_left_button.textcolor = color
    hard_ai_left_button.textcolor = color
    random_ai_left_button.textcolor = color
    player_left_button.textcolor = color
    basic_ai_right_button.textcolor = color
    medium_ai_right_button.textcolor = color
    hard_ai_right_button.textcolor = color
    random_ai_right_button.textcolor = color
    player_right_button.textcolor = color
    selection_ball_button.textcolor = color

    

# Object declarations
color_button = button(25,WINDOW_HEIGHT-75,200,50,object_color,background_item_color,"presser",text="Change Color",textcolor=color)
selection_left_button = button(25,WINDOW_HEIGHT-145,200,50,object_color,background_item_color,"presser",text="Left AI",textcolor=color)
basic_ai_left_button = button(225,WINDOW_HEIGHT-145,200,50,object_color,background_item_color,"presser",text="Basic AI",textcolor=color)
medium_ai_left_button = button(425,WINDOW_HEIGHT-145,200,50,object_color,background_item_color,"presser",text="Medium AI",textcolor=color)
hard_ai_left_button = button(625,WINDOW_HEIGHT-145,200,50,object_color,background_item_color,"presser",text="Hard AI",textcolor=color)
random_ai_left_button = button(825,WINDOW_HEIGHT-145,200,50,object_color,background_item_color,"presser",text="Random AI",textcolor=color)
player_left_button = button(1025,WINDOW_HEIGHT-145,200,50,object_color,background_item_color,"presser",text="Player",textcolor=color)
selection_right_button = button(25,WINDOW_HEIGHT-215,200,50,object_color,background_item_color,"presser",text="Right AI",textcolor=color)
basic_ai_right_button = button(225,WINDOW_HEIGHT-215,200,50,object_color,background_item_color,"presser",text="Basic AI",textcolor=color)
medium_ai_right_button = button(425,WINDOW_HEIGHT-215,200,50,object_color,background_item_color,"presser",text="Medium AI",textcolor=color)
hard_ai_right_button = button(625,WINDOW_HEIGHT-215,200,50,object_color,background_item_color,"presser",text="Hard AI",textcolor=color)
random_ai_right_button = button(825,WINDOW_HEIGHT-215,200,50,object_color,background_item_color,"presser",text="Random AI",textcolor=color)
player_right_button = button(1025,WINDOW_HEIGHT-215,200,50,object_color,background_item_color,"presser",text="Player",textcolor=color)
main_ball = ball(window, WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 3, 3, 20, object_color)
left_paddle = paddle(window, 75, WINDOW_HEIGHT/2, 6, 20, 120, object_color, "advanced_ai", 0, "hard")
right_paddle = paddle(window, WINDOW_WIDTH-95, WINDOW_HEIGHT/2, 6, 20, 120, object_color, "advanced_ai", 0, "hard")
selection_ball_button = button(25,WINDOW_HEIGHT-285,200,50,object_color,background_item_color,"presser",text="Ball Choices",textcolor=color)
ball_size_slider = slider(window, 250, WINDOW_HEIGHT-285+20, background_item_color, object_color, 200, 10, 15, 20)

while True:
    window.fill(color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                alternate()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
    keys=pygame.key.get_pressed()
    score_display()
    posx += velx
    posy += vely
    if monoPresser(color_button):
        alternate()
    if monoPresser(selection_left_button):
        if state_left:
            state_left = False
        else:
            state_left = True
    if monoPresser(selection_right_button):
        if state_right:
            state_right = False
        else:
            state_right = True
    if monoPresser(selection_ball_button):
        if state_ball:
            state_ball = False
        else:
            state_ball = True
    if state_left:
        basic_ai_left_button.update()
        medium_ai_left_button.update()
        hard_ai_left_button.update()
        random_ai_left_button.update()
        player_left_button.update()
        if monoPresser(basic_ai_left_button):
            left_paddle.strat = "basic_ai"
        elif monoPresser(medium_ai_left_button):
            left_paddle.strat = "advanced_ai"
            left_paddle.diff = "medium"
        elif monoPresser(hard_ai_left_button):
            left_paddle.strat = "advanced_ai"
            left_paddle.diff = "hard"
        elif monoPresser(random_ai_left_button):
            st = randint(0,6)
            if st < 3:
                left_paddle.strat = "basic_ai"
            elif st == 3 or st == 4:
                left_paddle.strat = "advanced_ai"
                left_paddle.diff = "medium"
            else:
                left_paddle.strat = "advanced_ai"
                left_paddle.diff = "hard"
        elif monoPresser(player_left_button):
            left_paddle.strat = "player"
            left_paddle.controls = "w"
    if state_right:
        basic_ai_right_button.update()
        medium_ai_right_button.update()
        hard_ai_right_button.update()
        random_ai_right_button.update()
        player_right_button.update()
        if monoPresser(basic_ai_right_button):
            right_paddle.strat = "basic_ai"
        elif monoPresser(medium_ai_right_button):
            right_paddle.strat = "advanced_ai"
            right_paddle.diff = "medium"
        elif monoPresser(hard_ai_right_button):
            right_paddle.strat = "advanced_ai"
            right_paddle.diff = "hard"
        elif monoPresser(random_ai_right_button):
            st = randint(0,6)
            if st < 3:
                right_paddle.strat = "basic_ai"
            elif st == 3 or st == 4:
                right_paddle.strat = "advanced_ai"
                right_paddle.diff = "medium"
            else:
                right_paddle.strat = "advanced_ai"
                right_paddle.diff = "hard"
        elif monoPresser(player_right_button):
            right_paddle.strat = "player"
            right_paddle.controls = "a"
    if state_ball:
        ball_size_slider.update()
    main_ball.radius = ball_size_slider.moverStatus
    set_color(color, object_color, background_item_color)
    pygame.draw.rect(window,background_item_color,pygame.Rect(WINDOW_WIDTH/2,-10,5,WINDOW_HEIGHT+20))
    color_button.update()
    selection_left_button.update()
    selection_right_button.update()
    selection_ball_button.update()
    main_ball.update()
    left_paddle.update(main_ball)
    right_paddle.update(main_ball)
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)