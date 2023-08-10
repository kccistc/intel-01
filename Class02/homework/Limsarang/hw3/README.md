# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조

./spitted_dataset/: 129
./spitted_dataset/val: 26
./spitted_dataset/val/defect: 13
./spitted_dataset/val/pass: 13
./spitted_dataset/train: 103
./spitted_dataset/train/defect: 53
./spitted_dataset/train/pass: 50

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|

|EfficientNet-V2-S	|1|54.1785|56.875600|5|0.0071|
|EfficientNet-B0  	|1|46.9857|51.929406|0.0001|
|DeiT-Tiny		|1|158.7301|33.787176|0.0049|
|MobileNet-V3-large-1x| |1|200.5756|25.986346|0.0058|

## FPS 측정 방법
각 모델마다 5번씩 인퍼런싱 하여 나온 인퍼런싱타임들의 평균을 구함 

