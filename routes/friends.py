from flask import Blueprint, render_template, flash, redirect, url_for, abort
from forms import TaskCreationForm, EmptyForm
from extensions import db
from models import Task
from flask_login import login_required, current_user
from datetime import datetime


friends = Blueprint("friends", __name__)


@friends.route("/friends")
@login_required
def index():
    form = EmptyForm()
    return render_template("friends.html", form=form)