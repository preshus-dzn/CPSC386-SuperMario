import pygame
from pygame.sprite import Sprite


class Mario(Sprite):
    def __init__(self, screen, small_regular_mario_images, large_regular_mario_images,
                 small_star_mario_images, large_star_mario_images):
        """Initialize the mario, and set its starting position."""
        super(Mario, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.mario_images = small_regular_mario_images
        self.star_mario_images = small_star_mario_images
        self.large_mario_images = large_regular_mario_images
        self.large_star_mario_images = large_star_mario_images

        self.image = pygame.transform.scale(self.mario_images[0], (34, 34))
        self.rect = self.image.get_rect()

        self.rect.centerx = self.screen_rect.left + 20
        self.rect.bottom = self.screen_rect.bottom - 48

        self.rect2 = pygame.Rect(0, 0, 34, 36)
        self.rect3 = pygame.Rect(0, 0, 28, 34)
        self.rect2.center = self.rect.center
        self.rect3.center = self.rect.center

        self.moving_right = False
        self.moving_left = False

        self.on_the_ground = True
        self.onblock = False
        self.looking_right = True
        self.dead = False
        self.large = False
        self.super = False
        self.reset_size = False

        self.gravity = 0.3
        self.y_veloctiy = 0
        self.x_velocity = 4
        self.frame = 0
        self.super_frame = 0
        self.death_timer = 0
        self.offset = 0

def update(self):
    """Update the mario's position, based on movement flags and if he's jumping."""
    self.y_veloctiy += self.gravity
    if self.dead:
        self.rect.centery += self.y_veloctiy
        self.x_velocity = 0

    elif not self.dead:
        if self.rect.bottom > 402:
            self.rect.bottom = 402
            self.y_veloctiy = 0
            self.on_the_ground = True

        if not self.on_the_ground:
            self.x_velocity = 3
            self.rect.centery += self.y_veloctiy
        elif self.on_the_ground:
            self.x_velocity = 4

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.x_velocity
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.x_velocity

    self.rect2.center = self.rect.center
    self.rect2.centery += 8
    self.rect3.center = self.rect.center
    self.rect3.centery -= 4

    def reset(self):
        """Reset mario's position and image."""
        self.image = pygame.transform.scale(self.mario_images[0], (34, 34))
        self.rect.centerx = self.screen_rect.left + 20
        self.rect.bottom = self.screen_rect.bottom - 48
        self.death_timer = 0

    def blitme(self):
        """Draw the mario at its current location."""
        if self.dead:
            self.image = pygame.transform.scale(self.mario_images[6], (34, 34))
            self.death_timer += 1

        elif not self.dead:
            if not self.on_the_ground:
                if self.looking_right:
                    if self.large and not self.super:
                        self.image = self.large_mario_images[5]
                        self.image = pygame.transform.scale(self.image, (34, 64))
                    elif self.large and self.super:
                        self.image = self.large_star_mario_images[5]
                        self.image = pygame.transform.scale(self.image, (34, 64))
                    elif not self.large and self.super:
                        self.image = self.star_mario_images[5]
                        self.image = pygame.transform.scale(self.image, (34, 34))
                    else:
                        self.image = self.mario_images[5]
                        self.image = pygame.transform.scale(self.image, (34, 34))
                else:
                    if self.large and not self.super:
                        self.image = pygame.transform.flip(self.large_mario_images[5], True, False)
                        self.image = pygame.transform.scale(self.image, (34, 64))
                    elif self.large and self.super:
                        self.image = pygame.transform.flip(self.large_star_mario_images[5], True, False)
                        self.image = pygame.transform.scale(self.image, (34, 64))
                    elif not self.large and self.super:
                        self.image = pygame.transform.flip(self.star_mario_images[5], True, False)
                        self.image = pygame.transform.scale(self.image, (34, 34))
                    else:
                        self.image = pygame.transform.flip(self.mario_images[5], True, False)
                        self.image = pygame.transform.scale(self.image, (34, 34))

            elif self.on_the_ground:
                if self.moving_right:
                    self.frame += 1
                    if self.frame >= 21:
                        self.frame = 0

                    if self.large and not self.super:
                        self.image = self.large_mario_images[int(self.frame / 7) + 1]
                    elif self.large and self.super:
                        self.image = self.large_star_mario_images[int(self.frame / 7) + 1]
                    elif not self.large and self.super:
                        self.image = self.star_mario_images[int(self.frame / 7) + 1]
                    else:
                        self.image = self.mario_images[int(self.frame / 7) + 1]
                elif self.moving_left:
                    self.frame += 1
                    if self.frame >= 21:
                        self.frame = 0

                    if self.large and not self.super:
                        self.image = pygame.transform.flip(self.large_mario_images[int(self.frame / 7) + 1],
                                                           True, False)
                    elif self.large and self.super:
                        self.image = pygame.transform.flip(self.large_star_mario_images[int(self.frame / 7) + 1],
                                                           True, False)
                    elif not self.large and self.super:
                        self.image = pygame.transform.flip(self.star_mario_images[int(self.frame / 7) + 1], True, False)
                    else:
                        self.image = pygame.transform.flip(self.mario_images[int(self.frame / 7) + 1], True, False)

                elif self.looking_right:
                    if self.large and not self.super:
                        self.image = self.large_mario_images[0]
                    elif self.large and self.super:
                        self.image = self.large_star_mario_images[0]
                    elif not self.large and self.super:
                        self.image = self.star_mario_images[0]
                    else:
                        self.image = self.mario_images[0]
                elif not self.looking_right:
                    if self.large and not self.super:
                        self.image = pygame.transform.flip(self.large_mario_images[0], True, False)
                    elif self.large and self.super:
                        self.image = pygame.transform.flip(self.large_star_mario_images[0], True, False)
                    elif not self.large and self.super:
                        self.image = pygame.transform.flip(self.star_mario_images[0], True, False)
                    else:
                        self.image = pygame.transform.flip(self.mario_images[0], True, False)

                if self.large:
                    self.image = pygame.transform.scale(self.image, (34, 68))
                    if not self.reset_size:
                        centerx = self.rect.centerx
                        self.rect = self.image.get_rect()
                        self.rect.centerx = centerx
                        self.rect.bottom = 402
                        self.rect2 = pygame.Rect(0, 0, 34, 70)
                        self.rect3 = pygame.Rect(0, 0, 28, 68)
                        self.rect2.center = self.rect.center
                        self.rect3.center = self.rect.center
                        self.reset_size = True
                else:
                    self.image = pygame.transform.scale(self.image, (34, 34))
                    if not self.reset_size:
                        self.rect2 = pygame.Rect(0, 0, 34, 36)
                        self.rect3 = pygame.Rect(0, 0, 28, 34)
                        centerx = self.rect.centerx
                        self.rect = self.image.get_rect()
                        self.rect.centerx = centerx
                        self.rect.bottom = 402
                        self.reset_size = True

        self.screen.blit(self.image, self.rect)
