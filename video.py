import argparse
import cv2
import os
import tqdm
import time

# images folder is list of images with name which is epoch time of the image

def convertImageSequenceToVideo(imagesFolder, images, outputVideoPath, fps):
    # Get the first image's dimensions
    height, width, layers = cv2.imread(filename=os.path.join(imagesFolder, images[0])).shape
    # Create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(outputVideoPath, fourcc, fps, (width, height))
    # Add all the images to the video
    try:
        last_image = images[0]
        for image in tqdm.tqdm(images[1:]):
            difference = float(image.split('_')[0]) - float(last_image.split('_')[0])
            frames = int(round(difference * fps))
            img = cv2.imread(os.path.join(imagesFolder, last_image))
            for i in range(frames):
                video.write(img)

            last_image = image


    except KeyboardInterrupt:
        print("Video conversion interrupted, cleaning up...")
    # Release the video writer
    cv2.destroyAllWindows()
    video.release()
    print("Video conversion complete")

parser = argparse.ArgumentParser(description='Converts a sequence of images to a video')
parser.add_argument('folder', type=str, help='The folder containing the images')
parser.add_argument('output', type=str, help='The output video path')
parser.add_argument('-ai', '--use_ai_images', action='store_true', help='Use the AI images instead of the original images')

args = parser.parse_args()

print("Determining FPS...")

FPS = 30

print(f"Determined FPS: {FPS}")

print("Converting images to video...")

# Get all the images from the images folder
if args.use_ai_images:
    images = [img for img in os.listdir(args.folder) if '_ai' in img]
else:
    images = [img for img in os.listdir(args.folder) if not '_ai' in img]
    
# Sort the images by name
images.sort(key=lambda x: int(x.split('_')[0].split('.')[0]))

convertImageSequenceToVideo(args.folder, images, args.output, FPS)
