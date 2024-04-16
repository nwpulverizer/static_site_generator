#!/usr/bin/bash
python src/main.py $1
python server.py --dir public
