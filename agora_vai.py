import pygame
import time
from os import path
import sys, os
import random

# O que deixa a tela centralizada quando rodar
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Importando as informações iniciais
from init import img_dir, snd_dir, fnt_dir, BLACK, WIDTH, HEIGHT, FPS, WHITE, YELLOW, bright_YELLOW

# Importando todas as classes
from classes import Player, Mob, Box, Coin, Nevasca, Floco, Laser
        
# Definindo o tamanho da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Carrega todos os assets de uma vez só
def load_assets(img_dir, snd_dir, fnt_dir):
    assets = {}
    assets["laser_img"] = pygame.image.load(path.join(img_dir, "redlaser.png")).convert()
    assets["flocos_img"] = pygame.image.load(path.join(img_dir, "floco_de_neve.png")).convert()
    assets["flocos2_img"] = pygame.image.load(path.join(img_dir, "neve.png")).convert()
    assets["box_img"] = pygame.image.load(path.join(img_dir, "misterybox.png")).convert()
    assets["coin_init"] = pygame.image.load(path.join(img_dir, "coin_init.png")).convert()
    assets["boom_sound"] = pygame.mixer.Sound(path.join(snd_dir, "crash.wav"))
    assets["moeda_sound"] = pygame.mixer.Sound(path.join(snd_dir, "m.wav"))
    assets["destroy_sound"] = pygame.mixer.Sound(path.join(snd_dir, "expl6.wav"))
    assets["box_sound"] = pygame.mixer.Sound(path.join(snd_dir, 'ta_da.wav'))
    assets["pew_sound"] = pygame.mixer.Sound(path.join(snd_dir, "pew.wav"))
    assets["score_font"] = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 25)
    return assets

# Função para a cor e objeto da fonte que é utilizada muitas vezes
def text_object(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

# Função que vê qual foi o high score no outro arquivo
def maior_pontuacao(pont, nomecolocado):
    RECORDE = get_high_score()
    if pont > RECORDE:
        save_high_score(pont)
        save_nome(nomecolocado)

# Função que lê o high score no outro arquivo
def get_high_score():
    high_score_file = open("ponto_high_score.txt", "r")
    high_score = int(high_score_file.read())
    high_score_file.close()
    return high_score
 
# Função para salvar o novo high score, caso seja maior
def save_high_score(new_high_score):
    high_score_file = open("ponto_high_score.txt", "w")
    high_score_file.write(str(new_high_score))
    high_score_file.close()

# Função para salvar o nome da pessoa do novo high score
def save_nome(nomecolocado):
    nome = open("nome_high_score.txt", "w")
    nome.write(nomecolocado)
    nome.close()

# Função para ler o nome da pessoa do high score
def get_name():
    nome = open("nome_high_score.txt", "r")
    nomee = nome.read()
    nome.close()
    return nomee

def button(msg, x, y, w, h, inactive, active, action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, active, (x, y, w, h))

    else:
        pygame.draw.rect(screen, inactive, (x, y, w, h))    

    smalltext = pygame.font.Font("freesansbold.ttf", 12)
    textSurf, textRect = text_object(msg, smalltext)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)

# Função que faz tudo da tela inicial do jogo
def tela_inicial(screen):

    largeText = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 27)
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(200, 250, 150, 40)
    color_inactive = WHITE
    color_active = YELLOW
    color = color_inactive
    active = False
    text = ''

    background = pygame.image.load(path.join(img_dir, 'tela_inicial.png')).convert()
    background_rect_1 = background.get_rect()
    background_rect_2 = background.get_rect()
    background_rect_2.y = -HEIGHT

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        nomecolocado = text
                        print(text)
                        text = ''
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Coloca a imagem de fundo
   
        background_rect_2.y += 5
        background_rect_1.y += 5

        if background_rect_1.y >= HEIGHT :
            background_rect_1.y = 0
            background_rect_2.y = -HEIGHT

        # background_rect_cima.y = background_y_cima
        # background_rect.y = background_y           
        screen.blit(background, background_rect_1)
        screen.blit(background, background_rect_2)

        # Coloca a caixinha
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Coloca o "INSIRA SEU NOME" junto à caixinha
        pedenome, thenew = text_object('INSIRA SEU NOME', largeText)
        thenew.center = ((WIDTH/2),(HEIGHT/2 - 170))
        screen.blit(pedenome, thenew)

        # Coloca o "E APERTE ENTER" abaixo da caixinha
        ENTER, thenew = text_object('APERTE ENTER', largeText)
        thenew.center = ((WIDTH/2),(HEIGHT/2 - 80))
        screen.blit(ENTER, thenew)

        # Coloca a maior pontuação e o nome do recordista
        puentos = get_high_score()
        nuemes = get_name()
        poemaior, poe = text_object('RECORDISTA', largeText)
        poe.center = ((WIDTH/2),(HEIGHT/2 - 360))
        screen.blit(poemaior, poe)
        pedenome, thenew = text_object(f'{nuemes}: {puentos}', largeText)
        thenew.center = ((WIDTH/2),(HEIGHT/2 - 330))
        screen.blit(pedenome, thenew)

        instruction= True
        while instruction:
            instrucao = pygame.image.load(path.join(img_dir, 'instrucao.png')).convert()
            background_rect = background.get_rect()
            screen.blit(instrucao, background_rect)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        instruction = False


        pygame.display.flip()
        clock.tick(30)

    # Retorna o nome para utilizar no High Score, caso necessário
    return nomecolocado

    
    


