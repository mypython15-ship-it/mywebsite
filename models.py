from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from extensions import db
from datetime import datetime
from typing import Optional
from sqlalchemy import or_, and_



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

    @property
    def get_friends(self):
        friendships = db.session.execute(db.select(Friendship).filter(and_(or_(Friendship.requester_id==self.id, Friendship.receiver_id==self.id), Friendship.status =="accepted"))).scalars().all()
        friends = [friendship.receiver if friendship.requester_id == self.id else friendship.requester for friendship in friendships]
        return friends                         

    @property
    def get_friends_requests_pending(self):
        request_pending = db.session.execute(db.select(Friendship).filter(and_(Friendship.requester_id==self.id, Friendship.status =="pending"))).scalars().all()
        friends = [friendship.receiver for friendship in request_pending]
        return friends


    @property
    def get_friends_requests_to_accept(self):
        request_pending = db.session.execute(db.select(Friendship).filter(and_(Friendship.receiver_id==self.id, Friendship.status =="pending"))).scalars().all()
        friends = [friendship.requester for friendship in request_pending]
        return friends        


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