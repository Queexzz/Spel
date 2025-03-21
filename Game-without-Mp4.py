# _author__  = Richard Whyte
 # __version__ = 1.6
 # __email__   = Richard.whyte@elev.ga.ntig.se

import pygame
import random

# Initiera Pygame
pygame.init()

# Konstanter
WIDTH, HEIGHT = 1920, 1080
CHICKEN_SIZE = 50
CAR_WIDTH, CAR_HEIGHT = 100, 50
FPS = 30
ROAD_Y = HEIGHT // 2
WINNING_Y = 100
LANE_SPACING = 150

# Standardvärden för svårighetsgraden
MOVE_SPEED = 5
CAR_SPEED = 5
MAX_CARS_PER_LANE = 5
SPAWN_INTERVAL = (30, 120)

# Färger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  # Kycklingens färg

# Skärm
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Crossing the Road")

# Kycklingklass
class Chicken:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT - CHICKEN_SIZE, CHICKEN_SIZE, CHICKEN_SIZE)
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(WIDTH - CHICKEN_SIZE, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - CHICKEN_SIZE, self.rect.y))
    
    def draw(self):
        pygame.draw.rect(screen, YELLOW, self.rect)

# Bilklass
class Car:
    def __init__(self, lane_y, direction):
        self.rect = pygame.Rect(
            -CAR_WIDTH if direction == 1 else WIDTH,
            lane_y + (50 - CAR_HEIGHT) // 2,
            CAR_WIDTH, CAR_HEIGHT
        )
        self.direction = direction
    
    def move(self):
        self.rect.x += self.direction * CAR_SPEED
        if self.rect.x > WIDTH:
            self.rect.x = -CAR_WIDTH
        elif self.rect.x < -CAR_WIDTH:
            self.rect.x = WIDTH
    
    def draw(self):
        pygame.draw.rect(screen, GREY, self.rect)

# LaneManager hanterar bilarnas spawn
class LaneManager:
    def __init__(self, lane_y, direction):
        self.lane_y = lane_y
        self.direction = direction
        self.cars = []
        self.spawn_timer = random.randint(*SPAWN_INTERVAL)
    
    def update(self):
        self.spawn_timer -= 1
        if self.spawn_timer <= 0 and len(self.cars) < MAX_CARS_PER_LANE:
            self.cars.append(Car(self.lane_y, self.direction))
            self.spawn_timer = random.randint(*SPAWN_INTERVAL)
        
        for car in self.cars:
            car.move()
        
        self.cars = [car for car in self.cars if -CAR_WIDTH < car.rect.x < WIDTH]
    
    def draw(self):
        for car in self.cars:
            car.draw()

# Välj svårighetsgrad
def select_difficulty():
    global MOVE_SPEED, CAR_SPEED, MAX_CARS_PER_LANE, SPAWN_INTERVAL

    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 40)

    title = font.render("Select Difficulty", True, WHITE)
    instructions = small_font.render("Use arrow keys to move the chicken!", True, WHITE)
    instructions2 = small_font.render("Avoid the cars and reach the top!", True, WHITE)
    instructions3 = small_font.render("The chicken starts off-screen, hold UP to see it!", True, WHITE)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, 200))
    screen.blit(instructions2, (WIDTH // 2 - instructions2.get_width() // 2, 250))
    screen.blit(instructions3, (WIDTH // 2 - instructions3.get_width() // 2, 800))

    buttons = [
        {"label": "Baby", "settings": (3, 2, 3, (80, 150))},
        {"label": "Easy", "settings": (5, 3, 5, (50, 120))},
        {"label": "Hard", "settings": (7, 4, 7, (30, 100))},
        {"label": "Impossible", "settings": (10, 5, 10, (20, 80))}
    ]

    for i, button in enumerate(buttons):
        button_rect = pygame.Rect(WIDTH // 2 - 150, 300 + i * 100, 300, 80)
        pygame.draw.rect(screen, GREY, button_rect)
        label = font.render(button["label"], True, WHITE)
        screen.blit(label, (button_rect.x + button_rect.width // 2 - label.get_width() // 2,
                            button_rect.y + button_rect.height // 2 - label.get_height() // 2))

    pygame.display.flip()

    selected = None
    while selected is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(buttons):
                    button_rect = pygame.Rect(WIDTH // 2 - 150, 300 + i * 100, 300, 80)
                    if button_rect.collidepoint(mouse_pos):
                        selected = i

    CAR_SPEED, MOVE_SPEED, MAX_CARS_PER_LANE, SPAWN_INTERVAL = buttons[selected]["settings"]

# Skapa körfält och bilhantering
lanes = []
lane_managers = []
for i in range(-3, 3):
    lane_y = ROAD_Y + LANE_SPACING * i
    direction = 1 if i >= 0 else -1
    lanes.append(lane_y)
    lane_managers.append(LaneManager(lane_y, direction))

# Huvudfunktion för spelet
def main():
    select_difficulty()
    clock = pygame.time.Clock()
    chicken = Chicken()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx = (-MOVE_SPEED if keys[pygame.K_LEFT] else MOVE_SPEED if keys[pygame.K_RIGHT] else 0)
        dy = (-MOVE_SPEED if keys[pygame.K_UP] else MOVE_SPEED if keys[pygame.K_DOWN] else 0)
        chicken.move(dx, dy)

        for manager in lane_managers:
            manager.update()

        for manager in lane_managers:
            for car in manager.cars:
                if chicken.rect.colliderect(car.rect):
                    print("Game Over! The chicken got hit!")
                    running = False

        if chicken.rect.y <= WINNING_Y:
            print("You crossed the road! You win!")
            running = False

        screen.fill(GREEN)
        for lane_y in lanes:
            pygame.draw.rect(screen, BLACK, (0, lane_y, WIDTH, 50))

        chicken.draw()
        for manager in lane_managers:
            manager.draw()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
    pygame.quit()
