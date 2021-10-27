from flask import Flask, render_template, request
import requests
import smtplib
import config


data_for_posts = requests.get(url=config.API_URL).json()

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


@app.route("/contact", methods=["GET", "POST"])
def get_contact():
    if request.method == "GET":
        title = "Contact Me"
    elif request.method == "POST":
        title = "Successfully send your message"
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        message_for_send = f"""\
        Subject: Hi there\n
        
        My name is {name}\n
        my email is {email}\n
        my phone number {phone}\n
        my message: {message}."""

        with smtplib.SMTP(config.SMTP_SERVER, config.PORT_FOR_SMTP) as server:
            server.starttls()
            server.login(user=config.SENDER_EMAIL, password=config.PASSWORD)
            server.sendmail(from_addr=config.SENDER_EMAIL, to_addrs=config.SENDER_EMAIL, msg=message_for_send)

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
