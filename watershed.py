import argparse

import numpy as np
import cv2

def save_image(image, output_path):
    cv2.imwrite(output_path, image)

def apply_threshold(image):
    thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    save_image(thresh, 'images/thresh.png')
    return thresh

def detect_edges_and_draw_contours(threshold_image, grayscale_image):
    edges = cv2.Canny(threshold_image, 100, 200)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(grayscale_image)  # Create a mask the same size as the gray image
    for cnt in contours:
        cv2.drawContours(mask, [cnt], -1, 255, -1)  # Draw filled contour in white
    # Convert mask to boolean
    mask_bool = mask.astype(bool)
    # Create an empty array with the same shape as the original image but filled with black
    result = np.zeros_like(threshold_image)
    # Apply the mask to copy the original color where the mask is true
    result[mask_bool] = threshold_image[mask_bool]

    save_image(result, 'images/contured_image.png')
    return result

def apply_watershed(noise_free_img, grayscale_image, original_image):
    kernel = np.ones((3, 3), np.uint8)
    # sure background area
    sure_bg = cv2.dilate(noise_free_img, kernel, iterations=1)
    save_image(sure_bg, 'images/sure_bg.png')

    dist_transform = cv2.distanceTransform(noise_free_img, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.3 * dist_transform.max(), 255, 0)
    save_image(sure_fg, 'images/sure_fg.png')

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    save_image(unknown, 'images/unknown_area.png')

    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    unknown = cv2.subtract(255 - grayscale_image, sure_fg)
    markers[unknown == 255] = 0
    markers = cv2.watershed(original_image, markers)
    original_image[markers == -1] = [255, 0, 0]

    # Generate a list of unique colors, one for each region
    # Skip -1 as it's used for boundaries
    unique_markers = np.unique(markers)
    unique_markers = np.delete(unique_markers, np.where(unique_markers == -1))

    # Generate random colors, but ensure you have enough colors for each marker
    colors = np.random.randint(0, 255, (len(unique_markers), 3))

    for i, marker in enumerate(unique_markers):
        # Color each region with a different color
        original_image[markers == marker] = colors[i]

    save_image(original_image, 'images/watershed_output.png')
    return markers

def count_stars(markers):
    unique_markers = np.unique(markers)
    unique_markers = np.delete(unique_markers, np.where(unique_markers <= 1))
    return len(unique_markers)

def main(image_path):
    print("Starting process...")
    image = cv2.imread(image_path)
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("Applying threshold...")
    threshold = apply_threshold(gray_img)
    print("Detecting edges and drawing contours...")
    edges_detected = detect_edges_and_draw_contours(threshold, gray_img)

    kernel = np.ones((3,3),np.uint8)
    print("Applying morphological transformations...")
    opening_image = cv2.morphologyEx(edges_detected, cv2.MORPH_OPEN, kernel)
    save_image(opening_image, 'images/opening.png')
    print("Applying watershed algorithm...")
    markers = apply_watershed(opening_image, gray_img, image)
    num_stars = count_stars(markers)
    print(f"Number of stars found: {num_stars}")

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description='Process an image.')
    # Add an argument
    parser.add_argument('image_path', type=str, help='The path to the image file')

    # Parse the arguments
    args = parser.parse_args()

    main(args.image_path)
