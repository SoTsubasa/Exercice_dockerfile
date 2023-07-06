from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/nom_de_la_base_de_donnees'
mongo = PyMongo(app)

# Créer une classe Task
class Task(mongo.Model):
    id = mongo.Column(mongo.Integer, primary_key=True)
    description = mongo.Column(mongo.String(200))
    completed = mongo.Column(mongo.Boolean)

    def __init__(self, description, completed=False):

        self.description = description

        self.completed = completed


@app.route('/')
def hello_world():
    return 'Web App with Python Flask!'

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

#Ajouter un utilisateur
@app.route('/add', methods=['POST'])
def add():
    description = request.form['description']
    mongo.db.tasks.insert_one({'description': description})
    return redirect(url_for('index'))


# Mettre à jour un utilisateur
@app.route('/update/<int:task_id>', methods=['POST'])
def update(task_id):
    task = Task.query.get(task_id)
    task.completed = not task.completed
    mongo.session.commit()
    return redirect(url_for('index'))

# Supprimer un utilisateur
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    task = Task.query.get(task_id)
    mongo.session.delete(task)
    mongo.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    mongo.create_all()
    app.run(debug=True)





