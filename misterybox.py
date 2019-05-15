import pygame
import random
from init import path, img_dir, WHITE, HEIGHT, WIDTH, BLACK

# Classe Mob que representa os carrinhos
class Box(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem.
        box_img = pygame.image.load(path.join(img_dir, "misterybox.png")).convert()
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(box_img, (35, 50))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        posicao_inicial=[100,195,280,365,455] # Posições iniciais dos carrinhos
        i=random.randrange(0,10)               # Sorteia uma faixa para aparecer carrinhos
        if i <= 2:
            self.rect.x = 100
        elif i <= 4:
            self.rect.x = 195
        elif i <=6:
            self.rect.x = 280
        elif i<=8:
            self.rect.x = 365
        elif i <=10:
            self.rect.x = 455
        
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(-100, -40)
        # Sorteia uma velocidade inicial
        self.speedx = 0
        self.speedy = 2
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85 / 2)
        
    # Metodo que atualiza a posição da navinha
    def update(self):
        self.rect.x += 0
        self.rect.y += self.speedy
        
        if self.rect.right > 520:
            self.rect.right = 520
        if self.rect.left < 90:
            self.rect.left = 90
        
        # Se o meteoro passar do final da tela, volta para cima
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
           
            i=random.randrange(0,10)

            if i <= 2:
                self.rect.x = 100
            elif i <= 4:
                self.rect.x = 195
            elif i <=6:
                self.rect.x = 280
            elif i<=8:
                self.rect.x = 365
            elif i <=10:
                self.rect.x = 455
                
            self.rect.y = random.randrange(-100, -40)
            self.speedx = 0
            self.speedy = 2