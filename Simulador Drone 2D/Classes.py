import pygame
from pygame.locals import *
from sys import exit
from PIL import Image
from PID import execute_PID
import numpy as np

# Global Variables
larg = 1000.0
alt = 640.0
global position_, angle_, velocidade
position_ = 0
angle_ = 0
velocidade = 0


class Screen:
	def __init__(self, larg, alt, bg_image):
		pygame.init()
		# Set window's name
		pygame.display.set_caption("Simulador 2D de Drone")
		# Load background image
		self.bg_image = bg_image
		self.background = pygame.image.load('Imagens/Imagem_fundo_resized.jpg')
		# Window's size
		self.larg = larg
		self.alt = alt
		self.screen = pygame.display.set_mode((self.larg, self.alt))

	def resize_screen_image(self):
		# Resizing background image to match the screen size
		image = Image.open(bg_image)
		image = image.resize((self.larg, self.alt))
		image.save('Imagens/Imagem_fundo_resized.jpg')

	def plot(self, x, y):
		self.screen.blit(x, y)
	
	def update_screen(self):
			# Screen configuration
			self.screen.fill((0, 0, 0))  # Clean the last screen to update the frames
			self.screen.blit(self.background, (0, 0))  # Load the bg at the (0, 0) position of the screen

			# Fonte 
			fonte = pygame.font.SysFont('arial', 15, True, True)
			# Destino
			texto = f'Destino do drone: ({mx_real:.2f}, {my_real:.2f})'
			texto_formatado = fonte.render(texto, True, (255, 255, 255))
			self.screen.blit(texto_formatado, (10, 10))
			# Posição Atual
			texto = f'Posição atual: ({position_})'
			texto_formatado = fonte.render(texto, True, (255, 255, 255))
			self.screen.blit(texto_formatado, (10, 30))
			# Velocidade Atual
			texto = f'Velocidade atual: ({velocidade})'
			texto_formatado = fonte.render(texto, True, (255, 255, 255))
			self.screen.blit(texto_formatado, (10, 50))
			# Angulo Atual
			texto = f'Ângulo: {angle_:.2f}'
			texto_formatado = fonte.render(texto, True, (255, 255, 255))
			self.screen.blit(texto_formatado, (10, 70))


class Drone:
	def __init__(self, position, angle, vel, drone_image):
		# Drone's position, angle and velocity
		self.position = position
		self.posH = self.position[0]
		self.posV = self.position[1]
		self.angle = angle
		self.vel = vel

		# Load drone image
		self.drone_image = drone_image
		self.drone = pygame.image.load('Imagens/drone_resized.png')
		self.tamX = self.drone.get_size()[0]
		self.tamY = self.drone.get_size()[0]
		self.height = 0, 0

		# Get screen class
		self.screen = Screen(larg, alt, None)

		self.drone_rotated = self.drone
		self.drone_rotated_pos = self.position

	def resize_drone_image(self):
		# Resizing player image
		image = Image.open(drone_image)
		image = image.resize((100, 50))
		image.save('Imagens/drone_resized.png')

	def drone_rotate(self, position, angle):
		# Rotate drone
		self.drone_rotated = pygame.transform.rotate(self.drone, angle)
		# correcting drone's rotated position to the center of the drone's image
		self.height = self.drone_rotated.get_height() / 2
		self.drone_rotated_pos = (position[0] - self.drone_rotated.get_width() / 2, position[1] - self.height)

	def drone_update(self, position, angle):
		# Rotating drone
		self.drone_rotate(position, angle)

		# spawn drone
		self.screen.plot(self.drone_rotated, self.drone_rotated_pos)


