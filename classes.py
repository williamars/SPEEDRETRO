import pygame
from init import BLACK, WIDTH, HEIGHT, img_dir, snd_dir, fnt_dir, WHITE, path
import random

# Classe Jogador que representa o carrinho
class Player(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, carro):
        
         # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carrega a animação da carro
        self.carro = carro        
        
        # Inicia o processo de animação colocando a primeira imagem na tela.
        self.frame = 0
        self.image = self.carro[self.frame]
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Centraliza embaixo da tela.
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 200
        
        # Velocidade do carrinho
        self.speedx = 0
                 
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = 11

        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 12
    
    # Metodo que atualiza a posição do carrinho
    def update(self):
        self.rect.x += self.speedx

        # Mantém dentro da tela
        if self.rect.right > 520:
            self.rect.right = 520
        if self.rect.left < 83:
            self.rect.left = 83
        
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1
            if self.frame == len(self.carro):
                self.frame = 0
            
            center = self.rect.center
            self.image = self.carro[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
              
        
    
    

# Classe Mob que representa os carrinhos
class Mob(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, mob_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem.
        self.image = mob_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (54, 70))
        
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        i=random.randrange(0,10)               # Sorteia uma faixa para aparecer carrinhos
        if i <=2:
            self.rect.x = 105
        elif i <=4:
            self.rect.x = 195
        elif i <=6:
            self.rect.x = 275
        elif i <= 8:
            self.rect.x = 365
        elif i <=10:
            self.rect.x = 455
        
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(-150, -100)
        # Sorteia uma velocidade inicial
        self.speedx = 0
        self.speedy = 9

        self.direction = 0 # -1 0 +1
        self.direction_count = 0

        self.reference = 0
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85 / 2)
        
    # Metodo que atualiza a posição do carrinho
    def update(self):
        if self.direction_count == 0:
            self.direction = random.randrange(3)-1
            self.direction_count=100
        self.direction_count -= 1
        
        if self.rect.x <= 100 and self.direction < 0:
            self.direction = 0
        if self.rect.x >= 455 and self.direction > 0:
            self.direction = 0

        if abs(self.reference) >= 85:
            self.direction=0

        self.rect.x += self.direction * 2
        self.reference += self.direction * 2
        # esquerda = -50
        # direita = 50
        # o=random.randrange(1,2)
        # p=random.randrange(1,3)
        # if self.rect.x == 100:
        #     if o == 1:
        #         self.rect.x +=0
        #     else:
        #         self.rect.x +=direita
        #         if self.rect.x == 195:
        #             self.rect.x=0
        # if self.rect.x == 455:
        #     if o == 1:
        #         self.rect.x +=0
        #     else:
        #         self.rect.x +=esquerda
        #         if self.rect.x==365:
        #             self.rect.x+=0 
        # if self.rect.x == 195:
        #     if p == 1:
        #         self.rect.x +=0
        #     if p == 2:
        #         self.rect.x +=direita
        #         if self.rect.x == 280:
        #             self.rect.x=0
        #     if p == 3:
        #         self.rect.x +=esquerda
        #         if self.rect.x==100:
        #             self.rect.x+=0 

        self.rect.y += self.speedy
        
        if self.rect.right > 520:
            self.rect.right = 520
        if self.rect.left < 90:
            self.rect.left = 90
        
        # Se o carro passar do final da tela, volta para cima
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:

            i=random.randrange(0,10)
            if i <=2:
                self.rect.x = 105
            elif i <=4:
                self.rect.x = 195
            elif i <=6:
                self.rect.x = 275
            elif i <= 8:
                self.rect.x = 365
            elif i <=10:
                self.rect.x = 455

            self.rect.y = random.randrange(-150, -100)
            if i % 2 == 0:
                self.speedx = 50
            else:
                self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(10, 15)
            self.reference=0

