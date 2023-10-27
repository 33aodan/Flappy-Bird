import pygame, random, sys
from pygame.locals import *
fps = 32
screenwidth = 289
screenheight = 511
screen = pygame.display.set_mode((screenwidth,screenheight))
GroundY = screenheight*0.8
game_sprite={}
game_sound={}
player="gallery/gallery/sprites/bird.png"
background="gallery/gallery/sprites/background.png"
obstacle="gallery/gallery/sprites/pipe.png"


def WelcomeScreen():
    playerX = int(screenwidth/5)
    playerY = int((screenheight-game_sprite["player"].get_height())/2)
    messageX = int((screenwidth-game_sprite["message"].get_width())/2)
    messageY = int(screenheight*0.13)
    baseX = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):#Closes game window
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): #starts the game through space key and up arrow key
                return
            else:
                screen.blit(game_sprite["background"], (0, 0))
                screen.blit(game_sprite["player"], (playerX, playerY))
                screen.blit(game_sprite["message"], (messageX, messageY))
                screen.blit(game_sprite["base"], (baseX, GroundY))
                pygame.display.update()
                FPSClock.tick(fps)

def mainGame():
    score = 0
    playerX = int(screenwidth/5)
    playerY = int(screenwidth/2)
    baseX = 0
    pipe1 = getrandompipe()
    pipe2 = getrandompipe()
    upperpipe = [
        {"x": screenwidth + 200, 'y': pipe1[0]['y']},
        {"x": screenwidth + 200 + (screenwidth / 2), "y": pipe2[0]["y"]},
    ]
    lowerpipe=[
        {"x": screenwidth+200, 'y': pipe1[1]['y']},
        {"x": screenwidth+ 200 + (screenwidth/2),"y": pipe2[1]["y"]},
    ]

    playerVelY=-9
    playerMaxY=10
    playerMinY=-8
    playerAccY=1
    playerFlappedAccV=-8
    playerflap = False
    pipeVelX=-4

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):#Closes game window
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playerY > 0:
                    playerVelY=playerFlappedAccV
                    playerflap= True
                    game_sound["wing"].play()

        crash = isCollide(playerX, playerY, upperpipe, lowerpipe)
        if crash:
            return

        playermidpos = playerX + game_sprite["player"].get_width()/2

        for pipe in upperpipe:
            pipemidpos = pipe["x"] + game_sprite["pipe"][0].get_width()/2
            if pipemidpos <= playermidpos < pipemidpos + 4:
                score += 1
                print(f"your score is {score}")
                game_sound["point"].play()

        if playerVelY < playerMaxY and not playerflap:
            playerVelY += playerAccY
        if playerflap:
            playerflap = False

        playerheight = game_sprite["player"].get_height()
        playerY = playerY + min(playerVelY, GroundY - playerY - playerheight)

        for up, lp in zip(upperpipe, lowerpipe):
            up['x'] += pipeVelX
            lp['x'] += pipeVelX

        if 0 < upperpipe[0]['x'] < 5:
            newpipe = getrandompipe()
            upperpipe.append(newpipe[0])
            lowerpipe.append(newpipe[1])

        if upperpipe[0]['x'] < -game_sprite["pipe"][0].get_width():
            upperpipe.pop(0)
            lowerpipe.pop(0)

        screen.blit(game_sprite["background"], (0, 0))
        for up, lp in zip(upperpipe,lowerpipe):
            screen.blit(game_sprite["pipe"][0],(up['x'], up['y']))
            screen.blit(game_sprite["pipe"][1], (lp['x'], lp['y']))

        screen.blit(game_sprite["base"],(baseX,GroundY))
        screen.blit(game_sprite["player"],(playerX,playerY))
        digits=[int(x) for x in list(str(score))]
        width=0

        for digit in digits:
            width += game_sprite["numbers"][digit].get_width()
        Xoffset=(screenwidth-width)/2

        for digit in digits:
            screen.blit(game_sprite["numbers"][digit],(Xoffset, screenheight*0.12))
            Xoffset += game_sprite["numbers"][digit].get_width()
        pygame.display.update()
        FPSClock.tick(fps)

def isCollide(playerX, playerY, upperpipe,lowerpipe):
    if playerY > GroundY - 25 or playerY < 0:
        game_sound["hit"].play()
        return True

    for pipe in upperpipe:
        pipeheight = game_sprite["pipe"][0].get_height()
        if (playerY < pipeheight + pipe["y"] and abs(playerX - pipe['x']) < game_sprite["pipe"][0].get_width()):
            game_sound["hit"].play()
            return True

    for pipe in lowerpipe:
        if (playerY + game_sprite["player"].get_height() > pipe["y"]) and abs(playerX - pipe['x']) < \
                game_sprite["pipe"][0].get_width():
            game_sound["hit"].play()
            return True

    return False
#3
def getrandompipe():
    pipeheight = game_sprite["pipe"][0].get_height()
    offset = screenheight/3
    y2 = offset + random.randint(0,int(screenheight - game_sprite["base"].get_height() - 1.2 * offset))
    y1 = pipeheight - y2 + offset
    pipex = screenwidth + 10
    pipe = [{'x': pipex,'y': -y1}, {'x': pipex, 'y': y2}]
    return pipe

if __name__ == '__main__':
    pygame.init()
    FPSClock=pygame.time.Clock()
    pygame.display.set_caption("flappy bird game that got deleted off of the app store.")
    game_sprite["numbers"]=(
        pygame.image.load("gallery/gallery/sprites/0.png").convert_alpha(),
        pygame.image.load("gallery/gallery/sprites/1.png").convert_alpha(),
        pygame.image.load("gallery/gallery/sprites/2.png").convert_alpha(),
        pygame.image.load("gallery/gallery/sprites/3.png").convert_alpha(),
        pygame.image.load("gallery/gallery/sprites/4.png").convert_alpha(),
        pygame.image.load("gallery/gallery/sprites/5.png").convert_alpha(),
        pygame.image.load("gallery/gallery/sprites/6.png").convert_alpha(),
        pygame.image.load("gallery/gallery/sprites/7.png").convert_alpha(),
        pygame.image.load("gallery/gallery/sprites/8.png").convert_alpha(),
        pygame.image.load("gallery/gallery/sprites/9.png").convert_alpha(),

    )
    game_sprite["base"] = (
        pygame.image.load("gallery/gallery/sprites/base.png").convert_alpha()
    )
    game_sprite["message"] = (
        pygame.image.load("gallery/gallery/sprites/message.jpg").convert_alpha()
    )
    game_sprite["pipe"] = (
        pygame.transform.rotate(pygame.image.load(obstacle).convert_alpha(),180),
        pygame.image.load(obstacle).convert_alpha()
    )

    game_sprite["player"] = (
        pygame.image.load(player)
    )

    game_sprite["background"] = (
        pygame.image.load(background).convert_alpha()
    )

    game_sound["die"] = pygame.mixer.Sound("gallery/gallery/audio/die.wav")
    game_sound["hit"] = pygame.mixer.Sound("gallery/gallery/audio/hit.wav")
    game_sound["point"] = pygame.mixer.Sound("gallery/gallery/audio/point.wav")
    game_sound["swoosh"] = pygame.mixer.Sound("gallery/gallery/audio/swoosh.wav")
    game_sound["wing"] = pygame.mixer.Sound("gallery/gallery/audio/wing.wav")

    while True:
        WelcomeScreen()
        mainGame()




