from qiskit import QuantumCircuit
import matplotlib.pyplot as plt

circuit = QuantumCircuit(2)
circuit.h([0,1])
circuit.measure_all()
circuit.draw(output='mpl')

plt.show()