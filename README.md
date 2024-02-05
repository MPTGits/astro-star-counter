
## Overview
Counting stars around galaxies, particularly in the context of astronomical observations and research, offers several advantages. This task, while challenging, can yield significant insights into the structure, formation, and evolution of galaxies, as well as the properties of the stars themselves. Here are some of the primary benefits:

- Detailing Stellar Populations: By counting stars in the vicinity of galaxies, astronomers can better understand the distribution and density of different stellar populations. This information is crucial for studying the structure of galaxies, including their spiral arms, bulge, and halo regions.
- Mapping Dark Matter: The gravitational effects of dark matter on the motion of stars around galaxies can be inferred by studying the distribution and velocity of these stars. Counting stars provides data necessary for such analyses.
- Star Formation Rates: The number of stars in various stages of development around galaxies helps estimate star formation rates. This, in turn, provides insights into the evolutionary stages of galaxies and the physical processes driving star formation.
- Chemical Enrichment: The composition of stars around galaxies can shed light on the chemical enrichment processes over time, offering clues about the history of star formation and the interstellar medium's evolution.
- Exoplanet Host Stars: By examining stars around galaxies, astronomers can identify potential exoplanet host stars. This broadens the search for exoplanets to different galactic environments, enhancing our understanding of planet formation and stability in varying conditions.
- Improving Simulations: Detailed observations of stars around galaxies provide empirical data to test and refine theoretical models of galaxy formation and evolution. This feedback loop between observation and theory is vital for advancing our understanding of the universe.


## Prerequisites
- Python 3.x
- OpenCV (`cv2`)
- NumPy (`np`)
- Matplotlib (`plt` and `mpimg`)

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
Consider an image of The Andromeda Galaxy, a majestic spiral galaxy located 2.5 million light-years away in the Andromeda constellation.

<p align="center">
  <img src='images/img_1.png' width='512'>
</p>

