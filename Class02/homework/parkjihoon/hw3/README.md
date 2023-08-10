# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
(.otx) intel@intel:~/workspace$ ds_count ./sample-classification-EfficientNet-V2-S/splitted_dataset/ 2
./sample-classification-EfficientNet-V2-S/splitted_dataset/:	108
./sample-classification-EfficientNet-V2-S/splitted_dataset/train:	86
./sample-classification-EfficientNet-V2-S/splitted_dataset/train/X:	38
./sample-classification-EfficientNet-V2-S/splitted_dataset/train/O:	48
./sample-classification-EfficientNet-V2-S/splitted_dataset/val:	22
./sample-classification-EfficientNet-V2-S/splitted_dataset/val/X:	10
./sample-classification-EfficientNet-V2-S/splitted_dataset/val/O:	12

(.otx) intel@intel:~/workspace$ ds_count ./sample-classification-EfficientNet-B0/splitted_dataset/ 2
./sample-classification-EfficientNet-B0/splitted_dataset/:	108
./sample-classification-EfficientNet-B0/splitted_dataset/train:	86
./sample-classification-EfficientNet-B0/splitted_dataset/train/X:	38
./sample-classification-EfficientNet-B0/splitted_dataset/train/O:	48
./sample-classification-EfficientNet-B0/splitted_dataset/val:	22
./sample-classification-EfficientNet-B0/splitted_dataset/val/X:	10
./sample-classification-EfficientNet-B0/splitted_dataset/val/O:	12

(.otx) intel@intel:~/workspace$ ds_count ./sample-classification-DeiT-Tiny/splitted_dataset/ 2
./sample-classification-DeiT-Tiny/splitted_dataset/:	108
./sample-classification-DeiT-Tiny/splitted_dataset/train:	86
./sample-classification-DeiT-Tiny/splitted_dataset/train/X:	38
./sample-classification-DeiT-Tiny/splitted_dataset/train/O:	48
./sample-classification-DeiT-Tiny/splitted_dataset/val:	22
./sample-classification-DeiT-Tiny/splitted_dataset/val/X:	10
./sample-classification-DeiT-Tiny/splitted_dataset/val/O:	12

(.otx) intel@intel:~/workspace$ ds_count ./sample-classification-MobileNet-V3-large-1x/splitted_dataset/ 2
./sample-classification-MobileNet-V3-large-1x/splitted_dataset/:	108
./sample-classification-MobileNet-V3-large-1x/splitted_dataset/train:	86
./sample-classification-MobileNet-V3-large-1x/splitted_dataset/train/X:	38
./sample-classification-MobileNet-V3-large-1x/splitted_dataset/train/O:	48
./sample-classification-MobileNet-V3-large-1x/splitted_dataset/val:	22
./sample-classification-MobileNet-V3-large-1x/splitted_dataset/val/X:	10
./sample-classification-MobileNet-V3-large-1x/splitted_dataset/val/O:	12
```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|1.0000|233016.89|0:00:59.781450|8|0.0071|x| 
|EfficientNet-B0|1.0000|199728.76|0:00:16.142087|16|0.0049|x| 
|DeiT-Tiny|1.0000|220752.84|0:00:39.180634|2048|0.0001|x| 
|MobileNet-V3-large-1x|1.0000|246723.76|0:00:14.034808|16|0.0058|x| 


## FPS 측정 방법


```
hello_classification.py 에서 inference 전후에
seq = time.time()
print("execution time :", time.time() - seq)를 삽입했습니다.
출력된 결과는 다음과 같습니다.
EfficientNet-V2-S
1장 4.291534423828125e-06초 소요.
FPS = 233016.89
EfficientNet-B0
1장 5.0067901611328125e-06초 소요.
FPS = 199728.76
DeiT-Tiny
1장 4.5299530029296875e-06초 소요.
FPS = 220752.84
MobileNet-V3-large-1x
1장 4.0531158447265625e-06초 소요.
FPS = 246723.76
```