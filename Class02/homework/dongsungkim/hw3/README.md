# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
(.otx)$ ds_count ./splitted_dataset 2
./splitted_dataset/: 129
./splitted_dataset/train: 103​
./splitted_dataset/train/pass: 51​
./splitted_dataset/train/defect: 52​

./splitted_dataset/val: 26
./splitted_dataset/val/pass: 12​
./splitted_dataset/val/defect: 14​
```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S| 1 | 49.284 | 72s | 8 | 0.0071 | null |
|EfficientNet-B0| 1 | 155.465 | 19s | 16 | 0.0049 | null | 
|DeiT-Tiny| 1 | 47.154 | 53s | 64 | 0.0001 | null |
|MobileNet-V3-large-1x| 1 | 184.454 | 13s | 16 | 0.0058 | null |


## FPS 측정 방법

# --------------------------- Step 6. Create infer request and do inference synchronously -----------------------------
    import time
    
    log.info('Starting inference in synchronous mode')
    start_time = time.time()
    results = compiled_model.infer_new_request({0: input_tensor})
    end_time = time.time()
    fps = 1 / (end_time - start_time)
    log.info(f"FPS: {fps}")
