#########################################################################
# File Name: build_uic.sh
# Author: ZhenhuaWei
# mail: weizhenhua94@163.com 
# Created Time: 2018-09-30 00:00:37
#########################################################################
#!/bin/bash

#local system Source file path
LOCAL_FILE=$(cd "$(dirname "$0")";pwd)
FLODER=$LOCAL_FILE/../build
ui_file_list=""
uic_file=""

echo "============================Start============================"
[ -d $FLODER ]
if [ $? -ne 0 ];then
	mkdir -p $FLODER
else
	rm -rf $FLODER/*
fi

cp -rf $LOCAL_FILE/../ui $FLODER/

cd $FLODER/ui
echo "[INFO]Enter $FLODER/ui"

ui_file_list=`ls *.ui`
if [ $? -ne 1 ];then
    for ui_file in $ui_file_list
    do
        if [ -d $ui_file ] 
        then
            continue
        fi
        temp_file=${ui_file%%.ui}".py"
        pyuic5 $ui_file -o $temp_file
        echo "[INFO]Pyuic $ui_file -o $temp_file"
    done

    cp *.py  $LOCAL_FILE/../pyuic/ -rf
    if [ $? -ne 0 ];then
        echo "[ERR ]Not have .py files !!!"
    else
        uic_file=`ls *.py`
        echo "[INFO]Copy $uic_file to .../pyuic/ floder"
    fi
else
    echo "[ERR ]Not have .ui files !!!"
fi

cd -
echo "[INFO]Leave $FLODER"
echo "[INFO]Pyuic execute success and pyuic floder's files have beed covered"
echo "=============================end============================="
echo ""