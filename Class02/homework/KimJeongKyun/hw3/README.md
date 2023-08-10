# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
(.otx)$ ds_count ./splitted_dataset 2
./splitted_dataset/:	188
./splitted_dataset/train:	150
./splitted_dataset/train/o:	76
./splitted_dataset/train/x:	74
./splitted_dataset/val:	38
./splitted_dataset/val/o:	18
./splitted_dataset/val/x:	20
```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S| |
|EfficientNet-B0| 
|DeiT-Tiny| 0|4.918113|0:00:43.696393|8|0.0001||
|MobileNet-V3-large-1x| 


## FPS 측정 방법
```
Step 1. Initialize OpenVINO Runtime Core
start_time = time.time()

t = time.time() - start_time
print(f"=============inferencing time = {t:.5f} 초")
print(f"FPS = {1/t}")
return 0
```
