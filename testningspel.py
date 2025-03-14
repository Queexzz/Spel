# Author: Richard Whyte
# Version: 1.4
# Email: Richard.whyte@elev.ga.ntig.se

import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800  
CHICKEN_SIZE = 50
CAR_WIDTH, CAR_HEIGHT = 100, 50
MOVE_SPEED = 2  # Speed of the chicken's movement
CAR_SPEED = 5  # Speed of the car's movement
NUM_LANES = 6  # Number of lanes for cars

# Colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0) 
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Chicken class
class Chicken:
    def __init__(self):
        # Chicken starts at the bottom center of the screen
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT - CHICKEN_SIZE, CHICKEN_SIZE, CHICKEN_SIZE)

    def draw(self):
        pygame.draw.rect(screen, YELLOW, self.rect)

    def move(self, dx, dy):
        # Optimized movement using max/min to keep chicken within screen
        self.rect.x = max(0, min(self.rect.x + dx, WIDTH - CHICKEN_SIZE))
        self.rect.y = max(0, min(self.rect.y + dy, HEIGHT - CHICKEN_SIZE))

# Car class
class Car:
    def __init__(self, lane, direction):
        # Cars are placed based on lanes instead of a fixed position
        y_pos = int((HEIGHT / NUM_LANES) * lane + ((HEIGHT / NUM_LANES - CAR_HEIGHT) / 2))
        self.rect = pygame.Rect(WIDTH if direction == "right" else -CAR_WIDTH, y_pos, CAR_WIDTH, CAR_HEIGHT)
        self.direction = direction  # Cars move left or right depending on assigned direction

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

    def move(self):
        # Cars move in their assigned direction
        self.rect.x += CAR_SPEED if self.direction == "right" else -CAR_SPEED
        # Reset position when car moves off-screen
        if self.rect.x > WIDTH:
            self.rect.x = -CAR_WIDTH
        elif self.rect.x < -CAR_WIDTH:
            self.rect.x = WIDTH

# Main function
def main():
    clock = pygame.time.Clock()
    chicken = Chicken()

    # Cars are now generated dynamically based on the number of lanes
    cars = [Car(lane, "right" if lane < NUM_LANES // 2 else "left") for lane in range(NUM_LANES)]

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Optimized movement input handling using a single line
        keys = pygame.key.get_pressed()
        chicken.move(
            (-MOVE_SPEED if keys[pygame.K_LEFT] else MOVE_SPEED if keys[pygame.K_RIGHT] else 0),
            (-MOVE_SPEED if keys[pygame.K_UP] else MOVE_SPEED if keys[pygame.K_DOWN] else 0)
        )

        # Move all cars
        for car in cars:
            car.move()

        screen.fill(GREEN)  
        chicken.draw()
        for car in cars:
            car.draw()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
