import matplotlib.pyplot as plt
import numpy as np
import PIL.Image
from PIL import Image

"""
This function loads an image and returns it as a numpy array of floating-points. 
The image can be automatically resized so the largest of the height or width equals `max_size`.
"""
def load_image(filename, max_size=None):
    image = PIL.Image.open(filename)

    if max_size is not None:
        # Calculate the appropriate rescale-factor for
        # ensuring a max height and width, while keeping
        # the proportion between them.
        factor = max_size / np.max(image.size)
    
        # Scale the image's height and width.
        size = np.array(image.size) * factor

        # The size is now floating-point because it was scaled.
        # But PIL requires the size to be integers.
        size = size.astype(int)

        # Resize the image.
        image = image.resize(size, PIL.Image.LANCZOS)

    # Convert to numpy floating-point array.
    return np.float32(image)

"""
Save an image as a jpeg-file. The image is given as a numpy array with pixel-values between 0 and 255.
"""
def save_image(image, filename):
    # Ensure the pixel-values are between 0 and 255.
    image = np.clip(image, 0.0, 255.0)
    
    # Convert to bytes.
    image = image.astype(np.uint8)
    
    # Write the image-file in jpeg-format.
    with open(filename, 'wb') as file:
        PIL.Image.fromarray(image).save(file, 'jpeg')

"""
This function plots a large image. The image is given as a numpy array with pixel-values between 0 and 255.
"""
def plot_image_big(image):
    # Ensure the pixel-values are between 0 and 255.
    image = np.clip(image, 0.0, 255.0)

    # Convert pixels to bytes.
    image = image.astype(np.uint8)

    # Convert to a PIL-image and display it.
    Image._show(PIL.Image.fromarray(image))

"""
This function plots the content-, mixed- and style-images.
"""
def plot_images(content_image, style_image, mixed_image):
    # Create figure with sub-plots.
    fig, axes = plt.subplots(1, 3, figsize=(15, 15))

    # Adjust vertical spacing.
    fig.subplots_adjust(hspace=0.1, wspace=0.1)

    # Use interpolation to smooth pixels?
    smooth = True
    
    # Interpolation type.
    if smooth:
        interpolation = 'sinc'
    else:
        interpolation = 'nearest'

    # Plot the content-image.
    # Note that the pixel-values are normalized to
    # the [0.0, 1.0] range by dividing with 255.
    ax = axes.flat[0]
    ax.imshow(content_image / 255.0, interpolation=interpolation)
    ax.set_xlabel("Content")

    # Plot the mixed-image.
    ax = axes.flat[1]
    ax.imshow(mixed_image / 255.0, interpolation=interpolation)
    ax.set_xlabel("Mixed")

    # Plot the style-image
    ax = axes.flat[2]
    ax.imshow(style_image / 255.0, interpolation=interpolation)
    ax.set_xlabel("Style")

    # Remove ticks from all the plots.
    for ax in axes.flat:
        ax.set_xticks([])
        ax.set_yticks([])
    
    plt.show()

def plot_styles(style1, style2, style3, combinedStyle):
    # Create figure with sub-plots.
    fig, axes = plt.subplots(1, 4, figsize=(15, 15))

    # Adjust vertical spacing.
    fig.subplots_adjust(hspace=0.1, wspace=0.1)

    # Use interpolation to smooth pixels?
    smooth = True
    
    # Interpolation type.
    if smooth:
        interpolation = 'sinc'
    else:
        interpolation = 'nearest'

    # Plot style 1
    # Note that the pixel-values are normalized to
    # the [0.0, 1.0] range by dividing with 255.
    ax = axes.flat[0]
    ax.imshow(style1 / 255.0, interpolation=interpolation)
    ax.set_xlabel("Style 1")

    # Plot style 2
    ax = axes.flat[1]
    ax.imshow(style2 / 255.0, interpolation=interpolation)
    ax.set_xlabel("Style 2")

    # Plot style 3
    ax = axes.flat[2]
    ax.imshow(style3 / 255.0, interpolation=interpolation)
    ax.set_xlabel("Style 3")

    # Plot the style-image
    ax = axes.flat[3]
    ax.imshow(combinedStyle / 255.0, interpolation=interpolation)
    ax.set_xlabel("Combined Thematic Style")

    # Remove ticks from all the plots.
    for ax in axes.flat:
        ax.set_xticks([])
        ax.set_yticks([])
    
    plt.show()    

