import pygame
from pygame.locals import *
from sys import exit
from PIL import Image
from Jogo import *

def main():
    # Tamanho da janela
    tela_larg = 1000
    tela_alt = 640

    pygame.init()
    tela = pygame.display.set_mode((tela_larg, tela_alt))
    pygame.display.set_caption('Menu do Simulador 2D de Drone')

    # Resizing background image to match the screen size
    image = Image.open('Imagens/ghibli_background_main.jpg')
    image = image.resize((tela_larg, tela_alt))
    image.save('Imagens/ghibli_background_main_resized.jpg')

    # Resizing menus images
    # Play image
    image_play_width = 200 # Set width size
    image_play_height = 72 # Set height size
    image = Image.open('Imagens/image_play.png')
    image = image.resize((image_play_width, image_play_height))
    image.save('Imagens/image_play_resized.png')
    # Credits image
    image_credits_width = 350 # Set width size
    image_credits_height = 80 # Set height size
    image = Image.open('Imagens/image_creditos.png')
    image = image.resize((image_credits_width, image_credits_height))
    image.save('Imagens/image_creditos_resized.png')


    # Load images
    background = pygame.image.load('Imagens/ghibli_background_main_resized.jpg')
    image_play = pygame.image.load('Imagens/image_play_resized.png')
    image_credits = pygame.image.load('Imagens/image_creditos_resized.png')
    image_drone = pygame.image.load('Imagens/image_drone.png')

    clock = pygame.time.Clock()

    click = False

    while True:
        clock.tick(30)  # Game FPS

        image_play_x = 710 # Set pos in x for image credits
        image_play_y = 450 # Set pos in y for image credits
        image_credits_x = 670 # Set pos in x for image credits
        image_credits_y = 550 # Set pos in y for image credits

        # Screen configuration
        tela.fill((0, 0, 0))  # Clean the last screen to update the frames
        tela.blit(background, (0, 0))  # Load the bg at the (0, 0) position of the screen
        tela.blit(image_play, (image_play_x, image_play_y)) # Load play image
        tela.blit(image_credits, (image_credits_x, image_credits_y)) # Load credits image
        tela.blit(image_drone, (50, 150)) # Load drone image
        
        # Creating a rect to get play click
        button_1 = pygame.Rect(image_play_x, image_play_y, image_play_width, image_play_height)
        # Creating a rect to get play click
        button_2 = pygame.Rect(image_credits_x, image_credits_y, image_credits_width, image_credits_height)

        # Get mouse positions in mouse_x and mouse_y
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Get click on image play
        if button_1.collidepoint((mouse_x, mouse_y)):
            if click:
                game() # Calls the function of the game in other file
                #pass
        # Get click on image credits
        if button_2.collidepoint((mouse_x, mouse_y)):
            if click:
                creditos() # Calls the function creditos responsible for screen credits

        click = False

        for event in pygame.event.get():
                # To quit the game
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

        pygame.display.update()


def creditos():
    # Tamanho da janela
    tela_larg = 1000
    tela_alt = 640

    pygame.init()
    tela = pygame.display.set_mode((tela_larg, tela_alt))
    pygame.display.set_caption('Créditos do Simulador 2D de Drone')

    # Resizing credits images
    # Back image
    image_back_width = 250 # Set width size
    image_back_height = 72 # Set height size
    image = Image.open('Imagens/image_back.png')
    image = image.resize((image_back_width, image_back_height))
    image.save('Imagens/image_back_resized.png')
    # Names Images
    image = Image.open('Imagens/image_amanda.png')
    image = image.resize((image_back_width+20, image_back_height))
    image.save('Imagens/image_amanda_resized.png')
    image = Image.open('Imagens/image_glenio.png')
    image = image.resize((image_back_width+10, image_back_height+10))
    image.save('Imagens/image_glenio_resized.png')
    image = Image.open('Imagens/image_isis.png')
    image = image.resize((image_back_width, image_back_height-10))
    image.save('Imagens/image_isis_resized.png')
    image = Image.open('Imagens/image_leonardo.png')
    image = image.resize((image_back_width+40, image_back_height))
    image.save('Imagens/image_leonardo_resized.png')
    image = Image.open('Imagens/image_neila.png')
    image = image.resize((image_back_width, image_back_height))
    image.save('Imagens/image_neila_resized.png')


    # Load images
    background = pygame.image.load('Imagens/ghibli_background_resized.jpg')
    image_back = pygame.image.load('Imagens/image_back_resized.png')
    image_amanda = pygame.image.load('Imagens/image_amanda_resized.png')
    image_glenio = pygame.image.load('Imagens/image_glenio_resized.png')
    image_isis = pygame.image.load('Imagens/image_isis_resized.png')
    image_leonardo = pygame.image.load('Imagens/image_leonardo_resized.png')
    image_neila = pygame.image.load('Imagens/image_neila_resized.png')

    cloc = pygame.time.Clock()

    click = False

    while True:
        cloc.tick(30)  # Game FPS

        image_back_x = 770 # Set pos in x for image back
        image_back_y = 550 # Set pos in y for image back

        # Screen configuration
        tela.fill((0, 0, 0))  # Clean the last screen to update the frames
        tela.blit(background, (0, 0))  # Load the bg at the (0, 0) position of the screen
        tela.blit(image_back, (image_back_x, image_back_y)) # Load Back image
        tela.blit(image_amanda, (355, 100)) # Load Amanda image
        tela.blit(image_glenio, (375, 180)) # Load Glênio image
        tela.blit(image_isis, (355, 260)) # Load Isis image
        tela.blit(image_leonardo, (350, 335)) # Load Leonardo image
        tela.blit(image_neila, (370, 410)) # Load Neila image

        # Get mouse positions in mouse_x and mouse_y
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Creating a rect to get back click
        button_1 = pygame.Rect(image_back_x, image_back_y, image_back_width, image_back_height)

        # Get click on image back
        if button_1.collidepoint((mouse_x, mouse_y)):
            if click:
                return # Returns to main function

        click = False

        for event in pygame.event.get():
                # To quit the game
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

        pygame.display.update()

main()