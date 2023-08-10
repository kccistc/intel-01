# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
(.otx)$ ds_count ./splitted_dataset 2
./splitted_dataset:	152
./splitted_dataset/val:	31
./splitted_dataset/val/defect:	16
./splitted_dataset/val/pass:	15
./splitted_dataset/train:	121
./splitted_dataset/train/defect:	64
./splitted_dataset/train/pass:	57
```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S| 1.0000 | 3.93 | 0:00:11.394243 | 48 | 0.0071 | num_iters 1 | 
|EfficientNet-B0| 1.0000 | 8.61 | 0:00:07.374774 | 22 | 0.0049 | num_iters 1 | 
|DeiT-Tiny| 1.0000 | 5.92 | 0:00:08.872311 | 70 | 0.0001 | num_iters 1 | 
|MobileNet-V3-large-1x| 1.0000 | 7.80 | 0:00:06.981617 | 22 | 0.0058 | num_iters 1 | 


## FPS 측정 방법
- 처리량(초당 프레임, FPS)은 배치 입력에 사용되는 측정값입니다.
- 처리 시간에 처리된 입력 수를 나눕니다.
- 처리량(FPS) = 추론된 이미지 수/ 처리 시간(초)
 
- 지연 시간 값은 단일 입력을 처리하는 데 필요한 추론 시간(ms)을 측정합니다.
 참고 https://www.intel.co.kr/content/www/kr/ko/support/articles/000091115/software/development-software.html
