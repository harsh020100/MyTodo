from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///todo.db"
db = SQLAlchemy(app)





class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)


# create the app context
with app.app_context():
    # run the code that requires the app context, e.g. db.create_all()
    db.create_all()

def __repr__(self)->str:
    return f"{self.sno} - {self.title}"

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']    
        desc = request.form['desc']      
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        # Redirect to the index page to avoid resubmitting the form on refresh
        return redirect("/")
    else:
        todo = Todo.query.all()
        return render_template('index.html', todo=todo)


@app.route('/about')
def product():
    #alltodo=Todo.query.all()
    return render_template('about.html')

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']    
        desc = request.form['desc']      
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo) 


if __name__=="__main__":
    app.run(debug=True)