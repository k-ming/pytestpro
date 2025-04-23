import pytest
'''
本文件测试 前后置函数相互调用
'''

@pytest.fixture()
def login1():
    print('函数一前置...')
    yield
    print('函数一后置...')

@pytest.fixture()
def login2(login1):
    print('函数二前置...')
    yield
    print('函数二后置...')

@pytest.fixture()
def login3(login2):
    print('函数三前置...')
    yield
    print('函数三后置...')

def test_xianghu(login3):
    print("测试函数一...")
class TestXiangHu:
    def test_login1(self, login1):
        print("测试方法一...")

    def test_login2(self, login2):
        print("测试方法二...")

    def test_login3(self, login3):
        print('测试前置函数三...')


if __name__ == '__main__':
    pytest.main()