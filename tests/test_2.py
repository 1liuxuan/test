import unittest
from unittest.mock import patch
import random
from game_engine import GameEngine

class TestGameEngine(unittest.TestCase):
    def setUp(self):
        self.game = GameEngine(width=10, height=10)

    # 测试初始化状态
    def test_initial_state(self):
        state = self.game.get_game_state()
        self.assertEqual(len(state['snake']), 1)
        self.assertEqual(state['score'], 0)
        self.assertFalse(state['game_over'])
        self.assertIn(state['food'], [(x, y) for x in range(10) for y in range(10) if (x, y) not in state['snake']])

    # 测试方向改变
    def test_change_direction(self):
        self.game.change_direction((0, 1))  # 向下
        self.assertEqual(self.game.direction, (0, 1))
        self.game.change_direction((1, 0))  # 向右
        self.assertEqual(self.game.direction, (1, 0))
        self.game.change_direction((-1, 0))  # 尝试向左（反向），方向不变
        self.assertEqual(self.game.direction, (1, 0))

    # 测试正常移动
    @patch.object(random, 'randint')
    def test_normal_move(self, mock_randint):
        mock_randint.return_value = 5  # 模拟生成的食物位置
        state = self.game.get_game_state()
        food_position = state['food']
        self.game.update()
        new_state = self.game.get_game_state()
        self.assertEqual(len(new_state['snake']), 2)
        self.assertEqual(new_state['snake'][0], (state['snake'][0][0] + 1, state['snake'][0][1]))
        # 如果新位置不是食物，确保蛇尾被移除
        if new_state['snake'][0] != food_position:
            self.assertNotEqual(new_state['snake'], state['snake'])
        else:
            self.assertEqual(new_state['score'], state['score'] + 10)
            self.assertNotEqual(new_state['food'], food_position)

    # 测试撞墙
    @patch.object(random, 'randint')
    def test_wall_collision(self, mock_randint):
        mock_randint.return_value = 5  # 模拟生成的食物位置
        self.game.snake = [(9, 5)]  # 蛇头在最右边
        self.game.update()
        self.assertTrue(self.game.game_over)

    # 测试撞到自己
    def test_self_collision(self):
        self.game.snake = [(5, 5), (4, 5), (3, 5), (4, 5)]  # 下一个位置会撞到自己
        self.game.update()
        self.assertTrue(self.game.game_over)

    # 测试吃到食物
    @patch.object(random, 'randint')
    def test_eat_food(self, mock_randint):
        mock_randint.return_value = 1  # 模拟生成的食物位置
        self.game.snake = [(1, 1), (0, 1)]
        self.game.food = (2, 1)  # 设置食物在蛇头的右边
        self.game.update()
        new_state = self.game.get_game_state()
        self.assertEqual(len(new_state['snake']), 3)
        self.assertEqual(new_state['score'], 10)

    # 测试重置游戏
    def test_reset_game(self):
        self.game.snake = [(1, 1), (0, 1)]
        self.game.food = (2, 1)
        self.game.score = 10
        self.game.game_over = True
        self.game.reset_game()
        state = self.game.get_game_state()
        self.assertEqual(len(state['snake']), 1)
        self.assertEqual(state['score'], 0)
        self.assertFalse(state['game_over'])
        self.assertIn(state['food'], [(x, y) for x in range(10) for y in range(10) if (x, y) not in state['snake']])

if __name__ == '__main__':
    unittest.main()
