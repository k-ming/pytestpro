import pytest

'''
fixture module 级别前后置处理scope="module", 同一个python文件中，所有的测试函数和方法都受影响
函数和方法需要在入参中显式调用，但是在第一个测试函数前调用前置，在最后一个测试函数或方法执行后调用后置
'''
@pytest.fixture(scope='module')
def login():
    print("module级别前置...")
    yield
    print("module级别后置...done")


def test_getInfo(login):
    print("测试函数一...")

def test_getUser(login):
    print("测试函数二...")

class TestLogin:
    def test_login(self, login):
        print("测试方法一...")

    def test_logout(self, login):
        print("测试方法二...")


if __name__ == '__main__':
    pytest.main()