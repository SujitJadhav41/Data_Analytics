
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
FPS = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT

    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self):
        head = self.body[0]
        # Check wall collision
        if (head[0] < 0 or head[0] >= SCREEN_WIDTH or 
            head[1] < 0 or head[1] >= SCREEN_HEIGHT):
            return True
        # Check self collision
        if head in self.body[1:]:
            return True
        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))


class Food:
    def __init__(self):
        self.position = self.spawn()

    def spawn(self, snake_body=None):
        while True:
            x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            position = (x, y)
            if snake_body is None or position not in snake_body:
                return position

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.food.position = self.food.spawn(self.snake.body)  # Ensure food doesn't spawn on snake
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != DOWN:
                    self.snake.next_direction = UP
                elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                    self.snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                    self.snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                    self.snake.next_direction = RIGHT
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        return True

    def update(self):
        if not self.game_over:
            self.snake.move()
            
            # Check collision BEFORE eating food
            if self.snake.check_collision():
                self.game_over = True
                return
            
            # Check if snake ate food
            if self.snake.body[0] == self.food.position:
                self.snake.grow()
                self.score += 10
                self.food.position = self.food.spawn(self.snake.body)

    def draw(self):
        self.screen.fill(BLACK)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            restart_text = self.font.render("Press SPACE to restart or Q to quit", True, YELLOW)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
            
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            self.screen.blit(final_score_text, score_rect)
        
        pygame.display.flip()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.food.position = self.food.spawn(self.snake.body)  # Ensure food doesn't spawn on snake
        self.score = 0
        self.game_over = False

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
    
