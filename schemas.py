from sqlmodel import Field, SQLModel

# TASK SCHEMAS

class TaskCreate(SQLModel):
    title: str
    description: str

class TaskRead(SQLModel):
    id: int
    title: str
    description: str
    completed: bool

class TaskUpdate(SQLModel):
    completed: bool


# USER SCHEMAS

class UserCreate(SQLModel):
    name: str
    email: str
    password: str

class UserLogin(SQLModel):
    email: str
    password: str

class UserRead(SQLModel):
    id: int
    name: str
    email: str
