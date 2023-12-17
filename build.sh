#!/bin/bash
project=TFCGyres-OreHints
version=2.1

file=${project}-${version}.jar
nohint_file=${project/OreHints/VeinBuffs}-${version}.jar

rm -f ${file}
rm -f ${nohint_file}

#delete and build here not working?!?
rm -rf src{,_veinbuffs}/{data,assets}/*
source ../WaterFlasks-120/venv/bin/activate
python resources worldgen
python resources book

cd src

jar --create --file ../${file} *
#cd ../src_veinbuffs
#rm -r assets
#jar --create --file ../${nohint_file} *

cd ..
ls -l *.jar
