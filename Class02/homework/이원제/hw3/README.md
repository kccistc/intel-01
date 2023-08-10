# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
(.otx)$ ds_count ./splitted_dataset/ 2
./splitted_dataset/:	323
./splitted_dataset/val:	65
./splitted_dataset/val/bravo:	31
./splitted_dataset/val/alfa:	34
./splitted_dataset/train:	258
./splitted_dataset/train/bravo:	128
./splitted_dataset/train/alfa:	130
```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|1.0000|34.25|0:02:14.637587|32|0.0071|
|EfficientNet-B0|1.0000|112.46|0:00:29.188812|16|0.0049| 
|DeiT-Tiny|1.0000|60.87|0:01:24.155345|64|0.0001| 
|MobileNet-V3-large-1x|1.0000|174.43|0:00:28.077723|16|0.0058|


## FPS 측정 방법
FPS = batch size * total number of iterations / training time in second

|Classification model|Batch size|Total iterations|Training time|FPS|
|----|----|----|----|----|
|EfficientNet-V2-S|32|144|134.637587|34.25|
|EfficientNet-B0|16|205|29.188812|112.46
|DeiT-Tiny|64|80|84.155345|60.87|
|MobileNet-V3-large-1x|16|306|28.077723|174.43|