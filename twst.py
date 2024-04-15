# Example file showing a basic pygame "game loop"
import pygame
import perlin
import random
import math
def worldcreate(width,height,seed):
    p = perlin.Perlin(seed) 
    a=[]
    for i in range(height):
        col=[]
        sol=(math.cos((i*2-(height-1))*math.pi/height)+1)/2
        for j in range(width):
            h=p.two(j*13,i*13)
            veg=max((p.two(j*13,i*13)+random.random()),0)
            co2=0.04
            h20=random.random()*0.2
            temp=sol*0.8-max(h,0)*0.013+co2+h20**1.5
            col.append([sol,veg,h,co2,h20,temp])
        a.append(col)
    return a
def rendertile(x,y):
    color=getcolor(x,y)
    pygame.draw.polygon(screen, color, ((y*8,x*8), (y*8+7, x*8), (y*8+7, x*8+7),(y*8, x*8+7)))
def getgroundcol(x,y):
    tile=world[x][y]
    if tile[5]<0.1:
        return (255,255,255)
    else:
        if getunderwater(x,y):
            return (min(tile[5]-.1,255)*255,min((tile[5]-.1)*255,255),255)
        else:
            return  (130+tile[5]*250,80*tile[5]*350,0)
def getunderwater(x,y):
    return world[x][y][2]<waterheight
def getcloudcoverage(x,y):
    tile=world[x][y]
    return tile[5]**3*tile[4]
def getfoliagecol(x,y):
    tile=world[x][y]
    if tile[5]<0.1:
        return (0,0,85)
    elif tile[5]<0.3:
        return (0,85+(tile[5]-.1)*850,0)
    elif tile[5]<0.6:
        return((tile[5]-.3)*400,255-(tile[5]-.3)*567,0)
    else:
        return(120,85,0)
def getcolor(x,y):
    tile=world[x][y]
    clouds=tuple(i*tile[4]*getcloudcoverage(x,y) for i in (1,1,1))
    ground=getgroundcol(x,y)
    veg=tuple(i*tile[1] for i in getfoliagecol(x,y))
    r=min(abs(ground[0]+veg[0]+clouds[0]),255)
    g=min(abs(ground[1]+veg[1]+clouds[1]),255)
    b=min(abs(ground[2]+veg[2]+clouds[2]),255)
    return (r,g,b)
def updateworld():
    worldcopy=world
    hlen=len(world)
    wlen=len(world[0])
    h=range(hlen)
    w=range(wlen)
    for i in h:
        for j in w:
            if i==0:
                world[i][j][3]=(worldcopy[i][j-1][3]+worldcopy[i][(j+1)%wlen][3]+worldcopy[i+1][j-1][3]+worldcopy[i+1][j][3]+worldcopy[i+1][(j+1)%wlen][3])/5
                world[i][j][4]=(worldcopy[i][j-1][4]+worldcopy[i][(j+1)%wlen][4]+worldcopy[i+1][j-1][4]+worldcopy[i+1][j][4]+worldcopy[i+1][(j+1)%wlen][4])/5
            elif i==len(h)-1:
                world[i][j][3]=(worldcopy[i][j-1][3]+worldcopy[i][(j+1)%wlen][3]+worldcopy[i-1][j-1][3]+worldcopy[i-1][j][3]+worldcopy[i-1][(j+1)%wlen][3])/5
                world[i][j][4]=(worldcopy[i][j-1][4]+worldcopy[i][(j+1)%wlen][4]+worldcopy[i-1][j-1][4]+worldcopy[i-1][j][4]+worldcopy[i-1][(j+1)%wlen][4])/5
            else:
                world[i][j][3]=(worldcopy[i][j-1][3]+worldcopy[i][(j+1)%wlen][3]+worldcopy[i+1][j-1][3]+worldcopy[i+1][j][3]+worldcopy[i+1][(j+1)%wlen][3]+worldcopy[i-1][j-1][3]+worldcopy[i-1][j][3]+worldcopy[i-1][(j+1)%wlen][3])/8
                world[i][j][4]=(worldcopy[i][j-1][4]+worldcopy[i][(j+1)%wlen][4]+worldcopy[i+1][j-1][4]+worldcopy[i+1][j][4]+worldcopy[i+1][(j+1)%wlen][4]+worldcopy[i-1][j-1][4]+worldcopy[i-1][j][4]+worldcopy[i-1][(j+1)%wlen][4])/8

        
            
            
# pygame setup
world=worldcreate(90,45,2231321)
pygame.init()
screen = pygame.display.set_mode((720, 360))
waterheight=0
clock = pygame.time.Clock()
running = True


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(0)
    for x in range(45):
        for y in range(90):
            rendertile(x,y)
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()