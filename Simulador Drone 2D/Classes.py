import pygame
from pygame.locals import *
from sys import exit
from PIL import Image
import math
from PID import execute_PID
import numpy as np

# Global Variables
larg = 1000.0
alt = 640.0


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
		# Boost control
		self.v_max = 18  # cm/s (1 px = 1 cm)
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
							self.real_pos['x'], self.real_pos['y'],
							self.v1, self.v2,
							self.angle * np.pi / 180.,
							self.ang_vel * np.pi / 180.])
		self.eP = np.array([1, 1])  # Position error
		self.ePhi = 2  # angle error

	def move(self):
		self.real_pos = {'x': -(larg / 2 - self.posH), 'y': alt - 100. - self.posV}
		# Gets the keys that are being pressed        
		self.keys = pygame.key.get_pressed()
		self.left_button()
		self.right_button()
		self.auto_stabilize()

		if self.steady:
			if not self.up_button() and not self.down_button():
				self.y_direction = 0

		self.acelerate()
		self.rotate()
		self.resulting_speed()
		
		self.position = [self.posH, self.posV]
		self.drone.drone_update(self.position, self.angle)

		self.x = np.array([self.w1, self.w2,
						self.real_pos['x'], self.real_pos['y'],
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

	def auto_stabilize(self):
		if self.keys[K_f]:
			self.steady = True
		if self.keys[K_g]:
			self.steady = False

	def rotate(self):
		if self.keys[pygame.K_q]:
			self.angle += 150/FPS

		if self.keys[pygame.K_e]:
			self.angle -= 150/FPS

		# Limit the max angle to 35°
		if self.angle >= 35:
			self.angle = 35
		if self.angle <= -35:
			self.angle = -35

		# Rotating drone
		self.drone_rotated = pygame.transform.rotate(self.drone.drone, self.angle)

	def acelerate(self):
		if self.keys[K_SPACE]:
			# boost control, hold space to activate drone boost
			self.F += 100 * t
			if self.F >= 155:
				self.F = 155
		else:
			# when space is released, the boost is slowly decreased
			self.F -= 100 * t
			if self.F <= 0:
				self.F = 0

	def resulting_speed(self):
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
				self.Fy += 50 * t
			if self.Fy > self.P:
				self.Fy -= 50 * t
			if self.P - 1 < self.Fy < self.P + 1:
				self.Fy = self.P

		ay = (self.Fy - self.P) / self.m
		ax = self.Fx / self.m

		vel_vertical = -ay * t + self.vel * self.y_direction * math.cos(self.angle * math.pi / 180)
		vel_horizontal = -ax * t - self.vel * math.sin(self.angle * math.pi / 180)

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
		self.eP = np.array([destiny_x - self.real_pos['x'], destiny_y - self.real_pos['y']])
		if np.abs(self.eP[0]) > 0.2 or np.abs(self.eP[1]) > 0.2 or np.abs(self.ePhi) > 0.1:
			self.x, self.eP, self.ePhi = execute_PID(self.x, [destiny_x, destiny_y], t)
			# Converting from real coordinate to screen coordinate
			self.posH, self.posV = self.x[2] + larg / 2, alt - 100 - self.x[3]

			self.angle = self.x[6]*180/np.pi
			self.v1, self.v2 = self.x[4], self.x[5]
			self.w1, self.w2 = self.x[0], self.x[1]
			self.ang_vel = self.x[7]

			self.position = [self.posH, self.posV]
			self.drone.drone_update(self.position, self.angle)
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
					# Get the destiny's position from mouse click
					auto_move = True
					mx, my = pygame.mouse.get_pos()
					mx_real, my_real = -(larg / 2 - mx), alt - 100 - my
					print(mx_real, my_real)

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