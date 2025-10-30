class GameEngine:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.reset_game()
    
    def reset_game(self):
        """重置游戏状态"""
        # 蛇的初始位置和方向
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = (1, 0)  # 向右移动
        
        # 生成第一个食物
        self.food = self._generate_food()
        self.score = 0
        self.game_over = False
    
    def _generate_food(self):
        """在随机位置生成食物，确保不在蛇身上"""
        import random
        while True:
            food = (random.randint(0, self.width - 1), 
                   random.randint(0, self.height - 1))
            # FIXME: 实验二：自动化测试用例生成
            if food not in self.snake: #正确
            # if food in self.snake: #错误
                return food
    
    # FIXME: 实验一：智能代码补全测试
    def change_direction(self, new_direction):
        """改变蛇的移动方向（防止直接反向移动）"""
        # 防止直接反向移动（例如从左直接向右）
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    
    def update(self):
        """更新游戏状态：移动蛇，检查碰撞，吃食物"""
        if self.game_over:
            return False
        
        # 计算新的蛇头位置
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # 检查碰撞：撞墙或撞到自己
        # FIXME：实验二：自动化测试用例生成
        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height or
            new_head in self.snake): #正确
        # if (new_head[0] < 0 or new_head[0] >= self.width or
        #     new_head[1] < 0 or new_head[1] >= self.height): #错误
            self.game_over = True
            return False
        
        # 移动蛇：添加新头，移除旧尾（除非吃到食物）
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            # 吃到食物：增加分数，生成新食物，不移除蛇尾
            self.score += 10
            self.food = self._generate_food()
        else:
            # 没吃到食物：移除蛇尾
            self.snake.pop()
        
        return True
    
    def get_game_state(self):
        """返回当前游戏状态（用于测试）"""
        return {
            'snake': self.snake.copy(),
            'food': self.food,
            'score': self.score,
            'game_over': self.game_over,
            'width': self.width,
            'height': self.height
        }