# _author__  = Richard Whyte
# __version__ = 1.3
# __email__   = Richard.whyte@elev.ga.ntig.se

import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
CHICKEN_SIZE = 50
CAR_WIDTH, CAR_HEIGHT = 100, 50
MOVE_SPEED = 2  # Speed of the chicken's movement
CAR_SPEED = 5  # Speed of the car's movement

# Colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


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
        self.rect = pygame.Rect(WIDTH, HEIGHT // 2, CAR_WIDTH, CAR_HEIGHT)  # Start off-screen to the right

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

    def move(self):
        # Move the car left
        self.rect.x -= CAR_SPEED
        # Reset the car's position to the right side of the screen if it goes off-screen
        if self.rect.x < -CAR_WIDTH:
            self.rect.x = WIDTH

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
        car.move()  # Update the car's position

        screen.fill((0, 255, 0))  # Fill the screen with white
        chicken.draw()
        car.draw()
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()