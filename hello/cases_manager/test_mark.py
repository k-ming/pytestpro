import pytest
'''
model: 标记模型相关的测试
regular: 标记常规测试
slow: 标记慢测试
smoke: 冒烟测试
integration: 集成测试
regression: 回归测试
执行时可指定具体的标记，如 pytest -m 'model'  pytest -m 'not regular' pytest -m 'model or regular'
'''

@pytest.mark.model
def test_mark_model():
    print('测试mark.model函数...')

@pytest.mark.regular
def test_mark_regular():
    print('测试mark.regular函数二...')

@pytest.mark.smoke
class TestMark:
    def test_mark1(self):
        print("测试方法一...")

    def test_mark2(self):
        print("测试方法二...")

# if __name__ == '__main__':
#     pytest.main(['-s', '-m', 'model'])