# Função da tela final do jogo, após a batida do carro 
def tela_mostra_pontuacao(screen, nomecolocado, pont):

    largeText = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 27)
    maiortext = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 40)
    clock = pygame.time.Clock()

    # Printando todas as informações na tela, junto com a imagem de fundo
    background = pygame.image.load(path.join(img_dir, 'tela_inicial.png')).convert()
    background_rect = background.get_rect()
    screen.blit(background, background_rect)

    poetexto, thenew = text_object(f'{nomecolocado}', maiortext)
    thenew.center = ((WIDTH/2),(HEIGHT/2-360))
    screen.blit(poetexto, thenew)

    poetexto2, thenew = text_object('SUA PONTUAÇÃO:', largeText)
    thenew.center = ((WIDTH/2),(HEIGHT/2 - 300))
    screen.blit(poetexto2, thenew)

    poenome, thenew = text_object(f'{pont}', maiortext)
    thenew.center = ((WIDTH/2),(HEIGHT/2 - 250))
    screen.blit(poenome, thenew)

    button("RESTART", 180, 540, 75, 50, YELLOW, bright_YELLOW, "restart")
    button("QUIT", 345, 540, 75, 50, WHITE, WHITE, "quit")

    maior_pontuacao = get_high_score()
    if pont > maior_pontuacao:
            poenome, thenew = text_object('O MAIS NOVO', largeText)
            thenew.center = ((WIDTH/2),(HEIGHT/2 - 100))
            screen.blit(poenome, thenew)
            poenome, thenew = text_object('RECORDISTA!', largeText)
            thenew.center = ((WIDTH/2),(HEIGHT/2 - 40))
            screen.blit(poenome, thenew)

    pygame.display.flip()
    clock.tick(30)

    # Esperar alguns segundos para a pessoa poder ler a informação
    time.sleep(4)

