from flask import Flask, render_template , request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///comments.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class comm(db.Model):
    sno  = db.Column( db.Integer , primary_key = True)
    name = db.Column( db.String(200) , nullable = False)
    email = db.Column( db.String(50) , nullable = False)
    comment = db.Column( db.String(500) , nullable = False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.email}"
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':

        fname = request.form.get('name')
        femail = request.form.get('email')
        fcomment = request.form.get('comment')

        newcomm = comm( name = fname , email = femail , comment = fcomment)
        db.session.add(newcomm)
        db.session.commit()

        return redirect(url_for('comments'))
    return render_template('contact.html')

@app.route('/comments')
def comments():
    all_comments = comm.query.all()
    return render_template('comments.html', comments=all_comments)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)
