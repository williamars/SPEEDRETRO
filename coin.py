import pygame
import random
from init import HEIGHT, WIDTH

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