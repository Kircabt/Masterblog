from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'Data_Structure.json')

def load_posts():
    """Read all blog posts from the JSON file (empty list if it doesn't exist yet)."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_posts(posts):
    """Write the full list of blog posts back to the JSON file."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4)

@app.route('/')
def index():
    blog_posts = load_posts()
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_posts()
        # Retrieve input data from the form fields
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Unique ID: one higher than the current maximum (1 if the list is empty)
        new_id = max((post['id'] for post in blog_posts), default=0) + 1

        blog_posts.append({
            'id': new_id,
            'author': author,
            'title': title,
            'content': content,
        })

        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_posts()

    # Keep every post except the one with the given id
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_posts(blog_posts)

    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)