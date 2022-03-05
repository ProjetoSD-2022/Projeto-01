from Classes import Game

# Screen size
larg = 1000
alt = 640

if __name__ == '__main__':
    # Background image
    bg_image = 'Imagens/ghibli_background.jpg'
    # Player Image
    drone_image = 'Imagens/drone.png'

    # Creating game class
    game = Game(larg, alt, bg_image, drone_image)
    game.run()
