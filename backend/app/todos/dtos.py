from web_fractal.dtos import Base


class TodoCreate(Base):
    title: str
    user_id: int
