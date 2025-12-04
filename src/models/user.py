"""
User 類別
使用者資料模型
"""

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING
from .user_profile import UserProfile

if TYPE_CHECKING:
    from .diet_log import DietLog


@dataclass
class User:
    """使用者"""
    user_id: str
    username: str
    hashed_password: str
    profile: Optional[UserProfile] = None
    diet_logs: List['DietLog'] = field(default_factory=list)

    def __init__(
        self,
        user_id: str,
        username: str,
        hashed_password: str,
        profile: Optional[UserProfile] = None
    ):
        self.user_id = user_id
        self.username = username
        self.hashed_password = hashed_password
        self.profile = profile
        self.diet_logs = []

    def login(self, username: str, password: str) -> bool:
        """
        登入驗證
        
        Args:
            username: 使用者名稱
            password: 密碼（明文）
        
        Returns:
            bool: 登入是否成功
        """
        # TODO: implement login logic
        # 應該使用 werkzeug.security.check_password_hash 驗證密碼
        return False

    def register(self) -> bool:
        """
        註冊新使用者
        
        Returns:
            bool: 註冊是否成功
        """
        # TODO: implement registration logic
        # 應該將使用者資料儲存到資料庫
        return False

    def get_profile(self) -> Optional[UserProfile]:
        """
        取得使用者個人資料
        
        Returns:
            UserProfile: 使用者個人資料，如果不存在則返回 None
        """
        return self.profile
