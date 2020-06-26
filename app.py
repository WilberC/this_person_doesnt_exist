from flask import Flask, redirect, url_for, request, Response
from flask import render_template
from PIL import Image
import json
import urllib3
import base64

app = Flask(__name__)


def get_random_person(base_64=False):
    # For default it returns bites
    url = 'https://thispersondoesnotexist.com/image'
    http = urllib3.PoolManager()
    img_response = http.request('GET', url)
    img_data = img_response.data
    if base_64 is True:
        base_64code = base64.b64encode(img_data).decode('UTF-8')
        return base_64code
    return img_data


def get_by_qt(quantity, json_format=False):
    photos_list = []
    for q in range(quantity):
        photo_data = get_random_person(base_64=True)
        if json_format is True:
            photos_list.append({"base_64_img": "data:image/jpg;base64, {}".format(photo_data)})
        else:
            photos_list.append(photo_data)
    return photos_list


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/photos/', methods=['POST', 'GET'])
def persons_photos():
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        if quantity != 1:
            get_by_qt(quantity)
        return Response(get_random_person(), mimetype="image/jpg",
                        headers={"Content-Disposition": "attachment;filename=person.jpg"})
    else:
        return redirect(url_for('index'))


@app.route('/persons/', methods=['POST', 'GET'])
def persons_table():
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        return render_template('persons_table.html', persons=get_by_qt(quantity))
    else:
        return redirect(url_for('index'))


@app.route('/json-file/', methods=['POST', 'GET'])
def persons_():
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        list_data = get_by_qt(quantity, json_format=True)
        return Response(json.dumps(list_data), mimetype="text/plain",
                        headers={"Content-Disposition": "attachment;filename=json-persons_file.json"})
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
