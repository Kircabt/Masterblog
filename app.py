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

def fetch_post_by_id(post_id):
    """Return the post with the given id from the JSON file, or None if it doesn't exist."""
    for post in load_posts():
        if post['id'] == post_id:
            return post
    return None
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

        save_posts(blog_posts)  # <-- add this line
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_posts()

    # Keep every post except the one with the given id
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_posts(blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog post from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        blog_posts = load_posts()
        for blog_post in blog_posts:
            if blog_post['id'] == post_id:
                blog_post['author'] = request.form.get('author')
                blog_post['title'] = request.form.get('title')
                blog_post['content'] = request.form.get('content')
                break
        save_posts(blog_posts)

        # Redirect back to index
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)