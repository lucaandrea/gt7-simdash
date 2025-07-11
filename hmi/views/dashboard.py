import pygame
from granturismo.model import Packet

from ai import AIRacingEngineer
from events import HMI_VIEW_BUTTON_PRESSED
from hmi.properties import Color
from hmi.widgets.button import Button
from hmi.widgets.carsor import Carsor
from hmi.widgets.gear import GearIndicator
from hmi.widgets.lap import BestLap, EstimatedLap, Laps
from hmi.widgets.led import LED
from hmi.widgets.minimap import Minimap
from hmi.widgets.rpm import GraphicalRPM, SimpleRPM
from hmi.widgets.speed import Speedometer
from hmi.widgets.voice import VoiceButton


class Dashboard:
    def __init__(self, openai_api_key: str | None = None):
        self.screen = pygame.display.get_surface()
        self.telemetry = pygame.sprite.Group()
        self.engineer = (
            AIRacingEngineer(api_key=openai_api_key) if openai_api_key else None
        )

        SimpleRPM(self.telemetry, 76, 33)
        GraphicalRPM(self.telemetry, 100, 40)
        GearIndicator(self.telemetry, 200, 248)
        Speedometer(self.telemetry, 200, 150)
        Laps(self.telemetry, 127, 96)
        EstimatedLap(self.telemetry, 260, 104)
        BestLap(self.telemetry, 260, 104)
        Minimap(self.telemetry, 350, 350)
        Carsor(self.telemetry, 350, 350)
        LED()

        # PSL = Pit Speed Limiter
        # ASM = Active Stability Management
        # TCS = Traction Control System
        labels = ["ASM", "TCS", "LIGHTS", "HIBEAM"]
        self.buttons = [
            Button(f"{labels[i]}", ((125 * (i % 4) + 120), 558), (115, 50), 40)
            for i in range(len(labels))
        ]
        if self.engineer:
            self.voice = VoiceButton((620, 558), self.engineer)
            self.buttons.append(self.voice)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for button in self.buttons:
            if button.is_pressed(events):
                if isinstance(button, VoiceButton):
                    button.toggle()
                pygame.event.post(
                    pygame.event.Event(HMI_VIEW_BUTTON_PRESSED, message=button.text)
                )

    def update(self, packet: Packet):
        self.screen.fill(Color.BLACK.rgb())
        self.telemetry.update(packet)
        self.telemetry.draw(self.screen)

        for button in self.buttons:
            button.update(packet)
            button.render(self.screen)
            if isinstance(button, VoiceButton):
                button.update_packet(packet)

    def update_rpm_alerts(self, rpmin, rpmax):
        for sprite in self.telemetry.sprites():
            if isinstance(sprite, SimpleRPM):
                sprite.alert_min(rpmin)
                sprite.alert_max(rpmax)
