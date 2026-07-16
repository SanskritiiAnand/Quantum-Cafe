#Transforms quantum features into musical events.
from dataclasses import dataclass
from typing import List
from config import ProjectSettings
import numpy as np

@dataclass(frozen=True)
class MusicalEvent:
    """
    Represents a single MIDI note.
    """
    note: int
    velocity: int
    start: int
    duration: int

@dataclass
class Composition:
    """
    A complete musical composition consisting of multiple tracks
    """
    melody: list[MusicalEvent]
    bass: list[MusicalEvent]
    pad: list[MusicalEvent]
    harp: list[MusicalEvent]
    flute: list[MusicalEvent]

class Composer:
    """
    Converts quantum features into musical phrases.
    """
    def __init__(self, settings: ProjectSettings):
        self.settings = settings
        self.scale = settings.scale
        self.total_bars = settings.total_bars

        # Deterministic random generator
        self.rng = np.random.default_rng(settings.random_seed)

        # A four-note motif that gives the piece its identity
        self.motif = self.rng.choice(self.scale.notes, size=4, replace=False).tolist()

    def compose(self, features) -> Composition:
        probabilities = features["probabilities"]

        quarter = self.settings.ticks_per_beat
        bar_length = quarter * 4

        melody = []
        bass = []
        pad = []
        harp = []
        flute = []

        bass_pattern = [0, 0, 2, 3]

        for bar in range(self.total_bars):
            bar_start = bar * bar_length

            progress = bar / (self.total_bars - 1)
            brew_curve = np.sin(progress * np.pi)

            evolved = np.abs(np.sin(probabilities + bar * 0.18))
            evolved /= np.sum(evolved)

            # More activity in the middle of the brew
            if brew_curve < 0.30:
                num_notes = 4
            elif brew_curve < 0.75:
                num_notes = 6
            else:
                num_notes = 8

            top_states = np.argsort(evolved)[-num_notes:]

            for i, state in enumerate(top_states):
                probability = float(evolved[state])

                # Silence makes the phrases breathe
                rest_probability = 0.15 + 0.20 * (1.0 - brew_curve)

                if self.rng.random() < rest_probability:
                    continue

                jitter = self.rng.integers(-2, 6)

                start = bar_start + i * (quarter // 2) + jitter

                # Call & Response phrasing
                phrase = (bar // 2) % 2

                if phrase == 0:
                    base_note = self.motif[i % len(self.motif)]
                else:
                    base_note = self.motif[(i + 1) % len(self.motif)]

                offset = (state % 5) - 2

                note_index = self.scale.notes.index(base_note)
                note_index = max(0, min(len(self.scale.notes) - 1, note_index + offset))

                note = self.scale.notes[note_index]

                velocity = int(40 + probability * 35 + brew_curve * 30)
                velocity = max(35, min(110, velocity))

                duration = int(quarter * 0.75 + probability * quarter * 1.10)
                duration += self.rng.integers(-10, 11)
                duration = max(200, duration)

                melody.append(MusicalEvent(note=note, velocity=velocity, start=start, duration=duration))

            # Flute
            if bar > self.total_bars // 2 and melody:
                source = melody[-1]
                
                flute.append(MusicalEvent(note=min(source.note + 12, 84), 
                                          velocity=55, 
                                          start=source.start + quarter // 2, 
                                          duration=int(quarter * 1.4)
                                         )
                            )

            # Bass
            root = bass_pattern[bar % len(bass_pattern)]

            bass_note = self.scale.notes[root] - 24

            bass.append(MusicalEvent(note=max(0, bass_note), velocity=62, start=bar_start, duration=bar_length))

            # Pad
            top_three = np.argsort(evolved)[-3:]

            pad_note = self.scale.notes[top_three[0] % len(self.scale.notes)]

            if bar % 4 == 0:
                pad.append(MusicalEvent(note=pad_note, velocity=42, start=bar_start, duration=bar_length * 4))
            
            # Harp
            harp_note = self.scale.notes[(bar // 2) % len(self.scale.notes)]
            if bar % 2 == 0:
                harp.append(MusicalEvent(note=harp_note + 24, velocity=35, start=bar_start, duration=quarter))
        
        return Composition(melody=melody, bass=bass, pad=pad, harp=harp, flute=flute)