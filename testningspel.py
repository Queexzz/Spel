import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CHICKEN_SIZE = 50
CAR_WIDTH, CAR_HEIGHT = 100, 50

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

        screen.fill((255, 255, 255))  # Fill the screen with white
        chicken.draw()
        car.draw()
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
