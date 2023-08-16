# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
./splitted_dataset:	129
./splitted_dataset/val:	26
./splitted_dataset/val/defect:	13
./splitted_dataset/val/pass:	13
./splitted_dataset/train:	103
./splitted_dataset/train/defect:	53
./splitted_dataset/train/pass:	50
```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|1.0000|4.0750|0:00:10.743002|7|0.0071|num_iters 1|
|EfficientNet-B0| 1.0000|8.7102|0:00:06.705538|16|0.0049|num_iters 1|
|DeiT-Tiny| 1.0000|5.5079|0:00:13.518779|64|0.0001|num_iters 1|
|MobileNet-V3-large-1x| 1.0000|7.9289|0:00:06.249592|0.0058|num_iters 1|


## FPS 측정 방법
fps = 이미지 개수 / 걸린 시간
