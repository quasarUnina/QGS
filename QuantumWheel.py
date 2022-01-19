from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ, BasicAer
from qiskit.circuit.library import MCPhaseGate
import math, random
from qiskit.test.mock import FakeMelbourne
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_bloch_multivector


def QuantumWheel(n, n2f, beta, iterations,provider, backend_name, shots, draw_circuit=False):
    reg = QuantumRegister(n, name='reg')
    scratch = QuantumRegister(n-3, name='scratch')
    c_reg = ClassicalRegister(n, name='output')
    qc = QuantumCircuit(reg, scratch, c_reg)
    qc.h(reg)

    for i in range(iterations):
        ## Flip the marked value
        qc.x(scratch)
        qc.barrier()
        k = 0
        for number_to_flip in n2f:
            x_bits = ~number_to_flip
            x_list = [reg[x] for x in range(len(reg)) if x_bits & (1 << x)]
            if x_list:
                qc.x(x_list)
            customize_phase_flip(qc, math.pi-k*beta, [x for x in reg], scratch[0])
            if x_list:
                qc.x(x_list)
            k = k+1
        qc.x(scratch)
        qc.barrier()
        Grover(qc, reg, scratch)
    qc.measure(reg, c_reg)
    if backend_name == 'fake':
        device_backend = FakeMelbourne()
        backend = QasmSimulator.from_backend(device_backend)
    else:
        backend = provider.get_backend(backend_name)
    job = execute(qc, backend, shots=shots, seed_simulator=random.randint(1,150))
    result = job.result()

    if draw_circuit:
        qc.draw(output='mpl').show()

    return result.get_counts(qc)




###############################################
## Some utility functions

def Grover(qc, qreg, scratch, condition_qubits=None):
    if condition_qubits is None:
        condition_qubits = []
    qc.h(qreg)
    qc.x(qreg)
    qubits = [x for x in qreg] + condition_qubits
    multi_cz(qc=qc, qubits=qubits, scratch=scratch)
    qc.x(qreg)
    qc.h(qreg)

def multi_cx(qc, qubits, scratch, do_cz=False):
    ## This will perform a CCCCCX with as many conditions as we want,
    ## as long as we have enough scratch qubits
    ## The last qubit in the list is the target.
    target = qubits[-1]
    conds = qubits[:-1]
    #print(conds)
    #print(target, conds)
    scratch_index = 0
    ops = []
    while len(conds) > 2:
        new_conds = []
        for i in range(len(conds)//2):
            #print(i, len(conds)//2 )
            ops.append((conds[i * 2], conds[i * 2 + 1], scratch[scratch_index]))
            new_conds.append(scratch[scratch_index])
            scratch_index += 1
        if len(conds) & 1:
            new_conds.append(conds[-1])
        conds = new_conds
    for op in ops:
        qc.ccx(op[0], op[1], op[2])
    if do_cz:
        qc.h(target)
    if len(conds) == 0:
        qc.x(target)
    elif len(conds) == 1:
        qc.cx(conds[0], target)
    else:
        qc.ccx(conds[0], conds[1], target)

    if do_cz:
        qc.h(target)
    ops.reverse()
    for op in ops:
        qc.ccx(op[0], op[1], op[2])

def customize_phase_flip(qc, angle, reg, scratch):
    qc.mcp(angle, reg, scratch)




def multi_cz(qc, qubits, scratch):
    ## This will perform a CCCCCZ on as many qubits as we want,
    ## as long as we have enough scratch qubits
    multi_cx(qc, qubits, scratch, do_cz=True)
