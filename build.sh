#!/bin/bash
project=TFCGyres-OreHints
version=1.5

file=${project}-${version}.jar
nohint_file=${project/OreHints/VeinBuffs}-${version}.jar

rm -f ${file}
rm -f ${nohint_file}

#delete and build here not working?!?
rm -rf src{,_veinbuffs}/data/*
source ../TerraFirmaCraft/venv3.11/bin/activate
python resources worldgen
python resources book

cd src
rm -r assets
jar --create --file ../${file} *
cd ../src_veinbuffs
rm -r assets
jar --create --file ../${nohint_file} *

cd ..
ls -l *.jar
