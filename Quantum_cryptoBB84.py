from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import numpy as np

# Alice prepares her qubits
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

# Bob measures the qubits
def bob_measure_qubits(qubits, bob_bases):
    num_qubits = len(qubits)
    for i in range(num_qubits):
        if bob_bases[i] == 1:
            qubits.h(i)
    qubits.measure(range(num_qubits), range(num_qubits))
    return qubits

# Simulate the protocol
def run_bb84(num_qubits):
    # Alice prepares her qubits
    alice_qubits, alice_bases = alice_prepare_qubits(num_qubits)
    
    # Bob chooses his measurement bases
    bob_bases = np.random.randint(2, size=num_qubits)
    
    # Bob measures the qubits
    bob_qubits = bob_measure_qubits(alice_qubits.copy(), bob_bases)
    
    # Execute the circuit on the simulator
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(bob_qubits, simulator, shots=1)
    result = job.result()
    counts = result.get_counts(bob_qubits)
    
    return alice_bases, bob_bases, counts

# Main function
if __name__ == "__main__":
    num_qubits = 10
    alice_bases, bob_bases, counts = run_bb84(num_qubits)
    
    print("Alice's bases:", alice_bases)
    print("Bob's bases:  ", bob_bases)
    print("Measurement outcomes:", counts)
    plot_histogram(counts)
