import pytest

@pytest.fixture(scope='class', autouse=True)
def login():
    print("autouse前置处理...")
    yield
    print("autouse后置处理...")


def test_fix1():
    print("测试函数一...")

def test_fix2():
    print("测试函数二...")

class TestLogin:
    def test_login(self):
        print("类一测试方法一")
    def test_login2(self):
        print("类二测试方法二...")

class TestLogout:
    def test_logout(self):
        print()

if __name__ == '__main__':
    pytest.main()