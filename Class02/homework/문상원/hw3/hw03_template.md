# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
./splitted_dataset/:	129
./splitted_dataset/val:	26
./splitted_dataset/val/pass:	12
./splitted_dataset/val/defect:	14
./splitted_dataset/train:	103
./splitted_dataset/train/pass:	51
./splitted_dataset/train/defect:	52

```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|1|3.96|1분 9초|0.0071|8|기본값|
|EfficientNet-B0| 1|8.27|18초|0.0049|16|기본값|
|DeiT-Tiny|1|45초|64|11.7|64|기본값|
|MobileNet-V3-large-1x|1|7.7|13초|0.0058|16|기본값|


## FPS 측정 방법

FPS 측정 방법
1. 학습된 모델을 로드합니다.
2. 테스트할 이미지나 프레임을 로드합니다.
3. 시작 시간을 기록합니다.
4. 이미지나 프레임을 모델에 입력하여 예측을 수행합니다.
5. 종료 시간을 기록하고, 경과 시간을 계산합니다.
6. FPS는 1초당 처리된 프레임 수로 계산됩니다. FPS = 1 / 경과 시간 으로 프레임을 예측합니다.

