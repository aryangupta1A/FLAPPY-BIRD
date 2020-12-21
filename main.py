import pygame, random, sys
pygame.init()

pygame.display.set_caption('Flappy Bird')
screen=pygame.display.set_mode((288,512))#main surface
clock=pygame.time.Clock()#code to fix frame rate don't know
background=pygame.image.load('images/background.png').convert()#main background
bottom=pygame.image.load('images/bottom.png').convert()#bottom


bird1=pygame.image.load('images/bird1.png').convert_alpha()
bird2=pygame.image.load('images/bird2.png').convert_alpha()
bird3=pygame.image.load('images/bird3.png').convert_alpha()
birdpositions=[bird1,bird2,bird3]#bird
bird_index = 2
bird = birdpositions[bird_index]
#birdrec
birdrect=bird.get_rect(center=(30,80))
birdflaprepeat=pygame.USEREVENT+1
pygame.time.set_timer(birdflaprepeat,5)
#sound
flapsound=pygame.mixer.Sound('audio/wing.wav')
collidesound=pygame.mixer.Sound('audio/hit.wav')
scoresound=pygame.mixer.Sound('audio/point.wav')
#pipe trial
pipe=pygame.image.load('images/pipe.png')
pipelist=[]
pipeclock=pygame.USEREVENT
pygame.time.set_timer(pipeclock,1000)
pipeheight=[250,260,270,280,290,300,310,320,330,340,350]

gameworks=False

#pipetrial
def makepipe():
    height=random.choice(pipeheight)
    belowpipe=pipe.get_rect(midtop=(550,height))
    toppipe=pipe.get_rect(midbottom=(550, height-heightset))#change difficulity level
    return belowpipe,toppipe
def collision(pipelist) :
    global canscore
    for i in pipelist :
        if birdrect.colliderect(i):
            collidesound.play()
            return False
            canscore=True
    if birdrect.top<=0 or birdrect.bottom>=430:
        collidesound.play()
        return False
        canscore=True
    return True
def movepipes(pipelist):
    global score
    for pipe in pipelist:
        pipe.centerx-=2.5
    visiblepipe=[pipe for pipe in pipelist if pipe.right>-50]
    return visiblepipe
def drawpipes(pipelist):
    for i in pipelist:
        if i.bottom >= 512:
            screen.blit(pipe, i)
        else:
            flippipe=pygame.transform.flip(pipe,False,True)
            screen.blit(flippipe,i)
def rotatedbirdscreen(bird):
    newscreen=pygame.transform.rotozoom(bird,-b*7,1)
    return newscreen
def flappingbird():
    nextbird=birdpositions[bird_index]
    nextbirdrect=bird.get_rect(center=(30,birdrect.centery))
    return nextbird,nextbirdrect
def displayscore(state):
    if state=='active':

        scoresurface=game_font.render(f'Score:{str(int(score))}',True,(255,255,255))
        scoresurfacerect=scoresurface.get_rect(center=(144,50))
        screen.blit(scoresurface,scoresurfacerect)
    if state == 'over':
        scoresurface = game_font.render(f'Score:{str(int(score))}', True, (255, 255, 255))
        scoresurfacerect = scoresurface.get_rect(center=(144, 50))
        screen.blit(scoresurface, scoresurfacerect)

        hscoresurface = game_font.render(f'Highscore:{str(int(highscore))}', True, (255, 255, 255))
        hscoresurfacerect = scoresurface.get_rect(center=(130, 400))
        screen.blit(hscoresurface, hscoresurfacerect)
def scorefunction():
    global score,canscore
    if pipelist:
        for pipe in pipelist:
            if 27 <pipe.centerx<33 and canscore :
                score+=1
                scoresound.play()
                canscore=False
            if pipe.centerx<0:
                canscore=True
def upgradehighscore(score,highscore):
    if score>highscore:
        highscore=score
    return highscore
#score
score=0
highscore=0
game_font=pygame.font.Font('04B_19__.TTF',21)
game_fonts=pygame.font.Font('04B_19__.TTF',18)

message=game_font.render(f'PRESS SPACE TO CONTINUE',True,(255,255,255))
messagerect=message.get_rect(center=(144,250))

main=0#for main screen
canscore=True
#score
#pipetrial
#bird movement
fallrate=0.14#falling down of bird
b=0#actual bird movement
#birdmovement
t=0#bottom movement
x=True#exitgame
while x:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            x=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and gameworks==True:
                b=0
                b-=6
                flapsound.play()
            if event.key == pygame.K_SPACE and gameworks==False:
                gameworks=True
                pipelist.clear()
                birdrect.center=(30,80)
                b=0
                score=0
        if event.type==pipeclock:
            pipelist.extend(makepipe())
        if event.type==birdflaprepeat:
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0
            bird,birdrect=flappingbird()
    screen.blit(background,(0, 0))
    while not gameworks and main==0:
        texted=pygame.image.load('images/welcometext.png').convert_alpha()
        screen.blit(texted,(40,50))
        messages = game_fonts.render('LEVELS', True, (255, 255, 255))
        messagerects = message.get_rect(center=(240, 130))
        screen.blit(messages, messagerects)
        messages = game_fonts.render('Hard:Press u to Play', True, (255, 255, 255))
        messagerects = message.get_rect(center=(180, 160))
        screen.blit(messages,messagerects)
        messages = game_fonts.render('Normal:Press t to Play', True, (255, 255, 255))
        messagerects = message.get_rect(center=(180, 190))
        screen.blit(messages, messagerects)
        messages = game_fonts.render('Easy:Press w to Play', True, (255, 255, 255))
        messagerects = message.get_rect(center=(180, 220))
        screen.blit(messages, messagerects)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_u:
                    gameworks=True
                    heightset=150
                    main=1
                if event.key==pygame.K_t:
                    gameworks=True
                    heightset=175
                    main=1
                if event.key==pygame.K_w:
                    gameworks=True
                    heightset=200
                    main=1
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
    if gameworks:
    #bird
        b+=fallrate
        birdrect.centery+=b
        rotatedbird=rotatedbirdscreen(bird)
        screen.blit(rotatedbird,birdrect)
        #pipe
        pipelist=movepipes(pipelist)
        drawpipes(pipelist)
        gameworks = collision(pipelist)
        #Score
        scorefunction()



        displayscore('active')
    else:
        highscore=upgradehighscore(score,highscore)
        displayscore('over')
        screen.blit(message, messagerect)
    #pipe

    # bottom
    screen.blit(bottom, (t, 430))
    screen.blit(bottom, (t + 288, 430))
    t-=1
    if t <= -288:
        t = 0
    # bottom

    pygame.display.update()
    clock.tick(120)

