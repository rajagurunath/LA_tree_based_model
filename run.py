# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 11:16:26 2018

@author: gurunath.lv
"""

import os
import argparse

from flask import Flask, request, send_from_directory,render_template

parser = argparse.ArgumentParser()
parser.add_argument('--file', dest='file_name', type=str, help='Name of the slides to run.')
args = parser.parse_args()

port = int(os.getenv('PORT', 9099))

app = Flask(__name__,static_url_path="/static", static_folder=r'D:\LA_tree_based_model\templates\static')


@app.route('/')
def serve():
    return render_template(args.file_name,)

#def serve_page(path):
#    print(path)
#    return send_from_directory('static', path)
#
#
#@app.route('/presentation')
#def main():
#    """Adjust the presentation_name if you rename the jupyter notebook."""
#    presentation_name = args.file_name.split('/')[-1]
#    print(presentation_name)
#    return app.send_static_file(presentation_name)


if __name__ == '__main__':
    app.run(host='192.168.55.96', port=port,debug=True)