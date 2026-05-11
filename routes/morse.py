from flask import Blueprint, render_template
from forms import TextToMorseForm
from morse import encode_to_morse

morse = Blueprint("morse", __name__)


@morse.route("/morse", methods=["GET", "POST"])
def index():
    form = TextToMorseForm()

    if form.validate_on_submit():
        text = encode_to_morse(form.text.data)
        return render_template("morse.html", text=text, form=form)

    return render_template("morse.html", form=form)