import pygame, sys ,random
#tao ham cho game
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos+432, 650))
def create_pipe():
    random_piple_pos = random.choice(pipe_height)
    bottom_pile = pipe_surface.get_rect(midtop = (500,random_piple_pos))
    top_pile = pipe_surface.get_rect(midtop=(500, random_piple_pos-700))
    return bottom_pile, top_pile
def move_pipe(piles):
    for pile in piles:
        pile.centerx -= 5
    return piles
def draw_pile(piles):
    for pile in piles:
        if pile.bottom >= 600:
            screen.blit(pipe_surface,pile)
        else :
            flip_pile = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pile,pile)
def check_coliision(piles):
    for pile in piles:
        if bird_rect.colliderect(pile):
            hip_sound.play()
            return False
        if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            return False
    return  True
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,300))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface,high_score_rect)
def update_high_score(score,high_score):
    if score > high_score:
        high_score = score
    return  high_score
pygame.mixer.pre_init(frequency=44100,size=-16,channels=2,buffer=512)
pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)
#tao cac bien cho tro choi
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
#chèn brackground
background = pygame.image.load('assets/background-night.png').convert()
background = pygame.transform.scale2x(background)
#chèn floor
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
#tạo bird

bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down,bird_mid,bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,384))
#tao timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,200)
#tao ong
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
#tao timer cho ong
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200)
pipe_height = [200,300,400]
#tao giao dien endgame
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216,384))
#chen sound
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hip_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
#whileloop tro choi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key ==  pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -11
                flap_sound.play()
            if event.key ==  pygame.K_SPACE and game_active == False :
                game_active = True
                pipe_list.clear()
                bird_rect.center == (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
            print(create_pipe)
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
    screen.blit(background,(0,0))
    if game_active:
        #bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_coliision(pipe_list)
        #pile(ống)
        pipe_list = move_pipe(pipe_list)
        draw_pile(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_high_score(score,high_score)
        score_display('game over')
    #floor
    floor_x_pos  -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)
