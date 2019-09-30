#!/bin/bash
rm -f ./result.csv
printf "Путь\tИмя\tРасширение\tРазмер\tДата Изменения\tПродолжительность(HH:MM:SS)\tРазмер изображения\n" >> result.csv
RESULT=$(pwd)

function extension() {
	echo $(basename "$FILE") | grep -Eo '\.[^.]+$'
}

function FileSize() {
	b=$(wc -c < "$FILE")
	let "c = "$b" / 1024"
	echo "$c"
}

function Date() {
	d=$(date -r "$FILE")
	echo "$d"
}

function fileduration() {
	dur=$(ffprobe -i "$FILE" -sexagesimal -show_entries format=duration -v quiet -of csv="p=0")
	echo ${dur%.*}
}

function ImSize() {
	IMAGE=$(identify -format "%w\*%h" "$FILE")
	echo $IMAGE
}

function fileinfo() {
	SAVEIFS=$IFS
	IFS=$(echo -en "\n\b")
	filelist=($(ls))  #массив, состоящий из файлов в текущей директории
	for FILE in ${filelist[*]}
	do
		echo "$FILE"
		if [[ -d "$FILE" ]]
		then
			next_dir=$(ls "$FILE")
			cd "$FILE"
			fileinfo "$next_dir"
			cd ..
		fi

		if [[ -f "$FILE" ]]
		then
			NAME=$(basename "$FILE")	#Имя файла
			EXT=$(extension)		#Расширение файла
			SIZE=$(FileSize)		#Размер файла
			MOD_DATE=$(Date)		#Дата последней модификации
			DURATION="-"			#Продолжительность аудио/видео
			IMAGESIZE="-"			#Размер изображения

			if file "$FILE" | grep -qE 'bitmap|image'	#Если файл - изображение, узнаем его размер
			then
				IMAGESIZE=$(ImSize)
			elif file -ib "$FILE" | grep -qE 'video|audio|octet-stream'	# Если видео/аудио -- его продолжительность
			then
				DURATION=$(fileduration)	
			fi
			PREVIOUS=$(pwd)	#Директория, в которой сейчас находимся
			cd "${RESULT}"	#Переход в директорию с файлом результата
			printf "$PREVIOUS\t$NAME\t$EXT\t$SIZE KB\t$MOD_DATE\t$DURATION\t$IMAGESIZE\n" >> result.csv
			cd "${PREVIOUS}"
		fi
	done
}

START=$(pwd)

fileinfo "$START"


