# code a space runner game in pygame
import pygame
import random
import os
import sys

pygame.mixer.init()
x = pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Game window of game
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game related images
Image = {
	"spaceship" : "media/spaceship.png",
	"Intro_background" : "media/background.jpg",
	"block":"media/block.png",
	"Game_background": "media/game_bg.png",
	"Game_background2":"media/game_bg2.png"
}

# Game related sound effects
Sound = {
	"woosh" : "media/woosh.mp3",
}

# Game related settings
clock = pygame.time.Clock()	

# Background Image intro
Intro_bg = pygame.image.load(Image["Intro_background"])
Intro_bg = pygame.transform.scale(Intro_bg, (screen_width, screen_height)).convert_alpha()

# Game title & icon ,spaceship
def Spaceship(size1,size2):
	spaceship = pygame.image.load(Image["spaceship"])
	spaceship = pygame.transform.scale(spaceship,(size1, size2)).convert_alpha()
	return spaceship 

pygame.display.set_caption("Space Runner")
pygame.display.set_icon(Spaceship(20,20))
pygame.display.update()

# gameplay background
game_bg = pygame.image.load(Image["Game_background"])
game_bg = pygame.transform.scale(game_bg, (screen_width, screen_height)).convert_alpha()

# Asteroid or Block image
def Block(size1,size2):
	block = pygame.image.load(Image["block"])
	block = pygame.transform.scale(block, (size1, size2)).convert_alpha()
	return block

# Game specific variables
exit_game = False
game_over = False
spaceship_x = 413
spaceship_y = 488
velocity_x = 0
velocity_y = 0
fps = 60

# Display text on screen
def text_screen(text, color, x, y, font_size):
	font = pygame.font.SysFont('timesnewroman',font_size)
	screen_text = font.render(text,True,color)
	gameWindow.blit(screen_text, [x,y])

# plotting blocks
def Plot_blocks(block_x,block_y):
	gameWindow.blit(Block(70,70), (block_x,block_y))

# Game related functions
def welcome_screen():
	global exit_game
	global fps
	while not exit_game:
		
		# showing intro with space and blocks
		gameWindow.fill((233,210,229))
		gameWindow.blit(Intro_bg, (0, 0))
		gameWindow.blit(Spaceship(400,400), (250,126))
		gameWindow.blit(Block(100,100), (210, 150))
		gameWindow.blit(Block(100,100), (232, 376)) 
		gameWindow.blit(Block(100,100), (124, 280))
		gameWindow.blit(Block(100,100), (698, 188))
		gameWindow.blit(Block(100,100), (658, 394))

		# Implement button to play game
		pygame.draw.rect(gameWindow,green, [340, screen_height/2, 220, 80], 4,4,4,4)
		text_screen("Play", white, 380, 290, 79)
		text_screen("SPACE RUNNER", white, 150, 30, 79)
		mouse_pos = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if 340<mouse_pos[0]<340+220 and 300<mouse_pos[1]<300+80:
			pygame.draw.rect(gameWindow,red, [340, screen_height/2, 220, 80], 6,6,6,6)
			if click==(1,0,0) or click==(0,0,1):
				gameloop()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit_game = True

			# A cheatsheet to begin the game
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					gameloop()
		pygame.display.flip()
		clock.tick(fps)
	pygame.quit()
	sys.exit()

# Game over
def Game_over():
	pass

# Creating a game loop
def gameloop():
	global exit_game
	global spaceship_x
	global spaceship_y
	global velocity_x
	global velocity_y
	global fps

	paused = False
	spaceship_width =53
	spaceship_height =85
	block_width = 35
	block_height = 40
	block_x = random.randint(20, screen_width)
	block_y = random.randint(20, 152)

	score = 0

	# Check if high score file exits.
	if not os.path.exists("high_score.txt"):
		with open("high_score.txt", "w") as f:
			f.write("0")

	with open("high_score.txt", "r") as f:
		high_scr = f.read()

	# Beginning the Game
	while not exit_game:		
		for event in pygame.event.get():
			# print(event)
			if event.type == pygame.QUIT:
				exit_game = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					paused = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					paused = False

			# pause functionality
			if not paused:
				if event.type == pygame.KEYDOWN:				
					if event.key == pygame.K_RIGHT:
						# print("You have presses right arrow key")
						spaceship_x = spaceship_x+10
						velocity_x = 5.7
						velocity_y = 0

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 3: 
						spaceship_x = spaceship_x+10
						velocity_x = 5.7
						velocity_y = 0

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						# print("You have presses right arrow key")
						spaceship_x = spaceship_x-10
						velocity_x = -5.7
						velocity_y = 0

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1: 
						spaceship_x = spaceship_x-10
						velocity_x = -5.7
						velocity_y = 0				

		# Pause functionality
		if not paused:
			spaceship_x = spaceship_x + velocity_x
			spaceship_y = spaceship_y +velocity_y


			# Game over logic after gamewindow collision
			if spaceship_x<-32 or spaceship_x>840:
				velocity_x = 0
				spaceship_x = 413
				text_screen("Game Over Score: "+str(score), white, 150, 226, 70)
				pygame.display.flip()
				pygame.time.wait(3000)
				welcome_screen()      
			# print(pygame.mouse.get_pos())

			gameWindow.fill((233,210,229))
			gameWindow.blit(game_bg, (0,0))
			gameWindow.blit(Spaceship(100,100), (spaceship_x,spaceship_y))
			block_y = block_y + 15
			block_x = block_x
			Plot_blocks(block_x,block_y)

			# Game over logic after collision with blocks
			if spaceship_x < block_x + block_width and spaceship_x + spaceship_width > block_x and spaceship_y < block_y + block_height and spaceship_y + spaceship_height > block_y:
				velocity_x =0
				spaceship_x = 413
				text_screen("Game Over Score: "+str(score), white, 150, 226, 70)
				pygame.display.flip()
				pygame.time.wait(3000)
				welcome_screen()

			# Update score and loading another block and playing sound effects
			if block_y > 550:
				# pygame.mixer.music.load(Sound["woosh"])
				# pygame.mixer.music.play()
				score+=4
				if score>int(high_scr):
					high_scr = score
					with open("high_score.txt", "w") as f:
						f.write(str(high_scr))
	               
				block_x = random.randint(20, screen_width)
				block_y = random.randint(20, 152)
				Plot_blocks(block_x,block_y)

			text_screen("Score: " + str(score) + "    High Score: "+str(high_scr), white, 5, 5, 40)		
			pygame.display.update()
			clock.tick(fps)
	pygame.quit()
	sys.exit()

# Starting welcome screen
if __name__ == '__main__':
	welcome_screen()