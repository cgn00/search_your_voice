import os
import datetime
from huggingsound import SpeechRecognitionModel
import torch
import librosa
import soundfile as sf

class Voice:
        
    def __init__(self, input_file: str = 'audio/audio.wav', time_split: int = 30, model: str = 'jonatasgrosman/wav2vec2-large-xlsr-53-english', device: str = 'cpu') -> None:
        """
        The object that handles the speech
        
        Args:
        ----
            input_file (str, optional): 
                the path of the audio to split. Defaults to 'audio/audio.wav'.
            time_split (int, optional): 
                the duration in secnds of each divided audio. Defaults to 30 seconds.
            model (str, optional): 
                The model for the Speech Recognition. Defaults to 'jonatasgrosman/wav2vec2-large-xlsr-53-english'.
            device (str, optional): 
                Divice to execute the model: cpu or gpu. Defaults to 'cpu'.
        """
        
        self._input_file = input_file
        self._time_split = time_split
        self._model = SpeechRecognitionModel(model, device = device)
        self._divided_audio_path = [] # a list with the path of the audio divided in N audios
        
        self.__split_audio() # split the audio in N audios of self._time_split length
        
        self._trasncriptions = self._model.transcribe(self._divided_audio_path) # make the trasncription of the audio to text


    def set_SpeechRecognitionModel(self, model: str = 'jonatasgrosman/wav2vec2-large-xlsr-53-english', device: str = 'cpu'):
        """Define the model for the Speech Recognition.

        Args:
        ----
            model (str, optional): 
                The model for the Speech Recognition. Defaults to 'jonatasgrosman/wav2vec2-large-xlsr-53-english'.
            device (str, optional): 
                Divice to execute the model: cpu or gpu. Defaults to 'cpu'.
        """
        #device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model = SpeechRecognitionModel(model, device = device)

            
    def audio_to_text(self) -> str:
        """
        Return a string with the transcription of the audio

        Returns:
        -------
            str: string with the transcription of the audio
        """
        
        full_transcript_text = ''
        
        for item in self._trasncriptions: # iterate over each transcription
            full_transcript_text += ''.join(item['transcription'])
        
        return full_transcript_text
          
    
    def search_phrase(self, phrase_to_search: str) -> list:
        """
        Search the phrase in the audio an return a list with the times where begin the phrase
        if the phrase is not in the audio return [-1]

        Args:
        -----
        phrase_to_search (str): the phrase to search in the audio

        Returns:
        -------
            list: the times where begin the phrase if the phrase isn't in the audio return [-1]
        """
        
        phrase_start_times = [] # -1 means that the phrase couldn't be searched
        number_of_repetitions: int = 0 # the count of the time that the phrase is repeated
        block_time: int = 30 # the time in seconds of each block in transcriptions
        duration = 0 # the initial time of the audio

        for block in self._trasncriptions:
            text = block['transcription']
            start_timestamp = block['start_timestamps'] # a list with the start time in milliseconds of each character of the text
            
            temp_start_time = [-1]
            temp_loc = self.__find_phrase(text=text, phrase=phrase_to_search)
            #print(f'The locations of the phrase {phrase_to_search} are: {str(temp_loc)}')


            if temp_loc != [-1]: # if the phrase was found return a lis with the locations else return -1
                temp_start_time = [start_timestamp[i] for i in temp_loc] # obtain the all the start time of the first character of the phrase
                temp_start_time = [t/1000 + duration for t in temp_start_time] # convert the time from milliseconds to seconds and increment the time of the block

                temp_start_time = [datetime.datetime.fromtimestamp(t).strftime('%H.%M:%S.%f') for t in temp_start_time] # convert to H-M-S-ms format 

            #print(f'{text} \n amount of words = {len(text.split())}')
            #print(str(block['start_timestamps']))
            #print(f'start_timestamps_length = {len(block["start_timestamps"])}')
            #print(f'The phrase {phrase_to_search} appears in the times: {temp_start_time}')

            duration = duration + block_time # increment the begin time of the next block of the transcription
            
            if temp_start_time != [-1]: # if the phrase was found save it
                #phrase_start_times += ''.join(temp_start_time)
                phrase_start_times.extend(temp_start_time)
                
        if phrase_start_times:
            return phrase_start_times
        
        else:
            return [-1] # the phrase wasn't found in the audio
                
    # private methods
    
           
    def __find_phrase(self, text: str, phrase: str) -> list[int]:
        """
        Search the phrase in the text and if find the phrase return a list with the location in the text
        If the phrase couldn't be searched return [-1]
        
        Parametrs
        --------
        text: str 
            text to search the phrase
        phrase: str 
            phrase to search in the text

        """
        index = []
        end = len(text) # the length of the text
        pos = text.find(phrase, 0, end) # search from the first character to te last
        index.append(pos) # save the possition

        while(pos != -1): # while find the phrase in the text
            pos = text.find(phrase, pos+1, end) # start the search in the next character of the previous position found
            
            if(pos != -1):
                index.append(pos)

        return index
  
 
 

    
    def __split_audio(self):
        """
        Split the audio in N audios of self._time_split length
        """
        
        dir_name = os.path.dirname(self._input_file)
        
        sample_rate = librosa.get_samplerate(self._input_file)
        #print(sample_rate)

        # Stream over 30 seconds chunks rather than load the full file
        stream = librosa.stream(
            self._input_file,
            block_length=self._time_split,
            frame_length=sample_rate,
            hop_length=sample_rate
        )

        
        for i,speech in enumerate(stream):
            file_to_save = os.path.join(dir_name, f'{i}.wav')
            sf.write(file_to_save, speech, sample_rate)
        
        for a in range(i+1):
            file_to_save = os.path.join(dir_name, f'{a}.wav')
            self._divided_audio_path.append(file_to_save) 
            
     
            
            