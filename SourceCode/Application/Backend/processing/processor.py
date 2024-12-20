from pydub import AudioSegment
from pydub.utils import make_chunks
from PIL import Image
import librosa
import librosa.display
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch
from torchvision import transforms
import torch.nn.functional as F

from model import VGG19_Pretrained

class Processor:
    def __init__(self, sound_file_name):
        self.sound_file_name = sound_file_name
        self.sound_file_path = os.path.join("input_sounds", sound_file_name)
        self.model_path = "vgg19_pretrained_model.pt"

        self.sound_chunk_parent = os.path.join("processing/sound_chunks", sound_file_name)
        self.spectrograms_original_parent = os.path.join("processing/spectrograms/original", sound_file_name)
        self.spectrograms_parent = os.path.join("processing/spectrograms", sound_file_name)

    def process(self):
        print("process run")
        if not self.check_sound_file():
            return

        self.create_sound_pieces()
        self.create_spectrograms()

    def check_sound_file(self):
        if not os.path.exists(self.sound_file_path):
            print(f"File not found: {self.sound_file_path}")
            return False

        print("check_sound_file run")
        file_extension = os.path.splitext(self.sound_file_path)[1].lower()

        if file_extension not in ['.mp3', '.wav']:
            print(f"Unsupported file format: {file_extension}. Only MP3 and WAV are supported.")
            return False

        return True

    def create_sound_pieces(self):
        print("create_sound_pieces run")
        sound = AudioSegment.from_file(self.sound_file_path)

        chunk_duration_ms = 3000
        chunks = make_chunks(sound, chunk_duration_ms)

        os.makedirs(self.sound_chunk_parent, exist_ok=True)

        for i, chunk in enumerate(chunks):
            normalize_db = -20
            chunk_name = os.path.join(self.sound_chunk_parent, f"chunk_{i + 1}.wav")
            db_diff = normalize_db - chunk.dBFS
            normalized_chunk = chunk.apply_gain(db_diff)
            normalized_chunk.export(chunk_name, format="wav")
            print(f"Saved: {chunk_name}")

    def create_spectrograms(self):
        print("create_spectrograms run")

        os.makedirs(self.spectrograms_parent, exist_ok=True)
        os.makedirs(self.spectrograms_original_parent, exist_ok=True)

        for i, chunk_name in enumerate(os.listdir(self.sound_chunk_parent)):
            chunk_path = os.path.join(self.sound_chunk_parent, chunk_name)
            spectrogram_name = f"spectrogram_{i + 1}.jpg"
            spectrogram_original_path = os.path.join(self.spectrograms_original_parent, spectrogram_name)
            spectrogram_resized_path = os.path.join(self.spectrograms_parent, spectrogram_name)

            if os.path.isfile(spectrogram_resized_path):
                print(f"Spectrogram file already exist: {spectrogram_resized_path}")
                continue
            else:
                print(f"Original spectrogram file processing: {spectrogram_resized_path}")

            y, sr = librosa.load(chunk_path)
            S = librosa.feature.melspectrogram(y=y, sr=sr)
            S_dB = librosa.power_to_db(S, ref=np.max)

            plt.figure(figsize=(6, 3), dpi=100)
            plt.axis('off')
            librosa.display.specshow(S_dB, sr=sr, x_axis=None, y_axis=None, fmax=sr / 2)

            plt.savefig(spectrogram_original_path, bbox_inches='tight', pad_inches=0)
            plt.close()

            with Image.open(spectrogram_original_path) as img:
                img = img.convert("RGB")
                resized_img = img.resize((224, 224))
                resized_img.save(spectrogram_resized_path, format="JPEG")


    def run_model(self):
        print("create_spectrograms run")
        if not os.path.exists(self.model_path):
            print(f"Model file not found: {self.model_path}")
            return []

        model = VGG19_Pretrained()
        model.load_state_dict(torch.load(self.model_path, map_location=torch.device('cpu')))
        model.eval()

        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        results = []
        for spectrogram_name in os.listdir(self.spectrograms_parent):
            spectrogram_path = os.path.join(self.spectrograms_parent, spectrogram_name)

            if not spectrogram_name.lower().endswith('.jpg'):
                print(f"Skipping non-JPG file: {spectrogram_name}")
                continue

            # Load and preprocess the image
            with Image.open(spectrogram_path) as img:
                tensor = transform(img).unsqueeze(0)  # Add batch dimension

            # Run the model on the image
            with torch.no_grad():
                output = model(tensor)
                _, predicted_class = torch.max(output, 1)  # Get the predicted class

            print(f"Processed {spectrogram_name}")
            print(f"output :  {F.softmax(output, dim=1)}")
            print(f"Predicted class {predicted_class.item()}")

            results.append((spectrogram_name, predicted_class.item(), F.softmax(output, dim=1).squeeze().tolist()))

        # Print all results
        print("All predictions:")
        for spectrogram_name, predicted_class, prediction_all in results:
            print(f"{spectrogram_name}: {predicted_class} : {prediction_all}")

        return results


if __name__ == '__main__':
    processor = Processor("01. I Don't Worry About a Thing.wav");
    processor.process()
    print(processor.run_model())
