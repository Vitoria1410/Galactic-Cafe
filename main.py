
import pygame
import random
import math
import sys
from settings import *

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Snack Bar - Estação Espacial L0-F1")
clock = pygame.time.Clock()

# --- SPRITES / DRAWING HELPERS ---
def draw_pixel_alien(surface, x, y, type_name):
    """Draws a simple pixel-art style alien based on type."""
    if type_name == "mushroom":
        # Cap
        pygame.draw.ellipse(surface, HOT_PINK, (x-25, y-30, 50, 40))
        # Stem
        pygame.draw.rect(surface, WHITE, (x-10, y, 20, 20))
        # Eyes
        pygame.draw.circle(surface, BLACK, (x-8, y-5), 3)
        pygame.draw.circle(surface, BLACK, (x+8, y-5), 3)
    elif type_name == "cyborg":
        # Head
        pygame.draw.rect(surface, GRAY, (x-20, y-25, 40, 40))
        # Glowing eye
        pygame.draw.rect(surface, (255, 0, 0), (x-10, y-15, 20, 5))
        # Antenna
        pygame.draw.line(surface, WHITE, (x, y-25), (x, y-35), 2)
    elif type_name == "tentacles":
        # Body
        pygame.draw.ellipse(surface, CYAN_NEON, (x-20, y-30, 40, 40))
        # Tentacles
        for i in range(3):
            offset = (i-1) * 15
            pygame.draw.line(surface, CYAN_NEON, (x+offset, y), (x+offset + math.sin(pygame.time.get_ticks()*0.01 + i)*5, y+20), 4)

def draw_chef(surface, x, y, idle_phase):
    """Draws the chef with a breathing idle animation."""
    breath = math.sin(idle_phase) * 3
    # Body
    pygame.draw.rect(surface, (200, 200, 200), (x-25, y-40+breath, 50, 60))
    # Hat
    pygame.draw.rect(surface, WHITE, (x-20, y-60+breath, 40, 25))
    # Face
    pygame.draw.circle(surface, (255, 220, 180), (x, y-30+breath), 15)

# --- CLASSES ---

class Particle:
    def __init__(self, x, y, color, particle_type="smoke"):
        self.x = x
        self.y = y
        self.color = color
        self.type = particle_type
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-2, -0.5)
        self.life = 255
        self.size = random.randint(3, 8) if particle_type == "smoke" else random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 5
        if self.type == "spark":
            self.vy += 0.1 # Gravity for sparks

    def draw(self, surface):
        if self.life > 0:
            alpha_surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(alpha_surf, (*self.color, self.life), (self.size, self.size), self.size)
            surface.blit(alpha_surf, (self.x - self.size, self.y - self.size))

class Customer:
    TYPES = ["mushroom", "cyborg", "tentacles"]
    ORDERS = ["Nitrogen", "Bolts", "Fuel"]

    def __init__(self):
        self.type = random.choice(self.TYPES)
        self.order = random.choice(self.ORDERS)
        self.x = WIDTH + 50
        self.y = COUNTER_Y - 50
        self.target_x = 200 # Waiting spot
        self.state = "entering" # entering, waiting, leaving
        self.order_status = "none" # none, served
        self.float_offset = random.random() * math.pi * 2

    def update(self, speed_mult):
        move_speed = 3 * speed_mult
        if self.state == "entering":
            if self.x > self.target_x:
                self.x -= move_speed
            else:
                self.state = "waiting"
        elif self.state == "leaving":
            self.x -= move_speed
            if self.x < -100:
                return True # Can be removed
        return False

    def draw(self, surface):
        floating_y = self.y + math.sin(pygame.time.get_ticks() * 0.005 + self.float_offset) * 10
        draw_pixel_alien(surface, self.x, floating_y, self.type)
        
        if self.state == "waiting":
            # Draw order bubble
            pygame.draw.circle(surface, WHITE, (self.x + 40, floating_y - 40), 10)
            pygame.draw.ellipse(surface, WHITE, (self.x + 50, floating_y - 80, 80, 40))
            
            # Text for order
            font = pygame.font.SysFont("Arial", 16, bold=True)
            txt = font.render(self.order, True, BLACK)
            surface.blit(txt, (self.x + 55, floating_y - 70))

# --- GAME ENGINE ---

