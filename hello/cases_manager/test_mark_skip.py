import pytest
'''
用例的跳过，及有条件判断的跳过
'''

@pytest.mark.skip(reason='无条件跳过测试函数一')
def test_login():
    print(' 测试函数一...')

def test_login1():
    print(' 测试函数二...')

@pytest.mark.skipif(condition=2>1, reason='条件判断为真，跳过测试函数三')
def test_login2():
    print(' 测试函数三...')

@pytest.mark.skip(reason="作用测试类，下面的测试方法都跳过")
class TestLogin:
    def test_login(self):
        print("测试方法一...")

class TestLogin2:
    def test_login1(self):
        print("测试方法二...")

    @pytest.mark.skipif(condition=2>1, reason="条件为真，跳过测试类中的方法三")
    def test_login2(self):
        print("测试方法三...")


if __name__ == '__main__':
    pytest.main()
