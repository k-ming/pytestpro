# pytest 测试框架
## 一、框架约束
### 1.1、命名规则
- module 文件以test结尾或开头，如test_login.py
- class 以Test开头，且不能有构造方法，如class TestLogin：
- function 以test开头 如def test_login():
## 二、运行方式
### 2.1、主函数运行
```
class TestLogin:
    def test_login(self):
        print('test_login...')

if __name__ == '__main__':
    pytest.main()
```
### 2.2、命令行运行
```
# 当前路径运行
pytest ./test_login.py 
```
### 2.3、配置文件 pytest.ini 运行(常用)
```
[pytest]
addopts=-vs -m slow --html=./report/report.html
testpaths=testcase
test_files=test_*.py
test_classes=Test*
test_functions=test_*
makerers=
    smock:冒烟测试
```
## 三、共享机制 conftest.py
- 共享文件中一般设置是全局fixate，具有以下特点
- pytest会默认读取 conftest.py里面的所有fixture，不用import
- conftest.py 文件名称是固定的
- conftest.py 对当前目录下面的所有测试函数和测试类生效
- conftest,py 中的fixture，一般scope="session", 如下面的文件
```python
import pytest

@pytest.fixture(scope='session')
def login():
    print("session级别前置...")
    yield
    print("session级别后置...done")
```
## 四、前后置处理 fixture装饰器
### 4.1、fixture调用方式
#### 4.1.1、入参式调用
- 入参式调用是指 测试用例把 前后置函数的函数名作为入参，来显式调用，yield 之前是前置处理，yield之后是后置处理
```
@pytest.fixture()
def loginByPwd():
    print("loginByPwd...")

class TestLogin:
    def test_login(self, loginByPwd): 
        print('test_login...')
```
#### 4.1.2、fixture相互调用
- 相互调用指被调用的前后置函数本身调用了别的前后置函数，例如下面的脚本
```python
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
```
- 则执行结果如下，最外层前置函数会最先被调用，然后在一层层往内调用，用例执行结束后，最内层后置函数会最先执行，最后执行的是外层后置函数
```
============================= test session starts ==============================
collecting ... collected 4 items

test_xianghu.py::test_xianghu 函数一前置...
函数二前置...
函数三前置...
PASSED                                     [ 25%]测试函数一...
函数三后置...
函数二后置...
函数一后置...

test_xianghu.py::TestXiangHu::test_login1 函数一前置...
PASSED                         [ 50%]测试方法一...
函数一后置...

test_xianghu.py::TestXiangHu::test_login2 函数一前置...
函数二前置...
PASSED                         [ 75%]测试方法二...
函数二后置...
函数一后置...

test_xianghu.py::TestXiangHu::test_login3 函数一前置...
函数二前置...
函数三前置...
PASSED                         [100%]测试前置函数三...
函数三后置...
函数二后置...
函数一后置...
============================== 4 passed in 0.01s ===============================
```
### 4.2、fixture做用域
#### 4.2.1 function域
- scope="function"时，会在所有调用的测试函数或方法的前后各执行一次，默认就是function
级别，有如下测试module test_fixture_function
```python
import pytest

@pytest.fixture(scope='function')
def loginByPwd():
    # name = 'kingming'
    print("function级别前置..")  # 前置处理
    yield
    print("function级别后置...done") # 后置处理
    # return name

def test_get_user(loginByPwd):
    print("测试函数一...")

def test_get_account(loginByPwd):
    print("测试函数二...")


class TestLogin:
    def test_login(self, loginByPwd):
        print('test_login...')

    def test_getInfo(self, loginByPwd):
        print("test_getInfo...")

if __name__ == '__main__':
    pytest.main()
```
- 可以看到，不管是外部函数， 还是测试类中的测试方法，只要显式调用了前置函数，都会在前后各执行一次
```
============================= test session starts ==============================
collecting ... collected 4 items

test_fixture_func.py::test_get_user function级别前置..
PASSED                               [ 25%]测试函数一...
function级别后置...done

test_fixture_func.py::test_get_account function级别前置..
PASSED                            [ 50%]测试函数二...
function级别后置...done

test_fixture_func.py::TestLogin::test_login function级别前置..
PASSED                       [ 75%]test_login...
function级别后置...done

test_fixture_func.py::TestLogin::test_getInfo function级别前置..
PASSED                     [100%]test_getInfo...
function级别后置...done
```
#### 4.2.2 class域
- scope="class"时，会在测试类下面的测试方法开始前和结束后执行一次，而在外部的测试函数不受影响，例如有如下测试module test_fixture_class.py
``` python
import pytest

@pytest.fixture(scope='class')
def login():
    print("class级别前置...")
    yield
    print("class级别后置...done")

def test_getUser(login):
    print("测试函数一...")
    
def test_getInfo(login):
    print("测试函数二...")

class TestLogin:
    def test_login(self, login):
        print("类一测试方法一...")

    def test_logout(self, login):
        print("类一测试方法二...")

    def test_logoff(self, login):
        print("类一测试方法三...")


class TestAccount:
    def test_amount(self, login):
        print("类二测试方法一...")

    def test_getInfo(self, login):
        print("类二测试方法二...")


if __name__ == '__main__':
    pytest.main()
```
- 则执行结果如下, 可以看到 外部的两个测试函数，各自执行了一次前置和后置，而在测试类下面的测试方法执行前后只执行了一次前后置函数
```
============================= test session starts ==============================
collecting ... collected 7 items

test_fixture_class.py::test_getUser class级别前置...
PASSED                               [ 14%]测试函数一...
class级别后置...done

test_fixture_class.py::test_getInfo class级别前置...
PASSED                               [ 28%]测试函数二...
class级别后置...done

test_fixture_class.py::TestLogin::test_login class级别前置...
PASSED                      [ 42%]类一测试方法一...

test_fixture_class.py::TestLogin::test_logout PASSED                     [ 57%]类一测试方法二...

test_fixture_class.py::TestLogin::test_logoff PASSED                     [ 71%]类一测试方法三...
class级别后置...done

test_fixture_class.py::TestAccount::test_amount class级别前置...
PASSED                   [ 85%]类二测试方法一...

test_fixture_class.py::TestAccount::test_getInfo PASSED                  [100%]类二测试方法二...
class级别后置...done


============================== 7 passed in 0.01s ===============================
```
#### 4.2.3 module域
- scope="module" 时，是对当前py文件生效，和class类似，有如下测试文件 test_fixture_module.py
```python
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
```
- 则测试结果如下，和class唯一的区别是，不会区分外部测试函数 ，还是测试类下面的测试方法，在第一个case前执行一次前置，在做后一个case后面执行一次后置
```
============================= test session starts ==============================
collecting ... collected 4 items

test_fixture_module.py::test_getInfo module级别前置...
PASSED                              [ 25%]测试函数一...

test_fixture_module.py::test_getUser PASSED                              [ 50%]测试函数二...

test_fixture_module.py::TestLogin::test_login PASSED                     [ 75%]测试方法一...

test_fixture_module.py::TestLogin::test_logout PASSED                    [100%]测试方法二...
module级别后置...done


============================== 4 passed in 0.01s ===============================
```
#### 4.2.4 session域
- scope="session" 时和共享文件conftest.py 一期使用，则根目录下的所有测试类、测试方法、测试函数都会受影响，且前后置只会在开始和结束后执行一次，有如下目录和文件
```
__init__.py
conftest.py
run.py
test_fixture_session1.py
test_fixture_session2.py
```
- conftest.py 内容如下
```python
import pytest

@pytest.fixture(scope='session')
def login():
    print("session级别前置...")
    yield
    print("session级别后置...done")
```
- run.py 内容如下
```python
import pytest

if __name__ == "__main__":
    pytest.main(['-vs', './test_fixture_session1.py', './test_fixture_session2.py'])
```
- test_fixture_session1.py 和 test_fixture_session2.py内容相似
```python
def test_fixture1(login):
    print("module1测试函数一...")

def test_fixture2(login):
    print("module1测试函数二...")


class TestLogin:
    def test_login(self, login):
        print("module1 class1 测试方法一...")

    def test_info(self, login):
        print("module1 class1 测试方法二...")

class TestLogin2:
    def test_account(self, login):
        print("module1 class2 测试方法一...")

    def test_logoff(self, login):
        print("module1 class2测试方法二...")
```
- 则在run.py 中执行方法后会发现，这个目录下只执行了一次前后置函数
```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.3.5, pluggy-1.5.0 -- /Users/hb32366/devs/PyTestPro/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/hb32366/devs/PyTestPro/hello/cust
collecting ... collected 12 items

test_fixture_session1.py::test_fixture1 session级别前置...
module1测试函数一...
PASSED
test_fixture_session1.py::test_fixture2 module1测试函数二...
PASSED
test_fixture_session1.py::TestLogin::test_login module1 class1 测试方法一...
PASSED
test_fixture_session1.py::TestLogin::test_info module1 class1 测试方法二...
PASSED
test_fixture_session1.py::TestLogin2::test_account module1 class2 测试方法一...
PASSED
test_fixture_session1.py::TestLogin2::test_logoff module1 class2测试方法二...
PASSED
test_fixture_session2.py::test_fixture1 module2测试函数一...
PASSED
test_fixture_session2.py::test_fixture2 module2测试函数二...
PASSED
test_fixture_session2.py::TestLogin::test_logout module2 class1 测试方法一...
PASSED
test_fixture_session2.py::TestLogin::test_register module2 class1 测试方法二...
PASSED
test_fixture_session2.py::TestLogin2::test_cor module2 class2 测试方法一...
PASSED
test_fixture_session2.py::TestLogin2::test_card module2 class2测试方法二...
PASSEDsession级别后置...done

============================== 12 passed in 0.01s ==============================
```
### 4.3、fixture参数
#### 4.3.1 name参数
- name参数是指可以给前置函数取别名，测试函数或方法调用的时候直接用别名作为入参，前置函数的返回值，测试函数或方法可以直接获取到，如下
```python
import pytest
'''
本文测试函数的name参数，及返回值
'''

@pytest.fixture(name='fun_1')
def login():
    print("login前置...")
    yield
    print("login后置...done")

@pytest.fixture()
def login1():
    print('login1前置...')
    return 66

def test_login(fun_1):
    print("测试函数一...")


def test_login1(login1):
    print("测试函数二，获取到的return:{}".format(login1))

def test_logins(fun_1, login1):
    print("测试函数三，多调用，获取到的return:{}".format(login1))

if __name__ == '__main__':
    pytest.main()
```
- 则执行结果如下哦
```
============================= test session starts ==============================
collecting ... collected 3 items

test_fixture_name.py::test_login login前置...
PASSED                                  [ 33%]测试函数一...
login后置...done

test_fixture_name.py::test_login1 login1前置...
PASSED                                 [ 66%]测试函数二，获取到的return:66

test_fixture_name.py::test_logins login前置...
login1前置...
PASSED                                 [100%]测试函数三，多调用，获取到的return:66
login后置...done


============================== 3 passed in 0.01s ===============================

```
#### 4.3.2 parame参数
- @pytest.fixture(params=[1,2,(3,4,5),{"key1":"val1","key2":"val2"}]) 支持可迭代参数
- 则下面的测试脚本执行结果如下
```python
import pytest

@pytest.fixture(params=[1,2,(3,4,5),{"key1":"val1","key2":"val2"}])
def params(request):
    return request.param
```
```
============================= test session starts ==============================
collecting ... collected 4 items

test_params.py::test_params[1] PASSED                                    [ 25%]值:1

test_params.py::test_params[2] PASSED                                    [ 50%]值:2

test_params.py::test_params[params2] PASSED                              [ 75%]值:(3, 4, 5)

test_params.py::test_params[params3] PASSED                              [100%]值:{'key1': 'val1', 'key2': 'val2'}


============================== 4 passed in 0.01s ===============================
```
#### 4.3.3 ids参数
- ids 一般与 params 配合使用，和参数一一对应，则下面的代码执行后结果如下
```python
import  pytest

@pytest.fixture(params=[1,2,(3,4,5),{"key1":"val1","key2":"val2"}], ids=["id_1","id_2","id_3","id_4"])
def params_ids(request):
    return request.param


def test_params_2(params_ids):
    print(params_ids)
```
```
============================= test session starts ==============================
collecting ... collected 4 items

test_params.py::test_params_2[id_1] PASSED                               [ 25%]1

test_params.py::test_params_2[id_2] PASSED                               [ 50%]2

test_params.py::test_params_2[id_3] PASSED                               [ 75%](3, 4, 5)

test_params.py::test_params_2[id_4] PASSED                               [100%]{'key1': 'val1', 'key2': 'val2'}

============================== 4 passed in 0.01s ===============================
```
#### 4.3.4 autouse参数
- 当@fixture(autouse=true)时，即使不显式调用，也会自动在测试方法或函数前调用，按照指定的作用域执行，例如 test_fixture_autouse.py
```python
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
```
- 则执行结果如下,测试函数一、二各执行了一次前后置，测试类一、二各执行了一次前后置
```
============================= test session starts ==============================
collecting ... collected 5 items

test_fixture_autouse.py::test_fix1 autouse前置处理...
PASSED                                [ 20%]测试函数一...
autouse后置处理...

test_fixture_autouse.py::test_fix2 autouse前置处理...
PASSED                                [ 40%]测试函数二...
autouse后置处理...

test_fixture_autouse.py::TestLogin::test_login autouse前置处理...
PASSED                    [ 60%]类一测试方法一

test_fixture_autouse.py::TestLogin::test_login2 PASSED                   [ 80%]类二测试方法二...
autouse后置处理...

test_fixture_autouse.py::TestLogout::test_logout autouse前置处理...
PASSED                  [100%]
autouse后置处理...


============================== 5 passed in 0.01s ===============================

```
## 五、用例管理
### 5.1、 跳过用例pytest.mark.skip、pytest.mark.skipif
- 这两种标记可做用于测试函数、测试类、测试方法
- 作用于测试类时，该类下面的所有方法都被跳过，如下面的脚本
```python
import pytest

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
```
- 则执行结果如下
```
============================= test session starts ==============================
collecting ... collected 6 items

test_make_skip.py::test_login SKIPPED (无条件跳过测试函数一)             [ 16%]
Skipped: 无条件跳过测试函数一

test_make_skip.py::test_login1 PASSED                                    [ 33%] 测试函数二...

test_make_skip.py::test_login2 SKIPPED (条件判断为真，跳过测试函数三)    [ 50%]
Skipped: 条件判断为真，跳过测试函数三

test_make_skip.py::TestLogin::test_login SKIPPED (作用测试类，下面的测试方法都跳过) [ 66%]
Skipped: 作用测试类，下面的测试方法都跳过

test_make_skip.py::TestLogin2::test_login1 PASSED                        [ 83%]测试方法二...

test_make_skip.py::TestLogin2::test_login2 SKIPPED (条件为真，跳过测试类中的方法二) [100%]
Skipped: 条件为真，跳过测试类中的方法二


========================= 2 passed, 4 skipped in 0.01s =========================
```
### 5.2、pytest.skip() 装饰器
- pytest.skip()装饰在测试方法或函数外部时，是module级别的，即所有的测试函数、测试类、测试方法都不会执行
- 当用在外部时，需要指定 allow_module_level=True 参数，否则会报错，如下面的测试函数
```python
import pytest

@pytest.fixture()
def login():
    print('前置处理器...')
    yield
    print('后置处理器...done')

@pytest.skip(reason="随机跳过")
def test_login1(login):
    print('测试函数一...')
```
- 则运行时会有如下报错
```
============================= test session starts ==============================
collecting ... 
test_skip.py:None (test_skip.py)
Using pytest.skip outside of a test will skip the entire module. If that's your intention, pass `allow_module_level=True`. If you want to skip a specific test or an entire class, use the @pytest.mark.skip or @pytest.mark.skipif decorators.
collected 0 items / 1 error

!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 0.09s ===============================
```
- 不论测试函数，还是测试类，或测方法 pytest.skip()加上 allow_module_level=True 参数后，本python文件的测试用例都会被跳过，运行结果如下
```
============================= test session starts ==============================
collecting ... 
Skipped: 跳过测试方法二
collected 0 items / 1 skipped

============================== 1 skipped in 0.00s ==============================
```
- 在测方法或函数内部跳出，类似break
```python
import  pytest
class TestLogin:
    def test_login(self, login):
        print("测试方法一...")
    # @pytest.skip(reason ="跳过测试方法二",allow_module_level=True)
    def test_login2(self, login):
        i = 0
        while i < 10:
            print("测试方法二,循环{}...".format(i))
            i += 1
            if i == 6:
                pytest.skip(" 后面的不执行了...")

if __name__ == '__main__':
    pytest.main()
```
- 执行结果如下
```
test_skip.py::TestLogin::test_login 前置处理器...
PASSED                               [ 75%]测试方法一...
后置处理器...done

test_skip.py::TestLogin::test_login2 前置处理器...
SKIPPED ( 后面的不执行了...)        [100%]测试方法二,循环0...
测试方法二,循环1...
测试方法二,循环2...
测试方法二,循环3...
测试方法二,循环4...
测试方法二,循环5...

Skipped:  后面的不执行了...
后置处理器...done


========================= 3 passed, 1 skipped in 0.01s =========================
```
### 5.3、pytest.importskip() 缺少导入跳过
### 5.4、@pytest.mark.model @pytest.mark.regular 自定义标记
### 5.3、执行顺序
### 5.4、失败标记和失败重试
### 5.5、设置断点
## 六、数据驱动
### 6.1、 pytest.mark.parametrize参数化
## 七、测试报告管理
## 八、日志级别