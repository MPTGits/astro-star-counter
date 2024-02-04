# Star Counter in Astronomy Images

## Overview
This project provides a Python script that counts the number of stars in astronomical images, specifically designed to ignore galaxies. Utilizing OpenCV, the script processes images to detect and count stars through a series of image processing techniques. The goal is to offer a tool for astronomers and enthusiasts to easily quantify stars in their captured images without the interference of galactic bodies or companions.

## Prerequisites
- Python 3.6 or newer
- OpenCV library
- NumPy library

## Installation
Clone the repository to your local machine:
```bash
git clone <repository-url>
pip install numpy opencv-python
```
## Usage
To use the script, navigate to the cloned directory and run:

```bash
python star_counter.py <path_to_your_image>
```
Replace <path_to_your_image> with the path to the image file you wish to process.

## Detailed Workflow
### Adaptive Thresholding
Consider an image of The Andromeda Galaxy, a majestic spiral galaxy located 2.5 million light-years away in the Andromeda constellation. Our approach begins with adaptive thresholding, a technique that shines in scenarios with uneven lighting or varying contrast between the foreground and background. This method is especially adept at isolating galaxies from stars and the background, making it invaluable for astronomy images plagued by brightness gradients from sources like the Milky Way or urban light pollution.

<p align="center">
  <img src='images/img_1.png' width='512'>
</p>

The outcome of adaptive thresholding is depicted below, showcasing the successful isolation of celestial objects.

<p align="center">
  <img src='images/thresh.png' width='512'>
</p>

### Edge Detection
Following this, we employ Canny edge detection to outline each celestial body. This step is crucial for differentiating between stars and galaxies, as demonstrated in the images below. Stars are neatly outlined, while galaxies, lacking clear borders, are identified by their gradual blend into the background. This distinction is further refined through morphological opening, which eliminates noise and removes galaxies based on their diffuse edges.

Star Edge Detection Example</br>
![image](https://github.com/MPTGits/astro-star-counter/assets/37246713/bb743769-9b23-435e-83ed-f2901e9b45e7) </br>

Galaxy Edge Detection Example</br>
![image](https://github.com/MPTGits/astro-star-counter/assets/37246713/09d0f975-059f-42dd-8c9a-223233c64597)</br>


### Watershed Algorithm

The final hurdle is distinguishing stars that appear to overlap. The Watershed algorithm is our solution, adeptly separating stars that are close to each other or overlapping, ensuring each star is counted accurately.

Before Watershed Application</br> 
![image](https://github.com/MPTGits/astro-star-counter/assets/37246713/c4d9416a-a925-4392-9050-bdf3c83ba508)</br>

After Watershed Application</br>
![image](https://github.com/MPTGits/astro-star-counter/assets/37246713/c4684532-9879-418e-a8a8-535259f413c7)</br>

Number of stars found: 1605

![watershed_output](https://github.com/MPTGits/astro-star-counter/assets/37246713/8fbd352b-9240-4cf1-bebf-909e8f305c33)


