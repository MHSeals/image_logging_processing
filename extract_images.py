import argparse
import os
import shutil
import sys
import tqdm

parser = argparse.ArgumentParser(description='Extracts images from computer output')
parser.add_argument('folder', type=str, help='The folder containing the images')
parser.add_argument('output', type=str, help='The output folder path')
parser.add_argument('-p', '--percentage', type=float, help='The percentage of images to extract', default=1)
parser.add_argument('-f', '--force', action='store_true', help='Force overwrite of output folder')
parser.add_argument('-ai', '--use_ai_images', action='store_true', help='Use the AI images instead of the original images')

args = parser.parse_args()

print("Extracting images...")
if args.use_ai_images:
    images = [img for img in os.listdir(args.folder) if '_ai' in img]
else:
    images = [img for img in os.listdir(args.folder) if not '_ai' in img]
    
images.sort(key=lambda x: int(x.split('_')[0].split('.')[0]))

num_images = int(len(images) * args.percentage)

interval = len(images) // num_images

images = images[::interval]

print(f"Extracting {len(images)} images")

if not os.path.exists(args.output):
    os.makedirs(args.output)
else:
    if not args.force:
        conf = input("Output folder already exists. Do you want to overwrite it? (y/n) ")
        if conf.lower() != 'y':
            print("Aborting")
            sys.exit(0)

    shutil.rmtree(args.output)
    os.makedirs(args.output)

for image in tqdm.tqdm(images):
    shutil.copy(os.path.join(args.folder, image), args.output)

print("Images extracted")