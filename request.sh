#!/bin/bash

curl -F "file=@$SAMPLES_DIR/file.pdf" http://127.0.0.1:5000/conv -o output.png
