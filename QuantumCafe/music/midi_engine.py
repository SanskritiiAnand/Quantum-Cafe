#Writes musical events to a MIDI file.
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
from config import ProjectSettings
from music.composer import Composition

class MidiEngine:
    """
    Converts MusicalEvent objects into a MIDI file.
    """
    def __init__(self, settings: ProjectSettings):
        self.settings = settings

    def _create_track(self, midi: MidiFile, name: str, program: int, channel):
        track = MidiTrack()
        midi.tracks.append(track)

        track.append(MetaMessage("track_name", name=name, time=0))
        track.append(Message("program_change", channel=channel, program=program, time=0))

        return track

    def _write_events(self, track: MidiTrack, events, channel):
        timeline = []
        for event in events:
            timeline.append((event.start, Message("note_on", channel=channel, note=event.note, velocity=event.velocity, time=0)))

            timeline.append((event.start + event.duration, Message("note_off", channel=channel, note=event.note, velocity=0, time=0)))

        timeline.sort(key=lambda x: x[0])

        previous_time = 0

        for absolute_time, message in timeline:
            message.time = absolute_time - previous_time
            track.append(message)
            previous_time = absolute_time

    def write(self, composition: Composition):
        midi = MidiFile(ticks_per_beat=self.settings.ticks_per_beat)

        tempo_track = MidiTrack()
        midi.tracks.append(tempo_track)

        tempo_track.append(MetaMessage("track_name", name=self.settings.performance_name, time=0))

        tempo_track.append(MetaMessage("set_tempo", tempo=bpm2tempo(self.settings.bpm_start), time=0))

        # Piano Melody
        melody_track = self._create_track(midi, "Piano Melody", 0, 0)

        self._write_events(melody_track, composition.melody, 0)

        # Pad
        pad_track = self._create_track(midi, "Pad", 89, 1)

        self._write_events(pad_track, composition.pad, 1)

        # Harp
        harp_track = self._create_track(midi, "Harp", 46, 2)

        self._write_events(harp_track, composition.harp, 2)

        # Flute
        flute_track = self._create_track(midi, "Flute", 73, 3)

        self._write_events(flute_track, composition.flute, 3)

        # Bass
        bass_track = self._create_track(midi, "Bass", 0, 4)

        self._write_events(bass_track, composition.bass, 4)

        midi.save(self.settings.midi_filename)

        return self.settings.midi_filename