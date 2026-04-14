import random
import math
import pygame

class AntigravityStar:
    """Simulates moving background stars."""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(0, self.screen_height)
        self.speed = random.uniform(0.1, 1.5)
        self.size = random.randint(1, 2)
        self.alpha = random.randint(100, 255)
        self.alpha_dir = random.choice([-1, 1])

    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = self.screen_width
            self.y = random.randint(0, self.screen_height)
        
        # Twinkle
        self.alpha += self.alpha_dir * 2
        if self.alpha >= 255 or self.alpha <= 100:
            self.alpha_dir *= -1

    def draw(self, surface):
        s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, self.alpha), (self.size, self.size), self.size)
        surface.blit(s, (int(self.x), int(self.y)))

class ShootingStar:
    """Occasional streaks across the screen."""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        
    def spawn(self):
        self.x = self.screen_width + 100
        self.y = random.randint(0, self.screen_height // 2)
        self.speed = random.uniform(10, 20)
        self.angle = random.uniform(math.pi * 0.7, math.pi * 0.9)
        self.length = random.randint(40, 80)
        self.active = True

    def update(self):
        if not self.active:
            if random.random() < 0.005:
                self.spawn()
            return

        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        if self.x < -100 or self.y > self.screen_height + 100:
            self.active = False

    def draw(self, surface):
        if not self.active: return
        end_x = self.x - math.cos(self.angle) * self.length
        end_y = self.y - math.sin(self.angle) * self.length
        pygame.draw.line(surface, (200, 230, 255), (self.x, self.y), (end_x, end_y), 2)

class Particle:
    """Low gravity particles for smoke and sparks."""
    def __init__(self, x, y, p_type="smoke"):
        self.x = x
        self.y = y
        self.p_type = p_type
        if p_type == "smoke":
            self.color = (255, 255, 255)
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(-1.5, -0.5)
            self.gravity = -0.01
            self.size = random.uniform(4, 10)
        else: # sparks
            self.color = (255, 200, 50)
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-3, -1)
            self.gravity = 0.1
            self.size = random.uniform(2, 4)
            
        self.lifetime = 255
        self.decay = random.randint(4, 8)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= self.decay
        
        if self.p_type == "smoke":
            self.size += 0.1
            self.vx += math.sin(pygame.time.get_ticks() * 0.01) * 0.02
        else:
            self.vx *= 0.98

    def is_alive(self):
        return self.lifetime > 0

    def draw(self, surface):
        alpha = max(0, self.lifetime)
        s = pygame.Surface((int(self.size*2), int(self.size*2)), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (int(self.size), int(self.size)), int(self.size))
        surface.blit(s, (self.x - self.size, self.y - self.size))

class FloatMotion:
    """Utility to provide idle floating animation."""
    def __init__(self, frequency=0.005, amplitude=5):
        self.frequency = frequency
        self.amplitude = amplitude
        self.offset = random.random() * 100

    def get_offset(self, override_freq=None):
        freq = override_freq if override_freq else self.frequency
        t = pygame.time.get_ticks()
        return math.sin(t * freq + self.offset) * self.amplitude

