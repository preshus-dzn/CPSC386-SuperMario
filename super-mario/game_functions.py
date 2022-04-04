import sys
import spritesheet
import pygame


def check_keyup_events(event, mario):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        mario.moving_right = False
    elif event.key == pygame.K_LEFT:
        mario.moving_left = False
    elif event.key == pygame.K_SPACE:
        jump_small(mario)

def check_keydown_events(event, mario, screen, bp, background, enemies, blocks):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        mario.moving_right = True
        mario.looking_right = True
    elif event.key == pygame.K_LEFT:
        mario.moving_left = True
        mario.looking_right = False
    elif event.key == pygame.K_SPACE:
        jump_super(mario)
    elif event.key == pygame.K_m:
        print("Mario at = " + str(mario.rect.centerx - mario.offset))
        print("Mario bottom = " + str(mario.rect.bottom))
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_DOWN:
        bp.keydown_event(mario, background, enemies, blocks)


def check_events(screen, stats, sb, play_button, mario, enemies, bp, background, blocks):
    """Respond to keypresses and mouse events."""
    bp.check_pipe(mario, background, enemies, blocks)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, mario, screen, bp, background, enemies, blocks)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, mario)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(screen, stats, sb, play_button, mario, enemies, mouse_x, mouse_y)


def check_play_button(screen, stats, sb, play_button, mario, enemies, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_coins()
        sb.prep_level()
        sb.prep_time()
        sb.prep_lives()


def check_game_over(game_stats):
    hs_file = "text/high_scores.txt"
    update_high_scores(game_stats)
    update_high_scores_file(hs_file, game_stats)
    game_stats.game_active = False
    game_stats.reset_stats()
    pygame.mouse.set_visible(True)


def play_sound(sound):
    small_jump_sound = pygame.mixer.Sound('sounds/jump_small.wav')
    mario_die_sound = pygame.mixer.Sound('sounds/mario_die.wav')
    mario_kick = pygame.mixer.Sound('sounds/kick.wav')
    powerup = pygame.mixer.Sound('sounds/powerup.wav')
    if sound == "small_jump":
        small_jump_sound.play()
    elif sound == "mario_die":
        mario_die_sound.play()
    elif sound == "mario_kick":
        mario_kick.play()
    elif sound == "powerup":
        powerup.play()


def update_screen(screen_rect, stats, sb, background, mario, enemies, play_button, blocks, items):
    """Update images on the screen, and flip to the new screen."""

    if mario.rect.centerx > screen_rect.centerx and mario.rect.centerx - mario.offset < 6180:
        mario.rect.centerx -= mario.x_velocity
        background.rect.centerx -= mario.x_velocity
        mario.offset += mario.x_velocity
        for enemy in enemies:
            enemy.rect.centerx -= mario.x_velocity
            enemy.left_limit -= mario.x_velocity
            enemy.right_limit -= mario.x_velocity
        for block1 in blocks.sprites():
            block1.rect.centerx -= mario.x_velocity

    background.blitme()
    for enemy in enemies:
        enemy.blitme()
    mario.blitme()
    for block1 in blocks.sprites():
        block1.update()
        block1.blitme()

    sb.refresh_time()
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def check_block_collision(screen, mario, blocks):
    test = 0
    for block1 in blocks:
        if pygame.Rect.colliderect(mario.rect3, block1.rect):
            if mario.y_veloctiy < 0:
                mario.rect.top = block1.rect.bottom + 4
                mario.y_veloctiy = 0
                block1.is_hit = True
        elif pygame.Rect.colliderect(mario.rect, block1.rect):
            if mario.moving_right:
                mario.rect.right = block1.rect.left - 4
                mario.x_velocity = 0

            if mario.moving_left:
                mario.rect.left = block1.rect.right + 4
                mario.x_velocity = 0

        elif pygame.Rect.colliderect(mario.rect2, block1.rect):
            if mario.y_veloctiy < 0:

                if not mario.on_the_ground and mario.onblock:
                    mario.rect.bottom = block1.rect.top - 4
                    mario.on_the_ground = True
                    mario.y_veloctiy = 0
                    mario.onblock = True


            if mario.y_veloctiy > 0:
                mario.rect.bottom = block1.rect.top
                mario.on_the_ground = True
                mario.y_veloctiy = 0

        if not pygame.Rect.colliderect(mario.rect2, block1.rect) and mario.rect.bottom < mario.screen_rect.bottom - 48:
            test += 1

    if test == len(blocks):
        mario.on_the_ground = False
        mario.onblock = False


def check_item_collision(screen, mario, items):
    """see if mario collided with an item"""
    collision = pygame.sprite.spritecollide(mario, items, True)
    if collision:
        for item in collision:
            play_sound("powerup")
            if item.type == 1:
                mario.large = True

            elif item.type == 3:
                mario.super = True
            mario.reset_size = False


def check_mario_hit(screen, stats, sb, mario, enemies):
    """Respond to mario being hit by enemy."""
    collision = pygame.sprite.spritecollide(mario, enemies, False)
    if collision and mario.on_the_ground:
        play_sound("mario_die")
        mario.dead = True
        mario.large = False
        mario.reset_size = False
        mario.y_veloctiy = -6

        if stats.lives_left > 0:
            stats.lives_left -= 1
            sb.prep_lives()

    elif collision and not mario.on_the_ground:
        play_sound("mario_kick")
        mario.y_veloctiy = -3
        for enemy in collision:
            enemy.dead = True


def reset(background, stats, mario, enemies, blocks):
    """resets mario and enemies starting positions"""
    mario.dead = False
    mario.reset()
    for enemy in enemies:
        enemy.reset()
    background.reset()
    blocks.empty()

    stats.game_active = False
    pygame.mouse.set_visible(True)


def jump_super(mario):
    if mario.on_the_ground:
        play_sound("small_jump")
        mario.on_the_ground = False
        mario.y_veloctiy = -9.0


def jump_small(mario):
    if mario.y_veloctiy < -4.0:
        mario.y_veloctiy = -4.0


def load_high_scores(hs_file, game_stats):

    with open(hs_file) as f:
        game_stats.high_scores = f.read().splitlines()
        f.close()


def update_high_scores(game_stats):
    for num_score in range(len(game_stats.high_scores)):
        if game_stats.score >= int(game_stats.high_scores[num_score]):
            game_stats.high_scores[num_score] = game_stats.score
            break


def update_high_scores_file(hs_file, game_stats):
    with open(hs_file, 'w') as f:
        for num_scores in range(len(game_stats.high_scores)):
            f.write("{}\n".format(str(game_stats.high_scores[num_scores])))
        f.close()


def get_sprites():
    mario_ss_file = 'images/Mario_Spritesheet.png'
    star_mario_ss_file = 'images/Invincible Mario-1.png'
    enemies_ss_file = 'images/enemies.png'
    items_ss_file = 'images/Mushroom, Flower, Star, Question Block, Static Coin, Dynamic Coin.png'
    items2_ss_file = 'images/items.png'
    blocks_ss_file = 'images/OWBrick, OWFloor, UWFloor, HitTile.png'
    pipes_ss_file = 'images/Pipe.png'

    mario_ss = spritesheet.Spritesheet(mario_ss_file)

    star_mario_ss = spritesheet.Spritesheet(star_mario_ss_file)
    enemies_ss = spritesheet.Spritesheet(enemies_ss_file)
    items_ss = spritesheet.Spritesheet(items_ss_file)
    items2_ss = spritesheet.Spritesheet(items2_ss_file)
    blocks_ss = spritesheet.Spritesheet(blocks_ss_file)
    pipes_ss = spritesheet.Spritesheet(pipes_ss_file)

    large_regular_mario_images = []
    num_large_mario_sprites = 21
    width_large_mario_sprites = 17
    height_large_mario_sprites = 33
    for num in range(num_large_mario_sprites):
        x = num * width_large_mario_sprites
        rect = ((x, 0), (width_large_mario_sprites, height_large_mario_sprites))
        large_regular_mario_images.append(mario_ss.image_at(rect, -1))

    small_regular_mario_images = []
    num_small_mario_sprites = 14
    width_small_mario_sprites = 17
    height_small_mario_sprites = 17
    for num in range(num_small_mario_sprites):
        x = num * width_small_mario_sprites
        rect = ((x, 34), (width_small_mario_sprites, height_small_mario_sprites))
        small_regular_mario_images.append(mario_ss.image_at(rect, -1))

    large_star_mario_images = []
    for num in range(num_large_mario_sprites):
        x = num * width_large_mario_sprites
        rect = ((x, 0), (width_large_mario_sprites, height_large_mario_sprites))
        large_star_mario_images.append(star_mario_ss.image_at(rect, -1))

    small_star_mario_images = []
    for num in range(num_small_mario_sprites):
        x = num * width_small_mario_sprites
        rect = ((x, 34), (width_small_mario_sprites, height_small_mario_sprites))
        small_star_mario_images.append(star_mario_ss.image_at(rect, -1))


    goomba_images = [
        enemies_ss.image_at((0, 4, 16, 16), -1),
        enemies_ss.image_at((30, 4, 16, 16), -1),
        enemies_ss.image_at((60, 8, 16, 8), -1)
    ]


    turtle_images = []
    num_turtle_sprites = 10
    width_turtle_sprites = 17
    height_turtle_sprites = 24
    height_shell_sprites = 12
    for num in range(num_turtle_sprites):
        x = (num * (width_turtle_sprites + 13)) + 90
        if num < 8:
            rect = ((x, 0), (width_turtle_sprites, height_turtle_sprites))
        else:
            rect = ((x, 5), (width_turtle_sprites, height_shell_sprites))
        turtle_images.append(enemies_ss.image_at(rect, -1))

    mushroom_images = [
        items2_ss.image_at((0, 0, 16, 16), -1),
        items2_ss.image_at((16, 0, 16, 16), -1),
        items2_ss.image_at((32, 0, 16, 16), -1)
    ]
    mushroom_image = [items2_ss.image_at((184, 34, 16, 16), -1)]

    star_images = [
        items2_ss.image_at((4, 94, 16, 16), -1),
        items2_ss.image_at((34, 94, 16, 16), -1),
        items2_ss.image_at((64, 94, 16, 16), -1),
        items2_ss.image_at((94, 94, 16, 16), -1)
    ]

    question_block_images = [
        items_ss.image_at((0, 80, 16, 16), -1),
        items_ss.image_at((16, 80, 16, 16), -1),
        items_ss.image_at((32, 80, 16, 16), -1),
        items_ss.image_at((48, 80, 16, 16), -1),
        blocks_ss.image_at((47, 0, 16, 16), -1)
    ]

    static_coin_images = [
        items_ss.image_at((0, 96, 16, 16), -1),
        items_ss.image_at((16, 96, 16, 16), -1),
        items_ss.image_at((32, 96, 16, 16), -1),
        items_ss.image_at((48, 96, 16, 16), -1)
    ]

    dynamic_coin_images = [
        items_ss.image_at((0, 112, 16, 16), -1),
        items_ss.image_at((16, 112, 16, 16), -1),
        items_ss.image_at((32, 112, 16, 16), -1),
        items_ss.image_at((48, 112, 16, 16), -1)
    ]

    overworld_brick_images = [
        blocks_ss.image_at((16, 0, 16, 16), -1),
        blocks_ss.image_at((32, 0, 16, 16), -1)
    ]
    overworld_floor_image = [blocks_ss.image_at((0, 0, 16, 16), -1)]
    overworld_stair_image = [blocks_ss.image_at((0, 16, 16, 16))]

    underworld_brick_image = [blocks_ss.image_at((16, 32, 16, 16), -1)]
    underworld_floor_image = [blocks_ss.image_at((0, 32, 16, 16), -1)]

    pipe_image = [items_ss.image_at((48, 16, 16, 16), -1)]
    pipe_image[0].set_alpha(0)

    vertical_pipe_images = [
        pipes_ss.image_at((0, 0, 32, 32), -1),
        pipes_ss.image_at((0, 32, 32, 32), -1)
    ]

    horizontal_pipe_images = [
        pipes_ss.image_at((32, 0, 48, 32), -1),
        pipes_ss.image_at((32, 32, 48, 32), -1)
    ]

    return large_regular_mario_images, small_regular_mario_images, \
           large_star_mario_images, small_star_mario_images, \
           goomba_images, turtle_images, \
           mushroom_images, pipe_image, mushroom_image,question_block_images, \
           star_images, static_coin_images, dynamic_coin_images, \
           overworld_brick_images, overworld_floor_image, overworld_stair_image, \
           underworld_brick_image, underworld_floor_image, \
           vertical_pipe_images, horizontal_pipe_images
