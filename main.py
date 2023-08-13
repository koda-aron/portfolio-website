import smtplib
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from ttmc import Encoder
import datetime

MY_EMAIL = "contact.form.python@gmail.com"
PASSWORD = "muhpyeuefxpzkwmd"


def create_app():
    application = Flask(__name__)
    Bootstrap(application)
    return application


app = create_app()

encoder = Encoder()

year = datetime.datetime.now().year
first_date = datetime.date(2023, 1, 1)
second_date = datetime.date.today()
coding_length = second_date - first_date


def message_sent(name, email, message):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="tymicki.konrad@gmail.com",
            msg=f"Subject:Portfolio Website Contact Form\n\nName: {name}\nEmail: {email}\n\n{message}"
        )
    return redirect(url_for('success'))


def encode_text(user_input):
    text = user_input
    encoded = encoder.encoder(message=text)
    return render_template('text-to-morse-code.html',
                           encoded_text=encoded,
                           current_page='projects',
                           no_input=False,
                           user_input=user_input,
                           year=year)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('index.html', current_page='home', year=year, coding_length=coding_length)
    elif request.method == 'POST':
        name = request.form.get('name').encode('ascii', 'ignore').decode('ascii')
        email = request.form.get('email').encode('ascii', 'ignore').decode('ascii')
        message = request.form.get('message').encode('ascii', 'ignore').decode('ascii')
        return message_sent(name, email, message)


@app.route('/<project_name>', methods=['POST', 'GET'])
def project(project_name):
    if project_name == 'text-to-morse-code':
        if request.method == 'GET':
            return render_template('text-to-morse-code.html',
                                   encoded_text='',
                                   current_page='projects',
                                   no_input=True,
                                   year=year)
        elif request.method == 'POST':
            text = request.form['text']
            return encode_text(text)


@app.route('/success', methods=['GET', 'POST'])
def success():
    if request.method == 'GET':
        return render_template('form-entry.html', year=year)
    elif request.method == 'POST':
        if request.form.get('submit_button') == 'Return Home':
            return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
