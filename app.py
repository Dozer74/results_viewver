import sys
from builtins import print
from os import path
import os
from flask import Flask, render_template, send_from_directory, redirect, url_for
import argparse
import pandas as pd
from collections import namedtuple

BoxesInfo = namedtuple('BoxesInfo', ('img_name', 'boxes'))

app = Flask(__name__)


@app.route('/')
def index():
    boxes = [read_annots_file(boxes_path) for boxes_path in current_info().boxes]
    colors = ['#ff8000', '#0000ff', '#00ff00', '#ff0000']
    for i, box in enumerate(boxes):
        box['color'] = colors[i % len(colors)]

    params = {
        'images_count': len(app.config['BOXES_INFO']),
        'current_image_index': app.config['HEAD'],
        'current_image_number': app.config['HEAD'] + 1,
        'images_dir_name': path.basename(app.config['IMAGES_DIR']),
        'image_name': current_info().img_name,
        'boxes': boxes,
        'labels_mapping': app.config['CLASSES']
    }

    return render_template('index.html', **params)


@app.route('/first')
def first():
    app.config['HEAD'] = 0
    return redirect(url_for('index'))


@app.route('/next')
def next():
    app.config['HEAD'] += 1
    return redirect(url_for('index'))


@app.route('/prev')
def prev():
    app.config['HEAD'] -= 1
    return redirect(url_for('index'))


@app.route('/last')
def last():
    app.config['HEAD'] = len(app.config['BOXES_INFO']) - 1
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
    parser = argparse.ArgumentParser(description='Simple viewer for ResNet detections results')
    parser.add_argument('images_dir', help='Path to the images folder.')
    parser.add_argument('boxes', nargs='+', help='Paths to folders with bouncing boxing information. '
                                                 'File names must match the names of the images '
                                                 'and extension must be .txt.')
    parser.add_argument('--classes', help='Path to file with label class to label name mapping.')
    return parser.parse_args(args)


def check_args(args):
    for p in [args.images_dir, *args.boxes]:
        if not path.exists(p) or not path.isdir(p):
            print(f'{p} - folder does not exist')
            exit(-1)

    if args.classes and not path.exists(args.classes):
        print('Classes file does not exist')
        exit(-1)


def read_input_info(args):
    boxes_info = []
    for img_name in os.listdir(args.images_dir):
        img_path = path.join(args.images_dir, img_name)
        if not path.isfile(img_path) or \
                path.splitext(img_name)[1].lower() not in ['.jpg', '.jpeg', '.png']:
            continue

        img_name_without_ext = path.splitext(img_name)[0]
        boxes = [path.join(box_path, img_name_without_ext + '.txt') for box_path in args.boxes]

        boxes_info.append(BoxesInfo(
            img_name=img_name,
            boxes=boxes
        ))
    return boxes_info


def read_annots_file(filepath):
    boxes = [] if not path.exists(filepath) else pd.read_csv(filepath, header=None).values.tolist()
    folder_name = path.basename(path.dirname(filepath))
    return {
        'folder_name': folder_name,
        'boxes': boxes
    }


def current_info():
    return app.config['BOXES_INFO'][app.config['HEAD']]


def read_classes(classes_path):
    import pandas as pd
    df_classes = pd.read_csv(classes_path, header=None)
    return df_classes[0].to_dict()

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    check_args(args)

    app.config['IMAGES_DIR'] = args.images_dir
    app.config['BOXES_INFO'] = read_input_info(args)
    app.config['HEAD'] = 0

    app.config['CLASSES'] = read_classes(args.classes) if args.classes else None

    app.run(debug=True)
