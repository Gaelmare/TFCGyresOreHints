#!/bin/bash
project=TFCGyres-OreHints
version=1.0

file=${project}-${version}.jar
rm -f ${file}

rm -rf src/data/*
../TerraFirmaCraft/venv/bin/python resources book

cd src
jar --create --file ../${file} *

cd ..
ls -l ${file}
