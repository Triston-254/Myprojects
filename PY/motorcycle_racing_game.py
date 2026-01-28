# snake_game_advanced.py
import tkinter as tk
from tkinter import messagebox
import random
import json
import os

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # Game constants
        self.CELL_SIZE = 25
        self.GRID_WIDTH = 30
        self.GRID_HEIGHT = 25
        self.GAME_WIDTH = self.GRID_WIDTH * self.CELL_SIZE
        self.GAME_HEIGHT = self.GRID_HEIGHT * self.CELL_SIZE
        
        # Colors
        self.COLORS = {
            'snake_head': '#4CAF50',  # Green
            'snake_body': '#8BC34A',  # Light Green
            'food': '#FF5722',        # Orange Red
            'super_food': '#E91E63',  # Pink
            'poison': '#9C27B0',      # Purple
            'wall': '#607D8B',        # Blue Gray
            'background': '#212121',   # Dark Gray
            'grid': '#37474F',        # Darker Gray
            'text': '#FFFFFF'         # White
        }
        
        # Game variables
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.speed = 150  # milliseconds
        self.direction = 'Right'
        self.next_direction = 'Right'
        self.game_running = False
        self.game_paused = False
        self.snake_length = 3
        self.special_food_timer = 0
        self.poison_food_timer = 0
        self.walls = []
        
        # Load high score
        self.load_high_score()
        
        # Create UI
        self.create_widgets()
        
        # Initialize game
        self.reset_game()
        
        # Bind keys
        self.bind_keys()
        
        # Center window
        self.center_window()
    
    def create_widgets(self):
        # Create main frame
        main_frame = tk.Frame(self.root, bg=self.COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Score panel at top
        score_frame = tk.Frame(main_frame, bg=self.COLORS['background'], height=60)
        score_frame.pack(fill=tk.X, padx=10, pady=5)
        score_frame.pack_propagate(False)
        
        # Score labels
        self.score_label = tk.Label(
            score_frame, 
            text=f"Score: {self.score}",
            font=('Arial', 16, 'bold'),
            fg=self.COLORS['text'],
            bg=self.COLORS['background']
        )
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        self.high_score_label = tk.Label(
            score_frame,
            text=f"High Score: {self.high_score}",
            font=('Arial', 16, 'bold'),
            fg='#FFD700',  # Gold color for high score
            bg=self.COLORS['background']
        )
        self.high_score_label.pack(side=tk.LEFT, padx=20)
        
        self.level_label = tk.Label(
            score_frame,
            text=f"Level: {self.level}",
            font=('Arial', 16, 'bold'),
            fg=self.COLORS['text'],
            bg=self.COLORS['background']
        )
        self.level_label.pack(side=tk.LEFT, padx=20)
        
        # Game controls frame
        controls_frame = tk.Frame(main_frame, bg=self.COLORS['background'])
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Control buttons
        self.start_button = tk.Button(
            controls_frame,
            text="START",
            command=self.start_game,
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=5
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(
            controls_frame,
            text="PAUSE",
            command=self.toggle_pause,
            font=('Arial', 12, 'bold'),
            bg='#FF9800',
            fg='white',
            padx=20,
            pady=5
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(
            controls_frame,
            text="RESET",
            command=self.reset_game,
            font=('Arial', 12, 'bold'),
            bg='#F44336',
            fg='white',
            padx=20,
            pady=5
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Instructions label
        instructions = tk.Label(
            controls_frame,
            text="Controls: ↑ ↓ ← → or W A S D | P: Pause | SPACE: Start",
            font=('Arial', 10),
            fg=self.COLORS['text'],
            bg=self.COLORS['background']
        )
        instructions.pack(side=tk.RIGHT, padx=20)
        
        # Create game canvas
        canvas_frame = tk.Frame(main_frame, bg=self.COLORS['background'])
        canvas_frame.pack(pady=10)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.GAME_WIDTH,
            height=self.GAME_HEIGHT,
            bg=self.COLORS['background'],
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Legend frame
        legend_frame = tk.Frame(main_frame, bg=self.COLORS['background'])
        legend_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create legend items
        legend_items = [
            ('Snake Head', self.COLORS['snake_head']),
            ('Snake Body', self.COLORS['snake_body']),
            ('Normal Food', self.COLORS['food']),
            ('Super Food (+5)', self.COLORS['super_food']),
            ('Poison (-2)', self.COLORS['poison']),
            ('Wall', self.COLORS['wall'])
        ]
        
        for text, color in legend_items:
            item_frame = tk.Frame(legend_frame, bg=self.COLORS['background'])
            item_frame.pack(side=tk.LEFT, padx=10)
            
            # Color box
            tk.Canvas(
                item_frame,
                width=20,
                height=20,
                bg=color,
                highlightthickness=0
            ).pack(side=tk.LEFT, padx=2)
            
            # Text label
            tk.Label(
                item_frame,
                text=text,
                font=('Arial', 10),
                fg=self.COLORS['text'],
                bg=self.COLORS['background']
            ).pack(side=tk.LEFT, padx=2)
    
    def bind_keys(self):
        # Arrow keys
        self.root.bind('<Up>', lambda e: self.change_direction('Up'))
        self.root.bind('<Down>', lambda e: self.change_direction('Down'))
        self.root.bind('<Left>', lambda e: self.change_direction('Left'))
        self.root.bind('<Right>', lambda e: self.change_direction('Right'))
        
        # WASD keys
        self.root.bind('w', lambda e: self.change_direction('Up'))
        self.root.bind('s', lambda e: self.change_direction('Down'))
        self.root.bind('a', lambda e: self.change_direction('Left'))
        self.root.bind('d', lambda e: self.change_direction('Right'))
        
        # Other controls
        self.root.bind('<space>', lambda e: self.start_game())
        self.root.bind('p', lambda e: self.toggle_pause())
        self.root.bind('r', lambda e: self.reset_game())
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_high_score(self):
        try:
            if os.path.exists('snake_high_score.json'):
                with open('snake_high_score.json', 'r') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
        except:
            self.high_score = 0
    
    def save_high_score(self):
        try:
            with open('snake_high_score.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass
    
    def draw_grid(self):
        # Draw grid lines
        for x in range(0, self.GAME_WIDTH, self.CELL_SIZE):
            self.canvas.create_line(
                x, 0, x, self.GAME_HEIGHT,
                fill=self.COLORS['grid'],
                width=1
            )
        for y in range(0, self.GAME_HEIGHT, self.CELL_SIZE):
            self.canvas.create_line(
                0, y, self.GAME_WIDTH, y,
                fill=self.COLORS['grid'],
                width=1
            )
    
    def reset_game(self):
        # Reset game state
        self.score = 0
        self.level = 1
        self.speed = 150
        self.direction = 'Right'
        self.next_direction = 'Right'
        self.game_running = False
        self.game_paused = False
        self.snake_length = 3
        self.special_food_timer = 0
        self.poison_food_timer = 0
        
        # Initialize snake
        self.snake = []
        start_x = self.GRID_WIDTH // 2
        start_y = self.GRID_HEIGHT // 2
        
        for i in range(self.snake_length):
            self.snake.append({
                'x': start_x - i,
                'y': start_y
            })
        
        # Initialize food and obstacles
        self.food = self.generate_food()
        self.super_food = None
        self.poison_food = None
        self.generate_walls()
        
        # Clear canvas and redraw
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_snake()
        self.draw_food()
        self.draw_walls()
        
        # Update labels
        self.update_labels()
        
        # Enable start button
        self.start_button.config(state=tk.NORMAL)
    
    def generate_food(self):
        while True:
            food = {
                'x': random.randint(0, self.GRID_WIDTH - 1),
                'y': random.randint(0, self.GRID_HEIGHT - 1)
            }
            
            # Check if food is on snake
            if not any(segment['x'] == food['x'] and segment['y'] == food['y'] 
                      for segment in self.snake):
                # Check if food is on wall
                if not any(wall['x'] == food['x'] and wall['y'] == food['y'] 
                          for wall in self.walls):
                    return food
    
    def generate_walls(self):
        self.walls = []
        
        # Generate walls based on level
        num_walls = min(self.level * 2, 10)
        
        for _ in range(num_walls):
            while True:
                wall = {
                    'x': random.randint(0, self.GRID_WIDTH - 1),
                    'y': random.randint(0, self.GRID_HEIGHT - 1)
                }
                
                # Check if wall is not on snake or food
                if (not any(segment['x'] == wall['x'] and segment['y'] == wall['y'] 
                           for segment in self.snake) and
                    not (self.food['x'] == wall['x'] and self.food['y'] == wall['y'])):
                    self.walls.append(wall)
                    break
    
    def draw_snake(self):
        # Draw snake body
        for i, segment in enumerate(self.snake):
            x1 = segment['x'] * self.CELL_SIZE
            y1 = segment['y'] * self.CELL_SIZE
            x2 = x1 + self.CELL_SIZE
            y2 = y1 + self.CELL_SIZE
            
            if i == 0:  # Snake head
                color = self.COLORS['snake_head']
                # Draw eyes
                eye_size = self.CELL_SIZE // 5
                eye_offset = self.CELL_SIZE // 3
                
                # Determine eye positions based on direction
                if self.direction == 'Right':
                    left_eye = (x2 - eye_offset, y1 + eye_offset)
                    right_eye = (x2 - eye_offset, y2 - eye_offset)
                elif self.direction == 'Left':
                    left_eye = (x1 + eye_offset, y1 + eye_offset)
                    right_eye = (x1 + eye_offset, y2 - eye_offset)
                elif self.direction == 'Up':
                    left_eye = (x1 + eye_offset, y1 + eye_offset)
                    right_eye = (x2 - eye_offset, y1 + eye_offset)
                else:  # Down
                    left_eye = (x1 + eye_offset, y2 - eye_offset)
                    right_eye = (x2 - eye_offset, y2 - eye_offset)
                
                # Draw head
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline='',
                    tags='snake'
                )
                
                # Draw eyes
                self.canvas.create_oval(
                    left_eye[0] - eye_size, left_eye[1] - eye_size,
                    left_eye[0] + eye_size, left_eye[1] + eye_size,
                    fill='white',
                    outline='',
                    tags='snake'
                )
                self.canvas.create_oval(
                    right_eye[0] - eye_size, right_eye[1] - eye_size,
                    right_eye[0] + eye_size, right_eye[1] + eye_size,
                    fill='white',
                    outline='',
                    tags='snake'
                )
                
                # Draw pupils
                pupil_size = eye_size // 2
                self.canvas.create_oval(
                    left_eye[0] - pupil_size, left_eye[1] - pupil_size,
                    left_eye[0] + pupil_size, left_eye[1] + pupil_size,
                    fill='black',
                    outline='',
                    tags='snake'
                )
                self.canvas.create_oval(
                    right_eye[0] - pupil_size, right_eye[1] - pupil_size,
                    right_eye[0] + pupil_size, right_eye[1] + pupil_size,
                    fill='black',
                    outline='',
                    tags='snake'
                )
            else:  # Snake body
                color = self.COLORS['snake_body']
                # Create rounded corners effect
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline='',
                    tags='snake'
                )
                
                # Draw body pattern
                pattern_size = self.CELL_SIZE // 4
                pattern_x = x1 + pattern_size
                pattern_y = y1 + pattern_size
                self.canvas.create_oval(
                    pattern_x, pattern_y,
                    pattern_x + pattern_size, pattern_y + pattern_size,
                    fill='#33691E',
                    outline='',
                    tags='snake'
                )
    
    def draw_food(self):
        # Draw normal food
        x1 = self.food['x'] * self.CELL_SIZE
        y1 = self.food['y'] * self.CELL_SIZE
        x2 = x1 + self.CELL_SIZE
        y2 = y1 + self.CELL_SIZE
        
        # Draw apple-like food
        self.canvas.create_oval(
            x1 + 2, y1 + 2, x2 - 2, y2 - 2,
            fill=self.COLORS['food'],
            outline='',
            tags='food'
        )
        
        # Draw stem
        stem_width = self.CELL_SIZE // 6
        self.canvas.create_rectangle(
            x1 + self.CELL_SIZE // 2 - stem_width // 2,
            y1 - 2,
            x1 + self.CELL_SIZE // 2 + stem_width // 2,
            y1 + self.CELL_SIZE // 4,
            fill='#795548',
            outline='',
            tags='food'
        )
        
        # Draw highlight
        highlight_size = self.CELL_SIZE // 4
        self.canvas.create_oval(
            x1 + self.CELL_SIZE // 3,
            y1 + self.CELL_SIZE // 4,
            x1 + self.CELL_SIZE // 3 + highlight_size,
            y1 + self.CELL_SIZE // 4 + highlight_size,
            fill='#FF8A65',
            outline='',
            tags='food'
        )
        
        # Draw super food if exists
        if self.super_food:
            x1 = self.super_food['x'] * self.CELL_SIZE
            y1 = self.super_food['y'] * self.CELL_SIZE
            x2 = x1 + self.CELL_SIZE
            y2 = y1 + self.CELL_SIZE
            
            # Draw star shape
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            radius = self.CELL_SIZE // 2 - 2
            
            points = []
            for i in range(10):
                angle = i * 36 * 3.14159 / 180
                r = radius if i % 2 == 0 else radius / 2
                points.append(center_x + r * math.cos(angle))
                points.append(center_y + r * math.sin(angle))
            
            self.canvas.create_polygon(
                points,
                fill=self.COLORS['super_food'],
                outline='',
                tags='super_food'
            )
        
        # Draw poison food if exists
        if self.poison_food:
            x1 = self.poison_food['x'] * self.CELL_SIZE
            y1 = self.poison_food['y'] * self.CELL_SIZE
            x2 = x1 + self.CELL_SIZE
            y2 = y1 + self.CELL_SIZE
            
            # Draw skull shape
            self.canvas.create_oval(
                x1 + self.CELL_SIZE // 4, y1 + self.CELL_SIZE // 4,
                x2 - self.CELL_SIZE // 4, y2 - self.CELL_SIZE // 4,
                fill=self.COLORS['poison'],
                outline='',
                tags='poison'
            )
            
            # Draw eye sockets
            eye_size = self.CELL_SIZE // 6
            self.canvas.create_oval(
                x1 + self.CELL_SIZE // 3 - eye_size, y1 + self.CELL_SIZE // 3 - eye_size,
                x1 + self.CELL_SIZE // 3 + eye_size, y1 + self.CELL_SIZE // 3 + eye_size,
                fill='white',
                outline='',
                tags='poison'
            )
            self.canvas.create_oval(
                x2 - self.CELL_SIZE // 3 - eye_size, y1 + self.CELL_SIZE // 3 - eye_size,
                x2 - self.CELL_SIZE // 3 + eye_size, y1 + self.CELL_SIZE // 3 + eye_size,
                fill='white',
                outline='',
                tags='poison'
            )
    
    def draw_walls(self):
        for wall in self.walls:
            x1 = wall['x'] * self.CELL_SIZE
            y1 = wall['y'] * self.CELL_SIZE
            x2 = x1 + self.CELL_SIZE
            y2 = y1 + self.CELL_SIZE
            
            # Draw brick pattern
            brick_height = self.CELL_SIZE // 3
            for i in range(3):
                brick_y1 = y1 + i * brick_height
                brick_y2 = brick_y1 + brick_height
                
                # Alternate brick offsets
                offset = (i % 2) * (self.CELL_SIZE // 2)
                
                self.canvas.create_rectangle(
                    x1 + offset, brick_y1,
                    x1 + offset + self.CELL_SIZE // 2, brick_y2,
                    fill=self.COLORS['wall'],
                    outline='#455A64',
                    width=1,
                    tags='wall'
                )
                self.canvas.create_rectangle(
                    x1 + offset + self.CELL_SIZE // 2, brick_y1,
                    x2, brick_y2,
                    fill=self.COLORS['wall'],
                    outline='#455A64',
                    width=1,
                    tags='wall'
                )
    
    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        if (new_direction == 'Up' and self.direction != 'Down' or
            new_direction == 'Down' and self.direction != 'Up' or
            new_direction == 'Left' and self.direction != 'Right' or
            new_direction == 'Right' and self.direction != 'Left'):
            self.next_direction = new_direction
    
    def start_game(self):
        if not self.game_running:
            self.game_running = True
            self.start_button.config(state=tk.DISABLED)
            self.game_loop()
    
    def toggle_pause(self):
        if self.game_running:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.pause_button.config(text="RESUME", bg='#4CAF50')
            else:
                self.pause_button.config(text="PAUSE", bg='#FF9800')
                self.game_loop()
    
    def update_labels(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")
        self.level_label.config(text=f"Level: {self.level}")
    
    def move_snake(self):
        # Update direction
        self.direction = self.next_direction
        
        # Get head position
        head = self.snake[0].copy()
        
        # Move head based on direction
        if self.direction == 'Up':
            head['y'] -= 1
        elif self.direction == 'Down':
            head['y'] += 1
        elif self.direction == 'Left':
            head['x'] -= 1
        elif self.direction == 'Right':
            head['x'] += 1
        
        # Check wall collision
        if (head['x'] < 0 or head['x'] >= self.GRID_WIDTH or
            head['y'] < 0 or head['y'] >= self.GRID_HEIGHT):
            self.game_over()
            return False
        
        # Check self collision
        if any(segment['x'] == head['x'] and segment['y'] == head['y'] 
               for segment in self.snake):
            self.game_over()
            return False
        
        # Check wall obstacle collision
        if any(wall['x'] == head['x'] and wall['y'] == head['y'] 
               for wall in self.walls):
            self.game_over()
            return False
        
        # Add new head
        self.snake.insert(0, head)
        
        # Check food collision
        food_eaten = False
        if head['x'] == self.food['x'] and head['y'] == self.food['y']:
            self.score += 1
            self.food = self.generate_food()
            food_eaten = True
            
            # Check for level up
            if self.score % 5 == 0:
                self.level_up()
        
        # Check super food collision
        if self.super_food and head['x'] == self.super_food['x'] and head['y'] == self.super_food['y']:
            self.score += 5
            self.super_food = None
            food_eaten = True
        
        # Check poison food collision
        if self.poison_food and head['x'] == self.poison_food['x'] and head['y'] == self.poison_food['y']:
            self.score = max(0, self.score - 2)
            self.poison_food = None
            
            # Remove tail segments as penalty
            for _ in range(2):
                if len(self.snake) > 3:
                    self.snake.pop()
        
        # Remove tail if no food was eaten
        if not food_eaten:
            self.snake.pop()
        
        return True
    
    def generate_special_foods(self):
        # Generate super food occasionally
        if self.special_food_timer <= 0 and random.random() < 0.02 and not self.super_food:
            while True:
                super_food = {
                    'x': random.randint(0, self.GRID_WIDTH - 1),
                    'y': random.randint(0, self.GRID_HEIGHT - 1)
                }
                
                # Check valid position
                if (not any(segment['x'] == super_food['x'] and segment['y'] == super_food['y'] 
                           for segment in self.snake) and
                    not (self.food['x'] == super_food['x'] and self.food['y'] == super_food['y']) and
                    not any(wall['x'] == super_food['x'] and wall['y'] == super_food['y'] 
                           for wall in self.walls)):
                    self.super_food = super_food
                    self.special_food_timer = 100  # Frames until next chance
                    break
        
        # Generate poison food occasionally
        if self.poison_food_timer <= 0 and random.random() < 0.015 and not self.poison_food:
            while True:
                poison_food = {
                    'x': random.randint(0, self.GRID_WIDTH - 1),
                    'y': random.randint(0, self.GRID_HEIGHT - 1)
                }
                
                # Check valid position
                if (not any(segment['x'] == poison_food['x'] and segment['y'] == poison_food['y'] 
                           for segment in self.snake) and
                    not (self.food['x'] == poison_food['x'] and self.food['y'] == poison_food['y']) and
                    not (self.super_food and self.super_food['x'] == poison_food['x'] and 
                         self.super_food['y'] == poison_food['y']) and
                    not any(wall['x'] == poison_food['x'] and wall['y'] == poison_food['y'] 
                           for wall in self.walls)):
                    self.poison_food = poison_food
                    self.poison_food_timer = 150  # Frames until next chance
                    break
        
        # Decrease timers
        if self.special_food_timer > 0:
            self.special_food_timer -= 1
        if self.poison_food_timer > 0:
            self.poison_food_timer -= 1
        
        # Remove special foods after some time
        if self.super_food and random.random() < 0.01:
            self.super_food = None
        if self.poison_food and random.random() < 0.008:
            self.poison_food = None
    
    def level_up(self):
        self.level += 1
        # Increase speed (but not too fast)
        self.speed = max(50, self.speed - 10)
        
        # Add more walls
        self.generate_walls()
        
        # Show level up message
        self.show_floating_text("LEVEL UP!", self.COLORS['super_food'])
    
    def show_floating_text(self, text, color):
        # Show temporary text on canvas
        x = self.GAME_WIDTH // 2
        y = self.GAME_HEIGHT // 2
        
        text_id = self.canvas.create_text(
            x, y,
            text=text,
            font=('Arial', 24, 'bold'),
            fill=color,
            tags='floating_text'
        )
        
        # Animate text
        def animate_text(step=0):
            if step < 30:
                self.canvas.move(text_id, 0, -2)
                self.root.after(50, lambda: animate_text(step + 1))
            else:
                self.canvas.delete(text_id)
        
        animate_text()
    
    def game_over(self):
        self.game_running = False
        self.start_button.config(state=tk.NORMAL)
        
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            self.show_floating_text("NEW HIGH SCORE!", '#FFD700')
        
        # Show game over text
        self.canvas.create_text(
            self.GAME_WIDTH // 2,
            self.GAME_HEIGHT // 2,
            text="GAME OVER",
            font=('Arial', 32, 'bold'),
            fill='#F44336',
            tags='game_over'
        )
        
        self.canvas.create_text(
            self.GAME_WIDTH // 2,
            self.GAME_HEIGHT // 2 + 40,
            text=f"Score: {self.score} | Level: {self.level}",
            font=('Arial', 16),
            fill='white',
            tags='game_over'
        )
        
        self.canvas.create_text(
            self.GAME_WIDTH // 2,
            self.GAME_HEIGHT // 2 + 70,
            text="Press START to play again",
            font=('Arial', 14),
            fill='white',
            tags='game_over'
        )
    
    def game_loop(self):
        if self.game_running and not self.game_paused:
            # Clear canvas
            self.canvas.delete("all")
            self.draw_grid()
            
            # Update game state
            if self.move_snake():
                self.generate_special_foods()
                
                # Draw everything
                self.draw_walls()
                self.draw_snake()
                self.draw_food()
                
                # Update labels
                self.update_labels()
                
                # Schedule next frame
                self.root.after(self.speed, self.game_loop)
        elif self.game_paused:
            # Draw pause text
            self.canvas.create_text(
                self.GAME_WIDTH // 2,
                self.GAME_HEIGHT // 2,
                text="PAUSED",
                font=('Arial', 32, 'bold'),
                fill='#FF9800',
                tags='pause'
            )

# Import math for star shape
import math

def main():
    root = tk.Tk()
    game = SnakeGame(root)
    
    # Show welcome message
    messagebox.showinfo(
        "Snake Game - Advanced",
        "Welcome to Snake Game!\n\n"
        "CONTROLS:\n"
        "• Arrow Keys or WASD: Control snake direction\n"
        "• SPACE: Start game\n"
        "• P: Pause/Resume\n"
        "• R: Reset game\n\n"
        "GAME FEATURES:\n"
        "• Normal Food: +1 point\n"
        "• Super Food (star): +5 points\n"
        "• Poison Food (skull): -2 points, removes tail\n"
        "• Walls: Avoid them!\n"
        "• Level Up: Every 5 points increases difficulty\n\n"
        "Try to beat the high score!"
    )
    
    root.mainloop()

if __name__ == "__main__":
    main()