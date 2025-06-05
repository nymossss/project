import pygame
import sys
import math
import os
import time
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mortal Kombat Sub-Zero")

# Инициализация звука
pygame.mixer.init()
try:
    chill_music = pygame.mixer.Sound(r"C:\\Users\\User\\Desktop\\проект\\obm.mp3")  
    battle_music = pygame.mixer.Sound(r"C:\\Users\\User\\Desktop\\проект\\battle.mp3")  
    music_loaded = True
except:
    print("Музыкальные файлы не найдены")
    music_loaded = False

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
light_blue = (0, 191, 255)
skin_color = (255, 224, 189)
menu_color = (56, 81, 105)
button_color = (100, 100, 100) #FIGHT
red = (255, 0, 0)

# ИЗОБРАЖЕНИЯ
try:
    r1_bg = pygame.image.load(r"C:\\\Users\User\\Desktop\\проект\\ds.jpg").convert()
    r1_bg = pygame.transform.scale(r1_bg, (width, height))
except:
    r1_bg = pygame.Surface((width, height))
    r1_bg.fill((250, 0, 0))

try:
    # r2_bg = pygame.image.load(r"C:\\Users\\User\\Desktop\\проект\sm.jpg").convert()
    r2_bg = pygame.image.load(r"C:\\Users\\User\\Desktop\\проект\\ddd.jpg").convert()
    r2_bg = pygame.transform.scale(r2_bg, (width, height))
except:
    r2_bg = pygame.Surface((width, height))
    r2_bg.fill((0, 0, 250))

try:
    r3_bg = pygame.image.load(r"C:\\Users\\User\\Desktop\\проект\\zzz.jpg").convert()
    r3_bg = pygame.transform.scale(r3_bg, (width, height))
except:
    r3_bg = pygame.Surface((width, height))
    r3_bg.fill((0, 250, 0))

try:
    defeat_img = pygame.image.load(r"C:\\Users\\User\\Desktop\\проект\\rrr.png").convert()
    defeat_img = pygame.transform.scale(defeat_img, (width, height))
except:
    defeat_img = pygame.Surface((width, height))
    defeat_img.fill((255, 0, 0))

try:
    victory_img = pygame.image.load(r"C:\\Users\\User\\Desktop\\проект\\ttt.jpg").convert()
    victory_img = pygame.transform.scale(victory_img, (width, height))
except:
    victory_img = pygame.Surface((width, height))
    victory_img.fill((0, 255, 0))

current_bg = None
game_started = False
battle_mode = True  # Сразу начинаем в режиме боя
showing_video = False
video_finished = False
game_over = False
victory = False

# Позиция персонажа
character_x = 400
character_y = 300
speed = 3
is_moving_left_right = False

# Параметры анимации
right_arm_angle = 0
left_arm_angle = 0
arm_rotation_speed = 0.1
leg_animation_angle = 0
leg_animation_speed = 0.3

# Параметры для ударов
punching = False
punch_angle = 0
punch_speed = 0.2
punch_duration = 30
punch_frame = 0

# Параметры для шаров
fireballs = []
blue_fireballs = []
red_fireballs = []
fireball_speed = 10
fireball_radius = 15
fireball_color = (255, 100, 0)
blue_fireball_color = (0, 100, 255)
red_fireball_color = (255, 50, 50)
fireball_lifetime = 5
last_red_fireball_time = 0
red_fireball_interval = 3

# Параметры здоровья
health = 100
max_health = 100
hit_cooldown = 0
hit_cooldown_duration = 1

# Параметры шкалы попаданий
hit_counter = 0
max_hits = 5
hit_bar_width = 200
hit_bar_height = 20
hit_bar_x = width // 2 - hit_bar_width // 2
hit_bar_y = 10

clock = pygame.time.Clock()

