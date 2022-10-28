#!/usr/bin/python3

import pygame
import colors
import random
import images

#start pygame
pygame.init()

#set display size
display_width = 800   
display_height = 600

game_display = pygame.display.set_mode((display_width,display_height))

#Title
pygame.display.set_caption('Snake Game')

#Set Game Icon
pygame.display.set_icon(images.icon)

#Time object to work with Frames each Second
clock = pygame.time.Clock()

#Frames per second
FPS = 15

#thickness
snake_thickness = 15
apple_thickness = 15

#snake movement direction
direction = 'right'

def pause():

	paused = True

	message_to_screen('Paused', colors.black, -100,50)
	message_to_screen('Press ESC to continue or Q to quit', colors.black, 0,20)
	pygame.display.update()

	while paused:
		
		#Player choices
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					paused = False

				elif event.key == pygame.K_q:
					pygame.quit()
					quit()
	
		clock.tick(10)


def score(score):
	#Print the numbers of apples you've eaten, on the left-top corner
	font = pygame.font.Font('PressStart2P-Regular.ttf',20)
	text = font.render('Score: '+ str(score), True, colors.black)
	game_display.blit(text, [0,0])


def start_screen():

	start = True

	#Draw background image
	game_display.blit(images.start_screen_background, [0,0])

	#Draw start screen
	#message_to_screen('Welcome to Snake Game',colors.green, -100,35)
	message_to_screen('The objective of the game is to eat apples', colors.black, -30,15)
	message_to_screen('The more apples you eat, the longer you get', colors.black, 0,15)
	message_to_screen('If you run into yourself, or the edges, you die!', colors.black, 30,15)
	message_to_screen('Press C to play, Q to quit or ESC to pause', colors.black, 120,15)
	pygame.display.update()

	while start:

		#Player choices
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					start = False

				if event.key == pygame.K_q:
					pygame.quit()
					quit()

		
		#set the FPS to 10
		clock.tick(10)


def snake(snake_thickness,snake_list):

	#Change the image according to the snake movement
	if direction == 'right': 
		head_image =  pygame.transform.rotate(images.snake_head_image,270)
		body_image = pygame.transform.rotate(images.snake_body_image,270)

	elif direction == 'left': 
		head_image =  pygame.transform.rotate(images.snake_head_image,90)
		body_image = pygame.transform.rotate(images.snake_body_image,90)

	elif direction == 'up': 
		head_image =  images.snake_head_image
		body_image = images.snake_body_image

	elif direction == 'down': 
		head_image =  pygame.transform.rotate(images.snake_head_image,180)
		body_image = pygame.transform.rotate(images.snake_body_image,180)

	#Draw Snake head
	head = game_display.blit(head_image, (snake_list[-1][0], snake_list[-1][1]))

	#Draw Snake body
	for XnY in snake_list[:-1]:
		game_display.blit(body_image, (XnY[0],XnY[1]))

	#Return the Snake head to know its location
	return head


def apple(apple_x,apple_y,apple_thickness):
	#Draw and return the aplle to know its location
	return game_display.blit(images.apple_image, (apple_x,apple_y))


def random_position_apple():
	#Draw the apple in a random position, but avoid crossing-over the screen
	apple_x = random.randrange(0,display_width-apple_thickness,apple_thickness)
	apple_y = random.randrange(0,display_height-apple_thickness,apple_thickness)

	return apple_x, apple_y


def message_to_screen(message,color,y_displace=0,font_size=20):

	#Set the font and the size
	font = pygame.font.Font('PressStart2P-Regular.ttf',font_size)
	#Write the message and set the color
	text = font.render(message,True,color)
	#Align the text as you wish
	text_rectangle = text.get_rect(center=(display_width/2,display_height/2  + y_displace)) 
	#Print the text in the screen
	game_display.blit(text, text_rectangle)


def game_over():

	#Draw game over screen
	message_to_screen("Game over",colors.red, -50, 50)
	message_to_screen("Press C to play again or Q to quit",colors.black, 50, 20)
	pygame.display.update()

	while True:
		
		#Player choices
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					#direction = 'right'
					game_loop()
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()

	
def game_loop():

	#Global variable in order to acess it from any function
	global direction	

	game_exit = False

	#Coordinates from the front of the Snake Head
	lead_x = display_width/2
	lead_y = display_height/2

	#Pixels added every frame to make the movement
	#Initialized with 10 in order to start the game with the snake moving slowing
	lead_x_change = 10
	lead_y_change = 0

	#Snake speed
	speed = snake_thickness

	#The snake is a list of same sized rectangles
	snake_list = []
	#Numbers of rectangles
	snake_lenght = 1

	#randomly positioning the apple in the display
	apple_x, apple_y = random_position_apple()

	while not game_exit:

		#Player actions in the game
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				game_exit = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					direction = 'left'
					lead_x_change = -speed
					lead_y_change = 0

				elif event.key == pygame.K_RIGHT:
					direction = 'right'
					lead_x_change = speed
					lead_y_change = 0

				elif event.key == pygame.K_UP:
					direction = 'up'
					lead_y_change = -speed
					lead_x_change = 0

				elif event.key == pygame.K_DOWN:
					direction = 'down'
					lead_y_change = speed
					lead_x_change = 0

				elif event.key == pygame.K_ESCAPE:
					pause()


		#If the snake crosses the display boundaries, it dies
		if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0 :
			direction = 'right'
			game_over()


		#Adding the Pixels to the coordinates
		lead_x += lead_x_change
		lead_y += lead_y_change

		#Draw background image
		game_display.blit(images.background_image, [0,0])

		#Add the Snake head to the Snake list
		snake_head = []
		snake_head.append(lead_x)
		snake_head.append(lead_y)
		snake_list.append(snake_head)

		if len(snake_list) > snake_lenght:
			del snake_list[0]

		#If the Snake hits its own body, it dies
		for each_segment in snake_list[:-1]:
			if each_segment == snake_head:
				direction = 'right'
				game_over()
				


		#Draw Snake
		Snake = snake(snake_thickness,snake_list)

		#Draw Apple
		Apple = apple(apple_x,apple_y,apple_thickness)

		#Draw Score
		score(snake_lenght-1)
		
		pygame.display.update()

		#If the Snake eats the Apple
		if Snake.colliderect(Apple):
			#Change randomly the Apple coordinates
			apple_x, apple_y = random_position_apple()
			#Grow the Snake by one rectangle
			snake_lenght += 1

		#Set frame rate per second in the Game
		clock.tick(FPS)

	pygame.quit()
	quit()

start_screen()
game_loop()