### Adaptive Thresholding
- **Purpose:** The first major step involves applying adaptive thresholding to the grayscale version of the original image. Adaptive thresholding is chosen over simple binary thresholding because astronomical images often suffer from varying lighting conditions. Stars may be faint or bright and distributed against a complex background that includes gradients due to the galaxy's light, nebulae, or other celestial phenomena.
- **How it Works:** cv2.adaptiveThreshold is used with the Gaussian method to calculate thresholds for smaller regions of the image, allowing for more accurate differentiation between stars and the background across varying lighting conditions. This results in a binary image where stars are highlighted against a dark background.
- **Why:** This step is critical for isolating potential stars from the background, making subsequent steps more focused and effective.
  ![image](https://github.com/MPTGits/astro-star-counter/assets/37246713/3511a4e7-8d14-4b63-b5dc-5c135b21367a)

✅ The stars are now easily identified by looking at the image</br>
❌ There is a lot of noise caused by the galaxy in the center so it is sitll difficult to process the image and identify the number of stars
  

### Detecting Connected Components
- **Purpose:** After thresholding, the script identifies connected components in the binary image. Each connected component is presumed to be either a star or a cluster of stars/galaxies.
- **How it Works**: cv2.connectedComponents is employed to label each distinct object in the image. To visualize these components, the labels are converted to hues, allowing for easy differentiation between individual objects.
- **Why:** This step is essential for counting and analyzing individual celestial objects. By labeling each component, the script can distinguish between multiple objects that might be touching or very close to each other.
  ![image](https://github.com/MPTGits/astro-star-counter/assets/37246713/9c6e6ee5-f499-464a-8e21-4ccc84b862e9)</br>

✅ The stars are now sepearted and all of the noise from the galaxy was removed as sepearte connected componets were extracted</br>
❌ We still have some noise in the resulted image and some of the stars are 'fused' and overlapping with eachother:
![image](https://github.com/MPTGits/astro-star-counter/assets/37246713/97826bf5-1873-4cb5-8a4f-ac26fa5a4668)
> [!WARNING]  
> This should be two stars and the little dots around the bigger objects are noise that should be removed.

### Applying Morphological Transformations
- **Purpose:** This step aims to enhance the image by reducing noise and separating objects that are very close to each other. Morphological operations are a set of tools in image processing that apply specific shapes (kernels) to process images based on their structures.
- **How it Works:** The code uses a morphological operation known as "opening," which is a combination of erosion followed by dilation. This process is performed using a 3x3 square kernel, which is a small matrix used to apply the operation across the image.
Erosion removes pixels on the boundaries of objects in the image, reducing their size and separating objects that are close together.
Dilation then adds pixels to the boundaries of objects, but since it is applied after erosion, it primarily restores the size of the original object rather than merging objects back together.
- Why: The opening operation is particularly useful in astronomical images for a few reasons:
    - Noise Reduction: It helps remove small dots or noise that could be mistakenly identified as stars, ensuring that the algorithm focuses on significant objects.
    - Separating Close Objects: In dense star fields, stars can appear very close to each other. The opening operation can help in separating these stars before applying more sophisticated segmentation algorithms like watershed.
    - Improving Watershed Efficiency: By cleaning up the image beforehand, the watershed algorithm can more effectively distinguish between different objects, leading to a more accurate count of stars.</br>

✅ The image is now clean from noise</br>
❌ We still have some of the stars fused toggeter

### Applying Watershed Algorithm
- **Purpose:** The watershed algorithm is a sophisticated image segmentation technique used to separate objects in the image that are touching or overlapping—a common scenario in dense star fields or clusters.
- **How it Works:** The process involves several preparatory steps, including additional noise reduction via morphological operations and the distinction between sure foreground (stars) and sure background areas. The watershed algorithm is then applied to the modified image to delineate individual stars, even in crowded regions.
- **Why:** This algorithm is crucial for accurately counting stars in complex images where simple thresholding and component detection might fail due to overlapping objects.</br>

✅ Some of the fused stars are now seperated</br>
  ![image](https://github.com/MPTGits/astro-star-counter/assets/37246713/a39d0c30-2c56-4790-8716-31376bc053b5)
> [!IMPORTANT]  
> Some of the stas will still remain fusesd as it is almost impossible to determain even from the original image how many stars there are in some places that are overlapping


This workflow is particularly designed to handle the complexities of astronomical images, where the primary challenge is distinguishing and counting stars among various sources of noise and interference, such as the brightness of galaxies or nebulae. Each step builds upon the previous to refine the detection and counting of stars, ensuring a robust tool for astronomical analysis.

## Function Definitions
- save_image(image, output_path)
  - Purpose: Saves an image to a specified path.
  - Parameters:
    - image: The image to be saved.
    - output_path: Destination path for the image.
- apply_threshold(image)
  - Purpose: Applies adaptive Gaussian thresholding to an image to separate stars from the background.
  - Parameters:
    - image: Grayscale image of the night sky.
    - Returns: A binary image where stars are highlighted.
- detect_connected_components(threshold_image)
  - Purpose: Detects connected components in a binary image.
  - Parameters:
    - threshold_image: Binary image from the thresholding step.
    - Returns: A labeled image with distinct components marked differently.
- apply_watershed(noise_free_img, grayscale_image, original_image)
  - Purpose: Applies the Watershed algorithm to separate overlapping stars.
  - Parameters:
    - noise_free_img: Preprocessed image for the Watershed algorithm.
    - grayscale_image: Original image in grayscale.
    - original_image: Original image in color.
    - Returns: Markers indicating separated objects in the image.
- display_images(image_path)
  - Purpose: Displays the original and processed images side by side.
  - Parameters:
    - image_path: Path to the original image.
- count_stars(markers)
  - Purpose: Counts the number of stars detected in the image.
  - Parameters:
    - markers: Markers from the Watershed algorithm output.
    - Returns: The count of detected stars.

# Examples

## Galaxy AM 0520-390
Stars counted: 44
![image](https://github.com/MPTGits/astro-star-counter/assets/37246713/777f6482-8294-4627-8372-41143420bc92)

## Galaxy NGC 5236 (M83)
Stars counted: 209
![image](https://github.com/MPTGits/astro-star-counter/assets/37246713/bd8f7f28-49a4-4f76-9168-918042f10f26)

## Galaxy M33(The Triangulum Galaxy)
Stars Counted: 2372
![image](https://github.com/MPTGits/astro-star-counter/assets/37246713/66bfa9db-aaf1-4704-a429-78baf4e589d8)

# Resources
- Galaxy images
  - https://www.galactic-hunter.com/post/m33-the-triangulum-galaxy
  - https://bigthink.com/starts-with-a-bang/loneliest-galaxy-in-universe/
  - https://www.flickr.com/photos/geckzilla/48059479108
- Future improvements
  - Watershed transform of astronomical images - https://www.researchgate.net/publication/250758339_Watershed_transform_and_the_segmentation_of_astronomical_images




