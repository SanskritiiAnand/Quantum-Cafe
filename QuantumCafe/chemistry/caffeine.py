# Molecule:Caffeine (C8H10N4O2)
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class MolecularOrbital:
   """ Represents a frontier molecular orbital """
   name: str
   energy: float         #Hartree
   phase_factor: float   #geometry-derived phase factor

@dataclass(frozen=True)
class Molecule:
    """Stores molecular information required for Quantum Cafe """
    name: str
    formula: str
    orbitals: List[MolecularOrbital]

    @property
    def num_frontier_orbitals(self) -> int:
        return len(self.orbitals)
    
#Caffeine Data
CAFFEINE= Molecule(name= "Caffeine", formula= "C8H10N4O2",
                   orbitals=[MolecularOrbital(name="HOMO-2", energy=-0.312, phase_factor=1.37),
                             MolecularOrbital(name="HOMO-1", energy=-0.285, phase_factor=1.40),
                             MolecularOrbital(name="HOMO", energy=-0.245, phase_factor=1.37),
                             MolecularOrbital(name="LUMO", energy=0.012, phase_factor=1.39),
                             MolecularOrbital(name="LUMO+1", energy=0.085, phase_factor=1.38),
                             MolecularOrbital(name="LUMO+2", energy=0.142, phase_factor=1.40)
                            ]
                  )