class Game:
    def __init__(self):
        self.state = "MENU"
        self.score = 0
        self.speed_mult = 1.0
        self.customers = []
        self.particles = []
        self.spawn_timer = 0
        self.cup_color = WHITE
        self.last_mix = None
        
        # Menu assets
        self.stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.random()*2+1] for _ in range(50)]
        self.font_neon = pygame.font.SysFont("Courier", 60, bold=True)
        self.font_small = pygame.font.SysFont("Courier", 30)

    def reset(self):
        self.score = 0
        self.speed_mult = 1.0
        self.customers = []
        self.particles = []
        self.state = "PLAYING"
        self.spawn_timer = pygame.time.get_ticks()

    def handle_input(self, event):
        if self.state == "MENU":
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.reset()
        elif self.state == "PLAYING":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # Check buttons
                # Nitrogen (Blue) - [100, 500, 150, 50]
                if 100 <= mx <= 250 and 500 <= my <= 550:
                    self.serve_mix("Nitrogen")
                # Bolts (Gray) - [325, 500, 150, 50]
                elif 325 <= mx <= 475 and 500 <= my <= 550:
                    self.serve_mix("Bolts")
                # Fuel (Green) - [550, 500, 150, 50]
                elif 550 <= mx <= 700 and 500 <= my <= 550:
                    self.serve_mix("Fuel")
        elif self.state == "GAMEOVER":
            if event.type == pygame.KEYDOWN:
                self.state = "MENU"

    def serve_mix(self, mix_type):
        self.last_mix = mix_type
        if mix_type == "Nitrogen":
            self.cup_color = COLOR_NITROGEN
            for _ in range(10): 
                self.particles.append(Particle(300, COUNTER_Y-20, WHITE, "smoke"))
        elif mix_type == "Bolts":
            self.cup_color = COLOR_BOLTS
            for _ in range(10):
                self.particles.append(Particle(300, COUNTER_Y-20, (255, 200, 0), "spark"))
        elif mix_type == "Fuel":
            self.cup_color = COLOR_FUEL
            for _ in range(10):
                self.particles.append(Particle(300, COUNTER_Y-20, CYAN_NEON, "smoke"))
        
        # Check current customer
        if self.customers:
            cust = self.customers[0]
            if cust.state == "waiting":
                if cust.order == mix_type:
                    self.score += 100
                    cust.state = "leaving"
                    # Speed up
                    if self.score % SPEED_INCREASE_STEP == 0:
                        self.speed_mult += 0.2
                else:
                    # Wrong order? Maybe penalty or just wait
                    pass

    def update(self):
        if self.state == "MENU":
            # Move stars (Antigravity movement)
            for star in self.stars:
                star[0] -= star[2]
                if star[0] < 0: star[0] = WIDTH
        elif self.state == "PLAYING":
            now = pygame.time.get_ticks()
            if now - self.spawn_timer > CUSTOMER_SPAWN_TIME / self.speed_mult:
                if len(self.customers) < 3:
                    self.customers.append(Customer())
                self.spawn_timer = now

            for cust in self.customers[:]:
                if cust.update(self.speed_mult):
                    self.customers.remove(cust)
            
            # Check for failure (Too many waiting? Or just time based)
            # For simplicity, if a customer waits too long... we don't have a timer here yet.
            
            for p in self.particles[:]:
                p.update()
                if p.life <= 0: self.particles.remove(p)

    def draw(self):
        screen.fill(BG_COLOR)

        if self.state == "MENU":
            # Stars
            for star in self.stars:
                pygame.draw.circle(screen, WHITE, (int(star[0]), int(star[1])), 1)
            
            title = self.font_neon.render("GALACTIC SNACK BAR", True, CYAN_NEON)
            start_txt = self.font_small.render("Pressione qualquer tecla para iniciar", True, HOT_PINK)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
            screen.blit(start_txt, (WIDTH//2 - start_txt.get_width()//2, 350))

        elif self.state == "PLAYING":
            # Draw Counter
            pygame.draw.rect(screen, (50, 50, 70), (0, COUNTER_Y, WIDTH, 20))
            
            # Draw Chef
            draw_chef(screen, 100, COUNTER_Y, pygame.time.get_ticks() * 0.005)

            # Draw Customers
            for cust in self.customers:
                cust.draw(screen)

            # Draw Cup
            pygame.draw.rect(screen, self.cup_color, (280, COUNTER_Y - 30, 40, 30))
            pygame.draw.rect(screen, WHITE, (280, COUNTER_Y - 30, 40, 30), 2)

            # Particles
            for p in self.particles:
                p.draw(screen)

            # --- CONSOLE ---
            pygame.draw.rect(screen, (20, 20, 40), (0, HEIGHT - CONSOLE_HEIGHT, WIDTH, CONSOLE_HEIGHT))
            pygame.draw.line(screen, CYAN_NEON, (0, HEIGHT - CONSOLE_HEIGHT), (WIDTH, HEIGHT - CONSOLE_HEIGHT), 3)

            # Buttons
            btns = [
                (100, "Nitrogen", COLOR_NITROGEN),
                (325, "Parafusos", COLOR_BOLTS),
                (550, "Combustível", COLOR_FUEL)
            ]
            for x, text, color in btns:
                pygame.draw.rect(screen, color, (x, 500, 150, 50), border_radius=10)
                pygame.draw.rect(screen, WHITE, (x, 500, 150, 50), 2, border_radius=10)
                txt = self.font_small.render(text, True, WHITE)
                screen.blit(txt, (x + 75 - txt.get_width()//2, 510))

            # UI Text
            score_txt = self.font_small.render(f"PONTOS: {self.score}", True, CYAN_NEON)
            speed_txt = self.font_small.render(f"VEL: x{self.speed_mult:.1f}", True, HOT_PINK)
            screen.blit(score_txt, (20, 20))
            screen.blit(speed_txt, (20, 60))

        elif self.state == "GAMEOVER":
            screen.fill((5, 0, 10))
            title = self.font_neon.render("A ESTAÇÃO FALIU!", True, (255, 0, 0))
            score_txt = self.font_small.render(f"Pontuação Final: {self.score}", True, WHITE)
            retry_txt = self.font_small.render("Pressione qualquer tecla para menu", True, GRAY)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
            screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, 300))
            screen.blit(retry_txt, (WIDTH//2 - retry_txt.get_width()//2, 450))

        pygame.display.flip()

# --- MAIN LOOP ---
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.handle_input(event)

    game.update()
    game.draw()
    clock.tick(FPS)
