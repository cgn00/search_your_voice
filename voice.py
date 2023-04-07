import os
from huggingsound import SpeechRecognitionModel
import torch
import librosa
import soundfile as sf


model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english", device = device)

split_audio_path = []

def set_SpeechRecognitionModel(model: str = 'jonatasgrosman/wav2vec2-large-xlsr-53-english', device: str = 'cpu'):
    """Define the model for the Speech Recognition.

    Args:
    ----
        model (str, optional): The model for the Speech Recognition. Defaults to 'jonatasgrosman/wav2vec2-large-xlsr-53-english'.
        device (str, optional): Divice to execute the model: cpu or gpu. Defaults to 'cpu'.
    """
    #device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SpeechRecognitionModel(model, device = device)


def split_audio(input_file: str = 'audio/audio.wav', time_split: int = 30):
    """Split the audio in N audios of time_split length

    Args:
    -----
        input_file (str, optional): 
            the path of the audio to split. Defaults to 'audio/audio.wav'.
        time_split (int, optional): 
            the duration in secnds of each divided audio. Defaults to 30 seconds.
    """
    
    dir_name = os.path.dirname(input_file)
    
    sample_rate = librosa.get_samplerate(input_file)
    #print(sample_rate)

    # Stream over 30 seconds chunks rather than load the full file
    stream = librosa.stream(
        input_file,
        block_length=time_split,
        frame_length=sample_rate,
        hop_length=sample_rate
    )

    
    for i,speech in enumerate(stream):
        sf.write(f'{i}.wav', speech, sample_rate)
    
    for a in range(i+1):
        file_to_save = os.path.join(dir_name, f'{a}.wav')
        split_audio_path.append(file_to_save) 
        
        
    def audio_to_text():
        
        
        
        