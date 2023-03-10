from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emarket.db'

db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    available = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.id} - {self.title}'
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def postd():
    posts = Books.query.all()
    return render_template('posts.html', books=posts)

@app.route('/create', methods=['POST', 'GET'])
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        intro = request.form['intro']
        amount = request.form['amount']
        genre = request.form['genre']
        price = request.form['price']
        available = request.form['available']

        books = Books(title=title, author=author, intro=intro, amount=amount, genre=genre, price=price, available=available)
        db.session.add(books)
        db.session.commit()
        return 'Данные сохранены'
    else:
        return render_template('create_post.html')
    



@app.route('/post/<int:id>/update', methods=['POST', 'GET'])
def update_book(id):
    post = Books.query.get(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.intro = request.form['intro']
        post.amount = request.form['amount']
        post.genre = request.form['genre']
        post.price = request.form['price']
        post.available = request.form['available']

        db.session.commit()
        return 'Изменения сохранены'
    else:
        return render_template('update.html', books=post)




@app.route('/post/<int:id>')
def hello(id):
    post = Books.query.get(id)
    return render_template('post_detail.html', books=post)


@app.route('/post/<int:id>/delete')
def delete(id):
    post = Books.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return 'Удалено'
    except:
        return 'Ошибка при удалении'
    
    
    

if __name__ == '__main__':
    app.run(debug=True)