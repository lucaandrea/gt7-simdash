import tempfile
import threading
from typing import Optional

import sounddevice as sd
from granturismo.model import Packet
from scipy.io import wavfile

from ai import AIRacingEngineer
from common.logger import Logger

from .button import Button


class VoiceButton(Button):
    def __init__(self, position: tuple[int, int], engineer: AIRacingEngineer):
        super().__init__("MIC", position, (115, 50), 40)
        self.engineer = engineer
        self.listening = False
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self.logger = Logger(self.__class__.__name__).get()
        self.current_packet: Optional[Packet] = None

    def _listen_loop(self) -> None:
        fs = 16000
        while not self._stop.is_set():
            duration = 5
            audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()
            with tempfile.NamedTemporaryFile(suffix=".wav") as f:
                wavfile.write(f.name, fs, audio)
                with open(f.name, "rb") as f_audio:
                    try:
                        transcript = self.engineer.client.audio.transcriptions.create(
                            model="whisper-1", file=f_audio
                        ).text
                    except Exception as e:
                        self.logger.error(f"transcription error: {e}")
                        continue
            if transcript.strip() and self.current_packet is not None:
                try:
                    answer = self.engineer.answer(transcript, self.current_packet)
                    self.logger.info(f"AI response: {answer}")
                except Exception as e:
                    self.logger.error(f"AI error: {e}")

    def toggle(self) -> None:
        self.listening = not self.listening
        self.set_text("PAUSE" if self.listening else "MIC")
        if self.listening:
            self._stop.clear()
            self._thread = threading.Thread(target=self._listen_loop, daemon=True)
            self._thread.start()
        else:
            self._stop.set()

    def update_packet(self, packet: Packet) -> None:
        self.current_packet = packet
