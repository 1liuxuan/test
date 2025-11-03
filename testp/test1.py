import unittest
from unittest.mock import patch
import random
from game_engine import GameEngine

class TestGameEngine(unittest.TestCase):
    def setUp(self):
        # 初始化游戏引擎
        self.engine = GameEngine(width=10, height=10)

    def test_update_happy_path(self):
        # 正常更新，蛇移动但未吃到食物
        initial_snake = self.engine.snake.copy()
        self.engine.update()
        updated_snake = self.engine.snake
        self.assertNotEqual(initial_snake, updated_snake)
        self.assertEqual(len(updated_snake), len(initial_snake))
        self.assertNotIn(self.engine.food, updated_snake)
        self.assertFalse(self.engine.game_over)

    def test_update_eat_food(self):
        # 蛇移动并吃到食物
        initial_score = self.engine.score
        initial_snake_length = len(self.engine.snake)
        self.engine.food = self.engine.snake[0]  # 将食物位置设为蛇头位置
        self.engine.update()
        self.assertEqual(self.engine.score, initial_score + 10)
        self.assertEqual(len(self.engine.snake), initial_snake_length + 1)
        self.assertFalse(self.engine.game_over)

    def test_update_hit_wall(self):
        # 蛇头撞墙
        self.engine.snake = [(0, 0)]
        self.engine.direction = (-1, 0)  # 向左移动
        self.engine.update()
        self.assertTrue(self.engine.game_over)

    def test_update_hit_self(self):
        # 蛇头撞到自己
        self.engine.snake = [(0, 0), (1, 0), (2, 0), (1, 0)]  # 制造自撞情况
        self.engine.direction = (-1, 0)  # 向左移动
        self.engine.update()
        self.assertTrue(self.engine.game_over)

    @patch('random.randint')
    def test_generate_food_not_on_snake(self, mock_randint):
        # 生成的食物不在蛇身上
        mock_randint.side_effect = [5, 5]  # 假设生成的食物位置为(5, 5)
        food = self.engine._generate_food()
        self.assertNotIn(food, self.engine.snake)

    @patch('random.randint')
    def test_generate_food_on_snake(self, mock_randint):
        # 生成的食物在蛇身上，直到生成不在蛇身上的位置
        self.engine.snake = [(5, 5)]
        mock_randint.side_effect = [5, 5, 6, 6]  # 前两次生成的食物位置为(5, 5)，后两次为(6, 6)
        food = self.engine._generate_food()
        self.assertNotIn(food, self.engine.snake)

    def test_change_direction_valid(self):
        # 改变方向为有效方向
        self.engine.change_direction((0, 1))  # 向下移动
        self.assertEqual(self.engine.direction, (0, 1))

    def test_change_direction_invalid(self):
        # 改变方向为无效方向（直接反向）
        self.engine.change_direction((-1, 0))  # 反向左移动
        self.assertNotEqual(self.engine.direction, (-1, 0))
        self.assertEqual(self.engine.direction, (1, 0))  # 方向不变

    def test_get_game_state(self):
        # 获取游戏状态
        state = self.engine.get_game_state()
        self.assertIn('snake', state)
        self.assertIn('food', state)
        self.assertIn('score', state)
        self.assertIn('game_over', state)
        self.assertIn('width', state)
        self.assertIn('height', state)
        self.assertEqual(state['snake'], self.engine.snake)
        self.assertEqual(state['food'], self.engine.food)
        self.assertEqual(state['score'], self.engine.score)
        self.assertEqual(state['game_over'], self.engine.game_over)
        self.assertEqual(state['width'], self.engine.width)
        self.assertEqual(state['height'], self.engine.height)

if __name__ == '__main__':
    unittest.main()
