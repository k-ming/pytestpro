from pickle import FALSE

import pytest
'''
pytest.mark.xfail
'''

@pytest.mark.own
@pytest.mark.xfail(condition=2>1, reason='满足条件，标记失败', run=False, raises=BaseException, strict=False)
def test_fail():
    print("测试标记失败...")
@pytest.mark.own
def test_success():
    print("测试通过...")