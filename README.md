# Installation

#### Install miniconda

```bash
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
$ bash Miniconda3-latest-Linux-x86_64.sh
```

#### Create conda environment

```bash
$ conda create --name env python==3.7 -y
$ conda activate env
$ pip install -r requirements.txt
```
# Test

#### Predict a s image
```bash
$ python demo.py --image "path_to_image" --save "output_directory"
```


