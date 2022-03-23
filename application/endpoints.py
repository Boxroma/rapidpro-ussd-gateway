import datetime

from flask import Blueprint, jsonify, redirect, url_for, render_template, request, session
from datetime import datetime
from . import db
from .models import message
import requests as requests
import uuid
import time
import re

test = Blueprint('test', __name__, url_prefix='/', template_folder='../templates', static_folder='../static',
                 static_url_path='/test')
# TODO Handle Session ID
session_id = '78b0a974-ebae-4a3a-9121-3c554e4a95b2'

# TODO Handle Session Init
smsc = ''
content = ''
reciever = ''


@test.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        # remove span tags and clean
        res = request.form['textarea']
        res = res.replace('<span>', "")
        res = res.replace('</span>', "")
        print(res)
        ussd_response = get_front_end('+260977662653', session_id, '', res)
        return render_template("index.html", phone_number='+260977662653', content=ussd_response)

    else:
        return render_template("index.html", phone_number='+260977662653', content='Sample text')


@test.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        flask_user = request.form["nm"]
        session["user"] = flask_user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))

        return render_template("../templates/login.html")


@test.route("/user")
def user():
    if "user" in session:
        flask_user = session["user"]
        return f"<h1>{flask_user}</h1>"
    else:
        return redirect(url_for("login"))


@test.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@test.route('/test/', methods=['POST'])
def print_contents():
    # collect submitted data
    request_data = request.get_json()

    print('Received Data: ')
    print(request_data)

    content = ''
    if request_data is not None:
        content = str(request_data)

    with open("test.txt", "w") as fo:
        fo.write("\n\nThis is Test Data: \n" + content)

    return jsonify({'status': 'success'},
                   {'content': content})


# Method to receive message from frontend and reroute to rapidpro
def get_front_end(tel, session_id, operation_type, received_msg):
    request_id = '1'
    # TODO Handle what frontend does with continue body
    # message_cont = False

    # Handle operation type
    init = False
    if operation_type == "1":
        init = True
        # send flow trigger

    # Create a new message entry
    new_message = message(
        tel=tel,
        session_id=session_id,
        received_msg=received_msg,
        received_time=datetime.utcnow(),
        received_msg_init=init
    )
    db.session.add(new_message)
    db.session.commit()

    # Send request to rapidPro
    send_to_rapidPro(tel, received_msg)

    # Wait (3 Second)
    time.sleep(2)

    # Query Update in Database
    responded_msg = message.query.filter_by(tel=tel)\
        .order_by(-message.msg_id)\
        .first()
    # If null respond system busy
    if responded_msg.response_msg is None:
        responded_msg.response_msg = "none"
        db.session.commit()
        response = "Service Not available. Please try again"
    # Else Respond with Response
    else:
        response = responded_msg.response_msg
    # Handle Close Message
    return response


# Method to receive message from frontend and reroute to rapidpro
@test.route('/ussd/', methods=['GET'])
def get_message():
    tel = request.args.get('MSISDN')
    request_id = '1'
    session_id = request.args.get('SESSION_ID')
    operation_type = request.args.get('NewRequest')
    received_msg = request.args.get('INPUT')
    message_cont = False
    response = ""

    # Handle operation type
    init = False
    if operation_type == "1":
        init = True

    # Create a new message entry
    new_message = message(
        tel=tel,
        session_id=session_id,
        received_msg=received_msg,
        received_time=datetime.utcnow(),
        received_msg_init=init
    )
    db.session.add(new_message)
    db.session.commit()

    # Send request to rapidPro
    send_to_rapidPro(tel, received_msg)

    # Wait (3 Second)
    time.sleep(3)

    # Query Update in Database
    responded_msg = message.query.filter_by(tel=tel)\
        .order_by(-message.msg_id)\
        .first()
    # If null respond system busy
    if responded_msg.response_msg is None:
        responded_msg.response_msg = "none"
        db.session.commit()
        response = "Service Not available. Please try again"
    # Else Respond with Response
    else:
        response = responded_msg.response_msg
    # Handle Close Message
    return response


@test.route('/send', methods=['POST'])
def get_response():
    response = request.get_json()
    # Get matching entry
    message_to_be_updated = message.query.filter_by(tel=response['to'])\
        .filter_by(response_msg=None)\
        .order_by(-message.msg_id)\
        .first()
    # Update entry in database
    if message_to_be_updated is not None:
        message_to_be_updated.response_msg = response['text']
        db.session.commit()

    # Handle Continue Message
    return jsonify({'status': 'success'})


def send_to_rapidPro(tel, text):
    url = "http://176.58.99.46/c/ex/"
    channel = "ef494071-369b-4a0c-88d5-c556975ef47e"
    send_url = f"{url}{channel}/receive?from={tel}&text={text}"
    print('Request :' + send_url)
    print(tel)
    try:
        res = requests.post(send_url)
        print('Server is sending requests: ', res.text)
        response = res.content
        print("/n")
        print(response)

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    pass

# TODO Handle continue message
# Handle in code
# Check Numbers Last Interaction
# If exists and last message entry is equal to response_continue
# Call method:
# Would You like to continue or start again?
# Else Just Start mans in the new session
