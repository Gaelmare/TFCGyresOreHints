#!/bin/bash
project=TFCGyres-OreHints
version=3.0.0

file=${project}-${version}.jar
nohint_file=${project/OreHints/VeinBuffs}-${version}.jar

rm -f ${file}
rm -f ${nohint_file}

rm -rf src/{data,assets}/*
source ./venv/bin/activate
python resources all

cd src

jar --create --file ../${file} *

cd ..
ls -l *.jar


