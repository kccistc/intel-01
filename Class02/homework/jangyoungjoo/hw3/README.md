# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
$ ds_count splitted_dataset/ 2
splitted_dataset/:	129
splitted_dataset/train:	103
splitted_dataset/train/pass:	51
splitted_dataset/train/defect:	52
splitted_dataset/val:	26
splitted_dataset/val/pass:	12
splitted_dataset/val/defect:	14

```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|1.0|59.0015|0:01:25|8|0.0071
|EfficientNet-B0|1.0|166.229|0:00:06|16|0.0049
|DeiT-Tiny|1.0|44.363|0:00:42|16|0.0001
|MobileNet-V3-large-1x|1.0|189.864|0:00:15|16|0.0058


## FPS 측정 방법
```python
import time
start_infer_time = time.time()
results = compiled_model.infer_new_request({0: input_tensor})
elapsed_time = time.time() - start_infer_time
fps = 1./elapsed_time
log.info(f'inference FPS : {fps}')
#inference FPS : 59.00157551204141
```