import pygame
from pygame.locals import *
from sys import exit
from PIL import Image
import math
from PID import execute_PID
import numpy as np


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
	def __init__(self, position, angle, vel, imagem_drone):
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

		self.ylim = tela.alt - self.tamY * 1.5

		self.drone_rotated = self.drone
		self.drone_rotated_pos = self.position

	def desenha_drone(self):
		# Resizing player image
		image = Image.open(imagem_drone)
		image = image.resize((100, 50))
		image.save('Imagens/drone_resized.png')

	def drone_rotate(self, position, angle):
		self.drone_rotated = pygame.transform.rotate(self.drone, angle)
		self.height = self.drone_rotated.get_height() / 2
		self.drone_rotated_pos = (position[0] - self.drone_rotated.get_width() / 2, position[1] - self.height)

	def drone_update(self, position, angle):
		# Load drone image
		self.drone = pygame.image.load('Imagens/drone_resized.png')
		# Rotating drone
		self.drone_rotate(position, angle)

		# Limit the ground border
		if self.posY >= self.ylim:
			position[1] = self.ylim
		if self.posY <= self.drone_rotated.get_height() / 2:
			position[1] = self.drone_rotated.get_height() / 2

		# spawn drone
		tela.plot(self.drone_rotated, self.drone_rotated_pos)
		

