"""Token 刷新机制单元测试（Python 内置 unittest，无需额外依赖）。

运行方式：
    cd backend
    python -m unittest discover -s tests -v

说明：测试依赖后端连接的 MySQL 与系统初始化的 admin 账号（admin/123456），
本测试只发起登录与刷新请求，不修改数据库业务数据。
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # noqa: E402

ADMIN_USER = 'admin'
ADMIN_PWD = '123456'


class TokenRefreshTest(unittest.TestCase):
    """验证登录双 Token 与 /api/auth/refresh 刷新逻辑。"""

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.app = app
        cls.client = app.test_client()

    def login(self, username=ADMIN_USER, password=ADMIN_PWD):
        return self.client.post('/api/auth/login',
                                json={'username': username, 'password': password})

    def test_login_returns_both_tokens(self):
        """登录成功应同时返回 access_token 与 refresh_token，且时长符合约定。"""
        r = self.login()
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertTrue(data.get('access_token'), '缺少 access_token')
        self.assertTrue(data.get('refresh_token'), '缺少 refresh_token')
        self.assertEqual(data.get('access_expires'), 2 * 3600)
        self.assertEqual(data.get('refresh_expires'), 7 * 24 * 3600)

    def test_refresh_token_exchanges_new_access(self):
        """用 refresh_token 应换取新的 access_token。"""
        rt = self.login().get_json()['refresh_token']
        r = self.client.post('/api/auth/refresh', json={'refresh_token': rt})
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertTrue(data.get('access_token'))

    def test_new_access_token_works_on_protected_api(self):
        """刷新得到的新 access_token 应能访问受保护接口。"""
        rt = self.login().get_json()['refresh_token']
        new_at = self.client.post('/api/auth/refresh',
                                  json={'refresh_token': rt}).get_json()['access_token']
        r = self.client.get('/api/logs/',
                            headers={'Authorization': f'Bearer {new_at}'})
        # 200=正常；403/400 均说明 token 本身有效（进入了权限/参数判断）
        self.assertIn(r.status_code, (200, 403))

    def test_refresh_rejects_access_token(self):
        """access_token 不能当作 refresh_token 使用。"""
        at = self.login().get_json()['access_token']
        r = self.client.post('/api/auth/refresh', json={'refresh_token': at})
        self.assertEqual(r.status_code, 401)
        self.assertIn('token 类型', r.get_json().get('error', ''))

    def test_refresh_rejects_invalid_token(self):
        """无效 refresh_token 应返回 401。"""
        r = self.client.post('/api/auth/refresh',
                             json={'refresh_token': 'invalid.token.value'})
        self.assertEqual(r.status_code, 401)

    def test_refresh_missing_token(self):
        """缺少 refresh_token 应返回 400。"""
        r = self.client.post('/api/auth/refresh', json={})
        self.assertEqual(r.status_code, 400)
        self.assertIn('refresh_token', r.get_json().get('error', ''))

    def test_whitespace_or_null_refresh_token(self):
        """refresh_token 为空串/null 应视为缺失返回 400。"""
        for bad in ('', None, '   '):
            with self.subTest(value=bad):
                r = self.client.post('/api/auth/refresh',
                                     json={'refresh_token': bad})
                self.assertEqual(r.status_code, 400)


if __name__ == '__main__':
    unittest.main()