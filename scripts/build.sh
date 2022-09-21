#!/bin/sh
#SRC="src"
python3 -m venv venv &&\
    source venv/bin/activate &&\
    pip install --upgrade pip &&\
    pip install -r requirements.txt &&\
    git clone https://github.com/rodfer0x80/autopy &&\
    cd autopy &&\
    make &&\
    make install &&\
    cd ..
