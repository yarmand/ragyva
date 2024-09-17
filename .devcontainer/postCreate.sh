#!/bin/bash

username=$1

wdir=$(pwd)

ln -s /home/${username}/dotfiles ~/
cd ~/dotfiles
./setup.sh


cd ${wdir}
# python libs
pip install --user -r requirements.txt

python3 -c 'import nltk
nltk.download("punkt")'