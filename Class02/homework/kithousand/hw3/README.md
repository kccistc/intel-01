# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
(.otx)$ ds_count ./splitted_dataset 2
./:	159
./splitted_dataset:	129
./splitted_dataset/val:	26
./splitted_dataset/train:	103
./outputs:	20
./outputs/20230810_181848_export:	9
./outputs/20230810_181524_train:	2
./outputs/20230810_181823_train:	7
./outputs/20230810_181218_train:	2



## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|1.0|   |0:00:10.442259|16|0.0071|   |
|EfficientNet-B0|1.0|   | 0:00:27.580886|64| 0.0049|   |
|DeiT-Tiny|1.0|    |0:00:45.544587|64|0.0001|   |
|MobileNet-V3-large-1x|1.0|  |0:00:26.840460|64|0.0071|    |


## FPS 측정 방법
