# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
./splitted_dataset:	96
./splitted_dataset/train:	76
./splitted_dataset/train/O:	40
./splitted_dataset/train/X:	36
./splitted_dataset/val:	20
./splitted_dataset/val/O:	11
./splitted_dataset/val/X:	9


## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|   |  1    |  200000   |  0:01:12.209496 |  2 |   0.0071  | x |
|EfficientNet-B0      | 0.95  |  250000   |  0:00:36.099777 | 64 |   0.0001  | x |
|DeiT-Tiny            |  1    |  250000   |  0:00:14.939354 | 16 |   0.0049  | x |
|MobileNet-V3-large-1x| 0.95  |  250000   |  0:00:14.852294 | 16 |   0.0058  | x |




## FPS 측정 방법
inference시간을 
    start = time.time()
    predictions = next(iter(results.values()))
    end = time.time()
    end-start로 구하여 ,
측정한 이미지 개수 / inference시간을 하여 fps를 계산하였습니다.
