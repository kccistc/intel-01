# Homework03

## Dataset 구조
```
(.otx)$ ds_count ./splitted_dataset 2
./splitted_dataset/: 18
./splitted_dataset/train: 150
./splitted_dataset/train/o: 74
./splitted_dataset/train/x: 76
./splitted_dataset/val: 38
./splitted_dataset/val/o: 20
./splitted_dataset/val/x: 18
```
|Classification model  |Accuracy|FPS  |Training time|Batch size|Learning rate|Other prams|
|----                  |----    |---  |----         |----      |----         |----       |
|EfficientNet-V2-S     | 1.0    |     |             |          |             |           |
|EfficientNet-B0       | 1.0    |6.66 | 26.08       | 18       | 0.0049      |   x       |
|DeiT-Tiny             | 1.0		|4.65 | 51.65       | 9        | 0.0001      |   x       |
|MobileNet-V3-large-1x | 1.0    |6.38 | 19.33       | 8        | 0.0058      |   x       |

EfficientNet-V2-S 모델을 otx train 명령 후 진행이 안되서 생략했습니다

## FPS 측정 방법
```
hello_classification.py 파일의 main 함수에서
함수 시작 s = time.time() 
함수  끝 q = time.time() -s 
print(f' fps : {1/q} ')
로 fps 를 측정했습니다.
```
