import pytest
from game_engine import GameEngine

# 初始化测试
def test_initialization():
    engine = GameEngine()
    assert engine.width == 20
    assert engine.height == 20
    assert engine.snake == [(10, 10)]
    assert engine.direction == (1, 0)
    assert engine.score == 0
    assert engine.game_over is False

# 方向改变测试
def test_change_direction():
    engine = GameEngine()
    engine.change_direction((0, -1))  # 向下移动
    assert engine.direction == (0, -1)

    # 尝试反向移动，方向不应改变
    engine.change_direction((0, 1))  # 向上移动，应该是反向
    assert engine.direction == (0, -1)  # 方向保持不变

    # 正常改变方向
    engine.change_direction((-1, 0))  # 向左移动
    assert engine.direction == (-1, 0)

# 更新测试 - 正常移动
def test_update_normal_move():
    engine = GameEngine(width=5, height=5)
    engine.snake = [(1, 1)]
    engine.food = (2, 2)
    engine.direction = (1, 0)
    assert engine.update() is True
    assert engine.snake == [(2, 1)]
    assert engine.score == 0

# 更新测试 - 吃到食物
def test_update_eat_food():
    engine = GameEngine(width=5, height=5)
    engine.snake = [(1, 1)]
    engine.food = (2, 1)
    engine.direction = (1, 0)
    assert engine.update() is True
    assert engine.snake == [(2, 1), (1, 1)]
    assert engine.score == 10

# 更新测试 - 游戏结束 - 撞墙
def test_update_game_over_wall():
    engine = GameEngine(width=5, height=5)
    engine.snake = [(0, 0)]
    engine.food = (2, 1)
    engine.direction = (-1, 0)
    assert engine.update() is False
    assert engine.game_over is True

# 更新测试 - 游戏结束 - 撞到自己
def test_update_game_over_self():
    engine = GameEngine(width=5, height=5)
    engine.snake = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    engine.food = (2, 1)
    engine.direction = (-1, 0)
    assert engine.update() is False
    assert engine.game_over is True

# 获取游戏状态测试
def test_get_game_state():
    engine = GameEngine(width=10, height=10)
    state = engine.get_game_state()
    assert state['width'] == 10
    assert state['height'] == 10
    assert state['snake'] == [(5, 5)]
    assert state['food'] is not None
    assert state['score'] == 0
    assert state['game_over'] is False
