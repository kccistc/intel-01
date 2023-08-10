# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
(.otx)$ ds_count ./splitted_dataset 2
./splitted_dataset/: ???
./splitted_dataset/train: ???​
./splitted_dataset/train/<class#>: ???​
./splitted_dataset/train/<class#>: ???​
./splitted_dataset/val: ???
./splitted_dataset/train/<class#>: ???​
./splitted_dataset/train/<class#>: ???​

```
## 나의 Dataset 구조
```
./:	759
./passorfail-MobileNet-V3-large-1x:	155
./passorfail-MobileNet-V3-large-1x/splitted_dataset:	129
./passorfail-MobileNet-V3-large-1x/outputs:	16
./passorfail-EfficientNet-B0:	155
./passorfail-EfficientNet-B0/splitted_dataset:	129
./passorfail-EfficientNet-B0/outputs:	16
./passorfail-EfficientNet-V2-S:	166
./passorfail-EfficientNet-V2-S/splitted_dataset:	129
./passorfail-EfficientNet-V2-S/outputs:	27
./passorfail-DeiT-Tiny:	154
./passorfail-DeiT-Tiny/splitted_dataset:	129
./passorfail-DeiT-Tiny/outputs:	16
./passorfail:	129
./passorfail/defect:	66
./passorfail/pass:	63
```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|1.0|----|0:00:10.982438|32|0.0064|----|
|EfficientNet-B0| 1.0|----|0:00:11.743629|16|0.0049|----|
|DeiT-Tiny|1.0|----|0:00:14.696411|32|0.0001|----|
|MobileNet-V3-large-1x| 1.0|----|0:00:06.791582|32|0.0056|----|


## FPS 측정 방법
