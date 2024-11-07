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
            if intendedpos<0:
                intendedpos=abs(intendedpos)
            if intendedpos>WINDOW_HEIGHT:
                intendedpos=WINDOW_HEIGHT-(intendedpos-WINDOW_HEIGHT-2)
            if intendedpos>=0 and intendedpos<=WINDOW_HEIGHT:
                cont=False
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
            if intendedpos<0:
                intendedpos=abs(intendedpos)
            if intendedpos>WINDOW_HEIGHT:
                intendedpos=WINDOW_HEIGHT-(intendedpos-WINDOW_HEIGHT-2)
            if intendedpos>=0 and intendedpos<=WINDOW_HEIGHT:
                cont=False
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
    # print(intendedpos)