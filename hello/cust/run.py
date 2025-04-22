import pytest
'''
fixture session级别前后置处理，方法需要定义在 conftest.py文件中，scope="session"
所有在 conftest.py 的测试脚本都会收到影响，效果是在所有脚本执行前调用前置处理，所有脚本执行后调用后置脚本
'''

if __name__ == "__main__":
    pytest.main(['-vs', './test_fixture_session1.py', './test_fixture_session2.py'])