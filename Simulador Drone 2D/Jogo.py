import pygame
from pygame.locals import *
from sys import exit
from PIL import Image

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
xlim = larg - drone.get_size()[0]
ylim = alt - drone.get_size()[1]

# Movement, position and rotation parameters
vel = 8
posX = 100
posY = 540
angle = 0

# Game clock to control the FPS
clock = pygame.time.Clock()

while True:
    clock.tick(30)  # Game FPS

    # Screen configuration
    tela.fill((0, 0, 0))  # Clean the last screen to update the frames
    tela.blit(background, (0, 0))  # Load the bg at the (0, 0) position of the screen

    for event in pygame.event.get():
        # To quit the game
        if event.type == QUIT:
            pygame.quit()
            exit()

    # Gets the keys that are being pressed
    keys = pygame.key.get_pressed()

    # Moving and limiting the player position on the screen
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and posY > 0:
        posY -= vel
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and posY < ylim:
        posY += vel
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and posX > 0:
        posX -= vel
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and posX < xlim:
        posX += vel
    if keys[pygame.K_e]:
        angle += 10
    if keys[pygame.K_q]:
        angle -= 10

    # Rotating drone
    drone_rotated = pygame.transform.rotate(drone, angle)
    drone_rotated_pos = (posX - drone_rotated.get_width() / 2, posY - drone_rotated.get_height() / 2)

    # spawn drone
    tela.blit(drone_rotated, drone_rotated_pos)

    pygame.display.update()
