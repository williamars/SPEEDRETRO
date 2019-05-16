import pygame
import random
from init import path, img_dir, HEIGHT, WIDTH, BLACK


class Nevasca(pygame.sprite.Sprite):
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
        self.rect.x = random.randrange(0,600)
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(-100, -40)
        # Sorteia uma velocidade inicial
        self.speedx = random.randrange(10,20)
        self.speedy = random.randrange(10,20)
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * 85 / 2)
            
    def update(self):
        
        self.rect.x += random.randrange(10,20)
        self.rect.y += random.randrange(10,20)
        
        
        # Se o floco passar do final da tela, volta para cima
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(0,600)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(10,20)
            self.speedy = random.randrange(10,20)