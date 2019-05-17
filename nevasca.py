import pygame
import random
from init import BLACK


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
        
        
        
        
        