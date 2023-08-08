#!/bin/bash

CAMID=${1:-2}

v4l2-ctl --device=/dev/video${CAMID} --set-ctrl=focus_auto=0
v4l2-ctl --device=/dev/video${CAMID} --set-ctrl=focus_absolute=65

v4l2-ctl --device=/dev/video${CAMID} --set-ctrl=exposure_auto=1
v4l2-ctl --device=/dev/video${CAMID} --set-ctrl=exposure_absolute=128

v4l2-ctl --device=/dev/video${CAMID} --set-ctrl=white_balance_temperature_auto=0
v4l2-ctl --device=/dev/video${CAMID} --set-ctrl=white_balance_temperature=4000

# apt install libxcb-xinerama0
# sudo chmod a+rw /dev/ttyACM0

# ./resource/factory/ motion.cfg, color.cfg
# 모션 디텍 감도 테스트 필요..

# 물티슈, 아두이노 케이블
