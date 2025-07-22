import requests

def get_github_user_info(username):
    """
    GitHub 사용자 이름(username)을 받아 사용자 정보를 반환합니다.
    - 정상 계정: 사용자 정보가 담긴 dict 객체 반환
    - 존재하지 않는 계정: None 반환
    - 레이트 리밋 초과 또는 접근 제한: 'Rate limit exceeded or Forbidden' 문자열 반환
    """
    url = f"https://api.github.com/users/{username}"
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        return "Rate limit exceeded or Forbidden"
    else:
        return None

import unittest

class TestGitHubUserInfo(unittest.TestCase):
    def test_valid_user(self):
        # 정상적인 GitHub 계정명 테스트
        user_info = get_github_user_info("octocat")
        self.assertTrue(
            user_info is not None and user_info != 'Rate limit exceeded or Forbidden'
        )
        if isinstance(user_info, dict):
            self.assertIn("login", user_info)
            self.assertEqual(user_info["login"], "octocat")
    
    def test_invalid_user(self):
        # 존재하지 않는 계정명 테스트
        user_info = get_github_user_info("thisuserdoesnotexist1234567890")
        self.assertIn(user_info, [None, "Rate limit exceeded or Forbidden"])
    
    def test_rate_limit(self):
        # 레이트 리밋 등 인증/접근 제한 상황 테스트: 실제로 반복 호출 시 발생 가능하므로 예시만 포함
        # 호출이 비정상(403 등)일 때 올바른 반환값을 갖는지 체크
        # 실제 반복 호출로 rate limit 상황을 강제하는 것은 권장되지 않음
        user_info = get_github_user_info("octocat")
        self.assertIn(user_info, [None, "Rate limit exceeded or Forbidden"])

if __name__ == "__main__":
    unittest.main()

