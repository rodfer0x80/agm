#!/bin/sh
SRC="test"
python3 -m venv venv &&\
    source venv/bin/activate &&\
    pip install --upgrade pip &&\
    pip install -r $SRC/requirements.txt &&\
    python $SRC/__main__.py &&\
    rm -rf venv
