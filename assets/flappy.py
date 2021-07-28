import  pygame, sys, random 

pygame.init()
screen = pygame.display.set_mode((432,768))

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()




pygame.quit()