# Função principal do jogo, onde tem todas as ações
def principal(nomecolocado):
    game_roda = True   
    while game_roda:
        #instrução
        

        # Carrega a fonte para desenhar o score.
        score_font = assets["score_font"]

        # Cria um carrinho. O construtor será chamado automaticamente.
        carro=[]
        for i in range(4):
            carrinho = 'finally{}.png'.format(i)
            player_img = pygame.image.load(path.join(img_dir, carrinho)).convert()
            player_img = pygame.transform.scale(player_img, (58, 75))
            player_img.set_colorkey(WHITE)
            carro.append(player_img)
        
        player = Player(carro)
        # Cria todos os sprites e adiciona o player em tal
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)

        # Cria um grupo só dos carrinhos inimigos
        mobs = pygame.sprite.Group()


        inimigo=[]
        for i in range(4):
            filename = 'inimigo{}.png'.format(i)
            inimigo_img = pygame.image.load(path.join(img_dir, filename)).convert()
            inimigo_img = pygame.transform.scale(inimigo_img, (58, 75))  
            inimigo_img.set_colorkey(WHITE)
            inimigo.append(inimigo_img)
        

        # Cria grupo para as moedas
        coin = pygame.sprite.Group()

        # Cria um grupo para as caixas
        box = pygame.sprite.Group()

        #Cria grupo para os flocos
        flocos = pygame.sprite.Group()

        #Cria um grupo para o laser
        laser = pygame.sprite.Group()

        # Cria carrinhos e adiciona no grupo mobs
        for i in range(4):
            m = Mob(inimigo)
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

        # Cria moedas
        c = Coin(imagem_coin)
        all_sprites.add(c)
        coin.add(c)

        # Função para criar o floco de neve (FUNÇÃO POIS SÓ QUER UM POR VEZ)
        def chama_floco():
            f = Floco(assets["flocos_img"])
            all_sprites.add(f)
            flocos.add(f) 
        # Chama a função
        chama_floco()   

        estanevando = False
        estanevando_tempo = 0
        speedx = 0
        timee=0
        clock.tick(FPS)
        pygame.mixer.music.play(loops=-1)
        velocidade=0
        aceleracao=0.75
        background_y_cima = -HEIGHT
        background_y = 0
        contagemdetiros = 3
        score = 0

        # Pegar o nome colocado pela pessoa na tela inicial
        nomecolocado = tela_inicial(screen)

        # Loop principal.
        running = True
        while running:
        # Ajusta a velocidade do jogo.
            clock.tick(FPS)

            # Para o x parar de acelerar quando se pega a neve em algum momento
            estanevando_tempo -= 1
            if estanevando_tempo == 1:
                estanevando_tempo = 0
                speedx = 0
                estanevando = False
    
            # Probabilidade de sortear caixinha
            if random.randrange(1, 700) == 1:
                b = Box(assets["box_img"])
                all_sprites.add(b)
                box.add(b)
            

            
            # Probabilidade de sortear moeda
            if random.randrange(1,500) == 1:
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
                    
                    # Se for um espaço, atira! (caso tenha tiro)
                    if contagemdetiros > 0:    
                        if event.key == pygame.K_SPACE:
                            laserr = Laser(assets['laser_img'], player.rect.centerx, player.rect.top)
                            all_sprites.add(laserr)
                            laser.add(laserr)
                            pew_sound.play()
                            contagemdetiros -= 1
                                      
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
            
            # Aponta a velocidade em x do player (carro)
            player.speedx = speedx
                        
            # Verifica se jogador encostou a parede. Se encostar, morre.
            if player.rect.right > 519:
                boom_sound.play()
                running = False
            if player.rect.left < 89:
                boom_sound.play()
                running = False    
            
            # Atualiza a acao de cada sprite.
            all_sprites.update()
                
            # Verifica se houve colisão entre Laser e carrinhos
            hits = pygame.sprite.groupcollide(mobs, laser, True, True)
            for hit in hits:
                # O carrinho é destruido e precisa ser recriado
                destroy_sound.play()
                m = Mob(inimigo) 
                all_sprites.add(m)
                mobs.add(m) 
            
            # Verifica se houve colisão entre os carrinhos
            hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
            if hits:
                boom_sound.play()
                # Precisa esperar senão fecha duma vez
                time.sleep(0.5)
                running = False
            
            # Verifica se houve colisão com a moeda. Se houve, soma pontos.
            hits = pygame.sprite.spritecollide(player, coin, True, False)
            if hits:
                moeda.play()
                score += 10

            # Verifica se houve colisão com o misterybox. Se houve, soma pontos e ativa laser (ou soma)
            hits = pygame.sprite.spritecollide(player, box, True, False)
            for hit in hits:
                Ta_Da.play()
                score += 5
                contagemdetiros += 3
                
            # Verifica se houve colisão entre player e floco de neve
            hits = pygame.sprite.spritecollide(player, flocos, True, False)
            if hits:
                # Ativa o modo nevasca
                estanevando = True
                estanevando_tempo = 120
                speedx = 1
                for i in range(30):
                    n = Nevasca(assets["flocos2_img"])
                    all_sprites.add(n)
                chama_floco()

            if velocidade < 18:
                velocidade += aceleracao
            else:
                velocidade = 18

            # A cada loop, redesenha o fundo e os sprites 
            screen.fill(BLACK)    
            background_y_cima += velocidade
            background_y += velocidade
    
            if background_y >= HEIGHT :
                background_y = 0
                background_y_cima = -HEIGHT

            background_rect_cima.y = background_y_cima
            background_rect.y = background_y               

            screen.blit(background, background_rect_cima)
            screen.blit(background, background_rect)
            all_sprites.draw(screen)

            # Desenha o score, por tempo
            timee+=1
            pont=(timee//FPS)+score
            text_surface = score_font.render("{:01d}".format(pont), True, BLACK)           
            text_rect = text_surface.get_rect()
            text_rect.midtop = (WIDTH-300,  10)
            screen.blit(text_surface, text_rect)

            if contagemdetiros > 0:
                text_surface = score_font.render("SPACE:{:01d} ESPECIAIS".format(contagemdetiros), True, BLACK)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (WIDTH/2,  HEIGHT-130)
                screen.blit(text_surface, text_rect)                

            # Depois de desenhar tudo, inverte o display.
            pygame.display.flip()

        tela_mostra_pontuacao(screen, nomecolocado, pont)

        # Chamando a função para ver se a pessoa fez a maior pontuação
        maior_pontuacao(pont, nomecolocado)

        # Matando os mobs e o player para fazê-lo novamente quando voltar o loop
        for mobs in all_sprites:
            mobs.kill()
            player.kill()

# Inicialização do Pygame.
pygame.init() 
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("SpeedRetro")

# Ícone do jogo
icon = pygame.image.load(path.join(img_dir, "Finally0.png")).convert()
pygame.display.set_icon(icon)

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
Ta_Da = assets['box_sound']
moeda = assets['moeda_sound']

nomecolocado = ''

# Comando para evitar travamentos.
try: 
    
    principal(nomecolocado)

finally:
    
    pygame.quit()