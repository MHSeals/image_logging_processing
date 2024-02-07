import argparse
import cv2
import os
import tqdm

# images folder is list of images with name which is epoch time of the image

def convertImageSequenceToVideo(images, outputVideoPath, fps):
    # Get the first image to get the size
    frame = cv2.imread(os.path.join(imagesFolder, images[0]))
    height, width, layers = frame.shape
    # Create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(outputVideoPath, fourcc, fps, (width, height))
    # Add all the images to the video
    try:
        for image in tqdm.tqdm(images):
            video.write(cv2.imread(os.path.join(imagesFolder, image)))
    except KeyboardInterrupt:
        print("Video conversion interrupted")
    # Release the video writer
    cv2.destroyAllWindows()
    video.release()

def getFPS(imagesFolder):
    images = [img for img in os.listdir(imagesFolder) if not '_ai' in img]
    images.sort(key=lambda x: int(x.split('_')[0].split('.')[0]))
    firstImage = cv2.imread(os.path.join(imagesFolder, images[0]))
    lastImage = cv2.imread(os.path.join(imagesFolder, images[-1]))
    timeDifference = int(images[-1].split('_')[0].split('.')[0]) - int(images[0].split('_')[0].split('.')[0])
    return len(images) / timeDifference

parser = argparse.ArgumentParser(description='Converts a sequence of images to a video')
parser.add_argument('folder', type=str, help='The folder containing the images')
parser.add_argument('output', type=str, help='The output video path')
parser.add_argument('-ai', '--use_ai_images', action='store_true', help='Use the AI images instead of the original images')

args = parser.parse_args()

print("Determining FPS...")

FPS = getFPS(args.folder)

print(f"Determined FPS: {FPS}")

print("Converting images to video...")

# Get all the images from the images folder
if args.use_ai_images:
    images = [img for img in os.listdir(args.folder) if '_ai' in img]
else:
    images = [img for img in os.listdir(args.folder) if not '_ai' in img]
    
# Sort the images by name
images.sort(key=lambda x: int(x.split('_')[0].split('.')[0]))

convertImageSequenceToVideo(args.folder, args.output, FPS)
