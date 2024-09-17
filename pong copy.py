import pygame as pg
import random

# Initialize the pygame library
pg.init()

# Create and name the game window
width = 800
height = 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("PONG by Ishann Agarwal")

# Create a clock object to keep track of time
clock = pg.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
RED = (255, 57, 57)
PURPLE = (200, 0, 250)

# Ball class
class Ball(pg.sprite.Sprite):
    def __init__(self, position, radius, color):
        """Initialize the ball"""
        super().__init__()
        self.radius = radius
        
        # Create a new surface to draw the ball on
        self.image = pg.Surface([2 * self.radius] * 2)
        
        # Draw a circle with given radius on the new surface
        pg.draw.circle(self.image, color, [self.radius] * 2, self.radius)
        
        # Create a bounding rectangle for the surface
        self.rect = self.image.get_rect()
        
        # Place the ball at the given position
        self.rect.center = position
        
        # Keep track of x and y components of velocity
        self.velocity = [0, 0]

    def set_velocity(self, x, y):
        """Used to change the velocity of the ball"""
        self.velocity[0] = x
        self.velocity[1] = y
        
    def calc_new_pos(self, t):
        """Calculate the position of the ball after movement"""
        # distance = speed * time
        # dx = change in x, dy = change in y
        dx = self.velocity[0] * t
        dy = self.velocity[1] * t
        new_pos = (round(self.rect.centerx + dx),
                   round(self.rect.centery + dy))
        return new_pos

    def bounce_x(self):
        """Flip x velocity"""
        self.velocity[0] *= -1
        
    def bounce_y(self):
        """Flip y velocity"""
        self.velocity[1] *= -1
    
    def update(self, t):
        """Runs every frame to move the ball and bounce if necessary"""
        # Update position
        self.rect.center = self.calc_new_pos(t)
        
        # Bounce if hitting screen edges
        if self.rect.bottom >= height or self.rect.top <= 0:
            self.bounce_y()

# Paddle class
class Paddle(pg.sprite.Sprite):
    def __init__(self, position, dimensions, color):
        """Initialize the paddle object"""
        super().__init__()
        
        # Create surface with paddle dimensions
        self.image = pg.Surface(dimensions)
        
        # Fill surface to create visible rectangle
        self.image.fill(color)
        
        # Get bounding rectangle
        self.rect = self.image.get_rect()
        
        # Set position
        self.rect.topleft = position
        
        # Track speed
        self.y_velocity = 0

    def set_y_velocity(self, v):
        """Set y velocity of paddle"""
        self.y_velocity = v

    def calc_new_pos(self, t):
        """Calculate the position of the ball after movement"""
        # distance = speed * time
        # dy = change in y
        dy = self.y_velocity * t
        new_y = round(self.rect.centery + dy)
        return new_y

    def update(self, t):
        """Make sure paddle is on-screen and move"""
        # Check boundaries
        if self.rect.bottom >= height and self.y_velocity > 0:
            self.y_velocity = 0
        if self.rect.top <= 0 and self.y_velocity < 0:
            self.y_velocity = 0
        self.rect.center = (self.rect.centerx, self.calc_new_pos(t))

def respawn_ball(direction):
    ball.rect.center = (width // 2, height // 2)
    x = direction * random.randint(2, 4) / 10
    y = random.randint(2, 4) / 10
    ball.set_velocity(x, y)

# Create a ball object
ball = Ball((width // 2, height // 2), width // 40, PURPLE)

# Create paddles for players
paddle_size = (width // 50, height // 10)
p1 = Paddle((0, 0), paddle_size, RED)
p2 = Paddle((width - paddle_size[0], 0), paddle_size, BLUE)
paddle_speed = 0.4

# Create sprite group to store the paddles
paddles = pg.sprite.Group(p1, p2)

# Main function to run the game
def main():
    # Keep track of the player scores
    p1score = 0
    p2score = 0
    
    # Get the ball moving
    respawn_ball(1)
    
    # Variable to keep track of game status
    running = True
    
    # Game loop
    while running:
        t = clock.tick(60)
        
        # Event-checking loop
        for event in pg.event.get():
            # Check for a QUIT event
            if event.type == pg.QUIT:
                running = False
            # Check for  KEYDOWN event
            if event.type == pg.KEYDOWN:
                # Check different keys
                if event.key == pg.K_w:
                    p1.set_y_velocity(-paddle_speed)
                if event.key == pg.K_s:
                    p1.set_y_velocity(paddle_speed)
                if event.key == pg.K_UP:
                    p2.set_y_velocity(-paddle_speed)
                if event.key == pg.K_DOWN:
                    p2.set_y_velocity(paddle_speed)
            # Check for KEYUP event:
            if event.type == pg.KEYUP:
                # Check keys
                if event.key == pg.K_s or event.key == pg.K_w:
                    p1.set_y_velocity(0)
                if event.key == pg.K_DOWN or event.key == pg.K_UP:
                    p2.set_y_velocity(0)

        # Check for collision between ball and paddles
        if pg.sprite.spritecollide(ball, paddles, False):
            ball.velocity[0] *= -1.1

        # Award points if ball passes a paddle
        if ball.rect.right >= width:
            p1score += 1
            respawn_ball(1)
        if ball.rect.left <= 0: 
            p2score += 1
            respawn_ball(-1)

        # Check for winner
        if p1score >= 10:
            running = False
            print("Player 1 wins!")
        if p2score >= 10:
            running = False
            print("Player 2 wins!")
                
        # Fill screen with white
        screen.fill(WHITE)
        
        # Draw dividing line
        pg.draw.line(screen, BLACK, (width // 2, 0), (width // 2, height), 5)
        
        # Blit all images to the screen
        screen.blit(ball.image, ball.rect)
        paddles.draw(screen)
        
        # Update all objects
        ball.update(t)
        paddles.update(t)
        
        # Update the screen
        pg.display.flip()
        

main()
            
