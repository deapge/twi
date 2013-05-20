#!/bin/bash
# 自动运行脚本: 每个工作日执行该脚本,提醒自己应该要执行Python发weibo了
base_path=/home/meadhu/workspace/twi
current_time=$(date +"%H")
notify_title="Python Twi 温馨提醒"
notify_body="暂时没有要执行的脚本"
if [ $current_time -eq "11" ]; then 
    notify_body="bns d3 dota"
elif [ $current_time -eq "12" ]; then #condition2
    notify_body="gameguyz_browsergame"
elif [ $current_time -eq "13" ]; then #condition3
    notify_body="lol_pictures"
elif [ $current_time -eq "14" ]; then #condition4
    notify_body="gw2 wow sc2_pictures"
elif [ $current_time -eq "1" ]; then #condition4
    echo ""
#    notify_body="gameguyz_browsergame gameguyz_pictures gameguyz"
elif [ $current_time -eq "15" ]; then #condition4
    notify_body="gameguyz_pictures"
elif [ $current_time -eq "16" ]; then #condition4
    notify_body="gameguyz"
elif [ $current_time -eq "16" ]; then #condition4
    echo ""
#    notify_body="gameguyz_browsergame gameguyz_pictures gameguyz"
elif [ $current_time -eq "18" ]; then #condition4
    echo ""
#    notify_body="gameguyz"
elif [ $current_time -eq "18" ]; then #condition4
    notify_body="twi"
fi

DISPLAY=:0.0 /usr/bin/notify-send "$notify_title" \
            "$notify_body" \
            -i "$base_path/16x16.png" -t 0

