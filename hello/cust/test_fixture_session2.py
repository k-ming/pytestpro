
def test_fixture1(login):
    print("module2测试函数一...")

def test_fixture2(login):
    print("module2测试函数二...")


class TestLogin:
    def test_logout(self, login):
        print("module2 class1 测试方法一...")

    def test_register(self, login):
        print("module2 class1 测试方法二...")

class TestLogin2:
    def test_cor(self, login):
        print("module2 class2 测试方法一...")

    def test_card(self, login):
        print("module2 class2测试方法二...")