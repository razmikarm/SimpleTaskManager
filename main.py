import uvicorn
import bcrypt
from sqlmodel import Session, select
from fastapi import FastAPI, Depends, HTTPException

from database import get_session, create_db_and_tables
from models import Task, User
from schemas import TaskRead, TaskCreate, UserRead, UserCreate, UserLogin, TaskUpdate


def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


# USER ROUTES

@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_session)):
    return db.exec(select(User).where(User.id == user_id)).first()

@app.post("/users/login", response_model=UserRead)
def login_user(user: UserLogin, db: Session = Depends(get_session)):
    db_user = db.exec(select(User).where(User.email == user.email)).first()
    if db_user and bcrypt.checkpw(user.password.encode('utf-8'), db_user.password):
        return db_user
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


# TASK ROUTES

@app.post("/tasks", response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_session)):
    db_task = Task(
        title=task.title,
        description=task.description
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_session)):
    return db.exec(select(Task).where(Task.id == task_id)).first()

@app.get("/tasks", response_model=list[TaskRead])
def get_tasks(db: Session = Depends(get_session)):
    return db.exec(select(Task)).all()


@app.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_session)):
    db_task = db.exec(select(Task).where(Task.id == task_id)).first()
    db_task.completed = task.completed
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_session)):
    db_task = db.exec(select(Task).where(Task.id == task_id)).first()
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}

# END ROUTES

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
