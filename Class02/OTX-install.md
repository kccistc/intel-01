# OpenVINO Training Extensions


## Download and install CUDA 11.7
Note, link below is for Ubuntu20.04. For other versoins please refer [CUDA Toolkit 11.7 Downloads](https://developer.nvidia.com/cuda-11-7-0-download-archive)
```bash
cd ~/Downloads/
wget https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda_11.7.0_515.43.04_linux.run
sudo sh cuda_11.7.0_515.43.04_linux.run
```


## OTX install
```bash
mkdir -p ~/repo && cd $_
git clone https://github.com/openvinotoolkit/training_extensions.git
cd training_extensions
git checkout develop
```

```bash
# Create virtual env.
python -m venv .otx

# Activate virtual env.
source .otx/bin/activate
```

```bash
# install command for torch==1.13.1 for CUDA 11.7:
pip install torch==1.13.1 torchvision==0.14.1 --extra-index-url https://download.pytorch.org/whl/cu117
pip install otx[full]
```

## Dataset links
* Flowers:
    http://download.tensorflow.org/example_images/flower_photos.tgz

* Dogs & cats:
    https://shorturl.at/qxKS8
