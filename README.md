# Build mini_rag 

This is a mini  impelementaion of the rag

## Requirements

- python 3.8 or later

#### Install python using MiniConda On mac

1) curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh

2) bash Miniconda3-latest-MacOSX-arm64.sh

3) create new environment using the following command:
'''
conda create -n mini-rag-app python=3.8
'''
4) Activate the environment:
'''
conda activate mini-rag-app
'''


- for API use fastapi and uvicorn to run the server in real time as a service
 
- to upload files with python we need python-multipart 

#### install them 
''' bash
pip install -r requirements.txt
'''

