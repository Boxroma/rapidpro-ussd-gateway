import datetime

from flask import request, Blueprint, jsonify
import json

test = Blueprint('test', __name__, url_prefix='/')


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

