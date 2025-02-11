from qiskit import QuantumRegister, QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit_aer import Aer
import matplotlib.pyplot as plt

reg = QuantumRegister(1)

circuit = QuantumCircuit(reg)
circuit.x(reg[0])
circuit.h(reg[0])

circuit.draw(output='mpl', initial_state=True)

vector = Statevector(circuit)
plot_bloch_multivector(vector.data)

device = Aer.get_backend('qasm_simulator')

circuit.measure_all()

new_circuit = transpile(circuit, backend=device)
job = device.run(new_circuit, shots=1000)
print(job.job_id())

result = job.result()
counts = result.get_counts(circuit)
print(counts)

plot_histogram(counts)

plt.show()
