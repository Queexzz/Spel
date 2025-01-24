# _author__  = Richard Whyte
# __version__ = 1.1
# __email__   = Richard.whyte@elev.ga.ntig.se

import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CHICKEN_SIZE = 50
CAR_WIDTH, CAR_HEIGHT = 100, 50
MOVE_SPEED = 3  # Speed of the chicken's movement

# Colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Chicken class
class Chicken:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT - CHICKEN_SIZE, CHICKEN_SIZE, CHICKEN_SIZE)

    def draw(self):
        pygame.draw.rect(screen, YELLOW, self.rect)

    def move(self, dx, dy):
        # Move the chicken left/right and up/down
        self.rect.x += dx
        self.rect.y += dy
        # Keep the chicken within the screen bounds
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - CHICKEN_SIZE:
            self.rect.x = WIDTH - CHICKEN_SIZE
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > HEIGHT - CHICKEN_SIZE:
            self.rect.y = HEIGHT - CHICKEN_SIZE

# Car class
class Car:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, CAR_WIDTH, CAR_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

# Main function
def main():
    clock = pygame.time.Clock()
    chicken = Chicken()
    car = Car()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle key presses
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT]:
            dx = -MOVE_SPEED  # Move left
        if keys[pygame.K_RIGHT]:
            dx = MOVE_SPEED  # Move right
        if keys[pygame.K_UP]:
            dy = -MOVE_SPEED  # Move up
        if keys[pygame.K_DOWN]:
            dy = MOVE_SPEED  # Move down

        chicken.move(dx, dy)

        screen.fill((255, 255, 255))  # Fill the screen with white
        chicken.draw()
        car.draw()
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()