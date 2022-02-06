import pygame
from pygame.locals import *
from sys import exit
from PIL import Image
import math

class Tela:
	def __init__(self, larg, alt, imagem_fundo ):
		pygame.init()
		pygame.display.set_caption("Simulador 2D de Drone")
        # Tamanho da janela
		self.larg = larg
		self.alt = alt
		# Load background image
		self.imagem_fundo = imagem_fundo
		self.background = pygame.image.load('Imagens/Imagem_fundo_resized.jpg')
		self.tela = pygame.display.set_mode((self.larg, self.alt))
       
	def desenha_tela(self):
		#Resizing background image to match the screen size
		image = Image.open(imagem_fundo)
		image = image.resize((self.larg, self.alt))
		image.save('Imagens/Imagem_fundo_resized.jpg')


	def plot(self,x,y):
		self.tela.blit(x,y)
	
	def update_tela(self):
			# Screen configuration
			self.tela.fill((0, 0, 0))  # Clean the last screen to update the frames
			self.tela.blit(self.background, (0, 0))  # Load the bg at the (0, 0) position of the screen

class Drone:
	def __init__(self,position,angle,vel,imagem_drone):
		self.position = position
		self.posX = position[0]
		self.posY = position[1]
		self.angle = angle
		self.vel = vel 		
		self.drone = 0
		
		# Load drone image
		self.imagem_drone = imagem_drone
		self.drone = pygame.image.load('Imagens/drone_resized.png')
		self.tamX = self.drone.get_size()[0]
		self.tamY = self.drone.get_size()[0]
		self.height = 0,0

	def desenha_drone(self):
		# Resizing player image
		image = Image.open(imagem_drone)
		image = image.resize((100, 50))
		image.save('Imagens/drone_resized.png')
	
	def drone_update(self):
		# Load drone image
		self.drone = pygame.image.load('Imagens/drone_resized.png')
		# Rotating drone
		drone_rotated = pygame.transform.rotate(self.drone, self.angle)
		self.height = drone_rotated.get_height()/2
		drone_rotated_pos = (self.position[0] - drone_rotated.get_width() / 2, self.position[1] - self.height)
		# spawn drone
		tela.plot(drone_rotated, drone_rotated_pos)
		

class Controle:
	def __init__(self):
		# Movement, position and rotation parameters
		self.position = 500,540
		self.posX = self.position[0]
		self.posY = self.position[1]
		self.vel = 8
		self.angle = 0
		self.drone = Drone(self.position, self.angle, self.vel, imagem_drone)
		# Screen limits (The screen size minus the player size)
		self.xlim = tela.larg - self.drone.tamX / 30
		self.ylim = tela.alt - self.drone.tamY * 1.5
		self.keys = 0
		# Boost control
		self.v_up = 0
		self.v_fall = 0
		self.vel_vertical = 0
		self.v_max = 18  # cm/s (1 px = 1 cm)
		self.a_up = 10


	def key_control(self):
		# Gets the keys that are being pressed        
		self.keys = pygame.key.get_pressed()
 
		self.left_button()
		self.right_button()
		self.up_button()
		self.down_button()
		self.acelerar()
		self.a_gravidade()	
		
		self.position = self.posX, self.posY
		drone.drone_update()


	def left_button(self):
		if (self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]) and self.posX > 0:
			self.posX -= self.vel

	def right_button(self):
		if (self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]) and self.posX < self.xlim:
			self.posX += self.vel

	def up_button(self):
		if (self.keys[pygame.K_UP] or self.keys[pygame.K_w]) and self.posY > 0:
			self.posY -= self.vel

	def down_button(self):
		if (self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]) and self.posY < self.ylim:
			self.posY += self.vel

	def acelerar(self):
		v_up = self.v_up
		v_max = self.v_max
		a_up = self.a_up
		
		if self.keys[K_SPACE] and self.posY > 0:
			# Up velocity control
			v_up += 0.1 * abs(self.vel_vertical) + a_up
			if v_up >= v_max:
				v_up = v_max
		else:
			v_up -= 2 * a_up
			if v_up <= 0:
				v_up = 0
	def a_gravidade(self):
		g = 9.81 #gravidade
		aux = self.drone.height
		#print(aux)

		# self.v_fall += -math.sqrt(self.vel_vertical ** 2 + 2 * g * (self.ylim - (self.posY - aux)))
		# if self.v_fall <= -10:
 	# 		self.v_fall = -10
		# self.vel_vertical = - self.v_up - self.v_fall
		# self.posY += self.vel_vertical


	def mouse_control(self):
		# Drone's destiny: a (x, y) coordinate
		mx, my = pygame.mouse.get_pos()
		self.position = (mx - self.drone.tamX / 2, my - self.drone.tamY / 2)
		print(self.position)
		#drone.drone_update()


class Game:
	
	def __init__(self):
		self.clock = pygame.time.Clock()
		self.ticks = 60
		self.exit = False
		
	def run(self):
		while True:
			self.clock.tick(30)  # Game FPS
			t = self.clock.get_time() / 1000

			for event in pygame.event.get():
				# To quit the game
				if event.type == QUIT:
					pygame.quit()
					exit()
					
				if event.type == pygame.MOUSEBUTTONDOWN:
					controle.mouse_control()


			drone.position = controle.position
			controle.key_control()
			tela.update_tela()
			drone.drone_update()
			pygame.display.update()



if __name__ == '__main__':

	imagem_fundo = 'Imagens/ghibli_background.jpg'
	imagem_drone = 'Imagens/drone.png'
	tela = Tela(1000,640,imagem_fundo)
	controle = Controle()
	drone = Drone(controle.position, controle.angle, controle.vel, imagem_drone)
	
	game = Game()
	game.run()




    