class Controle:
	def __init__(self):
		# Movement, position and rotation parameters
		self.position = [500, 540]
		self.posH = self.position[0]
		self.posV = self.position[1]
		self.vel = 10
		self.angle = 0
		self.drone = Drone(self.position, self.angle, self.vel, imagem_drone)
		self.drone_rotated = self.drone.drone_rotated
		# Screen limits (The screen size minus the player size)
		self.xlim = tela.larg - self.drone.tamX / 2
		self.ylim = tela.alt - self.drone.tamY / 2
		self.keys = 0
		# Boost control
		self.v_max = 18  # cm/s (1 px = 1 cm)
		self.t = 0
		self.vel_vertical = 0
		self.vel_horizontal = 0
		# Boost Impulse
		self.F = 0
		self.Fx = 0
		self.Fy = 0
		# Drone's weight
		self.m = 0.25
		self.g = 9.81
		self.P = self.m * self.g * 31
		# Auto gravity control
		self.steady = False
		self.y_direction = 0  # changes the y direction to + or - depending on the direction key pressed

		# Initializing control parameters
		self.w1 = 0
		self.w2 = 0
		self.v1 = 0
		self.v2 = 0
		self.ang_vel = 0
		self.x = np.array([self.w1, self.w2,
					  self.posH, self.posV,
					  self.v1, self.v2,
					  self.angle * np.pi / 180.,
					  self.ang_vel * np.pi / 180.])
		self.eP = np.array([1, 1])  # Position error
		self.ePhi = 2  # angle error

	def move(self):
		self.t = game.clock.get_time() / 1000
		# Gets the keys that are being pressed        
		self.keys = pygame.key.get_pressed()
		self.left_button()
		self.right_button()
		self.auto_stabilizar()

		if self.steady:
			if not self.up_button() and not self.down_button():
				self.y_direction = 0

		self.acelerar()
		self.rotacionar()
		self.velocidade_resultante()
		
		self.position = [self.posH, self.posV]
		self.drone.drone_update(self.position, self.angle)

		self.x = np.array([self.w1, self.w2,
						self.posH, self.posV,
						self.v1, self.v2,
						self.angle * np.pi / 180.,
						self.ang_vel * np.pi / 180.])

	def left_button(self):
		if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
			self.posH -= self.vel

	def right_button(self):
		if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
			self.posH += self.vel

	def up_button(self):
		if self.keys[pygame.K_UP] or self.keys[pygame.K_w]:
			self.y_direction = -1
			return True
		return False

	def down_button(self):
		if self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]:
			self.y_direction = 1
			return True
		return False

	def auto_stabilizar(self):
		if self.keys[K_f]:
			self.steady = True
		if self.keys[K_g]:
			self.steady = False

	def rotacionar(self):
		if self.keys[pygame.K_q]:
			self.angle += 5

		if self.keys[pygame.K_e]:
			self.angle -= 5

		# Limit the max angle to 35°
		if self.angle >= 35:
			self.angle = 35
		if self.angle <= -35:
			self.angle = -35

		# Rotating drone
		self.drone_rotated = pygame.transform.rotate(self.drone.drone, self.angle)

	def acelerar(self):
		if self.keys[K_SPACE]:
			# boost control, hold space to activate drone boost
			self.F += 100 * self.t
			if self.F >= 155:
				self.F = 155
		else:
			# when space is released, the boost is slowly decreased
			self.F -= 100 * self.t
			if self.F <= 0:
				self.F = 0

	def velocidade_resultante(self):
		# FORCE
		self.Fx = self.F * math.sin(self.angle * math.pi / 180)

		if not self.steady:
			self.Fy = self.F * math.cos(self.angle * math.pi / 180)
			self.vel -= 0.05
			if self.vel <= 0:
				self.vel = 0
		else:
			self.vel = 10
			if self.Fy < self.P:
				self.Fy += 50 * self.t
			if self.Fy > self.P:
				self.Fy -= 50 * self.t
			if self.P - 1 < self.Fy < self.P + 1:
				self.Fy = self.P

		ay = (self.Fy - self.P) / self.m
		ax = self.Fx / self.m

		vel_vertical = -ay * self.t + self.vel * self.y_direction * math.cos(self.angle * math.pi / 180)
		vel_horizontal = -ax * self.t - self.vel * math.sin(self.angle * math.pi / 180)

		if vel_vertical >= 10:
			vel_vertical = 10
		elif vel_vertical <= -10:
			vel_vertical = -10

		if vel_horizontal >= 10:
			vel_horizontal = 10
		elif vel_horizontal <= -10:
			vel_horizontal = -10

		self.posV += vel_vertical
		self.posH += vel_horizontal

		# Limit the ground border
		if self.posV >= self.ylim:
			self.posV = self.ylim
		if self.posV <= self.drone_rotated.get_height() / 2:
			self.posV = self.drone_rotated.get_height() / 2

		# Limit the left and right borders
		if self.posH >= self.xlim:
			self.posH = self.xlim
		if self.posH <= self.drone_rotated.get_width() / 2:
			self.posH = self.drone_rotated.get_width() / 2

	def mouse_control(self, mx, my):
		if np.abs(self.eP[0]) > 0.2 or np.abs(self.eP[1]) > 0.2 or np.abs(self.ePhi) > 1.0:
			self.x, self.eP, self.ePhi = execute_PID(self.x, [mx, my], t)
			self.posH, self.posV = self.x[2], self.x[3]
			self.angle = np.round(self.x[6]*180/np.pi)
			self.v1, self.v2 = self.x[4], self.x[5]
			self.w1, self.w2 = self.x[0], self.x[1]
			self.ang_vel = self.x[7]
			print(self.angle)
			self.position = [self.posH, self.posV]
			#print(self.position)
			self.drone.drone_update(self.position, self.angle)
			return True
		return False


class Game:
	
	def __init__(self):
		self.clock = pygame.time.Clock()
		self.ticks = 60
		self.exit = False
		
	def run(self):
		global t
		auto_move = False
		mx, my = 0, 0
		while True:
			self.clock.tick(60)  # Game FPS
			t = game.clock.get_time() / 1000
			tela.update_tela()

			for event in pygame.event.get():
				# To quit the game
				if event.type == QUIT:
					pygame.quit()
					exit()
					
				if event.type == pygame.MOUSEBUTTONDOWN:
					auto_move = True
					mx, my = pygame.mouse.get_pos()
					print(mx, my)

			if auto_move:
				auto_move = controle.mouse_control(mx, my)
			else:
				controle.move()
			pygame.display.update()


if __name__ == '__main__':

	imagem_fundo = 'Imagens/ghibli_background.jpg'
	imagem_drone = 'Imagens/drone.png'
	tela = Tela(1000,640,imagem_fundo)
	controle = Controle()
	drone = Drone(controle.position, controle.angle, controle.vel, imagem_drone)
	
	game = Game()
	game.run()




    


