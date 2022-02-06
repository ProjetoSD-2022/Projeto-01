import pygame
from pygame.locals import *
from sys import exit
from PIL import Image
from Jogo import *

def main():
    # Tamanho da janela
    main_larg = 1000
    main_alt = 640

    pygame.init()
    tela = pygame.display.set_mode((main_larg, main_alt))
    pygame.display.set_caption('Menu do Simulador 2D de Drone')

    # Resizing background image to match the screen size
    main_image = Image.open('Imagens/ghibli_background_main.jpg')
    main_image = main_image.resize((main_larg, main_alt))
    main_image.save('Imagens/ghibli_background_main_resized.jpg')

    # Resizing menus images
    # Play image
    main_image_play_width = 200 # Set width size
    main_image_play_height = 72 # Set height size
    main_image = Image.open('Imagens/image_play.png')
    main_image = main_image.resize((main_image_play_width, main_image_play_height))
    main_image.save('Imagens/image_play_resized.png')
    # Credits image
    main_image_credits_width = 350 # Set width size
    main_image_credits_height = 80 # Set height size
    main_image = Image.open('Imagens/image_creditos.png')
    main_image = main_image.resize((main_image_credits_width, main_image_credits_height))
    main_image.save('Imagens/image_creditos_resized.png')


    # Load images
    main_background = pygame.image.load('Imagens/ghibli_background_main_resized.jpg')
    main_image_play = pygame.image.load('Imagens/image_play_resized.png')
    main_image_credits = pygame.image.load('Imagens/image_creditos_resized.png')
    main_image_drone = pygame.image.load('Imagens/image_drone.png')

    main_clock = pygame.time.Clock()

    main_click = False

    while True:
        main_clock.tick(30)  # Game FPS

        # Screen configuration
        main_image_play_x = 710 # Set pos in x for image credits
        main_image_play_y = 450 # Set pos in y for image credits
        main_image_credits_x = 670 # Set pos in x for image credits
        main_image_credits_y = 550 # Set pos in y for image credits
        tela.fill((0, 0, 0))  # Clean the last screen to update the frames
        tela.blit(main_background, (0, 0))  # Load the bg at the (0, 0) position of the screen
        tela.blit(main_image_play, (main_image_play_x, main_image_play_y))
        tela.blit(main_image_credits, (main_image_credits_x, main_image_credits_y))
        tela.blit(main_image_drone, (50, 150))
        
        # Creating a rect to get play click
        button_1 = pygame.Rect(main_image_play_x, main_image_play_y, main_image_play_width, main_image_play_height)
        # Creating a rect to get play click
        button_2 = pygame.Rect(main_image_credits_x, main_image_credits_y, main_image_credits_width, main_image_credits_height)

        # Get mouse positions in mx and my
        main_mx, main_my = pygame.mouse.get_pos()

        # Get click on image play
        if button_1.collidepoint((main_mx, main_my)):
            if main_click:
                #game()
                pass
        # Get click on image credits
        if button_2.collidepoint((main_mx, main_my)):
            if main_click:
                func_creditos()

        main_click = False

        for event in pygame.event.get():
                # To quit the game
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        main_click = True

        pygame.display.update()


def func_creditos():
    # Tamanho da janela
    credits_larg = 1000
    credits_alt = 640

    pygame.init()
    tela = pygame.display.set_mode((credits_larg, credits_alt))
    pygame.display.set_caption('Créditos do Simulador 2D de Drone')

    # Resizing credits images
    # Back image
    credits_image_back_width = 250 # Set width size
    credits_image_back_height = 72 # Set height size
    credits_image = Image.open('Imagens/image_back.png')
    credits_image = credits_image.resize((credits_image_back_width, credits_image_back_height))
    credits_image.save('Imagens/image_back_resized.png')
    # Names Images
    credits_image = Image.open('Imagens/image_amanda.png')
    credits_image = credits_image.resize((credits_image_back_width+20, credits_image_back_height))
    credits_image.save('Imagens/image_amanda_resized.png')
    credits_image = Image.open('Imagens/image_glenio.png')
    credits_image = credits_image.resize((credits_image_back_width+10, credits_image_back_height+10))
    credits_image.save('Imagens/image_glenio_resized.png')
    credits_image = Image.open('Imagens/image_isis.png')
    credits_image = credits_image.resize((credits_image_back_width, credits_image_back_height-10))
    credits_image.save('Imagens/image_isis_resized.png')
    credits_image = Image.open('Imagens/image_leonardo.png')
    credits_image = credits_image.resize((credits_image_back_width+40, credits_image_back_height))
    credits_image.save('Imagens/image_leonardo_resized.png')
    credits_image = Image.open('Imagens/image_neila.png')
    credits_image = credits_image.resize((credits_image_back_width, credits_image_back_height))
    credits_image.save('Imagens/image_neila_resized.png')


    # Load images
    credits_background = pygame.image.load('Imagens/ghibli_background_resized.jpg')
    image_back = pygame.image.load('Imagens/image_back_resized.png')
    image_amanda = pygame.image.load('Imagens/image_amanda_resized.png')
    image_glenio = pygame.image.load('Imagens/image_glenio_resized.png')
    image_isis = pygame.image.load('Imagens/image_isis_resized.png')
    image_leonardo = pygame.image.load('Imagens/image_leonardo_resized.png')
    image_neila = pygame.image.load('Imagens/image_neila_resized.png')

    credits_clock = pygame.time.Clock()

    credits_click = False

    while True:
        credits_clock.tick(30)  # Game FPS

        tela.fill((0, 0, 0))  # Clean the last screen to update the frames
        tela.blit(credits_background, (0, 0))  # Load the bg at the (0, 0) position of the screen
        main_image_back_x = 770 # Set pos in x for image back
        main_image_back_y = 550 # Set pos in y for image back
        tela.blit(image_back, (main_image_back_x, main_image_back_y)) # Load Back image
        tela.blit(image_amanda, (355, 100)) # Load Amanda image
        tela.blit(image_glenio, (375, 180)) # Load Glênio image
        tela.blit(image_isis, (355, 260)) # Load Isis image
        tela.blit(image_leonardo, (350, 335)) # Load Leonardo image
        tela.blit(image_neila, (370, 410)) # Load Neila image

        # Get mouse positions in mx and my
        credits_mx, mcredits_my = pygame.mouse.get_pos()

        # Creating a rect to get play click
        button_1 = pygame.Rect(main_image_back_x, main_image_back_y, credits_image_back_width, credits_image_back_height)

        # Get click on image play
        if button_1.collidepoint((credits_mx, mcredits_my)):
            if credits_click:
                return

        credits_click = False

        for event in pygame.event.get():
                # To quit the game
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        credits_click = True

        pygame.display.update()

main()