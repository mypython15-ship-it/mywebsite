from flask import Blueprint, render_template, flash, redirect, url_for, abort
from forms import TaskCreationForm, EmptyForm, FriendForm
from extensions import db
from models import User, Friendship
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import or_, and_

friends = Blueprint("friends", __name__)


@friends.route("/friends")
@login_required
def index():
    friendships = 
    form = EmptyForm()
    return render_template("friends.html", form=form, friendships=friendships)


@friends.route("/friends/add", methods=["GET", "POST"])
@login_required
def send_friend_request():
    form = FriendForm()
    if form.validate_on_submit():
        receiver = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar()
        if not receiver or current_user.id == receiver.id:
            abort(403)
        if db.session.execute(db.select(Friendship).filter(or_(and_(Friendship.requester_id==current_user.id, Friendship.receiver_id== receiver.id),
                                     and_(Friendship.requester_id==receiver.id, Friendship.receiver_id== current_user.id)))).scalar():
            abort(403)
        new_friendship = Friendship(
            requester_id = current_user.id,
            receiver_id = receiver.id,
            status = "pending"
        )
        db.session.add(new_friendship)
        db.session.commit()
        return redirect(url_for("friends.index"))

    return render_template("addfriend.html")


