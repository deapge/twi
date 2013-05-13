#!/bin/bash
# 自动运行脚本: 每个工作日:09:20 09:40 10:10 10:30执行该脚本,提醒自己应该要执行Python发weibo了
base_path=/home/meadhu/workspace/twi
current_time=$(date +"%H%I")
notify_title="Python Twi 温馨提醒"
notify_body="暂时没有要执行的脚本"
if [ $current_time -eq "0920" ]; then 
    notify_body=" bns d3 dota gw2 wow "
elif [ $current_time -eq "0940" ]; then #condition2
    notify_body="gameguyz_browsergame gameguyz_pictures gameguyz"
elif [ $current_time -eq "1010" ]; then #condition3
    notify_body="lol_pictures sc2_pictures"
elif [ $current_time -eq "1030" ]; then #condition4
    notify_body="twi"
fi

notify-send "$notify_title" \
            "$notify_body" \
            -i "$base_path/16x16.png" -t 0

