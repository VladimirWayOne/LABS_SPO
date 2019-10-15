#!bin/bash
git clone https://github.com/Bitmessage/PyBitmessage $HOME/PyBitmessage #загружаем репозиторий
sudo apt-get install python openssl libssl-dev git python-msgpack python-qt4 #resolve dependencies
cd $HOME/PyBitmessage
git pull #upgrade
~/PyBitmessage/src/bitmessagemain.py #run
