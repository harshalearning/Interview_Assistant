"""Speech module for audio capture, processing, and text-to-speech."""

import asyncio
import numpy as np
from typing import Optional, List
import json

class AudioProcessor:
    """Handle audio capture and processing."""
    
    def __init__(self, sample_rate: int = 16000):
        """Initialize audio processor.
        
        Args:
            sample_rate: Audio sample rate in Hz (default 16000)
        """
        self.sample_rate = sample_rate
        self.audio_buffer = []
    
    def capture_audio(self, duration: float) -> np.ndarray:
        """Capture audio from microphone.
        
        Args:
            duration: Duration in seconds
            
        Returns:
            Audio data as numpy array
        """
        try:
            import sounddevice as sd
            print(f"Recording for {duration} seconds...")
            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.float32
            )
            sd.wait()
            print("Recording complete")
            return audio_data
        except Exception as e:
            print(f"Error capturing audio: {e}")
            return None
    
    def playback_audio(self, audio_data: np.ndarray):
        """Play audio data.
        
        Args:
            audio_data: Audio data to play
        """
        try:
            import sounddevice as sd
            sd.play(audio_data, samplerate=self.sample_rate)
            sd.wait()
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def normalize_audio(self, audio_data: np.ndarray) -> np.ndarray:
        """Normalize audio to [-1, 1] range.
        
        Args:
            audio_data: Audio data to normalize
            
        Returns:
            Normalized audio data
        """
        if audio_data.size == 0:
            return audio_data
        max_val = np.abs(audio_data).max()
        if max_val > 0:
            return audio_data / max_val
        return audio_data


class SpeechToText:
    """Convert speech to text using faster-whisper."""
    
    def __init__(self, model: str = "base"):
        """Initialize speech-to-text model.
        
        Args:
            model: Model size (tiny, base, small, medium, large)
        """
        try:
            from faster_whisper import WhisperModel
            self.model = WhisperModel(model, device="cpu", compute_type="int8")
            self.model_name = model
        except ImportError:
            print("faster-whisper not installed")
            self.model = None
    
    async def transcribe(self, audio_file: str) -> dict:
        """Transcribe audio file to text.
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            Dictionary with transcription and metadata
        """
        if not self.model:
            return {"error": "Model not initialized"}
        
        try:
            segments, info = self.model.transcribe(audio_file, language="en")
            text = " ".join([segment.text for segment in segments])
            
            return {
                "text": text,
                "language": info.language,
                "duration": info.duration,
                "segments": [
                    {
                        "text": seg.text,
                        "start": seg.start,
                        "end": seg.end,
                        "confidence": seg.confidence
                    }
                    for seg in segments
                ]
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def transcribe_stream(self, audio_stream) -> str:
        """Transcribe audio stream in real-time.
        
        Args:
            audio_stream: Audio stream object
            
        Returns:
            Transcribed text
        """
        # Placeholder for streaming transcription
        return "Streaming transcription not yet implemented"


class TextToSpeech:
    """Convert text to speech."""
    
    def __init__(self, engine: str = "pyttsx3"):
        """Initialize text-to-speech engine.
        
        Args:
            engine: TTS engine to use (pyttsx3, gTTS, etc.)
        """
        self.engine = engine
        self.voice_config = {
            "rate": 150,
            "volume": 1.0,
            "voice": 0  # 0 for male, 1 for female
        }
    
    async def synthesize(self, text: str) -> dict:
        """Synthesize text to speech.
        
        Args:
            text: Text to synthesize
            
        Returns:
            Dictionary with audio file path and metadata
        """
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', self.voice_config['rate'])
            engine.setProperty('volume', self.voice_config['volume'])
            
            output_file = f"/tmp/speech_{hash(text) % 10000}.mp3"
            engine.save_to_file(text, output_file)
            engine.runAndWait()
            
            return {
                "status": "success",
                "audio_file": output_file,
                "duration": len(text) / self.voice_config['rate']
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}


class VoiceQualityAnalyzer:
    """Analyze voice quality metrics."""
    
    @staticmethod
    def calculate_mfcc(audio_data: np.ndarray, sample_rate: int = 16000) -> np.ndarray:
        """Calculate MFCC (Mel-Frequency Cepstral Coefficients).
        
        Args:
            audio_data: Audio data
            sample_rate: Sample rate
            
        Returns:
            MFCC features
        """
        try:
            from librosa.feature import mfcc
            return mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)
        except ImportError:
            print("librosa not installed for MFCC calculation")
            return None
    
    @staticmethod
    def analyze_volume(audio_data: np.ndarray) -> dict:
        """Analyze volume characteristics.
        
        Args:
            audio_data: Audio data
            
        Returns:
            Volume metrics
        """
        rms = np.sqrt(np.mean(audio_data ** 2))
        return {
            "rms": float(rms),
            "peak": float(np.max(np.abs(audio_data))),
            "avg": float(np.mean(np.abs(audio_data)))
        }
    
    @staticmethod
    def analyze_pitch(audio_data: np.ndarray, sample_rate: int = 16000) -> dict:
        """Analyze pitch characteristics (placeholder).
        
        Args:
            audio_data: Audio data
            sample_rate: Sample rate
            
        Returns:
            Pitch metrics
        """
        return {
            "fundamental_frequency": 0.0,
            "variance": 0.0,
            "note": "Not implemented yet"
        }
