# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
(.otx) intel@intel:~/workspace/OX-classification3$ tree splitted_dataset/ -d
splitted_dataset/
├── train
│   ├── No
│   └── Yes
└── val
    ├── No
    └── Yes

6 directories
(.otx) intel@intel:~/workspace/OX-classification3$ ds_count splitted_dataset/ 2
splitted_dataset/:	402
splitted_dataset/val:	81
splitted_dataset/val/No:	40
splitted_dataset/val/Yes:	41
splitted_dataset/train:	321
splitted_dataset/train/No:	163
splitted_dataset/train/Yes:	158

```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Inference Time|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|1.0000|46.51|0:02:45.943034|32|1.775e-03|0.021502|
|EfficientNet-B0|1.0000|153.69|0:00:35.683465|16|1.225e-03|0.00657|
|DeiT-Tiny|1.0000|46.5|0:01:42.636185|64|2.500e-05|0.021487|
|MobileNet-V3-large-1x|1.0000|200.83|0:00:28.719783|16|1.450e-03|0.004979|


## FPS 측정 방법
* hello_classificaion.py 파일 수정!
```
+ import time
    ...
# --------------------------- Step 6. Create infer request and do inference synchronously -----------------------------
+   log.info('Starting inference in synchronous mode')
+   # 시간 측정 시작
+   start_time = time.time()

+   results = compiled_model.infer_new_request({0: input_tensor})

+   # 추론 후의 시간 측정 및 FPS 계산
+   end_time = time.time()
+   inference_time = end_time - start_time
+   fps = 1 / inference_time

# --------------------------- Step 7. Process output ------------------------------------------------------------------
    ...
    
+   log.info('')
+   log.info(f"Inference Time: {inference_time:.6f} seconds")
+   log.info(f"FPS: {fps:.2f}")

+   log.info('')

```
