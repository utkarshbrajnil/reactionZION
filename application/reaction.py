"""Core Flask app routes."""

from flask import Flask, render_template, url_for, redirect, flash
from flask import current_app as app
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

from application.ytmain import ytload


#app = Flask(__name__)
app.config['SECRET_KEY'] = 'acbsd'
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/overview")
def overview():
    return render_template('overview.html', title='Overview')

@app.route("/twitter")
def twitter():
    return render_template('twitter.html', title='Twitter')

@app.route("/reddit")
def reddit():
    return render_template('reddit.html', title='Reddit')

@app.route("/youtube")
def youtube():
    return render_template('youtube.html', title='Youtube')

@app.route("/analyse", methods=['GET','POST'])
def analyse():
    class inputform(FlaskForm):
        query=StringField('Enter the term you want to analyse.', validators=[DataRequired()])
        submit= SubmitField('Create Dashboard')

    form=inputform()
    if form.is_submitted():
        ytload(form.query.data)
        flash(f'Almost done! Now CLICK on Dashboard to start creating your analytics dashboard for {form.query.data}.','success')
        return redirect(url_for('home'))
    return render_template('analyse.html', title='Analyse',form=form)














if __name__=='__main__':
    app.run(debug=True)
