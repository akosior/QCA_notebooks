### Quantum Teleportation with Dynamic Circuit Scheduling
### Wstawiłem wszystkie fixy jakie znalazłem i działa ale wyniki pozostawiają wiele do życzenia
### Możliwe, że takie powinny być (w sumie nie są bardzo oddalone) ale warto wrócić kiedyć do tego kodu
### i sprawdzić czy nie ma błędów

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
import random
import numpy as np
from qiskit.result import marginal_counts
from qiskit_aer import Aer

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler.passmanager import PassManager

from qiskit.circuit.library import XGate

from qiskit_ibm_runtime.transpiler.passes.scheduling import DynamicCircuitInstructionDurations
from qiskit_ibm_runtime.transpiler.passes.scheduling import ALAPScheduleAnalysis
from qiskit_ibm_runtime.transpiler.passes.scheduling import PadDynamicalDecoupling

from qiskit_ibm_runtime.fake_provider import FakeJakartaV2

def create_registers():
    alice_q = QuantumRegister(1, name='alice (q)')
    peter_alice_q = QuantumRegister(1, name='peter/alice (q)')
    peter_bob_q = QuantumRegister(1, name='peter/bob (q)')
    bob_c = ClassicalRegister(3, name='bob (c)')
    circ = QuantumCircuit(alice_q, peter_alice_q, peter_bob_q, bob_c)
    return circ

def generate_amplitudes():
    alpha = np.sqrt(random.uniform(0, 1))
    beta = np.sqrt(1 - alpha**2)
    return alpha, beta

def add_gates(circ, alpha, beta):
    circ.initialize([alpha, beta], 0)
    circ.barrier()
    circ.h(1)
    circ.cx(1, 2)
    circ.barrier()
    circ.cx(0, 1)
    circ.h(0)
    circ.barrier()
    circ.measure(0,0)
    circ.measure(1,1)
    with circ.if_test((1,1)): # normal 'if' statement does not work here. The gate would be created at the creation
                              # of the circuit and not at the moment when the circuit is working
        circ.x(2)
    with circ.if_test((0,1)):
        circ.z(2)
    circ.measure(2,2)
    return circ

circuit = create_registers()
alpha, beta = generate_amplitudes()
circuit = add_gates(circuit, alpha, beta)
#circuit.draw(output='mpl')

print("Initial: |\u03C8\u27E9 ({:.4f}, {:.4f})".format(alpha, beta))

backend = FakeJakartaV2()
durations = DynamicCircuitInstructionDurations.from_backend(backend)

dd_sequence = [XGate(), XGate()]

pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
pm.scheduling = PassManager(
    [
        ALAPScheduleAnalysis(durations),
        PadDynamicalDecoupling(durations, dd_sequence),
    ]
)

scheduled_teleport = pm.run(circuit)
#scheduled_teleport.draw(output="mpl", style="iqp")

nshots = 10000
job = backend.run(scheduled_teleport, shots=nshots)
# #job = device.run(circuit, nshots)
# print(job.job_id())

result = job.result()
counts = result.get_counts(scheduled_teleport)
#print(counts)
counts_m = marginal_counts(counts, [2])
number_of_0s = counts_m.get('0')
number_of_1s = counts_m.get('1')
alpha = np.sqrt(number_of_0s/nshots)
beta = np.sqrt(number_of_1s/nshots)
print("Result :|\u03C8\u27E9 ({:.4f}, {:.4f})".format(alpha, beta))