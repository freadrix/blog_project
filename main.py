from flask import Flask, render_template
import requests

api_url = "https://api.npoint.io/e75e0e49fccb076f6e84"

data_for_posts = requests.get(url=api_url).json()

app = Flask(__name__)


@app.route("/")
def home():
    title = "Anton's blog!"
    subtitle = "Some interesting info."
    author_and_date = ""
    return render_template("index.html", title=title, subtitle=subtitle, author_and_date=author_and_date,
                           posts=data_for_posts, bg="../static/img/home-bg.jpg")


@app.route("/about")
def get_about():
    title = "About Me"
    subtitle = "This is what i do."
    author_and_date = ""
    return render_template("about.html", title=title, subtitle=subtitle, author_and_date=author_and_date,
                           posts=data_for_posts, bg="../static/img/about-bg.jpg")


@app.route("/contact")
def get_contact():
    title = "Contact Me"
    subtitle = "Have questions? I have answers."
    author_and_date = ""
    return render_template("contact.html", title=title, subtitle=subtitle, author_and_date=author_and_date,
                           posts=data_for_posts, bg="../static/img/contact-bg.jpg")


@app.route("/post/<number>")
def get_post(number):
    number = int(number)
    post_data = data_for_posts[number - 1]
    title = post_data["title"]
    subtitle = post_data["subtitle"]
    author_and_date = f"Posted by {post_data['author']} on {post_data['date']}"
    return render_template("post.html", title=title, subtitle=subtitle, author_and_date=author_and_date,
                           body=post_data["body"], bg=post_data["image"])


if __name__ == "__main__":
    app.run(debug=True)
