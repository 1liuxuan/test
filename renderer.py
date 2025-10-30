import pygame

class GameRenderer:
    def __init__(self, cell_size=20):
        self.cell_size = cell_size
        self.colors = {
            'background': (15, 15, 15),
            'snake': (50, 205, 50),      #  LimeGreen
            'food': (255, 0, 0),         #  Red
            'text': (255, 255, 255)      #  White
        }
    
    def initialize_display(self, width, height):
        """初始化游戏窗口"""
        screen_width = width * self.cell_size
        screen_height = height * self.cell_size
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("snake test")
        self.font = pygame.font.Font(None, 36)
    
    def draw(self, game_state):
        """绘制游戏画面"""
        self.screen.fill(self.colors['background'])
        
        # 绘制食物
        food_x, food_y = game_state['food']
        pygame.draw.rect(self.screen, self.colors['food'],
                        (food_x * self.cell_size, food_y * self.cell_size,
                         self.cell_size, self.cell_size))
        
        # 绘制蛇
        for segment in game_state['snake']:
            x, y = segment
            pygame.draw.rect(self.screen, self.colors['snake'],
                           (x * self.cell_size, y * self.cell_size,
                            self.cell_size, self.cell_size))
        
        # 绘制分数
        score_text = self.font.render(f'score: {game_state["score"]}', True, self.colors['text'])
        self.screen.blit(score_text, (10, 10))
        
        # 游戏结束显示
        if game_state['game_over']:
            game_over_text = self.font.render('die! R to restart', True, self.colors['text'])
            text_rect = game_over_text.get_rect(center=(game_state['width'] * self.cell_size // 2, 
                                                       game_state['height'] * self.cell_size // 2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()