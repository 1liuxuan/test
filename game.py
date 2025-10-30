import pygame
from game_engine import GameEngine
from renderer import GameRenderer

def main():
    # 初始化游戏
    pygame.init()
    game_engine = GameEngine(20, 20)
    renderer = GameRenderer()
    
    renderer.initialize_display(game_engine.width, game_engine.height)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game_engine.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    game_engine.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    game_engine.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    game_engine.change_direction((1, 0))
                elif event.key == pygame.K_r and game_engine.game_over:
                    game_engine.reset_game()
        
        # 更新游戏状态
        game_engine.update()
        
        # 渲染游戏画面
        renderer.draw(game_engine.get_game_state())
        
        # 控制游戏帧率
        clock.tick(5)  # 10 FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()