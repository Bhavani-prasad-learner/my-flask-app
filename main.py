#imports
from flask import Flask , render_template , request, redirect

from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy


#app
app = Flask(__name__)
Scss(app)
#app.config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Database URI for SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications to save resources
db = SQLAlchemy(app)  # Initialize SQLAlchemy with the Flask app

#models
class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the User model
    content= db.Column(db.String(100), nullable=False)  # Content field for the User model
    complete= db.Column(db.Integer, default=0)  # Completion status for the User model
    created= db.Column(db.DateTime, default=db.func.current_timestamp())  # Creation timestamp for the User model


    def __repr__(self)->str:
        return f'User {self.id}'

with app.app_context():
    db.create_all()  # Create all database tables if they don't exist





#home page route
@app.route('/',methods=["POST","GET"])#flask "@" decorator to create a route to the index page
def index():
    #add a task
    if request.method == "POST":
        current_task = request.form.get('content')
        new_task = User(content=current_task)
        try:
            db.session.add(new_task)  # Add the new task to the session
            db.session.commit()  # Commit the session to save changes to the database
            return redirect('/')  # Redirect to the index page after adding a task
        except Exception as e:
            print(f"Error occurred: {e}")
            return f"error: {e}"
    else:
        tasks=User.query.order_by(User.created).all()
        return render_template('index.html', tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)  # Delete the task from the session
        db.session.commit()  # Commit the session to save changes to the database
        return redirect('/')  # Redirect to the index page after deletion
    except Exception as e:
        return f"error: {e}"
    
@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id):
    task_to_edit = User.query.get_or_404(id)
    if request.method == "POST":
        task_to_edit.content = request.form['content']
        try:
            db.session.commit()  # Commit the session to save changes to the database
            return redirect('/')  # Redirect to the index page after editing
        except Exception as e:
            return f"error: {e}"
    else:
        return render_template('edit.html', task=task_to_edit)






if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  # Create all database tables if they don't exist
    app.run(debug=True)  # Run the Flask application in debug mode so its update itself when changes are made