class Drone_Control:

	def __init__(self, drone_image):
		# Movement, position and rotation parameters
		self.position = [500, 540]
		self.posH = self.position[0]
		self.posV = self.position[1]
		self.vel = 10
		self.angle = 0
		self.drone = Drone(self.position, self.angle, self.vel, drone_image)
		self.drone_rotated = self.drone.drone_rotated

		# Screen to Real coordinates
		self.real_pos = {'x': -(larg / 2 - self.posH), 'y': alt - 100 - self.posV}
		# Screen limits (The screen size minus the player size)
		self.xlim = larg - self.drone.tamX / 2
		self.ylim = alt - self.drone.tamY / 2
		self.keys = 0

		# Initializing control parameters
		self.w1 = 0
		self.w2 = 0
		self.v1 = 0
		self.v2 = 0
		self.ang_vel = 0
		self.x = np.array([self.w1, self.w2,
							self.real_pos['x'], self.real_pos['y'],
							self.v1, self.v2,
							self.angle * np.pi / 180.,
							self.ang_vel * np.pi / 180.])
		self.eP = np.array([1, 1])  # Position error
		self.ePhi = 2  # angle error

	def key_control(self):
		self.keys = pygame.key.get_pressed()
		self.real_pos = {'x': -(larg / 2 - self.posH), 'y': alt - 100 - self.posV}

		destiny_x, destiny_y = self.real_pos['x'], self.real_pos['y']
		if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
			destiny_x = self.real_pos['x'] - 100.0
		if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
			destiny_x = self.real_pos['x'] + 100.0
		if self.keys[pygame.K_UP] or self.keys[pygame.K_w]:
			destiny_y = self.real_pos['y'] + 100.0
		if self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]:
			destiny_y = self.real_pos['y'] - 100.0

		self.pid_control(destiny_x, destiny_y)

	def mouse_control(self, destiny_x, destiny_y):
		return self.pid_control(destiny_x, destiny_y)

	def pid_control(self, destiny_x, destiny_y):
		self.real_pos = {'x': -(larg / 2 - self.posH), 'y': alt - 100 - self.posV}
		self.eP = np.array([destiny_x - self.real_pos['x'], destiny_y - self.real_pos['y']])
		if np.abs(self.eP[0]) > 0.2 or np.abs(self.eP[1]) > 0.2 or np.abs(self.ePhi) > 0.1:
			self.x, self.eP, self.ePhi = execute_PID(self.x, [destiny_x, destiny_y], t)
			# Converting from real coordinate to screen coordinate
			self.posH, self.posV = self.x[2] + larg / 2, alt - 100 - self.x[3]

			# Updating state vector
			self.angle = self.x[6]*180/np.pi
			self.v1, self.v2 = self.x[4], self.x[5]
			self.w1, self.w2 = self.x[0], self.x[1]
			self.ang_vel = self.x[7]

			# Updating drone's pixel position and angle
			self.position = [self.posH, self.posV]
			self.drone.drone_update(self.position, self.angle)

			################ Printing drone's status
			global position_, angle_, velocidade
			position_ = (round(self.x[2], 2), round(self.x[3], 2))
			angle_ = self.angle
			velocidade = (round(self.v1, 2), round(self.v2, 2))
			return True

		else:
			self.real_pos = {'x': -(larg / 2 - self.posH), 'y': alt - 100 - self.posV}
			self.posH, self.posV = self.x[2] + larg / 2, alt - 100 - self.x[3]
			self.eP = np.array([destiny_x - self.real_pos['x'], destiny_y - self.real_pos['y']])
			self.drone.drone_update(self.position, self.angle)
			return False


class Game:
	
	def __init__(self, larg, alt, bg_image, drone_image):
		self.screen = Screen(larg, alt, bg_image)
		self.control = Drone_Control(drone_image)
		self.clock = pygame.time.Clock()
		self.ticks = 60
		self.exit = False
		
	def run(self):
		global t, FPS
		FPS = 600
		auto_move = False
		global mx_real, my_real
		mx_real, my_real = 0, 0
		while True:
			self.clock.tick(FPS)  # Game FPS
			t = self.clock.get_time() / 1000
			self.screen.update_screen()

			for event in pygame.event.get():
				# To quit the game
				if event.type == QUIT:
					pygame.quit()
					exit()
					
				if event.type == pygame.MOUSEBUTTONDOWN:
					auto_move = True
					# Get the destiny's position from mouse click
					mx, my = pygame.mouse.get_pos()
					# Transform the mouse click point in real coordinates
					mx_real, my_real = -(larg / 2 - mx), alt - 100 - my
					# print(mx_real, my_real)

			if auto_move:
				auto_move = self.control.mouse_control(mx_real, my_real)
			else:
				self.control.key_control()

			pygame.display.update()


if __name__ == '__main__':

	bg_image = 'Imagens/ghibli_background.jpg'
	drone_image = 'Imagens/drone.png'
	game = Game(larg, alt, bg_image, drone_image)
	game.run()
