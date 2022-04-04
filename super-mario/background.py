import pygame
from pygame.sprite import Sprite


class Background(Sprite):
    def __init__(self, screen):
        """Initialize the mario, and set its starting position."""
        super(Background, self).__init__()
        self.screen = screen

        self.image = pygame.image.load('images/world_no_blocks.png')
        self.image = pygame.transform.scale(self.image, (6784, 920))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.topleft = self.screen_rect.topleft

    def blitme(self):
        """Draw the background."""
        self.screen.blit(self.image, self.rect)

    def reset_background(self):
        """Reset the background's position."""
        self.rect.topleft = self.screen_rect.topleft
