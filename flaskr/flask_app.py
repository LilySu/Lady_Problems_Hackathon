from datetime import datetime
 
from flask import (
Flask,
abort,
flash,
redirect,
render_template,
request,
url_for,
)
from flask_stormpath import (
StormpathError,
StormpathManager,
User,
login_required,
login_user,
logout_user,
user,
)

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'ilovecookies'
app.config['STORMPATH_API_KEY_ID'] = "4S13D31GXTI53QFHR4SSQ6W4D"
app.config['STORMPATH_API_KEY_SECRET'] = "ObAKdLI3Q+rh41ayYnek9hM4oC+J0tGTQ/BWdh2J7Bk"
app.config['STORMPATH_APPLICATION'] = 'flaskr'
 
stormpath_manager = StormpathManager(app)

#Flask app goes here 
@app.route("/")
def index():
    return "Index Page"


@app.route('/add', methods=['POST'])
@login_required
def add_post():
    if not user.custom_data.get('posts'):
        user.custom_data['posts'] = []

        user.custom_data['posts'].append({
        'date': datetime.utcnow().isoformat(),
        'title': request.form['title'],
        'text': request.form['text'],
        })
        user.save()

    flash('New post successfully added.')
    return redirect(url_for('show_posts'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        try:
            _user = User.from_login(
            request.form['email'],
            request.form['password'],
            )
            login_user(_user, remember=True)
            flash('You were logged in.')

            return redirect(url_for('show_posts'))
        except StormpathError:
            error = StormpathError

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out.')

    return redirect(url_for('show_posts'))

if __name__ == '__main__':
    app.run()