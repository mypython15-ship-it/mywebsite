from flask import Blueprint, render_template, flash, redirect, url_for, abort
from forms import TaskCreationForm, EmptyForm
from extensions import db
from models import Task
from flask_login import login_required, current_user
from datetime import datetime


todolist = Blueprint("todolist", __name__)



@todolist.route("/todolist")
@login_required
def index():
    tasks = current_user.tasks
    form = EmptyForm()
    return render_template("todolist.html", tasks=tasks, form=form)

@todolist.route("/todolist/create_a_task", methods=["GET", "POST"])
@login_required
def task_creation():
    form = TaskCreationForm()
    if form.validate_on_submit():        
        new_task = Task(
            name = form.name.data,
            creator_id = current_user.id,
            repetition = form.repetition.data,
            category = form.category.data,
            deadline = form.deadline.data
        )
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for("todolist.index"))
    return render_template("taskcreation.html", form=form)


@todolist.route("/todolist/complete/<int:task_id>", methods=["POST"])
@login_required
def complete_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None or task.creator_id != current_user.id:
        abort(403)
    task.completed_at = datetime.utcnow()
    db.session.commit()
    return redirect(url_for("todolist.index"))


@todolist.route("/todolist/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None or task.creator_id != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("todolist.index"))