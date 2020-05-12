from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/overview")
def overview():
    return render_template('overview.html', title='Overview')

@app.route("/twitter")
def twitter():
    return render_template('twitter.html', title='Twitter')

@app.route("/redit")
def redit():
    return render_template('redit.html', title='Redit')

@app.route("/youtube")
def youtube():
    return render_template('youtube.html', title='Youtube')













if __name__=='__main__':
    app.run(debug=True)
