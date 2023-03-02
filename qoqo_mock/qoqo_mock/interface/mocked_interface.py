"""Define the mocked interface for qoqo operations."""
# Copyright © 2019-2023 HQS Quantum Simulations GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.

from qoqo import operations as ops
from qoqo import Circuit
from typing import cast, Dict, List, Any, Tuple
import numpy as np

_ALLOWED_PRAGMAS = [
    "PragmaSetNumberOfMeasurements",
    "PragmaSetStateVector",
    "PragmaSetDensityMatrix",
    "PragmaNoise",
    "PragmaDamping",
    "PragmaDepolarising",
    "PragmaDephasing",
    "PragmaRandomNoise",
    "PragmaGeneralNoise",
    "PragmaRepeatGate",
    "PragmaBoostNoise",
    "PragmaStopParallelBlock",
    "PragmaSleep",
    "PragmaGlobalPhase",
    "PragmaActiveReset",
    "InputSymbolic",
    "PragmaStartDecompositionBlock",
    "PragmaStopDecompositionBlock",
    "PragmaConditional",
]


def mocked_call_circuit(
    circuit: Circuit,
    classical_bit_registers: Dict[str, List[bool]],
    classical_float_registers: Dict[str, List[float]],
    classical_complex_registers: Dict[str, List[complex]],
    output_bit_register_dict: Dict[str, List[List[bool]]],
    output_complex_register_dict: Dict[str, List[List[complex]]],
    number_qubits: int = 1,
    **kwargs
) -> Tuple[
    Dict[str, List[bool]],
    Dict[str, List[float]],
    Dict[str, List[complex]],
    Dict[str, List[List[bool]]],
    Dict[str, List[List[complex]]],
]:
    """Execute mocked qoqo circuit.

    The Mocked interface is an interface which mock-simulates a quantum circuit. The quantum
    gates are not applied and the measurements produce random results coherent with the
    measured quantity.

    Args:
        circuit: The qoqo circuit that is executed
        classical_bit_registers: Dictionary or registers (lists) containing bit readout values
        classical_float_registers: Dictionary or registers (lists)
                                   containing float readout values
        classical_complex_registers: Dictionary or registers (lists)
                                     containing complex readout values
        output_bit_register_dict: Dictionary or lists of registers (lists)
                              containing a register for each repetition of the circuit
        output_complex_register_dict: Dictionary or lists of registers (lists)
                              containing a register for each repetition of the circuit
        number_qubits: Number of qubits mocked
        **kwargs: Additional keyword arguments

    Returns:
        Tuple[
            Dict[str, List[bool]],
            Dict[str, List[float]],
            Dict[str, List[complex]],
            Dict[str, List[List[bool]]],
            Dict[str, List[List[complex]]]]: modified registers

    """
    for op in circuit:
        (
            classical_bit_registers,
            classical_float_registers,
            classical_complex_registers,
            output_bit_register_dict,
            output_complex_register_dict,
        ) = mocked_call_operation(
            op,
            classical_bit_registers,
            classical_float_registers,
            classical_complex_registers,
            output_bit_register_dict,
            output_complex_register_dict,
            number_qubits,
            **kwargs
        )

    return (
        classical_bit_registers,
        classical_float_registers,
        classical_complex_registers,
        output_bit_register_dict,
        output_complex_register_dict,
    )


def mocked_call_operation(
    operation: Any,
    classical_bit_registers: Dict[str, List[bool]],
    classical_float_registers: Dict[str, List[float]],
    classical_complex_registers: Dict[str, List[complex]],
    output_bit_register_dict: Dict[str, List[List[bool]]],
    output_complex_register_dict: Dict[str, List[List[complex]]],
    number_qubits: int = 1,
    **kwargs
) -> Tuple[
    Dict[str, List[bool]],
    Dict[str, List[float]],
    Dict[str, List[complex]],
    Dict[str, List[List[bool]]],
    Dict[str, List[List[complex]]],
]:
    """Execute mocked qoqo operation.

    Args:
        operation: The qoqo operation that is executed
        classical_bit_registers: Dictionary or registers (lists) containing bit readout values
        classical_float_registers: Dictionary or registers (lists)
                                   containing float readout values
        classical_complex_registers: Dictionary or registers (lists)
                                     containing complex readout values
        output_bit_register_dict: Dictionary or lists of registers (lists)
                              containing a register for each repetition of the circuit
        output_complex_register_dict: Dictionary or lists of registers (lists)
                              containing a register for each repetition of the circuit
        number_qubits: Number of qubits mocked
        **kwargs: Additional keyword arguments

    Returns:
        stuff

    Raises:
        RuntimeError: Operation cannot be mocked

    """
    tags = operation.tags()
    if "GateOperation" in tags:
        pass
    elif "DefinitionFloat" in tags:
        pass
    elif "DefinitionComplex" in tags:
        pass
    elif "DefinitionBit" in tags:
        pass
    elif "DefinitionUsize" in tags:
        pass
    elif "MeasureQubit" in tags:
        operation = cast(ops.MeasureQubit, operation)
        res = np.random.randint(0, 1)
        if operation.readout() not in classical_bit_registers.keys():
            classical_bit_registers[operation.readout()] = [
                False for _ in range(number_qubits)
            ]
        else:
            index = cast(int, operation.readout_index())
            classical_bit_registers[operation.readout()][index] = res  # type: ignore
    elif "PragmaRepeatedMeasurement" in tags:
        operation = cast(ops.PragmaRepeatedMeasurement, operation)
        output_bit_register_dict[operation.readout()] = np.random.randint(
            0, 2, size=(operation.number_measurements(), number_qubits)
        ).tolist()
        if operation.readout() in classical_bit_registers.keys():
            del classical_bit_registers[operation.readout()]
    elif "PragmaGetPauliProduct" in tags:
        operation = cast(ops.PragmaGetPauliProduct, operation)
        classical_float_registers[operation.readout()] = [
            np.random.random(1).tolist(),
        ]
    elif "PragmaGetOccupationProbability" in tags:
        operation = cast(ops.PragmaGetOccupationProbability, operation)
        classical_float_registers[operation.readout()] = np.random.random(
            number_qubits
        ).tolist()
    elif "PragmaGetStateVector" in tags:
        operation = cast(ops.PragmaGetStateVector, operation)
        values = np.random.default_rng().uniform(0, 1, (2**number_qubits, 2))
        values_complex = values[..., 0] + 1j * values[..., 1]
        normalisation = 0
        for value in values_complex:
            normalisation += abs(value) ** 2
        values_normalised = values_complex / normalisation
        classical_complex_registers[operation.readout()] = values_normalised.tolist()
    elif "PragmaGetDensityMatrix" in tags:
        operation = cast(ops.PragmaGetDensityMatrix, operation)
        qubits = np.random.randint(0, 2, size=number_qubits)
        statevector = np.array([1])
        for qubit in qubits:
            if qubit == 0:
                statevector = np.kron(np.array([1, 0]), statevector)
            else:
                statevector = np.kron(np.array([0, 1]), statevector)
        output_complex_register_dict[operation.readout()] = np.kron(
            statevector[..., None], statevector
        ).tolist()
    elif any(pragma in tags for pragma in _ALLOWED_PRAGMAS):
        pass
    else:
        raise RuntimeError("Operation cannot be mocked")

    return (
        classical_bit_registers,
        classical_float_registers,
        classical_complex_registers,
        output_bit_register_dict,
        output_complex_register_dict,
    )
