import pygame
import time
from os import path
import random

# Estabelece a pasta que contem as figuras e sons.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Dados gerais do jogo.
WIDTH = 600 # Largura da tela
HEIGHT = 800 # Altura da tela
FPS = 80 # Frames por segundo
# Importando as informações iniciais
from init import img_dir, snd_dir, BLACK, WIDTH, HEIGHT, FPS, WHITE

# Importando arquivo do carrinho
from player import Player

# Importando arquivo dos outros carrinhos
from mob import Mob      
            
# Importando arquivo dos tiros
# from bullet import Bullet

# Importanto arquivo do outro tiro
from bullet2 import Bullet2

# Importando arquivo da classe
from coin import Coin

# Importando arquivo da classe box
from misterybox import Box

# Importando arquivo dos flocos de neve
from floco import Floco

# Importando arquivo da nevasca
from nevasca import Nevasca

# Carrega todos os assets de uma vez só
def load_assets(img_dir, snd_dir):
    assets = {}
    assets["player_img"] = pygame.image.load(path.join(img_dir, "Carrinhonovo.png")).convert()
    assets["mob_img"] = pygame.image.load(path.join(img_dir, "Carrinhonovo.png")).convert()
    assets["bullet_img"] = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
    assets["bullet2_img"] = pygame.image.load(path.join(img_dir, "laserBlue16.png")).convert()
    assets["flocos_img"] = pygame.image.load(path.join(img_dir, "floco_de_neve.png")).convert()
    assets["box_img"] = pygame.image.load(path.join(img_dir, "misterybox.png")).convert()
    assets["boom_sound"] = pygame.mixer.Sound(path.join(snd_dir, "expl3.wav"))
    assets["destroy_sound"] = pygame.mixer.Sound(path.join(snd_dir, "expl6.wav"))
    assets["pew_sound"] = pygame.mixer.Sound(path.join(snd_dir, "pew.wav"))
    return assets

# Inicialização do Pygame.
pygame.init() 
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("SpeedRetro")

# Carrega todos os assets uma vez só e guarda em um dicionário
assets = load_assets(img_dir, snd_dir)

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'screen-3.png')).convert()
background_rect = background.get_rect()
background_rect_cima = background.get_rect()
background_rect_cima.y = -HEIGHT

# Carrega os sons do jogo
pygame.mixer.music.load(path.join(snd_dir, 'joguito.mp3'))
pygame.mixer.music.set_volume(1) #Som da música de cima
boom_sound = assets['boom_sound']
destroy_sound = assets['destroy_sound']
pew_sound = assets['pew_sound']
Ta_Da = pygame.mixer.Sound(path.join(snd_dir, 'ta_da.wav'))

# Cria um carrinho. O construtor será chamado automaticamente.
player = Player(assets["player_img"])

# Cria um grupo de todos os sprites e adiciona a nave.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Cria um grupo só dos meteoros
mobs = pygame.sprite.Group()

# Cria um grupo para tiros (vermelho)
bullets = pygame.sprite.Group()
# Grupo para o segundo tiro (azul)
bullet2 = pygame.sprite.Group()
bullets.add(bullet2)

# Cria um grupo para as caixar
box = pygame.sprite.Group()

#Cria grupo para os flocos
flocos = pygame.sprite.Group()
    
x = 0
y = 0
# Cria carrinhos e adiciona no grupo mobs
for i in range(0):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
#Cria grupo das moedas
imagem_coin=[]
for i in range(9):
    filename = 'Gold_0{}.png'.format(i)
    Coin_img = pygame.image.load(path.join(img_dir, filename)).convert()
    Coin_img = pygame.transform.scale(Coin_img, (30, 35))        
    Coin_img.set_colorkey(WHITE)
    imagem_coin.append(Coin_img)

coin = pygame.sprite.Group()

#Cria 2 moedas
for i in range(1):
    c = Coin(imagem_coin)
    all_sprites.add(c)
    coin.add(c)
    
#Cria a box
misterybox = pygame.sprite.Group()
for i in range(1):
    b = Box(assets["box_img"])
    all_sprites.add(b)
    misterybox.add(b)


# Cria o floco de neve
for i in range(1):
    b = Floco(assets["flocos_img"])
    all_sprites.add(b)
    flocos.add(b)    

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
                    player.speedx = -5
                if event.key == pygame.K_RIGHT:
                    player.speedx = 5
                # Se for um espaço atira!
                if event.key == pygame.K_SPACE:
                    bullet = Bullet2(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    pew_sound.play()
                    
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                if event.key  == pygame.K_RIGHT:
                    player.speedx = 0
                    
        # Verifica se jogador encostou a parede
        if player.rect.right > 519:
            running = False
        if player.rect.left < 85:
            running = False    
        
        
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite.
        all_sprites.update()
        
        # Verifica se houve colisão entre tiro e carrinhos
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits: # Pode haver mais de um
            # O carrinho é destruido e precisa ser recriado
            destroy_sound.play()
            m = Mob() 
            all_sprites.add(m)
            mobs.add(m) 
        
        # Verifica se houve colisão entre os carrinhos
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            # Toca o som da colisão
            boom_sound.play()
            time.sleep(1) # Precisa esperar senão fecha
            running = False
        
        # Verifica se houve colisão com a moeda
#        hits = pygame.sprite.spritecollide(player, coin, False, pygame.sprite.collide_circle)
#        for hit in hits:
#            c = Coin(imagem_coin)
#            all_sprites.add(c)
#            coin.add(c)
          
        # Verifica se houve colisão com o misterybox
        hits = pygame.sprite.spritecollide(player, misterybox, False, False)
        for hit in hits:
            # Toca o som da colisão
            Ta_Da.play()
            time.sleep(0) # Precisa esperar senão fecha
            all_sprites.add(b)
            misterybox.add(b)
            running = True
            
        # Verifica se houve colisão entre player e floco de neve
        hits = pygame.sprite.spritecollide(player, flocos, False, False)
        if hits:
            nevasca=pygame.sprite.Group()
            for i in range(2):
                b = Nevasca(assets["flocos_img"])
                all_sprites.add(b)
                flocos.add(b)
                player.speedx=1  
        
        
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)     
        background_rect_cima.y += 10
        background_rect.y += 10
        screen.blit(background, background_rect_cima)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)

        if background_rect.y >= HEIGHT:
            background_rect.y = 0
            background_rect_cima.y = -HEIGHT
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    
    pygame.quit()
    

