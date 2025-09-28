from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    completed: bool = Field(default=False)


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
