from crypt import methods
from email.mime import image
from flask import Flask, render_template ,request, url_for, flash, redirect
import sqlite3
request, url_for, flash, redirect
from werkzeug.exceptions import abort
import requests
import urllib.request,json



url = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=3cded965754b4c3f9abc835d812259d3&query='
#Connects to sqlite database , use connection object for db operations 
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

#Allows for template auto reload
app.config["TEMPLATES_AUTO_RELOAD"] = True


#Renders search page when url for search is called
@app.route('/search',methods=('GET','POST'))
def search():
    if request.method == 'POST':
        title = request.form['title']
        if not title:
            flash('Title is required!')
        else:
            r = requests.get(url+title)
            data = r.json()
            global results 
            results = data['results']
            
            #dict = json.loads(data)
            #recipes = []
            #for recipe in dict["results"]:
            #    recipe = {
             #       "title": recipe["title"],
              #      "id": recipe["id"],
               #     "image": recipe["image"],
                #    "imageType": recipe["imageType"]
                #}
                #recipes.append(recipe)
            #print(dict)
            return redirect(url_for('recipe'))
    return render_template('search.html')

@app.route('/recipe')
def recipe():
    
    return render_template('recipe.html', recipes=results)





#Default page for 
@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)
