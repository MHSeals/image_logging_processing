import argparse
import os
import tqdm

parser = argparse.ArgumentParser(description='Processes the text files from the InferenceStats')
parser.add_argument('folder', type=str, help='The folder containing the text files')

args = parser.parse_args()

print("Processing text files...")

if not os.path.exists(args.folder):
    print("The folder does not exist")
    exit(1)

# Get all the text files from the folder
textFiles = [file for file in os.listdir(args.folder) if file.endswith('.txt')]
textFiles.sort()

# Create a dictionary to store the data
data = {}

# Process each text file

inferenceTime = 0
callbackTime = 0
alltimeFPS = 0
avgFPS = 0

for file in tqdm.tqdm(textFiles):
    with open(os.path.join(args.folder, file), 'r') as f:
        if f.read() == '':
            continue

        f.seek(0)
        lines = "".join([line.strip() for line in f.readlines()])
        """Inference took 12893.747840000287ms
Callback processing took 13386.44617600039msCurrent alltime FPS: 0.06755492552138413Current avg FPS: 0.6185334064251186"""

        inferenceTime += float(lines.split('Inference took ')[1].split('ms')[0])
        callbackTime += float(lines.split('Callback processing took ')[1].split('ms')[0])
        alltimeFPS = float(lines.split('Current alltime FPS: ')[1].split('Current avg FPS: ')[0])
        avgFPS += float(lines.split('Current avg FPS: ')[1])

inferenceTime /= len(textFiles)
callbackTime /= len(textFiles)
alltimeFPS /= len(textFiles)
avgFPS /= len(textFiles)

print(f"Inference time: {inferenceTime}ms")
print(f"Callback time: {callbackTime}ms")
print(f"Alltime FPS: {alltimeFPS}")
print(f"Avg FPS: {avgFPS}")