class Floco(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, flocos_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Diminuindo o tamanho da imagem.
        self.image = flocos_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(flocos_img, (35, 38))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        posicao_inicial=[195,280,365] # Posições iniciais dos flocos
        i=random.randrange(0,3)               # Sorteia uma faixa para aparecer os flocos
        self.rect.x = posicao_inicial[i]
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(-100, -40)
        # Sorteia uma velocidade inicial
        self.speedx = 0
        self.speedy = 3
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * 85 / 2)
            
    def update(self):
        
        self.rect.x += 0
        self.rect.y += self.speedy
    
        # Se o floco passar do final da tela, volta para cima
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            posicao_inicial=[195,280,365]
            i=random.randrange(0,3)
            self.rect.x = posicao_inicial[i]
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = 3

# Classe Coin que representa as moedas
class Coin(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, imagem_coin):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carrega a animação da coin
        self.imagem_coin = imagem_coin        
        
        # Inicia o processo de animação colocando a primeira imagem na tela.
        self.frame = 0
        self.image = self.imagem_coin[self.frame]
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        posicao_inicial=[100,195,280,365,455] # Posições iniciais das moedas
        i=random.randrange(0,5)               # Sorteia uma faixa para aparecer moedas
        self.rect.x = posicao_inicial[i]
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(-100, -40)
        # Sorteia uma velocidade inicial
        self.speedx = 0
        self.speedy = 3
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * 85 / 2)
        
        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 120

    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1
            if self.frame == len(self.imagem_coin):
                self.frame = 0
            
            center = self.rect.center
            self.image = self.imagem_coin[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
              
        self.rect.x += 0
        self.rect.y += self.speedy
        
        # Se a moeda passar do final da tela, volta para cima
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            posicao_inicial=[100,195,280,365,455]
            i=random.randrange(0,5)
            self.rect.x = posicao_inicial[i]
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = 3

# Classe Mob que representa os carrinhos
class Box(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, box_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem.
        self.image = box_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(box_img, (35, 50))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        posicao_inicial=[100,195,280,365,455] # Posições iniciais
        i=random.randrange(0,10)               # Sorteia uma faixa para aparecer
        if i <= 2:
            self.rect.x = posicao_inicial[0]
        elif i <= 4:
            self.rect.x = posicao_inicial[1]
        elif i <=6:
            self.rect.x = posicao_inicial[2]
        elif i<=8:
            self.rect.x = posicao_inicial[3]
        elif i <=10:
            self.rect.x = posicao_inicial[4]
        
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(-100, -40)
        # Sorteia uma velocidade inicial
        self.speedx = 0
        self.speedy = 2
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85 / 2)
        
    # Metodo que atualiza a posição da caixa
    def update(self):
        self.rect.x += 0
        self.rect.y += self.speedy
        
        if self.rect.right > 520:
            self.rect.right = 520
        if self.rect.left < 90:
            self.rect.left = 90
        
        # Se a caixa passar do final da tela, volta para cima
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            posicao_inicial=[100,195,280,365,455]
            i=random.randrange(0,10)

            if i <= 2:
                self.rect.x = posicao_inicial[0]
            elif i <= 4:
                self.rect.x = posicao_inicial[1]
            elif i <=6:
                self.rect.x = posicao_inicial[2]
            elif i<=8:
                self.rect.x = posicao_inicial[3]
            elif i <=10:
                self.rect.x = posicao_inicial[4]
                
            self.rect.y = random.randrange(-100, -40)
            self.speedx = 0
            self.speedy = 2

class Nevasca(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, flocos2_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Diminuindo o tamanho da imagem.
        self.image = flocos2_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(flocos2_img, (35, 38))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x                      
        self.rect.x = random.randrange(0,600)
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(-700, -40)
        # Sorteia uma velocidade inicial
        self.speedx = random.randrange(0,5)
        self.speedy = random.randrange(10,20)
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * 85 / 2)
            
    def update(self):
        
        self.rect.x += random.randrange(0,5)
        self.rect.y += random.randrange(10,20)
        
class Laser(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, laser_img, x, y):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        self.image = laser_img
        
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        
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