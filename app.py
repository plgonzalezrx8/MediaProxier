import os
from urllib.parse import urlparse
from flask import Flask, send_file, render_template, jsonify, send_from_directory
from flask import request as req
import requests
import shutil
from forms import ImageLinkForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ASKJNFKJDN'


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route('/cache/<path:filename>')
def base_static(filename):
    return send_from_directory(app.root_path + '/cache/', filename)


@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/this')
def this():
    return 'This'


@app.route('/imgur/<link>')
def display_image(link):
    image_link = 'https://i.imgur.com/' + link
    r = requests.get(image_link, stream=True)
    r.raw.decode_content = True
    with open('cache/' + link, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    folder = "cache/" + link
    return send_file(folder, mimetype='image/gif')


@app.route('/load', methods=['GET', 'POST'])
def loader():
    form = ImageLinkForm()
    if req.method == 'POST':
        image_link = form.link.data
        r = requests.get(image_link, stream=True)
        parsing = urlparse(image_link)
        filename = os.path.basename(parsing.path)
        with open('cache/' + filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        folder = 'cache/' + filename
        # return send_file(folder, mimetype='image/gif')
        return render_template('loader.html', title="Welcome", form=form, filename=filename)
    else:
        return render_template('loader.html', title="Welcome", form=form)


if __name__ == '__main__':
    app.run()
