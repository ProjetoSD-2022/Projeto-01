import pygame
from pygame.locals import *
from sys import exit
from PIL import Image
import math


def main():
    # Tamanho da janela
    larg = 1000
    alt = 640

    pygame.init()
    tela = pygame.display.set_mode((larg, alt))
    pygame.display.set_caption('Simulador 2D de Drone')

    # Resizing background image to match the screen size
    image = Image.open('Imagens/ghibli_background.jpg')
    image = image.resize((larg, alt))
    image.save('Imagens/ghibli_background_resized.jpg')

    # Load background image
    background = pygame.image.load('Imagens/ghibli_background_resized.jpg')

    # Resizing player image
    image = Image.open('Imagens/drone.png')
    image = image.resize((100, 50))
    image.save('Imagens/drone_resized.png')

    # Load drone image
    drone = pygame.image.load('Imagens/drone_resized.png')

    # Screen limits (The screen size minus the player size)
    xlim = larg - drone.get_size()[0] / 2
    ylim = alt - drone.get_size()[1] * 1.5

    # Movement and rotation parameters when the auto-stabilize is on
    vel = 10
    angle = 0
    y_direction = 0  # changes the y direction to + or - depending on the direction key pressed

    # Gravity
    g = 9.8

    # BOOST CONTROL
    v_up = 0  # boost velocity
    v_up_max = 20  # maximum v_up velocity cm/s (1 px = 1 cm)
    a_up = 10  # boost acceleration
    v_fall = 0  # free fall velocity (simulates gravity)
    vel_vertical = 0  # resultant y velocity (v_up - v_fall)
    v_stabilize = 0  # Stabilization velocity to compensate the gravity

    ax = 0
    ay = 0
    m = 0.25
    F = 0
    Fy = 0
    Fx = 0

    # Drone's position
    posX = 500
    posH = posX
    posY = 540

    # Drone's destiny position
    destino = (posX - drone.get_size()[0] / 2, posY - drone.get_size()[1] / 2)

    # Auto stabilize control, makes the drone automaticaly control its y position
    steady = False
    auto_stabilize = 0

    # Game clock to control the FPS
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)  # Game FPS
        t = clock.get_time() / 1000  # Time in seconds
        # print('t: ', t)

        # Screen configuration
        tela.fill((0, 0, 0))  # Clean the last screen to update the frames
        tela.blit(background, (0, 0))  # Load the bg at the (0, 0) position of the screen

        for event in pygame.event.get():
            # To quit the game
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Drone's destiny: a (x, y) coordinate
                mx, my = pygame.mouse.get_pos()
                destino = (mx - drone.get_size()[0] / 2, my - drone.get_size()[1] / 2)

        # Gets the keys that are being pressed
        keys = pygame.key.get_pressed()

        # Moving and limiting the player position on the screen
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and posX > 0:
            posX -= vel

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and posX < xlim:
            posX += vel

        if keys[K_f]:
            steady = True
            auto_stabilize = 1
        if keys[K_g]:
            steady = False
            auto_stabilize = 0

        if steady:
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and posY > 0:
                y_direction = -1
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and posY < ylim:
                y_direction = 1
            else:
                y_direction = 0

        '''if keys[K_SPACE] and posY > 0:
            # boost control, hold space to activate drone boost
            v_up += 0.1 * abs(vel_vertical) + a_up * t
            if v_up >= v_up_max:
                v_up = v_up_max
        else:
            # when space is released, the boost is slowly decreased
            v_up -= 2 * a_up * t
            if v_up <= 0:
                v_up = 0'''

        if keys[K_SPACE] and posY > 0:
            # boost control, hold space to activate drone boost
            F += 100*t
            if F >= 155:
                F = 155
        else:
            # when space is released, the boost is slowly decreased
            F -= 100 * t
            if F <= 0:
                F = 0

        if keys[pygame.K_q]:
            angle += 5

        if keys[pygame.K_e]:
            angle -= 5

        # Limit the max angle to 35°
        if angle >= 35:
           angle = 35
        if angle <= -35:
            angle = -35

        # Rotating drone
        drone_rotated = pygame.transform.rotate(drone, angle)

        '''# if auto stabilize is on, the drone will slowly top its boost until it stabilizes in a y position
        if not steady:
            auto_stable_on = 0
            auto = 1
            v_up_max = 20
            v_stabilize -= a_up * t
            if v_stabilize <= 0:
                v_stabilize = 0
        else:
            auto_stable_on = 1
            auto = 0
            v_up_max = 10
            v_stabilize += a_up*t
            if v_stabilize >= -v_fall:
                v_stabilize = -v_fall

        v_down = v_stabilize + v_fall

        # Simulates a free fall because of gravity
        v_fall += -g * t
        if v_fall <= -10:
            v_fall = -10

        vel_vertical = - v_up * math.cos(angle * math.pi / 180) - v_down
        vel_horizontal = -v_up * math.sin(angle * math.pi / 180)'''

        # FORCE
        Fx = F * math.sin(angle * math.pi / 180)

        if not steady:
            Fy = F*math.cos(angle * math.pi / 180)
            vel -= 0.2
            print(vel)
            if vel <= 0:
                vel = 0
        else:
            vel = 10
            if Fy < m*g*31:
                Fy += 50*t
            if Fy > m * g * 31:
                Fy -= 50 * t
            if m*g*31 - 1 < Fy < m*g*31 + 1:
                Fy = m*g*31

        ay = (Fy - m*g*31) / m
        ax = Fx / m

        vel_vertical = -ay * t + vel*y_direction*math.cos(angle * math.pi / 180)
        vel_horizontal = -ax * t - vel * math.sin(angle * math.pi / 180)

        if vel_vertical >= 10:
            vel_vertical = 10
        elif vel_vertical <= -10:
            vel_vertical = -10

        if vel_horizontal >= 10:
            vel_horizontal = 10
        elif vel_horizontal <= -10:
            vel_horizontal = -10

        posY += vel_vertical
        posH += vel_horizontal

        '''# Calculate the y movement
        posY += (vel_vertical*auto + auto_stable_on * y_direction * vel * math.cos(angle*math.pi/180))
        posH += vel_horizontal + auto_stable_on * y_direction * vel * math.sin(angle*math.pi/180)'''

        # Limit the ground border
        if posY >= ylim:
            posY = ylim
        if posY <= drone_rotated.get_height() / 2:
            posY = drone_rotated.get_height() / 2

        drone_rotated_pos = (posH - drone_rotated.get_width() / 2, posY - drone_rotated.get_height() / 2)
        # drone_rotated_pos = (posX - drone_rotated.get_width() / 2, posY - drone_rotated.get_height() / 2)

        # spawn drone
        tela.blit(drone_rotated, drone_rotated_pos)

        pygame.display.update()


if __name__ == '__main__':
    main()
