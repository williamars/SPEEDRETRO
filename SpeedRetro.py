import pygame
import time
from os import path
import os
import random
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Importando as informações iniciais
from init import img_dir, snd_dir, fnt_dir, BLACK, WIDTH, HEIGHT, FPS, WHITE

# Importando todas as classes
from classes import Player, Mob, Box, Bullet2, Coin, Nevasca, Floco, Laser 
        
# Carrega todos os assets de uma vez só
def load_assets(img_dir, snd_dir, fnt_dir):
    assets = {}
    assets["player_img"] = pygame.image.load(path.join(img_dir, "Carrinhonovo.png")).convert()
    assets["mob_img"] = pygame.image.load(path.join(img_dir, "Carrinhonovo.png")).convert()
    assets["bullet2_img"] = pygame.image.load(path.join(img_dir, "laserBlue16.png")).convert()
    assets["flocos_img"] = pygame.image.load(path.join(img_dir, "floco_de_neve.png")).convert()
    assets["flocos2_img"] = pygame.image.load(path.join(img_dir, "neve.png")).convert()
    assets["box_img"] = pygame.image.load(path.join(img_dir, "misterybox.png")).convert()
    assets["boom_sound"] = pygame.mixer.Sound(path.join(snd_dir, "crash.wav"))
    assets["moeda_sound"] = pygame.mixer.Sound(path.join(snd_dir, "m.wav"))
    assets["destroy_sound"] = pygame.mixer.Sound(path.join(snd_dir, "expl6.wav"))
    assets["pew_sound"] = pygame.mixer.Sound(path.join(snd_dir, "pew.wav"))
    assets["score_font"] = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 35)
    return assets

# Função que coloca a imagem no início do jogo
def init_screen(screen):

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(img_dir, 'Backgroundtime.png')).convert()
    background_rect = background.get_rect()

    running = True
    while running:
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

            if event.type == pygame.KEYUP:
                a = main()
                running = False
                    
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return a


# Função principal do jogo, onde tem todas as ações
def main():    
            
            estanevando = False
            estanevando_tempo = 0
            speedx = 0
            timee=0
            clock.tick(FPS)
            # Loop principal.
            pygame.mixer.music.play(loops=-1)
            running = True
            score = 0
            while running:
            
            # Ajusta a velocidade do jogo.
                clock.tick(FPS)

                estanevando_tempo -= 1
                if estanevando_tempo == 1:
                    estanevando_tempo = 0
                    speedx = 0
                    estanevando = False
        
                if random.randrange(1, 900) == 1:
                    b = Box(assets["box_img"])
                    all_sprites.add(b)
                    misterybox.add(b)
                
                if random.randrange(1,500) == 5:
                    c = Coin(imagem_coin)
                    all_sprites.add(c)
                    coin.add(c)
        
                # Processa os eventos (mouse, teclado, botão, etc).
                for event in pygame.event.get():
                    
                    # Verifica se foi fechado.
                    if event.type == pygame.QUIT:
                        running = False
                    
                    # Verifica se apertou alguma tecla.
                    if event.type == pygame.KEYDOWN:
                        # Dependendo da tecla, altera a velocidade.
                        fator = 0
                        if estanevando or estanevando_tempo > 0:
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
                            
                        if event.key == pygame.K_LCTRL:
                            laserr = Laser(player.rect.centerx, player.rect.top)
                            all_sprites.add(laserr)
                            laser.add(laserr)
                            pew_sound.play()
                            
                            
                    # Verifica se soltou alguma tecla.
                    if event.type == pygame.KEYUP:
                        fator = 0
                        if estanevando or estanevando_tempo > 0:
                            fator = 2
                        # Dependendo da nevasca, altera a velocidade.
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
                    
                # Verifica se houve colisão entre Laser e carrinhos
                hits = pygame.sprite.groupcollide(mobs, laser, True, True)
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
                    moeda.play()
                    score += 1
                  
                # Verifica se houve colisão com o misterybox
                hits = pygame.sprite.spritecollide(player, misterybox, True, False)
                for hit in hits:
                    # Toca o som da colisão
                    Ta_Da.play()
                    score += 1
                    
                # Verifica se houve colisão entre player e floco de neve
                hits = pygame.sprite.spritecollide(player, flocos, True, False)
                if hits:
                    estanevando = True
                    estanevando_tempo = 120
                    speedx = 1
                    for i in range(30):
                        n = Nevasca(assets["flocos2_img"])
                        all_sprites.add(n)
                    chama_floco()
                    
                # A cada loop, redesenha o fundo e os sprites
                contador = 0
                contador += 1
                aceleracao=2               
                if contador == 340:
                    aceleracao = 1

                screen.fill(BLACK)     
                background_rect_cima.y += 5 * aceleracao
                background_rect.y += 5 * aceleracao
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
                text_surface = score_font.render("{:01d}".format(pont), True, BLACK)
                
                text_rect = text_surface.get_rect()
                text_rect.midtop = (WIDTH-300,  10)
                screen.blit(text_surface, text_rect)
                
                # Depois de desenhar tudo, inverte o display.
                pygame.display.flip()

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
moeda = assets['moeda_sound']

# Cria um carrinho. O construtor será chamado automaticamente.
player = Player(assets["player_img"])

# Carrega a fonte para desenhar o score.
score_font = assets["score_font"]

# Cria um grupo de todos os sprites e adiciona a nave.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Cria um grupo só dos carrinhos
# Cria um grupo só dos carros inimigos
mobs = pygame.sprite.Group()

# Cria um grupo para tiros (vermelho)
bullets = pygame.sprite.Group()
# Grupo para o segundo tiro (azul)
bullet2 = pygame.sprite.Group()
bullets.add(bullet2)

# Cria grupo para as moedas
coin = pygame.sprite.Group()

# Cria um grupo para as caixas
box = pygame.sprite.Group()

#Cria grupo para os flocos
flocos = pygame.sprite.Group()

#Cria um grupo para o laser
laser = pygame.sprite.Group()
# Cria um grupo para a nevasca
nevasca = pygame.sprite.Group()

# Cria carrinhos e adiciona no grupo mobs
for i in range(5):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
#Cria grupo das moedas
imagem_coin=[]
for i in range(9):
    filename = 'Gold_0{}.png'.format(i)
    Coin_img = pygame.image.load(path.join(img_dir, filename)).convert()
    Coin_img = pygame.transform.scale(Coin_img, (35, 35))        
    Coin_img.set_colorkey(WHITE)
    imagem_coin.append(Coin_img)

# #Cria moedas
for i in range(1):
    c = Coin(imagem_coin)
    all_sprites.add(c)
    coin.add(c)
    
#Cria a box
misterybox = pygame.sprite.Group()

# Cria o floco de neve  
def chama_floco():
    for i in range(1):
        f = Floco(assets["flocos_img"])
        all_sprites.add(f)
        flocos.add(f)
chama_floco()

# Comando para evitar travamentos.
try:
     
    começar_na_tela_inicial = init_screen(screen)
        
finally:
    
    pygame.quit()