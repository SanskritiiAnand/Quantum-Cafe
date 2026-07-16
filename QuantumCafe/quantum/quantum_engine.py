#builds and simulates the paramaeterised quantum circuit used by quantum cafe
from qiskit import QuantumCircuit
from chemistry.caffeine import Molecule
from brewing.brew import BrewProfile
from config import ProjectSettings
import numpy as np
from qiskit.quantum_info import Statevector

class QuantumEngine:
    """Quantum engine for Quantum Café."""
    def __init__(self, settings: ProjectSettings):
        self.settings = settings
        self.molecule: Molecule = settings.molecule
        self.brew: BrewProfile = settings.brew_profile
        self.num_qubits = self.molecule.num_frontier_orbitals
        self.circuit = QuantumCircuit(self.num_qubits, name=self.settings.performance_name)

    def __repr__(self):
        return (f"QuantumEngine("f"{self.num_qubits} qubits, "f"{self.molecule.name})")
    
    def _normalize_energy(self, energy: float, min_energy: float, max_energy: float) -> float:
        """
        Normalize orbital energy into the range [0, π].
        """
        if max_energy == min_energy:
           return 0.0

        normalized = (energy - min_energy) / (max_energy - min_energy)

        return normalized * np.pi
    
    def _encode_orbitals(self):
        """
        Encode orbital energies and geometry into the circuit.
        """
        energies = [orbital.energy for orbital in self.molecule.orbitals]

        min_energy = min(energies)
        max_energy = max(energies)

        temperature_scale = (self.brew.temperature / 100.0)

        bloom_scale = (self.brew.bloom_time / self.brew.total_brew_time)

        for qubit, orbital in enumerate(self.molecule.orbitals):
            theta = (self._normalize_energy(orbital.energy, min_energy, max_energy) * temperature_scale)
            phi = (orbital.phase_factor * bloom_scale)

            self.circuit.ry(theta, qubit)
            self.circuit.rz(phi, qubit)
     
    def build_circuit(self):
        """
        Build the parameterized quantum circuit.
        """
        self._encode_orbitals()
        self._entangle_orbitals()
        return self.circuit
    
    def _entangle_orbitals(self):
        """
        Entangle neighbouring frontier orbitals.
        """
        for qubit in range(self.num_qubits - 1):
            self.circuit.cx(qubit, qubit + 1)
    
    def simulate(self):
        """
        Simulate the quantum circuit and return the final statevector.
        """
        if len(self.circuit.data) == 0:
            self.build_circuit()
        self.statevector = Statevector.from_instruction(self.circuit)
            
        return self.statevector
    
    def extract_features(self):
        """
        Extract musical features from the simulated quantum state.
        """

        if not hasattr(self, "statevector"):
            self.simulate()

        probabilities = self.statevector.probabilities()

        return {"probabilities": probabilities,
                "dominant_state": int(np.argmax(probabilities)),
                "max_probability": float(np.max(probabilities)),
                "average_probability": float(np.mean(probabilities)),
               }