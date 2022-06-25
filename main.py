
import pygame
import random
 
pygame.init()
pygame.mixer.init()

fondo = pygame.image.load('imagenes/ciudad.png')
fondo2 = pygame.image.load('imagenes/dirty.png')
cami_sonido = pygame.mixer.Sound('cami.wav')
lanzar_sonido = pygame.mixer.Sound('lanzarr.wav')
romper_sonido = pygame.mixer.Sound('roto.wav')
golpe_sonido = pygame.mixer.Sound('dolor.wav')
pygame.mixer.music.load("musica.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

particulas_list = []
for i in range(1,11):
	particulas = pygame.image.load(f'particulas/{i}.png')
	particulas_list.append(particulas)

sangre_list = []
for i in range(1,23):
	sangre = pygame.image.load(f'sangre/{i}.png')
	sangre_list.append(sangre)
	
width = fondo.get_width()
height = fondo.get_height()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Dirty Town')
run = True
fps = 60
clock = pygame.time.Clock()
score = 0
vida = 100
blanco = (255,255,255)
negro = (0,0,0)

def texto_puntuacion(frame, text, size, x,y):
	font = pygame.font.SysFont('Small Fonts', size, bold=True)
	text_frame = font.render(text, True, blanco,negro)
	text_rect = text_frame.get_rect()
	text_rect.midtop = (x,y)
	frame.blit(text_frame, text_rect)
def texto_portada(frame, text, size, x,y):
	font = pygame.font.SysFont('Small Fonts', size, bold=True)
	text_frame = font.render(text, True, blanco)
	text_rect = text_frame.get_rect()
	text_rect.midtop = (x,y)
	frame.blit(text_frame, text_rect)

def barra_vida(frame, x,y, nivel):
	longitud = 100
	alto = 20
	fill = int((nivel/100)*longitud)
	border = pygame.Rect(x,y, longitud, alto)
	fill = pygame.Rect(x,y,fill, alto)
	pygame.draw.rect(frame, (255,0,55),fill)
	pygame.draw.rect(frame, negro, border,4)

class Jugador(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('imagenes/A1.png').convert_alpha()
		pygame.display.set_icon(self.image)
		self.rect = self.image.get_rect()
		self.rect.centerx = width//2
		self.rect.centery = height-50
		self.velocidad_x = 0
		self.vida = 100

	def update(self):
		self.velocidad_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.velocidad_x = -5
		elif keystate[pygame.K_RIGHT]:
			self.velocidad_x = 5

		self.rect.x += self.velocidad_x
		if self.rect.right > width:
			self.rect.right = width
		elif self.rect.left < 0:
			self.rect.left = 0

	def disparar(self):
		bala = Balas(self.rect.centerx, self.rect.top)
		grupo_jugador.add(bala)
		grupo_balas_jugador.add(bala)
		cami_sonido.play()

class Enemigos(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load('imagenes/E1.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(1, width-50)
		self.rect.y = 100
		self.velocidad_y = random.randrange(-1,20)

	def update(self):
		self.time = random.randrange(-1, pygame.time.get_ticks()//5000)
		self.rect.x += self.time
		if self.rect.x >= width:
			self.rect.x = 0
			self.rect.y += 50

	def disparar_enemigos(self):
		bala = Balas_enemigos(self.rect.centerx, self.rect.bottom)
		grupo_jugador.add(bala)
		grupo_balas_enemigos.add(bala)
		lanzar_sonido.play()

class Balas(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load('imagenes/B2.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.y = y
		self.velocidad = -18

	def update(self):
		self.rect.y +=  self.velocidad
		if self.rect.bottom <0:
			self.kill()

class Balas_enemigos(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load('imagenes/B1.png').convert_alpha()
		self.image = pygame.transform.rotate(self.image, 180)
		self.rect = self.image.get_rect()
		self.rect.centerx = x 
		self.rect.y = random.randrange(10, width)
		self.velocidad_y = 4

	def update(self):
		self.rect.y +=  self.velocidad_y 
		if self.rect.bottom > height:
			self.kill()

class Particulas(pygame.sprite.Sprite):
	def __init__(self, position):
		super().__init__()
		self.image = particulas_list[0]	
		img_scala = pygame.transform.scale(self.image, (20,20))	
		self.rect = img_scala.get_rect()
		self.rect.center = position
		self.time = pygame.time.get_ticks()
		self.velocidad_explo = 30
		self.frames = 0 
		
	def update(self):
		tiempo = pygame.time.get_ticks()
		if tiempo - self.time > self.velocidad_explo:
			self.time = tiempo 
			self.frames+=1
			if self.frames == len(particulas_list):
				self.kill()
			else:
				position = self.rect.center
				self.image = particulas_list[self.frames]
				self.rect = self.image.get_rect()
				self.rect.center = position

class Sangre(pygame.sprite.Sprite):
	def __init__(self, position):
		super().__init__()
		self.image = particulas_list[0]	
		img_scala = pygame.transform.scale(self.image, (20,20))	
		self.rect = img_scala.get_rect()
		self.rect.center = position
		self.time = pygame.time.get_ticks()
		self.velocidad_explo = 30
		self.frames = 0 
		
	def update(self):
		tiempo = pygame.time.get_ticks()
		if tiempo - self.time > self.velocidad_explo:
			self.time = tiempo 
			self.frames+=1
			if self.frames == len(particulas_list):
				self.kill()
			else:
				position = self.rect.center
				self.image = particulas_list[self.frames]
				self.rect = self.image.get_rect()
				self.rect.center = position
def show_go_screen():
	window.blit(fondo2, (0, 0))
	texto_portada(window, "DIRTY TOWN", 65, width // 2, height / 4)
	texto_portada(window, "(Instrucciones)", 27, width // 2, height // 2)
	texto_puntuacion(window, "Presiona cualquier tecla...", 17, width // 2, height * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(fps)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False


game_over = True

while run:
	if game_over:
		show_go_screen()
		game_over = False
		grupo_jugador = pygame.sprite.Group()
		grupo_enemigos = pygame.sprite.Group()
		grupo_balas_jugador = pygame.sprite.Group()
		grupo_balas_enemigos = pygame.sprite.Group()

		player = Jugador()
		grupo_jugador.add(player)
		grupo_balas_jugador.add(player)

		for x in range(10):
			enemigo = Enemigos(10,10)
			grupo_enemigos.add(enemigo)
			grupo_jugador.add(enemigo)
	clock.tick(fps)
	window.blit(fondo, (0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.disparar()

	grupo_jugador.update()
	grupo_enemigos.update()
	grupo_balas_jugador.update()
	grupo_balas_enemigos.update() 

	grupo_jugador.draw(window)

    # Coliciones  balas_jugador -  enemigo
	colicion1 = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador,True,True)
	for i in colicion1:	
		score+=10
		enemigo.disparar_enemigos()
		enemigo = Enemigos(300,10)
		grupo_enemigos.add(enemigo)
		grupo_jugador.add(enemigo)

		explo = Particulas(i.rect.center)
		grupo_jugador.add(explo)
		romper_sonido.set_volume(0.3)		
		romper_sonido.play()

    # Coliciones  jugador - balas_enemigo 
	colicion2 = pygame.sprite.spritecollide(player, grupo_balas_enemigos, True)
	for j in colicion2:
		player.vida -= 10
		if player.vida <=0:
			game_over = True
		explo1 = Sangre(j.rect.center)
		grupo_jugador.add(explo1)
		golpe_sonido.play()  

    # Coliciones  jugador - enemigo
	hits =pygame.sprite.spritecollide(player, grupo_enemigos , False)
	for hit in hits:
		player.vida -= 100 
		enemigos = Enemigos(10,10)
		grupo_jugador.add(enemigos)
		grupo_enemigos.add(enemigos)		
		if player.vida <=0:
			game_over = True

	# Indicador y Score
	texto_puntuacion(window, ('  SCORE: '+ str(score)+'       '), 30, width-85, 2)
	barra_vida(window, width-285, 0, player.vida)

	pygame.display.flip()
pygame.quit()
