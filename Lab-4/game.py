import pygame
import random
import math
import time

WIDTH, HEIGHT = 800, 560
FPS = 60
BG = (30,35,25)

class Zombie:
    SPEED = 1.5

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = (60,140,60)
        self.hp = 3
        self.wobble = random.uniform(0, 6.28)
        self.frame = 0

    def update(self, player_pos):
        px, py = player_pos
        cx, cy = self.rect.center
        dx, dy = px-cx, py-cy
        dist = (dx**2+dy**2)**0.5
        if dist:
            self.rect.x += int(dx/dist*self.SPEED)
            self.rect.y += int(dy/dist*self.SPEED)
        self.frame += 1

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

    def draw(self, screen):
        wobble_y = int(math.sin(self.frame*0.2)*3)
        draw_rect = self.rect.move(0, wobble_y)
        pygame.draw.rect(screen, self.color, draw_rect, border_radius=5)
        for ex in [draw_rect.x+6, draw_rect.x+18]:
            pygame.draw.circle(screen, (200,40,40), (ex, draw_rect.y+10), 4)


# TASK 4: Fast Zombie
class FastZombie(Zombie):
    SPEED = 3.0

    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, 20, 20)
        self.hp = 1


# TASK 4: Tank Zombie
class TankZombie(Zombie):
    SPEED = 0.75

    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, 44, 44)
        self.hp = 6


def spawn_zombie(width, height, player_rect, margin=120, zombie_type="standard"):
    if zombie_type == "fast":
        size = 20
    elif zombie_type == "tank":
        size = 44
    else:
        size = 30

    while True:
        x = random.randint(0, width-size)
        y = random.randint(0, height-size)
        rect = pygame.Rect(x, y, size, size)

        if not rect.colliderect(player_rect.inflate(margin, margin)):
            if zombie_type == "fast":
                return FastZombie(x, y)
            elif zombie_type == "tank":
                return TankZombie(x, y)
            else:
                return Zombie(x, y)


