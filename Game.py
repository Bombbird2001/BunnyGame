import pygame
import math
import random

pygame.init()
pygame.mixer.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badGuyImg1 = pygame.image.load("resources/images/badguy.png")
badGuyImg = badGuyImg1
healthBar = pygame.image.load("resources/images/healthbar.png")
healthLeft = pygame.image.load("resources/images/health.png")
gameOver = pygame.image.load("resources/images/gameover.png")
youWin = pygame.image.load("resources/images/youwin.png")

hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

keys = [False, False, False, False]
playerPos = [100, 100]

accuracy = [0, 0]
arrows = []

badTimer = 100
badTimer1 = 0
badGuys = [[640, 100]]
health = 194

t = 0
gametime = 0
running = True
paused = False
exitCode = 0

while running:
    deltaTime = pygame.time.get_ticks() - t
    t = pygame.time.get_ticks()

    if not paused:
        screen.fill(0)

        for x in range(width // grass.get_width() + 1):
            for y in range(height // grass.get_height() + 1):
                screen.blit(grass, (x * 100, y * 100))

        if keys[0]:
            playerPos[1] -= 0.4 * deltaTime
        elif keys[2]:
            playerPos[1] += 0.4 * deltaTime
        if keys[1]:
            playerPos[0] -= 0.4 * deltaTime
        elif keys[3]:
            playerPos[0] += 0.4 * deltaTime

        mousePos = pygame.mouse.get_pos()
        angle = math.atan2(mousePos[1] - playerPos[1] - 32, mousePos[0] - playerPos[0] - 26)
        playerRot = pygame.transform.rotate(player, 360 - math.degrees(angle))
        playerPosCtr = (playerPos[0] - 26, playerPos[1] - 32)

        screen.blit(castle, (0, 30))
        screen.blit(castle, (0, 135))
        screen.blit(castle, (0, 240))
        screen.blit(castle, (0, 345))
        screen.blit(playerRot, playerPosCtr)

        if badTimer == 0:
            badGuys.append([640, random.randint(50, 430)])
            badTimer = 100 - (badTimer1 * 2)
            if badTimer1 < 27:
                badTimer1 += 3

        badTimer -= 1

        index = 0
        for badGuy in badGuys:
            badGuy[0] -= 0.2 * deltaTime
            badRect = pygame.Rect(badGuyImg.get_rect())
            badRect.top = badGuy[1]
            badRect.left = badGuy[0]
            if badRect.left < 64:
                hit.play()
                health -= random.randint(5, 20)
                badGuys.pop(index)
                index -= 1

            index1 = 0
            for bullet in arrows:
                bullRect = pygame.Rect(arrow.get_rect())
                bullRect.left = bullet[1]
                bullRect.top = bullet[2]
                if badRect.colliderect(bullRect):
                    enemy.play()
                    accuracy[0] += 1
                    badGuys.pop(index)
                    index -= 1
                    arrows.pop(index1)
                index1 += 1

            index += 1

        for badGuy in badGuys:
            screen.blit(badGuyImg, badGuy)

        index1 = 0
        for bullet in arrows:
            velX = math.cos(bullet[0]) * 10
            velY = math.sin(bullet[0]) * 10
            bullet[1] += velX
            bullet[2] += velY
            if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
                arrows.pop(index1)
                index1 -= 1
            index1 += 1

        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360 - math.degrees(projectile[0]))
            screen.blit(arrow1, (projectile[1], projectile[2]))

        font = pygame.font.Font(None, 24)
        survivedText = font.render(str(gametime / 1000), True, (0, 0, 0))
        textRect = survivedText.get_rect()
        textRect.topright = [635, 5]
        screen.blit(survivedText, textRect)

        screen.blit(healthBar, (5, 5))
        for health1 in range(health):
            screen.blit(healthLeft, (health1 + 8, 8))

        gametime += deltaTime
    else:
        font = pygame.font.Font(None, 36)
        pauseText = font.render("Paused, press P to continue", True, (255, 0, 0))
        pauseTextRect = pauseText.get_rect()
        pauseTextRect.center = [320, 240]
        screen.blit(pauseText, pauseTextRect)

    pygame.display.flip()

    if gametime > 90000:
        running = False
        exitCode = 1

    if health <= 0:
        running = False
        exitCode = 0

    for event in pygame.event.get():
        # check if the event is the X button
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keys[0] = True
            elif event.key == pygame.K_a:
                keys[1] = True
            elif event.key == pygame.K_s:
                keys[2] = True
            elif event.key == pygame.K_d:
                keys[3] = True

            if event.key == pygame.K_p:
                paused = not paused

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            accuracy[1] += 1
            arrows.append([math.atan2(mousePos[1] - (playerPosCtr[1] + 32), mousePos[0] - (playerPosCtr[0] + 26)), playerPosCtr[0] + 32, playerPosCtr[1] + 32])

acc = 0
if accuracy[1] > 0:
    acc = round(accuracy[0] / accuracy[1] * 100.0, 1)

if exitCode == 0:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: " + str(acc) + "%", True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(gameOver, (0, 0))
    screen.blit(text, textRect)
elif exitCode == 1:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: " + str(acc) + "%", True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(youWin, (0, 0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
