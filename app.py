import sys
from os import path
import os
from flask import Flask, render_template, send_from_directory, redirect, url_for
import argparse
import pandas as pd
from collections import namedtuple

BoxesInfo = namedtuple('BoxesInfo', ('boxes1', 'boxes2', 'img_name'))

app = Flask(__name__)


@app.route('/')
def index():
    boxes1_path = current_info().boxes1
    boxes2_path = current_info().boxes2
    boxes = {
        'boxes1': read_annots_file(boxes1_path),
        'boxes2': read_annots_file(boxes2_path)
    }

    first = app.config['HEAD'] == 0
    last = app.config['HEAD'] == len(app.config['BOXES_INFO']) - 1

    return render_template('index.html', boxes=boxes, first=first, last=last)


@app.route('/next')
def next():
    app.config['HEAD'] += 1
    return redirect(url_for('index'))


@app.route('/prev')
def prev():
    app.config['HEAD'] -= 1
    return redirect(url_for('index'))


@app.route('/image')
def get_current_image():
    img_name = current_info().img_name
    return send_from_directory(app.config['IMAGES_DIR'], img_name, as_attachment=False)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('images_dir')
    parser.add_argument('boxes1')
    parser.add_argument('boxes2')
    return parser.parse_args(args)


def check_args(args):
    for p in [args.images_dir, args.boxes1, args.boxes2]:
        if not path.exists(p) or not path.isdir(p):
            print(f'{p} - folder does not exist')
            exit(-1)


def read_input_info(args):
    boxes_info = []
    for img_name in os.listdir(args.images_dir):
        img_path = path.join(args.images_dir, img_name)
        if not path.isfile(img_path) or \
                path.splitext(img_name)[1].lower() not in ['.jpg', '.jpeg', '.png']:
            continue

        img_name_without_ext = path.splitext(img_name)[0]
        boxes1_path = path.join(args.boxes1, img_name_without_ext + '.txt')
        boxes2_path = path.join(args.boxes2, img_name_without_ext + '.txt')
        boxes_info.append(BoxesInfo(
            boxes1=boxes1_path,
            boxes2=boxes2_path,
            img_name=img_name
        ))
    return boxes_info


def read_annots_file(filepath):
    if not path.exists(filepath):
        return []
    return pd.read_csv(filepath, header=None).values.tolist()


def current_info():
    return app.config['BOXES_INFO'][app.config['HEAD']]


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    check_args(args)

    app.config['IMAGES_DIR'] = args.images_dir
    app.config['BOXES_INFO'] = read_input_info(args)
    app.config['HEAD'] = 0

    app.run(debug=True)
