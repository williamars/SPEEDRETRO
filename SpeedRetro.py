import pygame
import time
from os import path
import os
import random
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

# Estabelece a pasta que contem as figuras e sons.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
fnt_dir = path.join(path.dirname(__file__), 'font')

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
def load_assets(img_dir, snd_dir, fnt_dir):
    assets = {}
    assets["player_img"] = pygame.image.load(path.join(img_dir, "Carrinhonovo.png")).convert()
    assets["mob_img"] = pygame.image.load(path.join(img_dir, "Carrinhonovo.png")).convert()
    assets["bullet_img"] = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
    assets["bullet2_img"] = pygame.image.load(path.join(img_dir, "laserBlue16.png")).convert()
    assets["flocos_img"] = pygame.image.load(path.join(img_dir, "floco_de_neve.png")).convert()
    assets["flocos2_img"] = pygame.image.load(path.join(img_dir, "neve.png")).convert()
    assets["box_img"] = pygame.image.load(path.join(img_dir, "misterybox.png")).convert()
    assets["boom_sound"] = pygame.mixer.Sound(path.join(snd_dir, "expl3.wav"))
    assets["destroy_sound"] = pygame.mixer.Sound(path.join(snd_dir, "expl6.wav"))
    assets["pew_sound"] = pygame.mixer.Sound(path.join(snd_dir, "pew.wav"))
    assets["score_font"] = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 35)
    return assets

# Inicialização do Pygame.
pygame.init() 
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("SpeedRetro")

# Carrega todos os assets uma vez só e guarda em um dicionário
assets = load_assets(img_dir, snd_dir, fnt_dir)

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

# Carrega a fonte para desenhar o score.
score_font = assets["score_font"]

# Cria um grupo de todos os sprites e adiciona a nave.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Cria um grupo só dos carrinhos inimigos
mobs = pygame.sprite.Group()

# Cria um grupo para tiros (vermelho)
bullets = pygame.sprite.Group()
# Grupo para o segundo tiro (azul)
bullet2 = pygame.sprite.Group()
bullets.add(bullet2)

coin = pygame.sprite.Group()

# Cria um grupo para as caixas
box = pygame.sprite.Group()

#Cria grupo para os flocos
flocos = pygame.sprite.Group()

# Cria carrinhos e adiciona no grupo mobs
for i in range(5):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    z=random.randrange(0,10)
    #

    
#Cria grupo das moedas
imagem_coin=[]
for i in range(9):
    filename = 'Gold_0{}.png'.format(i)
    Coin_img = pygame.image.load(path.join(img_dir, filename)).convert()
    Coin_img = pygame.transform.scale(Coin_img, (30, 35))        
    Coin_img.set_colorkey(WHITE)
    imagem_coin.append(Coin_img)

#Cria moedas
for i in range(1):
    c = Coin(imagem_coin)
    all_sprites.add(c)
    coin.add(c)
    
#Cria a box
misterybox = pygame.sprite.Group()

# Cria o floco de neve  
for i in range(1):
    f = Floco(assets["flocos_img"])
    all_sprites.add(f)
    flocos.add(f)
    
estanevando = False
speedx = 0


timee=0

# Comando para evitar travamentos.
try:
    
    # Loop principal.
    pygame.mixer.music.play(loops=-1)
    running = True
    score = 0
    while running: 
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        if random.randrange(1,200) == 1:
            b = Box(assets["box_img"])
            all_sprites.add(b)
            misterybox.add(b)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                running = False
            
            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera a velocidade.
                fator = 0
                if estanevando:
                    fator = 2
                if event.key == pygame.K_LEFT:
                    speedx = -5 + fator
                if event.key == pygame.K_RIGHT:
                    speedx = 5 + fator
                # Se for um espaço atira!
                if event.key == pygame.K_SPACE:
                    bullet = Bullet2(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    pew_sound.play()
                    
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                fator = 0
                if estanevando:
                    fator = 2
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    speedx = fator
                if event.key  == pygame.K_RIGHT:
                    speedx = fator
                    
        player.speedx = speedx
                    
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
        hits = pygame.sprite.spritecollide(player, coin, True, False)
        for hit in hits:
            score += 1
          
        # Verifica se houve colisão com o misterybox
        hits = pygame.sprite.spritecollide(player, misterybox, True, False)
        for hit in hits:
            # Toca o som da colisão
            Ta_Da.play()
            score += 1
            
        # Verifica se houve colisão entre player e floco de neve
        hits = pygame.sprite.spritecollide(player, flocos, False, False)
        if hits:


            nevasca=pygame.sprite.Group()
            for i in range(1):
                b = Nevasca(assets["flocos_img"])
                all_sprites.add(b)
                flocos.add(b)
                player.speedx=1  
        
        


            estanevando = True
            speedx = 1
            nevasca = pygame.sprite.Group()
            for i in range(30):
                n = Nevasca(assets["flocos2_img"])
                all_sprites.add(n)

#            contador=0
#            if contador == 10:
#                estanevando=False
#                player.speedx=0
#            if contador < 10:
#                contador += 1
#        else:
#            estanevando=False
            
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
            
        # Desenha o score
        text_surface = score_font.render("{:01d}".format(score), True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH-125,  10)
        screen.blit(text_surface, text_rect)

        
        # Desenha o score, por tempo
        timee+=1
         # Run game
        pont=timee//FPS
        text_surface = score_font.render("{:04d}".format(pont), True, BLACK)
        
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH-300,  10)
        screen.blit(text_surface, text_rect)
        

        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    
    pygame.quit()
    