SPEED = 4


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = (60,160,220)
        self.bullets = []
        self.shoot_cooldown = 0

        # TASK 1: Health
        self.hp = 3
        self.max_hp = 3
        self.invincibility_timer = 0
        self.invincibility_duration = 60

        # TASK 2: Ammo and reload
        self.max_ammo = 12
        self.ammo = 12
        self.reload_duration = 2 * FPS
        self.reload_timer = 0

    def move(self, keys, width, height):
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]: dx = 0; dy = -SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dx = 0; dy = SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx = -SPEED; dy = 0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = SPEED; dy = 0

        self.rect.x = max(0, min(width-self.rect.width, self.rect.x+dx))
        self.rect.y = max(0, min(height-self.rect.height, self.rect.y+dy))

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # TASK 1: Invincibility timer
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        # TASK 2: Reload timer
        if self.reload_timer > 0:
            self.reload_timer -= 1

            if self.reload_timer <= 0:
                self.ammo = self.max_ammo

    def shoot(self, target_pos):
        # TASK 2: Cannot shoot while reloading or when magazine is empty
        if self.reload_timer > 0:
            return

        if self.ammo <= 0:
            self.reload_timer = self.reload_duration
            return

        if self.shoot_cooldown > 0:
            return

        cx, cy = self.rect.center
        tx, ty = target_pos
        dx, dy = tx-cx, ty-cy
        dist = (dx**2+dy**2)**0.5

        if dist == 0:
            return

        vx, vy = dx/dist*10, dy/dist*10

        self.bullets.append(pygame.Rect(cx-4, cy-4, 8, 8))
        self.bullets.append([cx-4, cy-4, vx, vy])
        self.bullets.pop(-2)

        self.shoot_cooldown = 15

        # TASK 2: Consume one bullet
        self.ammo -= 1

        # Automatically start reload when magazine becomes empty
        if self.ammo == 0:
            self.reload_timer = self.reload_duration

    def update_bullets(self, width, height):
        live = []

        for b in self.bullets:
            b[0] += b[2]
            b[1] += b[3]

            if 0 <= b[0] <= width and 0 <= b[1] <= height:
                live.append(b)

        self.bullets = live

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)

        for b in self.bullets:
            pygame.draw.circle(
                screen,
                (255,220,60),
                (int(b[0]), int(b[1])),
                5
            )


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zombie Escape")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 24)
        self.big_font = pygame.font.SysFont("monospace", 44, bold=True)
        self.reset()

    def reset(self):
        self.player = Player(WIDTH//2, HEIGHT//2)

        # Original initial zombies remain standard zombies
        self.zombies = [
            spawn_zombie(WIDTH, HEIGHT, self.player.rect)
            for _ in range(4)
        ]

        self.score = 0
        self.wave = 1
        self.kills = 0
        self.kills_to_next = 8
        self.game_over = False
        self.start_time = time.time()

        # TASK 3: Four barrels
        self.barrels = [
            pygame.Rect(100, 100, 28, 28),
            pygame.Rect(WIDTH-128, 100, 28, 28),
            pygame.Rect(100, HEIGHT-128, 28, 28),
            pygame.Rect(WIDTH-128, HEIGHT-128, 28, 28)
        ]

        # TASK 3: Active explosion effects
        self.explosions = []

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                self.player.shoot(event.pos)

        return True

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()

        self.player.move(keys, WIDTH, HEIGHT)
        self.player.update_bullets(WIDTH, HEIGHT)

        self.score = int(time.time() - self.start_time)

        # TASK 3: Update explosion effects
        for explosion in self.explosions[:]:
            explosion[2] -= 1

            if explosion[2] <= 0:
                self.explosions.remove(explosion)

        # Zombie movement and player collision
        for z in self.zombies:
            z.update(self.player.rect.center)

            if z.rect.colliderect(self.player.rect):

                # TASK 1: Player takes damage only when not invincible
                if self.player.invincibility_timer <= 0:

                    self.player.hp -= 1

                    # Brief invincibility after being hit
                    self.player.invincibility_timer = (
                        self.player.invincibility_duration
                    )

                    # Game over only when HP reaches zero
                    if self.player.hp <= 0:
                        self.player.hp = 0
                        self.game_over = True

        dead = []

        # Bullet collision
        for z in self.zombies:

            for b in self.player.bullets[:]:

                bx, by = int(b[0]), int(b[1])

                # TASK 3: Check if bullet hits a barrel
                barrel_hit = None

                for barrel in self.barrels:
                    if barrel.collidepoint(bx, by):
                        barrel_hit = barrel
                        break

                if barrel_hit is not None:

                    # Remove bullet
                    if b in self.player.bullets:
                        self.player.bullets.remove(b)

                    # Remove barrel
                    self.barrels.remove(barrel_hit)

                    explosion_center = barrel_hit.center
                    explosion_radius = 100

                    # Add explosion animation
                    self.explosions.append([
                        explosion_center,
                        explosion_radius,
                        20
                    ])

                    # Destroy all zombies inside explosion radius
                    for explosion_zombie in self.zombies[:]:

                        zx, zy = explosion_zombie.rect.center
                        ex, ey = explosion_center

                        distance = math.sqrt(
                            (zx-ex)**2 + (zy-ey)**2
                        )

                        if distance <= explosion_radius:

                            if explosion_zombie in self.zombies:
                                self.zombies.remove(explosion_zombie)

                            self.kills += 1
                            self.score += 10

                    # This bullet is already consumed
                    break

                # Normal zombie bullet collision
                if z.rect.collidepoint(bx, by):

                    if z.hit():
                        dead.append(z)

                    if b in self.player.bullets:
                        self.player.bullets.remove(b)

        # Remove zombies killed by normal bullets
        for z in dead:
            if z in self.zombies:
                self.zombies.remove(z)
                self.kills += 1
                self.score += 10

        # TASK 4: Wave progression with mixed zombie types
        if self.kills >= self.kills_to_next:

            self.kills = 0
            self.wave += 1
            self.kills_to_next = 8 + self.wave * 2

            for i in range(self.wave + 3):

                if i % 3 == 1:
                    zombie_type = "fast"

                elif i % 3 == 2:
                    zombie_type = "tank"

                else:
                    zombie_type = "standard"

                self.zombies.append(
                    spawn_zombie(
                        WIDTH,
                        HEIGHT,
                        self.player.rect,
                        zombie_type=zombie_type
                    )
                )

    def draw(self):
        self.screen.fill(BG)

        # Original background grid
        for x in range(0, WIDTH, 60):
            pygame.draw.line(
                self.screen,
                (40,45,35),
                (x,0),
                (x,HEIGHT),
                1
            )

        for y in range(0, HEIGHT, 60):
            pygame.draw.line(
                self.screen,
                (40,45,35),
                (0,y),
                (WIDTH,y),
                1
            )

        # TASK 3: Draw remaining barrels
        for barrel in self.barrels:
            pygame.draw.rect(
                self.screen,
                (150,90,30),
                barrel,
                border_radius=4
            )

        # TASK 3: Draw explosion effects
        for explosion in self.explosions:

            center, radius, timer = explosion

            progress = timer / 20
            current_radius = max(5, int(radius * (1 - progress)))

            pygame.draw.circle(
                self.screen,
                (255,140,30),
                center,
                current_radius,
                4
            )

            pygame.draw.circle(
                self.screen,
                (255,220,60),
                center,
                max(3, current_radius // 2),
                2
            )

        # Original zombie drawing
        for z in self.zombies:
            z.draw(self.screen)

        # Original player drawing
        self.player.draw(self.screen)

        # HUD
        hud_bg = pygame.Rect(0, 0, WIDTH, 40)

        pygame.draw.rect(
            self.screen,
            (15,20,15),
            hud_bg
        )

        # TASK 1 + TASK 2: HP and ammo shown in HUD
        if self.player.reload_timer > 0:

            reload_seconds = self.player.reload_timer / FPS

            ammo_text = (
                f"Reloading: {reload_seconds:.1f}s"
            )

        else:

            ammo_text = (
                f"Ammo: {self.player.ammo}/{self.player.max_ammo}"
            )

        hud = self.font.render(
            f"Wave: {self.wave}  "
            f"Score: {self.score}  "
            f"Kills: {self.kills}/{self.kills_to_next}  "
            f"HP: {self.player.hp}/{self.player.max_hp}  "
            f"{ammo_text}  |  "
            f"WASD Move, Click Shoot, R Restart",
            True,
            (160,220,120)
        )

        self.screen.blit(hud, (8, 8))

        # Original game-over screen
        if self.game_over:

            ov = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            ov.fill((0,0,0,160))

            self.screen.blit(
                ov,
                (0,0)
            )

            m = self.big_font.render(
                "DEVOURED!",
                True,
                (180,40,40)
            )

            s = self.font.render(
                f"Wave {self.wave} | Score {self.score} | Press R",
                True,
                (200,200,200)
            )

            self.screen.blit(
                m,
                (
                    WIDTH//2-m.get_width()//2,
                    HEIGHT//2-40
                )
            )

            self.screen.blit(
                s,
                (
                    WIDTH//2-s.get_width()//2,
                    HEIGHT//2+20
                )
            )

        pygame.display.flip()

    def run(self):
        running = True

        while running:

            running = self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    engine = GameEngine()
    engine.run()