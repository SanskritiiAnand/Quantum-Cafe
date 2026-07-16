from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from qiskit.visualization import (plot_bloch_multivector, plot_state_qsphere)

ASSETS = Path("assets")
ASSETS.mkdir(exist_ok=True)

class Visualizer:
    def __init__(self, engine, settings):
        self.engine = engine
        self.settings = settings

    def generate_all(self):
        print("\nGenerating visualizations...")

        print("  • Quantum circuit")
        self.save_quantum_circuit()

        print("  • Bloch spheres")
        self.save_bloch_spheres()

        print("  • QSphere")
        self.save_qsphere()

        print("  • Probability distribution")
        self.save_probability_distribution()

        print("  • Brew curve")
        self.save_brew_curve()

        print("  • Orbital energy diagram")
        self.save_orbital_energies()

        print("Visualizations saved to assets/")

    ##################################################

    def save_quantum_circuit(self):

        self.engine.build_circuit()
        fig = self.engine.circuit.draw(output="mpl")

        fig.savefig(ASSETS / "quantum_circuit.png",
                    dpi=300,
                    bbox_inches="tight"
                   )

        plt.close(fig)

    ##################################################

    def save_bloch_spheres(self):

        fig = plot_bloch_multivector(self.engine.statevector)

        fig.savefig(ASSETS / "bloch_multivector.png",
                    dpi=300,
                    bbox_inches="tight"
                   )

        plt.close(fig)

    ##################################################

    def save_qsphere(self):

        fig = plot_state_qsphere(self.engine.statevector)

        fig.savefig(ASSETS / "qsphere.png",
                    dpi=300,
                    bbox_inches="tight"
                   )

        plt.close(fig)

    ##################################################

    def save_probability_distribution(self):

        probabilities = self.engine.statevector.probabilities()

        plt.figure(figsize=(10,4))

        plt.bar(np.arange(len(probabilities)), probabilities)

        plt.xlabel("Basis State")

        plt.ylabel("Probability")

        plt.title("Quantum State Probability Distribution")

        plt.tight_layout()

        plt.savefig(ASSETS / "statevector_probabilities.png", dpi=300)

        plt.close()

    ##################################################

    def save_brew_curve(self):

        x = np.linspace(0,1,self.settings.total_bars)

        y = np.sin(np.pi*x)

        plt.figure(figsize=(7,4))

        plt.plot(x,y)

        plt.fill_between(x,y,alpha=0.2)

        plt.xlabel("Composition Progress")

        plt.ylabel("Brew Intensity")

        plt.title("Coffee Brew Curve")

        plt.tight_layout()

        plt.savefig(ASSETS / "brew_curve.png", dpi=300)

        plt.close()

    ##################################################

    def save_orbital_energies(self):

        orbitals = self.settings.molecule.orbitals

        names = [o.name for o in orbitals]

        energies = [o.energy for o in orbitals]

        plt.figure(figsize=(6,5))

        for y,label in zip(energies,names):

            plt.hlines(y,0,1,lw=3)

            plt.text(1.02, y, label, va="center")

        plt.xlim(0,1.3)

        plt.xticks([])

        plt.ylabel("Energy (Hartree)")

        plt.title("Frontier Molecular Orbitals")

        plt.tight_layout()

        plt.savefig(ASSETS / "orbital_energies.png", dpi=300)

        plt.close()