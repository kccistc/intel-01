# How to use OpenVINO on Raspberry pi 4
---

## Test environment
- Kernel: Linux raspberrypi 6.1.21-v8+
- OS: Raspberry Pi OS Release 11
- OpenVINO version: 2023.0.1
- Device: Raspberry Pi 4 Model B

## Install OpenVINO
- Create an installation folder for OpenVINO. If the folder already exists, skip this step
```
sudo mkdir -p /opt/intel
```
- Go to your ~/Downloads directory and download OpenVINO Runtime archive file for Debian
```
cd ~/Downloads/
curl -L https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0.1/linux/l_openvino_toolkit_debian9_2023.0.1.11005.fa1c41994f3_arm64.tgz
tar -xf l_openvino_toolkit_debian9_2023.0.1.11005.fa1c41994f3_arm64.tgz
sudo mv l_openvino_toolkit_debian9_2023.0.1.11005.fa1c41994f3_arm64 /opt/intel/openvino_2023.0.1
```
- Install required system dependencies on Linux. To do this, OpenVINO provides a script in the extracted installation directory. Run the following command:
```
cd /opt/intel/openvino_2023.0.1
sudo -E ./install_dependencies/install_openvino_dependencies.sh
```
- For simplicity, it is useful to create a symbolic link as below:
```
cd /opt/intel
sudo ln -s openvino_2023.0.1 openvino_2023
```

## Set the OpenVINO environment
You must update several environment variables before you can compile and run OpenVINO applications. Open a terminal window and run the setupvars.sh script as shown below to temporarily set your environment variables
```
source /opt/intel/openvino_2023/setupvars.sh
```

## Install OpenVINO development tools
* Download open_model_zoo repo
```
git clone --recurse-submodules https://github.com/openvinotoolkit/open_model_zoo.git
```
* Install model tools
```
cd open_model_zoo/tools/model_tools
pip install --upgrade pip
pip install .
```
