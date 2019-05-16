import pygame
from init import WIDTH, HEIGHT, WHITE

# Classe Jogador que representa o carrinho
class Player(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, player_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        self.image = player_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (58, 75))
        
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Centraliza embaixo da tela.
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 200
        
        # Velocidade do carrinho
        self.speedx = 0
                 
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = 11
    
    # Metodo que atualiza a posição do carrinho
    def update(self):
        self.rect.x += self.speedx
#        
#        # Mantém dentro da tela
        if self.rect.right > 520:
            self.rect.right = 520
        if self.rect.left < 83:
            self.rect.left = 83