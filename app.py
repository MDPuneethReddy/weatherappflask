from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)
#http://api.openweathermap.org/data/2.5/weather?q=chittoor&appid=45bddb0e44301c13b2e98836fd385505

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    temperature = db.Column(db.Text, nullable=False)
    icon = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return 'Blog post ' + str(self.id)


@app.route('/', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        city= request.form['title']
        address="http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=45bddb0e44301c13b2e98836fd385505"
        json_data = requests.get(address).json()
        format_add = json_data['base']
        description=(json_data["weather"][0]["description"])
        wtemperature=(json_data["main"]["temp"])
        wicon=(json_data["weather"][0]["icon"])
        new_post = BlogPost(title=city, content=description,temperature=wtemperature,icon=wicon)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
    else:
        all_posts = BlogPost.query.all()
        return render_template('posts.html', posts=all_posts)

@app.route('/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
