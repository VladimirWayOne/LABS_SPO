#!/bin/bash
function save() {
	echo 'Сохранить проект в...'
	read way
	if ! [ -d "$way" ] 
	then
		mkdir "$way"
	fi
echo "$way"
}
save
git clone https://github.com/Bitmessage/PyBitmessage.git "$way"
cd "$way"
python checkdeps.py
sudo apt-get install python openssl libssl-dev git python-msgpack python-qt4
#sudo apt install -f
git clone https://github.com/Bitmessage/PyBitmessage $HOME/PyBitmessage
~/PyBitmessage/src/bitmessagemain.py
