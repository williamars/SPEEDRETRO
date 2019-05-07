# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
import random
import time
from os import path

# Estabelece a pasta que contem as figuras e sons.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Dados gerais do jogo.
WIDTH = 480 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Classe Jogador que representa a nave
class Player(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
        self.image = player_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (50, 38))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Centraliza embaixo da tela.
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        
        # Velocidade da nave
        self.speedx = 0
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = 25
    
    # Metodo que atualiza a posição da navinha
    def update(self):
        self.rect.x += self.speedx
        
        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
                    
# Classe Mob que representa os meteoros
class Mob(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        mob_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (50, 38))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(-100, -40)
        # Sorteia uma velocidade inicial
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 9)
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85 / 2)
        
    # Metodo que atualiza a posição da navinha
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        # Se o meteoro passar do final da tela, volta para cima
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 9)
            
# Classe Bullet que representa os tiros
class Bullet(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
        self.image = bullet_img
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    # Metodo que atualiza a posição da navinha
    def update(self):
        self.rect.y += self.speedy
        
        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Navinha")

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()

# Carrega os sons do jogo
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)
boom_sound = pygame.mixer.Sound(path.join(snd_dir, 'expl3.wav'))
destroy_sound = pygame.mixer.Sound(path.join(snd_dir, 'expl6.wav'))
pew_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))

# Cria uma nave. O construtor será chamado automaticamente.
player = Player()

# Cria um grupo de todos os sprites e adiciona a nave.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Cria um grupo só dos meteoros
mobs = pygame.sprite.Group()

# Cria um grupo para tiros
bullets = pygame.sprite.Group()

# Cria 8 meteoros e adiciona no grupo meteoros
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Comando para evitar travamentos.
try:
    
    # Loop principal.
    pygame.mixer.music.play(loops=-1)
    running = True
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                running = False
            
            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
                # Se for um espaço atira!
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    pew_sound.play()
                    
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
                    
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite.
        all_sprites.update()
        
        # Verifica se houve colisão entre tiro e meteoro
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits: # Pode haver mais de um
            # O meteoro e destruido e precisa ser recriado
            destroy_sound.play()
            m = Mob() 
            all_sprites.add(m)
            mobs.add(m)
        
        # Verifica se houve colisão entre nave e meteoro
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            # Toca o som da colisão
            boom_sound.play()
            time.sleep(1) # Precisa esperar senão fecha
            
            running = False
    
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    
    pygame.quit()
