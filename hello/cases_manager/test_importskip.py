import pytest
'''
pytest.importorskip('pytest') 缺少导入就跳过该module
'''

@pytest.fixture()
def login():
    print("前置处理...")
    yield
    print('后置处理...done')

def test_login(login):
    print("测试函数一...")

# @pytest.importorskip("os", minversion='8.3.5', reason="框架必须")
def test_login1(login):
    print("测试函数二...")

@pytest.importorskip("fastapi", minversion='1.0.2', reason="测试导入", exc_type=ModuleNotFoundError )
def test_login2(login):
    print("测试函数三...")

# if __name__ == '__main__':
#     pytest.main()