#!/bin/bash
project=TFCGyres-OreHints
version=1.4

file=${project}-${version}.jar
rm -f ${file}

#delete and build here not working?!?
#rm -rf src/data/*
#../TerraFirmaCraft/venv/bin/python3.10 ./resources/__main__.py book

cd src
rm -r assets
jar --create --file ../${file} *

cd ..
ls -l ${file}
