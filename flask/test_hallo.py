#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://www.sejuku.net/blog/55507

from flask import Flask
app = Flask(__name__)
 
@app.route('/')
def hello():
    hello = "Hello world"
    return hello
 
if __name__ == "__main__":
    app.run()


