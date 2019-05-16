import pygame
import random
from init import path, img_dir, WHITE, HEIGHT, WIDTH, BLACK

class Floco(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, flocos_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.image.load(path.join(img_dir, "floco_de_neve.png")).convert()
        
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
        self.speedy = random.randrange(3,10)
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * 85 / 2)
            
    def update(self):
        
        self.rect.x += 0
        self.rect.y += self.speedy
        
        if self.rect.right > 520:
            self.rect.right = 520
        if self.rect.left < 90:
            self.rect.left = 90
        
        # Se o floco passar do final da tela, volta para cima
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            posicao_inicial=[100,195,280,365,455]
            i=random.randrange(0,5)
            self.rect.x = posicao_inicial[i]
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = 3