def reset_game():
    global character_x, character_y, health, hit_counter, fireballs, blue_fireballs, red_fireballs
    character_x = 400
    character_y = 300
    health = 100
    hit_counter = 0
    fireballs = []
    blue_fireballs = []
    red_fireballs = []

def draw_menu():
    screen.blit(r3_bg, (0, 0))
    
    menu_overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    menu_overlay.fill((0, 0, 0, 180))
    screen.blit(menu_overlay, (0, 0))
    
    font = pygame.font.SysFont('Arial Black', 60)
    title = font.render('MORTAL KOMBAT', True, white)
    screen.blit(title, (width//2 - title.get_width()//2, 100))
    
    sub_font = pygame.font.SysFont('Arial Black', 30)
    sub_title = sub_font.render('Начать игру', True, (200, 200, 200))
    screen.blit(sub_title, (width//2 - sub_title.get_width()//2, 170))
    
    button_bg = pygame.Surface((240, 100), pygame.SRCALPHA)
    button_bg.fill((50, 50, 50, 200))
    screen.blit(button_bg, (width//2 - 120, 220))
    
    pygame.draw.rect(screen, button_color, (width//2 - 100, 240, 200, 60))
    loc1_text = pygame.font.SysFont('Arial Black', 30).render('FIGHT', True, white)
    screen.blit(loc1_text, (width//2 - loc1_text.get_width()//2, 255))
    
    controls_font = pygame.font.SysFont('Arial', 16)
    controls_text = controls_font.render('Управление в бою Q - выстрел вправо, E - выстрел вверх', True, (150, 150, 150))
    screen.blit(controls_text, (width//2 - controls_text.get_width()//2, height - 50))
    
    pygame.display.flip()

def draw_game_over_menu():
    screen.blit(defeat_img, (0, 0))
    
    menu_overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    menu_overlay.fill((0, 0, 0, 180))
    screen.blit(menu_overlay, (0, 0))
    
    font = pygame.font.SysFont('Arial Black', 60)
    title = font.render('GAME OVER', True, white)
    screen.blit(title, (width//2 - title.get_width()//2, 100))
    
    button_bg = pygame.Surface((240, 200), pygame.SRCALPHA)
    button_bg.fill((50, 50, 50, 200))
    screen.blit(button_bg, (width//2 - 120, 220))
    
    pygame.draw.rect(screen, button_color, (width//2 - 100, 240, 200, 60))
    retry_text = pygame.font.SysFont('Arial Black', 30).render('Replay', True, white)
    screen.blit(retry_text, (width//2 - retry_text.get_width()//2, 255))
    
    pygame.draw.rect(screen, button_color, (width//2 - 100, 320, 200, 60))
    chill_text = pygame.font.SysFont('Arial Black', 30).render('сhill', True, white)
    screen.blit(chill_text, (width//2 - chill_text.get_width()//2, 335))
    
    pygame.display.flip()

def draw_sub_zero(x, y, right_angle, left_angle, battle_mode=False, is_punching=False, punch_progress=0):
    # Инициализация смещений
    left_offset = 0
    right_offset = 0
    
    if battle_mode and is_punching:
        punch_offset = punch_progress * 40
        pygame.draw.rect(screen, skin_color, (x + 68 + punch_offset, y + 55, 20, 26))
        pygame.draw.rect(screen, skin_color, (x + 75 + punch_offset, y + 70, 40, 20))
        pygame.draw.ellipse(screen, skin_color, (x + 140 + punch_offset, y + 73, 25, 14))
        pygame.draw.polygon(screen, black, [
            (x + 113 + punch_offset, y + 90), 
            (x + 113 + punch_offset, y + 70), 
            (x + 150 + punch_offset, y + 85)])
        pygame.draw.polygon(screen, black, [
            (x + 150 + punch_offset, y + 90), 
            (x + 150 + punch_offset, y + 70), 
            (x + 117 + punch_offset, y + 85)])
    else:
        right_offset = math.sin(right_angle) * 15
        left_offset = math.sin(left_angle) * 15
        
        pygame.draw.rect(screen, skin_color, (x + 68, y + 55 + right_offset*0.5, 20, 26))
        pygame.draw.rect(screen, skin_color, (x + 75, y + 70 + right_offset*0.5, 20, 56)) 
        pygame.draw.ellipse(screen, skin_color, (x + 73, y + 145 + right_offset*0.5, 16, 25))
        pygame.draw.polygon(screen, black, [
            (x + 94, y + 125 + right_offset*0.5),
            (x + 74, y + 125 + right_offset*0.5),
            (x + 84, y + 150 + right_offset*0.5)])
        pygame.draw.polygon(screen, black, [
            (x + 90, y + 155 + right_offset*0.5),
            (x + 71, y + 155 + right_offset*0.5),
            (x + 84, y + 129 + right_offset*0.5)])
    
    # Левая рука (всегда обычная анимация)
    left_offset = math.sin(left_angle) * 15
    pygame.draw.rect(screen, skin_color, (x - 50 + left_offset*0.2, y + 55, 20, 70))
    
    # Остальные элементы тела
    pygame.draw.rect(screen, skin_color, (x - 15, y + 70, 15, 15))
    pygame.draw.polygon(screen, black, [(x - 15, y + 70), (x - 30, y + 70), (x - 15, y + 85)])
    pygame.draw.polygon(screen, black, [(x - 15, y + 85), (x - 30, y + 85), (x - 15, y + 100)])
    
    # Голова
    pygame.draw.polygon(screen, black, [(x + 20, y - 1), (x + 51, y + 50), (x, y + 50)])
    pygame.draw.circle(screen, black, (x + 34, y + 10), 25)
    pygame.draw.rect(screen, skin_color, (x + 33, y + 9, 25, 16))
    pygame.draw.polygon(screen, light_blue, [(x + 28, y + 19), (x + 60, y + 19), (x + 48, y + 52)])
    pygame.draw.rect(screen, black, (x + 18, y + 19, 16, 16))

    # Торс
    pygame.draw.polygon(screen, light_blue, [(x - 50, y + 50), (x + 90, y + 50), (x + 18, y + 170)])
    pygame.draw.polygon(screen, black, [(x - 10, y + 50), (x + 50, y + 50), (x + 20, y + 170)])
    
    pygame.draw.ellipse(screen, skin_color, (x + 2 + left_offset*0.3, y + 99 + left_offset*0.5, 25, 18))
    pygame.draw.polygon(screen, black, [
            (x + 8 + left_offset*0.3, y + 95 + left_offset*0.5), 
            (x + 13 + left_offset*0.3, y + 120 + left_offset*0.5), 
            (x - 16 + left_offset*0.3, y + 116 + left_offset*0.5)])
    pygame.draw.polygon(screen, black, [
            (x - 40 + left_offset*0.3, y + 105 + left_offset*0.5), 
            (x - 28 + left_offset*0.3, y + 130 + left_offset*0.5), 
            (x + left_offset*0.3, y + 115 + left_offset*0.5)])

def draw_legs(screen, x, y, color_leg, color_joint, color_foot, color_belt, dance_angle=0, battle_mode=False):
    dance_offset = math.sin(dance_angle) * 10 if (is_moving_left_right and not battle_mode) else 0
    
    pygame.draw.polygon(screen, black, [
        (x + 13 - dance_offset*0.3, y + 153), 
        (x + 40 - dance_offset*0.3, y + 145), 
        (x + 64 - dance_offset, y + 250 + dance_offset*0.5)])
    
    pygame.draw.polygon(screen, black, [
        (x + 40 - dance_offset*0.3, y + 145), 
        (x + 64 - dance_offset, y + 250 + dance_offset*0.5), 
        (x + 80 - dance_offset, y + 242 + dance_offset*0.5)])
    
    pygame.draw.polygon(screen, black, [
        (x + dance_offset*0.3, y + 147), 
        (x + 24 + dance_offset*0.3, y + 150), 
        (x - 38 + dance_offset, y + 250 - dance_offset*0.5)])
    
    pygame.draw.polygon(screen, black, [
        (x - 1 + dance_offset*0.3, y + 147), 
        (x - 38 + dance_offset, y + 250 - dance_offset*0.5), 
        (x - 55 + dance_offset, y + 235 - dance_offset*0.5)])
    
    pygame.draw.rect(screen, light_blue, (x + 60 - dance_offset, y + 240 + dance_offset*0.3, 19, 63))
    pygame.draw.rect(screen, light_blue, (x - 50 + dance_offset, y + 240 - dance_offset*0.3, 19, 63))
    
    pygame.draw.ellipse(screen, (2, 165, 219), (x + 56, y + 220 + dance_offset*0.2, 26, 31))
    pygame.draw.ellipse(screen, (2, 165, 219), (x - 55, y + 220 + dance_offset*0.2, 26, 31))
    
    pygame.draw.rect(screen, color_belt, (x - 8, y + 140, 54, 19))
    pygame.draw.rect(screen, color_belt, (x - 6, y + 157, 50, 70))
    
    pygame.draw.rect(screen, black, (x + 60 + dance_offset, y + 303 + dance_offset*0.2, 25, 15))
    pygame.draw.rect(screen, black, (x - 50 + dance_offset, y + 303 + dance_offset*0.2, 25, 15))

def draw_health_bar():
    bar_width = 200
    bar_height = 20
    bar_x = width - bar_width - 20
    bar_y = 20
    
    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
    
    health_width = (health / max_health) * bar_width
    health_color = (0, 255, 0) if health > max_health * 0.5 else (255, 165, 0) if health > max_health * 0.2 else (255, 0, 0)
    pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
    
    pygame.draw.rect(screen, white, (bar_x, bar_y, bar_width, bar_height), 2)
    
    font = pygame.font.SysFont('Arial', 16)
    health_text = font.render(f'HP {health}/{max_health}', True, white)
    screen.blit(health_text, (bar_x + bar_width//2 - health_text.get_width()//2, bar_y + bar_height//2 - health_text.get_height()//2))

def draw_hit_bar():
    pygame.draw.rect(screen, (50, 50, 50), (hit_bar_x, hit_bar_y, hit_bar_width, hit_bar_height))
    
    hit_width = (hit_counter / max_hits) * hit_bar_width
    hit_color = (0, 200, 255)
    pygame.draw.rect(screen, hit_color, (hit_bar_x, hit_bar_y, hit_width, hit_bar_height))
    
    pygame.draw.rect(screen, white, (hit_bar_x, hit_bar_y, hit_bar_width, hit_bar_height), 2)
    
    font = pygame.font.SysFont('Arial', 16)
    hit_text = font.render(f'HITS {hit_counter}/{max_hits}', True, white)
    screen.blit(hit_text, (hit_bar_x + hit_bar_width//2 - hit_text.get_width()//2, hit_bar_y + hit_bar_height//2 - hit_text.get_height()//2))

# Основной цикл
running = True
while running:
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not game_started and not showing_video:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if width//2 - 100 <= mouse_pos[0] <= width//2 + 100 and 240 <= mouse_pos[1] <= 300:
                    current_bg = r1_bg
                    game_started = True
                    battle_mode = True
                    if music_loaded:
                        pygame.mixer.stop()
                        battle_music.play(-1)
        
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if width//2 - 100 <= mouse_pos[0] <= width//2 + 100 and 240 <= mouse_pos[1] <= 300:
                # Повторить
                reset_game()
                game_over = False
                battle_mode = True
                current_bg = r1_bg
                if music_loaded:
                    pygame.mixer.stop()
                    battle_music.play(-1)
            elif width//2 - 100 <= mouse_pos[0] <= width//2 + 100 and 320 <= mouse_pos[1] <= 380:
                reset_game()
                game_over = False
                battle_mode = False
                current_bg = r2_bg
                if music_loaded:
                    pygame.mixer.stop()
                    chill_music.play(-1)
        
        if game_started and battle_mode and event.type == pygame.KEYDOWN and not showing_video and not game_over:
            if event.key == pygame.K_q and not punching:
                punching = True
                punch_frame = 0
                blue_fireballs.append({
                    'x': character_x + 150,
                    'y': character_y - 30,
                    'direction_x': 1,
                    'direction_y': 0,
                    'creation_time': current_time
                })
            
            if event.key == pygame.K_e and not punching:
                punching = True
                punch_frame = 0
                blue_fireballs.append({
                    'x': character_x + 50,
                    'y': character_y - 100,
                    'direction_x': 0,
                    'direction_y': -1,
                    'creation_time': current_time
                })
    
    if not game_started:
        draw_menu()
        continue

    if game_over:
        draw_game_over_menu()
        continue

    # Управление персонажем
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not showing_video and not game_over:
        character_x -= speed
    if keys[pygame.K_RIGHT] and not showing_video and not game_over:
        character_x += speed
    if keys[pygame.K_UP] and not battle_mode and not showing_video and not game_over:
        character_y -= speed
    if keys[pygame.K_DOWN] and not battle_mode and not showing_video and not game_over:
        character_y += speed
    
    # Анимация удара рукой
    if punching:
        punch_frame += 1
        if punch_frame >= punch_duration:
            punching = False
    
    # Расчет прогресса удара рукой
    punch_progress = 0
    if punching:
        if punch_frame < punch_duration / 2:
            punch_progress = punch_frame / (punch_duration / 2)
        else:
            punch_progress = 1 - (punch_frame - punch_duration / 2) / (punch_duration / 2)
    
    # Генерация красных шаров
    if battle_mode and current_time - last_red_fireball_time > red_fireball_interval:
        last_red_fireball_time = current_time
        red_fireball_interval = random.uniform(1.5, 3.5)
        
        red_fireballs.append({
            'x': random.randint(width - 300, width - 50),
            'y': -50,
            'direction_x': (character_x - (width - 100)) / 80,
            'direction_y': (character_y + 100) / 100,
            'creation_time': current_time
        })
    
    # Обновление позиций шаров
    for fireball in fireballs[:]:
        fireball['x'] += fireball_speed * fireball['direction']
        character_rect = pygame.Rect(character_x - 100, character_y - 50, 200, 350)
        fireball_rect = pygame.Rect(fireball['x'] - fireball_radius, fireball['y'] - fireball_radius, 
                                  fireball_radius*2, fireball_radius*2)
        
        if character_rect.colliderect(fireball_rect) or current_time - fireball['creation_time'] > fireball_lifetime:
            fireballs.remove(fireball)
    
    for fireball in blue_fireballs[:]:
        fireball['x'] += fireball_speed * fireball['direction_x']
        fireball['y'] += fireball_speed * fireball['direction_y']
        
        if fireball['x'] > width or fireball['y'] < 0 or current_time - fireball['creation_time'] > fireball_lifetime:
            blue_fireballs.remove(fireball)
    
    for fireball in red_fireballs[:]:
        fireball['x'] += fireball['direction_x']
        fireball['y'] += fireball['direction_y']
        
        fireball_rect = pygame.Rect(fireball['x'] - fireball_radius, fireball['y'] - fireball_radius, 
                                  fireball_radius*2, fireball_radius*2)
        
        for blue_fireball in blue_fireballs[:]:
            blue_rect = pygame.Rect(blue_fireball['x'] - fireball_radius, blue_fireball['y'] - fireball_radius, 
                                  fireball_radius*2, fireball_radius*2)
            
            if fireball_rect.colliderect(blue_rect):
                hit_counter += 1
                if hit_counter >= max_hits:
                    hit_counter = max_hits
                
                try:
                    red_fireballs.remove(fireball)
                    blue_fireballs.remove(blue_fireball)
                except:
                    pass
                break
        
        character_rect = pygame.Rect(character_x - 50, character_y - 50, 100, 150)
        if fireball_rect.colliderect(character_rect) and current_time > hit_cooldown:
            health -= 10
            hit_cooldown = current_time + hit_cooldown_duration
            try:
                red_fireballs.remove(fireball)
            except:
                pass
        
        if fireball['y'] > height or current_time - fireball['creation_time'] > fireball_lifetime:
            try:
                red_fireballs.remove(fireball)
            except:
                pass
    
    # Анимация ног
    is_moving_left_right = (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and not battle_mode and not showing_video and not game_over
    if is_moving_left_right:
        leg_animation_angle += leg_animation_speed
    
    # Управление руками
    if not battle_mode and not showing_video and not game_over:
        if keys[pygame.K_w]:
            right_arm_angle += arm_rotation_speed
        if keys[pygame.K_s]:
            right_arm_angle -= arm_rotation_speed
        if keys[pygame.K_a]:
            left_arm_angle += arm_rotation_speed
        if keys[pygame.K_d]:
            left_arm_angle -= arm_rotation_speed
    
    # Ограничение движения
    character_x = max(100, min(width - 100, character_x))
    character_y = max(50, min(height - 200, character_y))
    
    # Проверка здоровья
    if health <= 0 and not game_over:
        health = 0
        game_over = True
        if music_loaded:
            pygame.mixer.stop()
    
    # Отрисовка
    if not game_over:
        screen.blit(current_bg, (0, 0))
        
        # Отрисовка шаров
        for fireball in fireballs:
            pygame.draw.circle(screen, fireball_color, (int(fireball['x']), int(fireball['y'])), fireball_radius)
            pygame.draw.circle(screen, (255, 200, 100), (int(fireball['x']), int(fireball['y'])), fireball_radius - 5)
            pygame.draw.circle(screen, (255, 255, 200), (int(fireball['x']), int(fireball['y'])), fireball_radius - 10)
        
        for fireball in blue_fireballs:
            pygame.draw.circle(screen, blue_fireball_color, (int(fireball['x']), int(fireball['y'])), fireball_radius)
            pygame.draw.circle(screen, (100, 200, 255), (int(fireball['x']), int(fireball['y'])), fireball_radius - 5)
            pygame.draw.circle(screen, (200, 230, 255), (int(fireball['x']), int(fireball['y'])), fireball_radius - 10)
        
        for fireball in red_fireballs:
            pygame.draw.circle(screen, red_fireball_color, (int(fireball['x']), int(fireball['y'])), fireball_radius)
            pygame.draw.circle(screen, (255, 150, 50), (int(fireball['x']), int(fireball['y'])), fireball_radius - 5)
            pygame.draw.circle(screen, (255, 200, 100), (int(fireball['x']), int(fireball['y'])), fireball_radius - 10)
        
        # Отрисовка персонажа
        draw_sub_zero(character_x - 100, character_y - 50, right_arm_angle, left_arm_angle, battle_mode, punching, punch_progress)
        draw_legs(screen, character_x - 100, character_y - 50, black, light_blue, black, light_blue, leg_animation_angle, battle_mode)
        
        if battle_mode:
            draw_health_bar()
            draw_hit_bar()
        
        if hit_counter >= max_hits:
            screen.blit(victory_img, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            battle_mode = False
            current_bg = r2_bg
            hit_counter = 0
            if music_loaded:
                pygame.mixer.stop()
                chill_music.play(-1)
    
    pygame.display.flip()
    clock.tick(60)

if music_loaded:
    pygame.mixer.stop()
pygame.quit()
sys.exit()