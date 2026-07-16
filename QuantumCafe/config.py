#global configuration for quantum cafe
from dataclasses import dataclass
from chemistry.caffeine import Molecule, CAFFEINE
from brewing.brew import BrewProfile, MORNING_V60
from music.scales import Scale, MORNING_PENTATONIC

@dataclass(frozen=True)
class ProjectSettings:
    performance_name: str
    #chemistry
    molecule: Molecule
    #brewing
    brew_profile: BrewProfile
    #music
    total_bars: int
    ticks_per_beat: int
    bpm_start: float
    bpm_end: float
    random_seed: int
    midi_filename: str
    scale: Scale

#project settings
SETTINGS= ProjectSettings(performance_name="Morning Quantum Café",
                          molecule=CAFFEINE,
                          brew_profile=MORNING_V60,
                          scale= MORNING_PENTATONIC,
                          total_bars=32,
                          ticks_per_beat=480,
                          bpm_start=46,
                          bpm_end=72,
                          random_seed=1729,
                          midi_filename="quantum_cafe.mid"
                         )