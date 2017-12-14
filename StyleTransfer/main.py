import imageUtils
import sys
import glob
import downloadStyles
import os
import styleTransfer

# The VGG16-model has 13 convolutional layers.
NUMBER_OF_CONV_LAYERS_IN_VGG16 = 13

def main(contentFilePath, theme):
    mixedStyleImage = None
    contentImage = imageUtils.load_image(contentFilePath, max_size=None)
    
    content_layer_ids = [4]
    style_layer_ids = list(range(NUMBER_OF_CONV_LAYERS_IN_VGG16))
    
    # Remove all previous styles
    [os.remove(file) for file in glob.glob('Images/style*.jpg')]
    
    # Download style images and save them to disk.
    # Combine styles using this network itself.
    downloadStyles.downloadImages(theme, 'jpg', numberOfImages=3, height=600, width=600)
    styles = glob.glob('Images/style*.jpg')

    if len(styles) > 0:
        startStyle = imageUtils.load_image(styles[0], max_size=None)
        for image in styles[1:]:
            styleImage = imageUtils.load_image(image, max_size=None)
            mixedStyleImage = styleTransfer.style_transfer(content_image=startStyle,
                                 style_image=styleImage,
                                 content_layer_ids=content_layer_ids,
                                 style_layer_ids=style_layer_ids,
                                 alpha=5.0,
                                 beta=5.0,
                                 weight_denoise=0.3,
                                 num_iterations=100,
                                 step_size=2.0)
        
            startStyle = mixedStyleImage

    imageUtils.save_image(mixedStyleImage, "Images/" + "style.jpg")
    ##imageUtils.plot_image_big(mixedStyleImage)
    imageUtils.plot_styles(
        imageUtils.load_image(styles[0], max_size=None), 
        imageUtils.load_image(styles[1], max_size=None), 
        imageUtils.load_image(styles[2], max_size=None), 
        mixedStyleImage
        )
    
    # Now apply on the content image
    mixedImage = styleTransfer.style_transfer(content_image=contentImage,
                        style_image=mixedStyleImage,
                        content_layer_ids=content_layer_ids,
                        style_layer_ids=style_layer_ids,
                        alpha=1.5,
                        beta=10.0,
                        weight_denoise=0.3,
                        num_iterations=100,
                        step_size=2.0)

    imageUtils.plot_images(contentImage, mixedStyleImage, mixedImage)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        content = sys.argv[1]
        theme = sys.argv[2]
        main(content, theme)
    else:
        print()
        print("Run as:")
        print("python " + __file__ + " <Path to content image> <theme>")
        print()
    

