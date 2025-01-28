from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
import matplotlib.pyplot as plt
from qiskit_aer import Aer, AerSimulator
from qiskit.visualization import plot_histogram

qReg = QuantumRegister(1, 'q')
cReg = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qReg, cReg)
circuit.h(qReg[0])
circuit.measure(qReg[0], cReg[0])
#display(circuit.draw('latex'))
circuit.draw(output='mpl')

device = Aer.get_backend('qasm_simulator')

# job = execute(circuit, backend=device, shots=1024)
new_circuit = transpile(circuit, backend=device)
job = device.run(new_circuit, shots=1000)
print(job.job_id())

result = job.result()
counts = result.get_counts(circuit)

print(counts)

plot_histogram(counts)

plt.show()