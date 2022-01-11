# 2021 Fall NTU GICE Intor-to-IOT Final Project 

Please see the reports to understand the details of this project.

## Python version
Please use Python3.8 to run all the py files

## Install Packages
To install the packages automatically, we have provided a "requirements.txt" file. Please use the following script to set up the environment.
```bash
pip install -r requirements.txt
```
For Raspberry Pi, please check this [website](https://104.es/2021/01/30/%E5%9C%A8%E6%A8%B9%E8%8E%93%E6%B4%BE3-model-b%E4%B8%8A%E5%AE%89%E8%A3%9Dopencv/) to install OpenCV 

## Usage
Run the server code on the computer.
```bash
python3 tcp_img_server_GPS.py
```
Run the client code on Raspberry Pi with Pi Camera. 
```bash
python3 tcp_img_client_img_camera_GPS.py
```
