import pygame
import sys
import os

# general settings
W, H = 640, 360
FPS = 60
GRAVITY = 0.8
JUMP = -12
SPEED = 3.5
ANIM_SPEED = 0.1
HUNGER_DECREMENT_TIME = 2.0
HUNGER_DECREMENT = 1
HUNGER_INCREMENT = 1
MAX_HUNGER_ICONS = 4

# game states
MENU = 0
START = 1
GAME = 2
WIN = 3
LOSE = 4

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("Agnis Adventure")
        self.clock = pygame.time.Clock()
        self.state = MENU
        self.camera = 0
        self.load_assets()
        # Hunger
        self.hunger = MAX_HUNGER_ICONS
        self.hunger_timer = 0

    def main(self):
        while True:
            dt = self.clock.tick(FPS) / 1000
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(event)

            if self.state == MENU:
                self.draw_menu()
            elif self.state == START:
                self.update_start(keys, dt)
                self.draw_start()
            elif self.state == GAME:
                self.update_game(keys, dt)
                self.update_hunger(dt)
                self.draw_game()
            elif self.state == WIN:
                self.screen.blit(self.bg_win, (0,0))
                self.btn_restart_win.draw(self.screen)
            elif self.state == LOSE:
                self.screen.blit(self.bg_lose, (0,0))
                self.btn_restart_lose.draw(self.screen)

            pygame.display.update()

    def load_assets(self):
        self.bg_menu = load_image("assets/ui/title_bg.png")
        self.bg_start = load_image("assets/backgrounds/start/bg_start_0.png")
        self.bg_dungeon = load_image("assets/backgrounds/dungeon/bg_dungeon_0.png")
        self.bg_win = load_image("assets/ui/win_bg.png")
        self.bg_lose = load_image("assets/ui/lose_bg.png")
        self.btn_start = Button(load_image("assets/ui/buttons/button_start.png"), (470, 274))
        self.btn_quit = Button(load_image("assets/ui/buttons/button_quit.png"), (470, 334))
        self.btn_restart_win = Button(load_image("assets/ui/buttons/button_restart.png"), (549, 191))
        self.btn_restart_lose = Button(load_image("assets/ui/buttons/button_restart.png"), (141, 199))
        self.start_ground = load_image("assets/platforms/start_ground.png")
        self.dungeon_ground = load_image("assets/platforms/dungeon_ground.png")
        p0 = load_image("assets/platforms/platform_0.png")
        p1 = load_image("assets/platforms/platform_1.png")
        self.platforms = [
            Platform(300, 150, p0),
            Platform(500, 110, p1),
            Platform(700, 170, p0)
        ]
        idle = load_image("assets/agnis/agnis/idle/agnis_idle_0.png")
        left_imgs = [load_image(f"assets/agnis/agnis/run_left/agnis_run_left00{i}.png") for i in range(4)]
        right_imgs = [load_image(f"assets/agnis/agnis/run_right/agnis_run_right00{i}.png") for i in range(4)]
        self.player = Player(idle, left_imgs, right_imgs)
        self.food_img = load_image("assets/agnis/food/food.png")
        self.foods = [
            Food(pl.rect.x + 55, pl.rect.y - 30, self.food_img)
            for pl in self.platforms
        ]

    # get ground y positions
    def start_ground_y(self):
        return H - self.start_ground.get_height()
    def dungeon_ground_y(self):
        return H - self.dungeon_ground.get_height()
    
    # event handler
    def handle_event(self, event):
        if self.state == MENU and event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_start.is_clicked(event.pos):
                self.enter_start()
            if self.btn_quit.is_clicked(event.pos):
                pygame.quit()
                sys.exit()
        if self.state in (WIN, LOSE) and event.type == pygame.MOUSEBUTTONDOWN:
            if (self.state == WIN and self.btn_restart_win.is_clicked(event.pos)) or \
               (self.state == LOSE and self.btn_restart_lose.is_clicked(event.pos)):
                self.reset()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.jump()
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

    def enter_start(self):
        self.state = START
        self.player.x = W // 2
        self.player.y = self.start_ground_y() - self.player.height
        self.player.vy = 0

    def enter_game(self):
        self.state = GAME
        self.player.x = 200
        self.player.y = 300
        self.player.vy = 0
        self.hunger = MAX_HUNGER_ICONS
        self.hunger_timer = 0
        for f in self.foods:
            f.collected = False

    def reset(self):
        self.state = MENU
        self.player.x = 200
        self.player.y = 200
        self.player.vy = 0

    # the function so the player can jump on top of the obstacle platforms
    def jump(self):
        p = self.player
        on_ground = p.vy == 0 and p.y >= self.start_ground_y() - p.height if self.state == START else p.vy == 0 and p.y >= self.dungeon_ground_y() - p.height
        if self.state == START and on_ground:
            p.vy = JUMP
        elif self.state == GAME:
            for pl in self.platforms:
                if (p.x + p.width > pl.rect.x and p.x < pl.rect.x + pl.rect.width and
                    abs(p.y + p.height - pl.rect.y) < 5 and p.vy >= 0):
                    p.vy = JUMP
            if on_ground:
                p.vy = JUMP

    def update_start(self, keys, dt):
        p = self.player
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]
        if left: p.x -= SPEED
        if right: p.x += SPEED
        p.x = max(0, min(p.x, W - p.width))

        p.vy += GRAVITY
        p.y += p.vy

        # after the starting area ground, the negative space right of it is where the player falls
        ground_y = self.start_ground_y() - p.height
        hole_x = W - 100
        if p.x + p.width < hole_x and p.y >= ground_y:
            p.y = ground_y
            p.vy = 0

        if 0 <= p.x <= W and 0 <= p.y <= H:
            p.animate(left, right, dt)

        if p.y > H:
            self.enter_game()

    def update_game(self, keys, dt):
        p = self.player
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]
        if left: p.x -= SPEED
        if right: p.x += SPEED
        p.x = max(0, min(p.x, self.bg_dungeon.get_width() - p.width))

        p.vy += GRAVITY
        p.y += p.vy

        # platform collisions
        for pl in self.platforms:
            if (p.x + p.width > pl.rect.x and p.x < pl.rect.x + pl.rect.width and
                p.y + p.height >= pl.rect.y and p.y + p.height <= pl.rect.y + 10 and p.vy >= 0):
                p.y = pl.rect.y - p.height
                p.vy = 0

        # floor collision
        floor_y = self.dungeon_ground_y() - p.height
        if p.y > floor_y:
            p.y = floor_y
            p.vy = 0

        # animate
        if 0 <= p.x <= self.bg_dungeon.get_width() and 0 <= p.y <= H:
            p.animate(left, right, dt)

            # collect food
            p_rect = pygame.Rect(p.x,p.y,p.width,p.height)
            for f in self.foods:
                if not f.collected and p_rect.colliderect(f.rect):
                    f.collected = True
                    if self.hunger < MAX_HUNGER_ICONS:
                        self.hunger += HUNGER_INCREMENT

        # camera follows player so you can see the map as the player moves
        self.camera = max(0, min(p.x - W//2, self.bg_dungeon.get_width() - W))

        # win/lose
        if p.x > self.bg_dungeon.get_width() - 100:
            self.state = WIN
        if p.y > H:
            self.state = LOSE

    # The hunger bar should deplete over time the longer the player goes without picking up food
    def update_hunger(self, dt):
        self.hunger_timer += dt
        if self.hunger_timer >= HUNGER_DECREMENT_TIME:
            self.hunger_timer = 0
            if self.hunger > 0:
                self.hunger -= HUNGER_DECREMENT
            if self.hunger <= 0:
                self.state = LOSE

    # draws the game state screens
    def draw_menu(self):
        self.screen.blit(self.bg_menu, (0,0))
        self.btn_start.draw(self.screen)
        self.btn_quit.draw(self.screen)

    def draw_start(self):
        self.screen.blit(self.bg_start, (0,0))
        self.screen.blit(self.start_ground, (0,self.start_ground_y()))
        self.player.draw(self.screen,0)

    def draw_game(self):
        self.screen.blit(self.bg_dungeon, (-self.camera,0))
        self.screen.blit(self.dungeon_ground, (-self.camera,self.dungeon_ground_y()))
        for pl in self.platforms:
            pl.draw(self.screen, self.camera)
        for f in self.foods:
            f.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

        for i in range(self.hunger):
            self.screen.blit(self.food_img, (50 + i*35, 10))
            
# Please try to commit more often

# helps to load images
BASE = os.path.dirname(os.path.abspath(__file__))
def load_image(path):
    return pygame.image.load(os.path.join(BASE, path)).convert_alpha()

# the button functions
class Button:
    def __init__(self, image, pos):
        self.image = image
        self.rect = image.get_rect(center=pos)
    # draw button onto the screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    # checks if the button was clicked
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# drawing the platform onto the screen
class Platform:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x - camera, self.rect.y))

# drawing the food onto the screen
class Food:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
        self.collected = False
    def draw(self, screen, camera):
        if not self.collected:
            screen.blit(self.image, (self.rect.x - camera, self.rect.y))

class Player:
    def __init__(self, idle_img, left_imgs, right_imgs):
        self.idle_img = idle_img
        self.left_imgs = left_imgs
        self.right_imgs = right_imgs

        self.x = 200
        self.y = 200
        self.vy = 0
        self.sprite_index = 0
        self.anim_timer = 0
        self.sprite = idle_img
        self.width = idle_img.get_width()
        self.height = idle_img.get_height()

    # animates the player when moving
    def animate(self, left, right, dt):
        if not left and not right:
            self.sprite = self.idle_img
            self.sprite_index = 0
            self.anim_timer = 0
            return
        images = self.left_imgs if left else self.right_imgs
        self.anim_timer += dt
        if self.anim_timer >= ANIM_SPEED:
            self.sprite_index = (self.sprite_index + 1) % len(images)
            self.anim_timer = 0
        self.sprite = images[self.sprite_index]
    # draws the player
    def draw(self, screen, camera):
        screen.blit(self.sprite, (self.x - camera, self.y))

def main():
    Game().main()

if __name__ == "__main__":
    main()
