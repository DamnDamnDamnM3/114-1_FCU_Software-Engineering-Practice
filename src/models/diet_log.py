"""
DietLog 類別
飲食記錄
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .menu_item import MenuItem
else:
    from .user import User
    from .menu_item import MenuItem


@dataclass
class DietLog:
    """飲食記錄"""
    log_id: str
    timestamp: datetime
    portion_size: str
    user: Optional['User'] = None
    menu_item: Optional['MenuItem'] = None

    def __init__(
        self,
        log_id: str,
        timestamp: Optional[datetime] = None,
        portion_size: str = "1"
    ):
        self.log_id = log_id
        self.timestamp = timestamp if timestamp else datetime.now()
        self.portion_size = portion_size
        self.user = None
        self.menu_item = None

    @staticmethod
    def create_log(user: 'User', menu_item: 'MenuItem', portion_size: str = "1") -> 'DietLog':
        """
        建立飲食記錄
        
        Args:
            user: 使用者
            menu_item: 菜單項目
            portion_size: 份量大小
        
        Returns:
            DietLog: 新建立的飲食記錄
        """
        import uuid
        from datetime import datetime
        
        log = DietLog(
            log_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            portion_size=portion_size
        )
        log.user = user
        log.menu_item = menu_item
        
        # 將記錄加入使用者的飲食記錄列表
        if log not in user.diet_logs:
            user.diet_logs.append(log)
        
        return log
