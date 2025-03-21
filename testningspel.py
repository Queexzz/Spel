import pygame
import moviepy.editor as mp
import random
import os

# Initialize Pygame
pygame.init()

# Constents for the game
WIDTH, HEIGHT = 1920, 1080   # Dimenssions of the game window
CHICKEN_SIZE = 50  # Size of the chiken
CAR_WIDTH, CAR_HEIGHT = 100, 50  # Size of the cars
FPS = 30  # Frames per second for the game
ROAD_Y = HEIGHT // 2  # Y-coordinate for the road
WINNING_Y = 100  # Y-coordinate for the winning line
LANE_SPACING = 150  # Spacing between lanes

# Difficulty-dependant variables (default values for fallback)
MOVE_SPEED = 5  # Speed of the chicken
CAR_SPEED = 5  # Speed of the cars
MAX_CARS_PER_LANE = 5  # Maximum number of cars allowed in each lane
SPAWN_INTERVAL = (30, 120)  # Range for random car spawn timers

# Colors used in the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)

# Set up the display for the game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Crossing the Road")  # Title of the window

# Chicken class with animation
class Chicken:
    def __init__(self):
        # Load the chicken video file
        video_path = os.path.join(os.path.dirname(__file__), "chicken-bock.mp4")
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file 'chicken-bock.mp4' not found in {os.path.dirname(__file__)}")

        # Load video frames into a list
        self.frames = self.load_video_frames(video_path)
        self.current_frame = 0  # Current frame index for animation
        self.rect = self.frames[0].get_rect(center=(WIDTH // 2, HEIGHT - CHICKEN_SIZE))  # Position of the chicken
        self.animation_speed = 5  # Speed of the animation
        self.frame_counter = 0  # Counter to track the current frame

    def load_video_frames(self, video_path):
        # Load frames from the video file
        video = mp.VideoFileClip(video_path)
        frames = []
        for frame in video.iter_frames(fps=FPS):
            pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # Convert frame to Pygame surface
            frames.append(pygame.transform.scale(pygame_frame, (CHICKEN_SIZE, CHICKEN_SIZE)))  # Scale frame
        return frames

    def move(self, dx, dy):
        # Move the chicken based on input
        self.rect.x += dx
        self.rect.y += dy
        # Keep the chicken within the screen bounds
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - CHICKEN_SIZE:
            self.rect.x = WIDTH - CHICKEN_SIZE
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > HEIGHT - CHICKEN_SIZE:
            self.rect.y = HEIGHT - CHICKEN_SIZE

    def update(self):
        # Update the current frame for animation
        self.frame_counter += self.animation_speed
        if self.frame_counter >= len(self.frames):
            self.frame_counter = 0  # Reset frame counter if it exceeds the number of frames
        self.current_frame = int(self.frame_counter)  # Get the current frame index

    def draw(self):
        # Draw the current frame of the chicken on the screen
        screen.blit(self.frames[self.current_frame], self.rect)

# Car class
class Car:
    def __init__(self, lane_y, direction):
        # Initialize car position based on its direction
        if direction == 1:  # Left-to-right traffic
            x_pos = -CAR_WIDTH  # Start off-screen to the left
        else:  # Right-to-left traffic
            x_pos = WIDTH  # Start off-screen to the right

        # Create a rectangle for the car's position
        self.rect = pygame.Rect(
            x_pos,
            lane_y + (50 - CAR_HEIGHT) // 2,  # Center the car vertically within the lane
            CAR_WIDTH,
            CAR_HEIGHT
        )
        self.direction = direction  # 1 for left-to-right, -1 for right-to-left

    def move(self):
        # Move the car based on its direction
        self.rect.x += self.direction * CAR_SPEED
        if self.rect.x > WIDTH:  # Reset car to the left for left-to-right traffic
            self.rect.x = -CAR_WIDTH
        elif self.rect.x < -CAR_WIDTH:  # Reset car to the right for right-to-left traffic
            self.rect.x = WIDTH

    def draw(self):
        # Draw the car on the screen
        pygame.draw.rect(screen, GREY, self.rect)

# Lane manager to handle car spawning
class LaneManager:
    def __init__(self, lane_y, direction):
        self.lane_y = lane_y  # Y-coordinate of the lane
        self.direction = direction  # Direction of traffic in this lane
        self.cars = []  # List to hold cars in this lane
        self.spawn_timer = random.randint(*SPAWN_INTERVAL)  # Random spawn interval for cars

    def update(self):
        # Update the spawn timer and manage car spawning
        self.spawn_timer -= 1
        if self.spawn_timer <= 0 and len(self.cars) < MAX_CARS_PER_LANE:
            self.cars.append(Car(self.lane_y, self.direction))  # Add a new car to the lane
            self.spawn_timer = random.randint(*SPAWN_INTERVAL)  # Reset the spawn timer

        # Move existing cars
        for car in self.cars:
            car.move()
        # Remove cars that are off screen
        self.cars = [car for car in self.cars if car.rect.x > -CAR_WIDTH and car.rect.x < WIDTH]

    def draw(self):
        # Draw all cars in this lane
        for car in self.cars:
            car.draw()

# Selector screen with clickable buttons
def select_difficulty():
    global MOVE_SPEED, CAR_SPEED, MAX_CARS_PER_LANE, SPAWN_INTERVAL

    screen.fill(BLACK)  # Fill the screen with black
    font = pygame.font.Font(None, 74)  # Font for the title
    small_font = pygame.font.Font(None, 40)  # Font for instructions

    # Render title and instructions
    title = font.render("Select Difficulty", True, WHITE)
    instructions = small_font.render("Use arrow keys to move the chicken!", True, WHITE)
    instructions2 = small_font.render("Avoid the cars and reach the top!", True, WHITE)
    instructions3 = small_font.render("The chicken will start outside of the screen, hold the up arrow key to see the chicken!", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))  # Center title
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, 200))  # Center instructions
    screen.blit(instructions2, (WIDTH // 2 - instructions2.get_width() // 2, 250))  # Center second instruction
    screen.blit(instructions3, (WIDTH // 2 - instructions2.get_width() // 1, 800))

    # Button definitions for difficulty selection
    buttons = [
        {"label": "Baby", "settings": (3, 2, 3, (80, 150))},
        {"label": "Easy", "settings": (5, 3, 5, (50, 120))},
        {"label": "Hard", "settings": (7, 4, 7, (30, 100))},
        {"label": "Impossible", "settings": (10, 5, 10, (20, 80))},
    ]

    # Render buttons
    for i, button in enumerate(buttons):
        button_rect = pygame.Rect(WIDTH // 2 - 150, 300 + i * 100, 300, 80)  # Position of the button
        pygame.draw.rect(screen, GREY, button_rect)  # Draw button rectangle
        label = font.render(button["label"], True, WHITE)  # Render button label
        screen.blit(label, (button_rect.x + button_rect.width // 2 - label.get_width() // 2,
                            button_rect.y + button_rect.height // 2 - label.get_height() // 2))  # Center label

    pygame.display.flip()  # Update the display

    selected = None  # Variable to track selected difficulty
    while selected is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                mouse_pos = pygame.mouse.get_pos()  # Get mouse position
                for i, button in enumerate(buttons):
                    button_rect = pygame.Rect(WIDTH // 2 - 150, 300 + i * 100, 300, 80)  # Button rectangle
                    if button_rect.collidepoint(mouse_pos):  # Check if mouse is over the button
                        selected = i  # Set selected difficulty

    # Apply selected difficulty settings
    CAR_SPEED, MOVE_SPEED, MAX_CARS_PER_LANE, SPAWN_INTERVAL = buttons[selected]["settings"]

# Define lanes and assign directions
lanes = []  # List to hold lane Y-coordinates
lane_managers = []  # List to manage lanes
for i in range(-3, 3):
    lane_y = ROAD_Y + LANE_SPACING * i  # Calculate Y-coordinate for each lane
    direction = 1 if i >= 0 else -1  # Set direction based on lane index
    lanes.append(lane_y)  # Add lane Y-coordinate to the list
    lane_managers.append(LaneManager(lane_y, direction))  # Create a LaneManager for each lane

# Main game loop
def main():
    select_difficulty()  # Show difficulty selection screen
    clock = pygame.time.Clock()  # Create a clock to control the frame rate
    chicken = Chicken()  # Create a chicken instance
    running = True  # Game loop control variable

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game loop

        keys = pygame.key.get_pressed()  # Get the current state of the keyboard
        # Determine movement based on key presses
        dx = (-MOVE_SPEED if keys[pygame.K_LEFT] else MOVE_SPEED if keys[pygame.K_RIGHT] else 0)
        dy = (-MOVE_SPEED if keys[pygame.K_UP] else MOVE_SPEED if keys[pygame.K_DOWN] else 0)
        chicken.move(dx, dy)  # Move the chicken

        # Update lane managers and check for collisions
        for manager in lane_managers:
            manager.update()

        for manager in lane_managers:
            for car in manager.cars:
                if chicken.rect.colliderect(car.rect):  # Check for collision with cars
                    print("Game Over! The chicken got hit!")  # Print game over message
                    running = False  # Exit the game loop

        if chicken.rect.y <= WINNING_Y:  # Check if the chicken reached the winning line
            print("You crossed the road! You win!")  # Print win message
            running = False  # Exit the game loop

        screen.fill(GREEN)  # Fill the screen with green
        for lane_y in lanes:
            pygame.draw.rect(screen, BLACK, (0, lane_y, WIDTH, 50))  # Draw lanes

        chicken.update()  # Update chicken animation
        chicken.draw()  # Draw the chicken
        for manager in lane_managers:
            manager.draw()  # Draw cars in each lane

        pygame.display.flip()  # Update the display
        clock.tick(FPS)  # Control the frame rate

if __name__ == "__main__":
    main()  # Start the game
    pygame.quit()  # Quit P