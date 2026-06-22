from datetime import datetime
from web_fractal.dtos import Base


class TodoDM(Base):
    id: int
    title: str
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None
