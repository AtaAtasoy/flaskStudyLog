from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        subject_content = request.form['content']
        new_subject = Subject(content=subject_content)

        try:
            db.session.add(new_subject)
            db.session.commit()
            return redirect('/')
        except:
            return 'Could not add task'

    else:
        subjects = Subject.query.order_by(Subject.date_created).all()
        return render_template('index.html', subjects=subjects)

@app.route('/delete/<int:id>')
def delete(id):
    subject_to_delete = Subject.query.get_or_404(id)
    try:
        db.session.delete(subject_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Cannot delete that task'

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    subject = Subject.query.get_or_404(id)
    if request.method == 'POST':
        subject.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Could not update the subject'
    else:
        return render_template('update.html', subject = subject)

if __name__ == "__main__":
    app.run(debug=True)