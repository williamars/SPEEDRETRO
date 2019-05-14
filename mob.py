import pygame
import random
from init import path, img_dir, WHITE, HEIGHT, WIDTH

# Classe Mob que representa os carrinhos
class Mob(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem.
        mob_img = pygame.image.load(path.join(img_dir, "Carrinhonovo.png")).convert()
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (54, 70))
        
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        posicao_inicial=[100,195,280,365,455] # Posições iniciais dos carrinhos
        i=random.randrange(0,5)               # Sorteia uma faixa para aparecer carrinhos
        self.rect.x = posicao_inicial[i]
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(-100, -40)
        # Sorteia uma velocidade inicial
        self.speedx = 0
        self.speedy = 12
        
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
            posicao_inicial=[100,195,280,365,455]
            i=random.randrange(0,5)
            z=0
            while z<5:
                posicoes_iniciais_sorteadas=[]
                posicoes_iniciais_sorteadas.append(posicao_inicial[i])
                z+=1
            z=0
            while z<6:
                if posicoes_iniciais_sorteadas[i] != posicoes_iniciais_sorteadas[i-1]:
                    self.rect.x = posicao_inicial[i]
                    z+=1
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = 12