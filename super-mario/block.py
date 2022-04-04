from pygame.sprite import Sprite
import pygame


class Block(Sprite):
    def __init__(self, screen, block_type, images, item=None):
        super(Block, self).__init__()
        self.screen = screen
        self.block_type = block_type
        self.images = images
        self.transform_images()
        self.image = images[0]
        self.block_frame = 0
        self.rect = self.image.get_rect()
        self.item = item

        self.item_active = False

        self.animation_px_counter = 0
        self.is_hit = False

        self.invincible = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        if self.item_active:
            self.item.blitme()

    def __str__(self):
        return "Block Type: " + self.block_type + "at" + self.rect.center

    def hit(self):
        self.item_active = True

    def reset(self):
        self.image = self.images[0]

    def update(self):
        if self.block_type == '?' and not self.invincible:
            self.animate_question_block()
        elif self.block_type == 'ow_brick':
            self.animate_ow_brick_block()

    def animate_question_block(self):
        timer = pygame.time.get_ticks()
        if self.is_hit and (self.item.type == 1 or self.item.type == 2 or self.item.type == 3):

            rise_until = 12
            drop_until = 24
            item_show = 50
            item_rise_until = 55
            if self.animation_px_counter < rise_until:
                self.rect.y -= 2
            elif self.animation_px_counter < drop_until:
                self.rect.y += 2
            elif self.animation_px_counter < item_rise_until:
                self.item.rect.y -= 1
                if self.animation_px_counter > item_show:
                    self.item_active = True
            self.animation_px_counter += 1
            self.image = self.images[4]
        elif self.is_hit and self.item.type == 4:

            rise_until = 12
            drop_until = 24
            item_show = 45
            item_rise_until = 98
            item_drop_until = 146
            self.block_frame = 4
            if self.animation_px_counter < rise_until:
                self.rect.y -= 2
                self.animation_px_counter += 1
            elif self.animation_px_counter < drop_until:
                self.rect.y += 2
                self.animation_px_counter += 1
            elif self.animation_px_counter < item_rise_until:

                self.item.rect.y -= 1
                if self.animation_px_counter > item_show:
                    self.item_active = True
                self.animation_px_counter += 1
            elif self.animation_px_counter < item_drop_until:
                self.item.rect.y += 1
                self.animation_px_counter += 1
            elif self.animation_px_counter >= item_drop_until:
                self.item_active = False
            self.image = self.images[4]
        else:
            self.image = self.images[(int(timer / 200) % 4)]

    def animate_ow_brick_block(self):
        """If the brick is hit, animate small push. Otherwise, no animation"""
        rise_until = 8
        drop_until = 16
        if self.is_hit:

            if self.animation_px_counter < rise_until:
                self.rect.y -= 1
                self.block_frame = 1
                self.animation_px_counter += 1

            elif self.animation_px_counter < drop_until:
                self.rect.y += 1
                self.animation_px_counter += 1
        else:
            self.block_frame = 0

    def transform_images(self):
        ctr = 0
        for image in self.images:
            img = pygame.transform.scale(image, (30, 30))
            self.images[ctr] = img
            ctr += 1
