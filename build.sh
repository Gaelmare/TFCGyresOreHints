#!/bin/bash
project=TFCGyres-OreHints
version=1.5

file=${project}-${version}.jar
nohint_file=${project/Ore/No}-${version}.jar

rm -f ${file}
rm -f ${nohint_file}

#delete and build here not working?!?
rm -rf src{,_nohints}/data/*
source ../TerraFirmaCraft/venv3.11/bin/activate
python resources worldgen
python resources book

cd src
rm -r assets
jar --create --file ../${file} *
cd ../src_nohints
rm -r assets
jar --create --file ../${nohint_file} *

cd ..
ls -l *.jar
