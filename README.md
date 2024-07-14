# Two-dimensional Dispersion Sample Entropy: A Robust and Faster Method to Analyze Image Textures

This repository includes the implementation and experiments for my master essay "Two-dimensional Dispersion Sample Entropy: A Robust and Faster Method to Analyze Image Textures".

## Requirements
- Python 3.8.10
- C++ 17
- Requirements: requirements.txt
- Platform: Ubuntu 20.04.6 LTS

## Quick Start
```bash
# Install python packages
pip install -r requirements.txt

# Compile cpp lib to dll file
make

# Setup experiment datasets
python3 setup.py

# Compute entropy for synthetic dataset
## DispSampEn2D
python3 main.py --task compute_entropy --entropy DispSampEn2D --m_array 2 3 4 --mapping ncdf --c -1 --dataset synthetic
## DispEn2D
python3 main.py --task compute_entropy --entropy DispEn2D --m_array 2 3 4 --mapping ncdf --c 5 --dataset synthetic
## SampEn2D
python3 main.py --task compute_entropy --entropy SampEn2D --m_array 2 3 4 --r 0.24 --dataset synthetic

# Compute entropy for real-world datasets
python3 main.py --task compute_entropy --entropy DispSampEn2D --m_array 2 3 4 --mapping ncdf --c -1 --dataset Brodatz --p 0.0
python3 main.py --task compute_entropy --entropy DispSampEn2D --m_array 2 3 4 --mapping ncdf --c -1 --dataset Kylberg --p 0.0

# Classification task for real-world datasets
python3 main.py --task classification --entropy DispSampEn2D --m_array 2 3 4 --dataset Brodatz --p 0.0
python3 main.py --task classification --entropy DispSampEn2D --m_array 2 3 4 --dataset Kylberg --p 0.0
```
### Arguments
- --task: task to execute, e.g. compute_entropy, classification.
- --entropy: entropy algorithm, e.g. DispEn2D, SampEn2D, DispSampEn2D.
- --m_array: embedding dimensions array, e.g. [2], [3], [2, 3, 4].
- --mapping:
- --c: number of dispersion classes, for DispEn2D and DispSampEn2D only. DispSampEn2D can set to -1 in order to use suggested value. e.g. -1, 5
- --r: ratio of similarity threshold for SampEn2D only. e.g. 0.24.
- --dataset: image datasets. e.g. synthetic, Brodatz, Kylberg.
- --p: probability for noise mix. e.g. 0.0 ~ 1.0.
- --rerun_computation: rerun entropy computation or not.