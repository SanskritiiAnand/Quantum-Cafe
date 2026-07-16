from config import SETTINGS
from quantum.quantum_engine import QuantumEngine
from music.composer import Composer
from music.midi_engine import MidiEngine
from visuals import Visualizer

def main():
    print("=" * 50)
    print("Quantum Cafe")
    print("=" * 50)

    #quantum simulation
    print("\nRunning quantum simulation...")
    
    engine = QuantumEngine(SETTINGS)
    engine.simulate()
    features= engine.extract_features()
    visualizer = Visualizer(engine, SETTINGS)
    visualizer.generate_all()

    print(f"Number of qubits: {engine.num_qubits}")
    print(f"Quantum states: {len(features['probabilities'])}")

    #composition
    print("\nComposing music...")
    
    composer= Composer(SETTINGS)
    composition= composer.compose(features)
    
    print(f"Melody events: {len(composition.melody)}")
    print(f"Bass events: {len(composition.bass)}")
    print(f"Pad events: {len(composition.pad)}")
    print(f"Harp events: {len(composition.harp)}")
    print(f"Flute events: {len(composition.flute)}")

    #MIDI export
    print("\nWriting MIDI...")

    midi= MidiEngine(SETTINGS)
    filename= midi.write(composition)
    print(f"MIDI saved as '{filename}' ")

if __name__ == "__main__":
    main()
