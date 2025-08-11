# DAE-YOLO: Remote Sensing Small Targets Detection Method

A implementation of the DAE-YOLO model proposed in the paper *"DAE-YOLO: Remote Sensing Small Targets Detection Method Integrating YOLO and State Space Models"* (File: remotesensing-3714155.pdf). This model is designed to enhance small target detection performance in remote sensing images by integrating YOLO11 with innovative modules, addressing challenges such as limited target information, weak feature representation, and complex backgrounds .


## 🌟 Key Innovations
- **Dynamic Spatial Sequence Module (DSSM)**: Replaces traditional C3k2 modules with visual state space models to capture long-range spatial dependencies, expanding the receptive field by 3.2× with linear computational complexity, which is crucial for sparsely distributed small targets in high-resolution remote sensing images .
- **Adaptive Multi-scale Feature Enhancement (AMFE)**: Utilizes separable kernel attention to adaptively enhance small target features while suppressing background interference, maintaining an equivalent 11×11 receptive field with reduced computational complexity (from O(k²) to O(k)) .
- **Efficient Dual-level Attention Mechanism (EDAM)**: Reduces computational complexity by 75.5% through hierarchical region-level and pixel-level routing attention, balancing global context modeling and efficiency for large-scale remote sensing images .


## 📋 Table of Contents
- [Installation](#installation)
- [Datasets](#datasets)
- [Training & Inference](#training--inference)
- [Experimental Results](#experimental-results)
- [Citation](#citation)


## ⚙️ Installation

### Prerequisites
- Python 3.8+
- PyTorch 2.0+
- Dependencies: `numpy`, `opencv-python`, `torchvision`, `tqdm`

### Setup
```bash
# Clone the base YOLO code repository
git clone https://github.com/ultralytics/ultralytics
cd ultralytics

# Install required dependencies
pip install -r requirements.txt

# Download YOLO11 code via Baidu Netdisk
# Link: https://pan.baidu.com/s/1oec1XYyuEZeujpVnWk2hdg?pwd=d9m2 
# Extraction code: d9m2
```


## 📊 Datasets

### 1. RS-APD Dataset
A custom dataset constructed for airport plane detection, featuring:
- 4,968 high-resolution images covering over 600 airports globally.
- 52,280 annotated aircraft instances with diverse densities, complex backgrounds (aprons, runways, etc.), and arbitrary orientations .
- Enhanced via 7 data augmentation methods (random cropping, rotation, Gaussian noise, etc.) to mitigate sample scarcity .

**Access**: Contact the authors for dataset access.

### 2. VisDrone2019 Dataset
A public dataset for validation, with:
- 10,000+ high-resolution aerial images (2000×1500 pixels) captured under diverse conditions.
- 2.7 million annotated instances across 10 categories, including extremely small targets (average 0.03% of image area) .

**Download**: [VisDrone2019 Dataset](https://github.com/five-days/VisDrone-Dataset)

## 📈 Experimental Results

### Performance on RS-APD Dataset
| Model         | mAP50 (%) | mAP50:95 (%) | APs (%) | Params (M) | FLOPs (G) |
|---------------|-----------|--------------|---------|------------|-----------|
| YOLO11n       | 80.2      | 42.1         | 40.8    | 2.6        | 6.5       |
| DAE-YOLO      | 82.3      | 44.6         | 43.6    | 2.6        | 6.3       |

- **Improvements**: +2.1% mAP50, +2.5% mAP50:95, +2.8% APs (small targets) compared to YOLO11n .

### Generalization on VisDrone2019 Dataset
| Model         | mAP50 (%) | mAP50:95 (%) | APs (%) |
|---------------|-----------|--------------|---------|
| YOLO11n       | 34.9      | 20.4         | 9.7     |
| DAE-YOLO      | 35.6      | 21.2         | 10.5    | 
