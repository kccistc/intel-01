# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
(.otx) intel@intel:~/workspace/EfficientNet-V2-S$ ds_count ./splitted_dataset/ 2
./splitted_dataset/:	231
./splitted_dataset/train:	184
./splitted_dataset/train/b:	92
./splitted_dataset/train/a:	92
./splitted_dataset/val:	47
./splitted_dataset/val/b:	24
./splitted_dataset/val/a:	23
```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S| 1.0000|3.98|01:32.215|8|0.0071|-|
|EfficientNet-B0|1.0000| 8.53|00:30.231|16|0.0049|-|
|DeiT-Tiny| 1.0000|5.89|01:01.943|32|0.0001|-|
|MobileNet-V3-large-1x| 1.0000|7.74|00:21.740|16|0.0058|-|


## FPS 측정 방법
```
ppp = PrePostProcessor(model)
    start = time.time()
    .
    .
    .

for class_id in top_10:
        probability_indent = ' ' * (len('class_id') - len(str(class_id)) + 1)
        log.info(f'{class_id}{probability_indent}{probs[class_id]:.7f}')
    
    print("FPS : ",1/(time.time() - start))
	
    log.info('')
```

전처리가 시작되는 지점 부터 probability를 print 하는 시점의 시간을 측정했습니다.