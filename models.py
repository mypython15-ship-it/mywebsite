from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from extensions import db
from datetime import datetime
from typing import Optional


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    tasks: Mapped[list["Task"]] = relationship(back_populates="creator")
    shared_tasks: Mapped[list["TaskShare"]] = relationship(back_populates="user")
    sent_requests: Mapped[list["Friendship"]] = relationship(
        back_populates="requester",
        foreign_keys="[Friendship.requester_id]"
    )

    received_requests: Mapped[list["Friendship"]] = relationship(
        back_populates="receiver",
        foreign_keys="[Friendship.receiver_id]"
    )    


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    deadline: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    category: Mapped[Optional[str]] = mapped_column(nullable=True)
    repetition: Mapped[Optional[int]] = mapped_column(nullable=True)


    creator: Mapped["User"] = relationship(back_populates="tasks")
    shares: Mapped[list["TaskShare"]] = relationship(back_populates="task")
    
    
    @property
    def is_completed(self):
        if self.completed_at is None:
            return False
        if not self.repetition:
            return True
        elapsed = datetime.utcnow() - self.completed_at
        return elapsed.days < self.repetition




class TaskShare(db.Model):
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    task: Mapped["Task"] = relationship(back_populates="shares")
    user: Mapped["User"] = relationship(back_populates="shared_tasks")



    # Permission to be added


class Friendship(db.Model):
    requester_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    status: Mapped[str] = mapped_column(nullable=False, default="pending")

    requester: Mapped["User"] = relationship(
        back_populates="sent_requests",
        foreign_keys=[requester_id]
    )

    receiver: Mapped["User"] = relationship(
        back_populates="received_requests", 
        foreign_keys=[receiver_id]
    )