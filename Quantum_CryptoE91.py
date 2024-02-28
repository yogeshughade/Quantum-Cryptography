from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
from qiskit.extensions import UnitaryGate
import numpy as np

def create_bell_pair(circuit, a, b):
    circuit.h(a)
    circuit.cx(a, b)

def alice_prepare_qubits(num_qubits):
    alice_bases = np.random.randint(2, size=num_qubits)
    alice_bits = np.random.randint(2, size=num_qubits)
    
    qubits = QuantumCircuit(num_qubits, num_qubits)
    for i in range(num_qubits):
        if alice_bits[i] == 1:
            qubits.x(i)
        if alice_bases[i] == 1:
            qubits.h(i)
    return qubits, alice_bases

def alice_measure_qubits(qubits, alice_bases):
    num_qubits = len(qubits)
    for i in range(num_qubits):
        if alice_bases[i] == 1:
            qubits.h(i)
    qubits.measure(range(num_qubits), range(num_qubits))
    return qubits

def e91_protocol(num_qubits):
    circuit = QuantumCircuit(num_qubits * 2, num_qubits * 2)
    
    create_bell_pair(circuit, 0, 1)
    create_bell_pair(circuit, 2, 3)
    
    circuit.barrier()
    
    circuit.cx(1, 2)
    circuit.h(0)
    
    circuit.measure([0, 1], [0, 1])
    circuit.measure([2, 3], [2, 3])
    
    return circuit

if __name__ == "__main__":
    num_qubits = 2
    
    alice_qubits, alice_bases = alice_prepare_qubits(num_qubits)
    alice_qubits = alice_measure_qubits(alice_qubits, alice_bases)
    
    e91_circuit = e91_protocol(num_qubits)
    circuit = alice_qubits + e91_circuit
    
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuit, simulator, shots=1)
    result = job.result()
    counts = result.get_counts(circuit)
    
    print("Measurement outcomes:", counts)
    plot_histogram(counts)
