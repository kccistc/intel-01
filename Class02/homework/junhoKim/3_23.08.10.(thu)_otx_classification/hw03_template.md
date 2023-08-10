# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
(.otx)$ ds_count ./splitted_dataset 2
./splitted_dataset/: 93
./splitted_dataset/train: 74
./splitted_dataset/train/pass: 38​
./splitted_dataset/train/fail: 36​
./splitted_dataset/val: 19
./splitted_dataset/train/pass: 10​
./splitted_dataset/train/fail: 9​
```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|100|3|9.44|23|0.0071|
|EfficientNet-B0|100|8|6.47|16|0.0049
|DeiT-Tiny|100|5|35.42|16|0.0001
|MobileNet-V3-large-1x|100|7|6.05|23|0.003092|


## FPS 측정 방법
1. 동영상 load
2. classification model을 불러오는 곳에 start_time 생성
3. classification model이 끝나는 시점에 end_time 생성
4. FPS = 1/(end_time - start_time )