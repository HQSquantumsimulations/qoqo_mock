"""Define the mocked interface for qoqo operations."""
# Copyright © 2019-2021 HQS Quantum Simulations GmbH. All Rights Reserved.
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
from typing import (
    Optional,
    Union,
    cast,
    Dict
)
from qoqo.registers import (
    BitRegister,
    FloatRegister,
    ComplexRegister,
)
import numpy as np
from hqsbase.calculator import Calculator, CalculatorFloat

# Create look-up table
_ALLOWED_PRAGMAS = ['PragmaSetNumberOfMeasurements',
                    'PragmaSetStateVector',
                    'PragmaSetDensityMatrix',
                    'PragmaNoise',
                    'PragmaDamping',
                    'PragmaDepolarise',
                    'PragmaDephasing',
                    'PragmaRandomNoise',
                    'PragmaRepeatGate',
                    'PragmaBoostNoise',
                    'PragmaOverrotation',
                    'PragmaStop',
                    'PragmaSleep',
                    'PragmaGlobalPhase',
                    'PragmaParameterSubstitution',
                    'PragmaGetStateVector',
                    'PragmaGetDensityMatrix']


# Defining the actual call

def mocked_call_circuit(
        circuit: Circuit,
        classical_registers: Dict[str, Union[BitRegister,
                                             FloatRegister, ComplexRegister]],
        mocked_qubits: Optional[int] = None,
        calculator: Optional[Calculator] = None,
        **kwargs) -> None:
    """Execute mocked qoqo circuit

    The Mocked interface is an interface which mock-simulates a quantum circuit. The quantum
    gates are not applied and the measurements produce random results coherent with the
    measured quantity.

    Args:
        circuit: The qoqo circuit that is executed
        classical_registers: Classical registers used for input/output
        mocked_qubits: Number of qubits mocked in quest
        calculator: HQSBase Calculator used to replace symbolic parameters
        **kwargs: Additional keyword arguments
    """
    for op in circuit:
        mocked_call_operation(op,
                              classical_registers,
                              mocked_qubits,
                              calculator=calculator,
                              **kwargs)


def mocked_call_operation(
        operation: ops.Operation,
        classical_registers: Dict[str, Union[BitRegister,
                                             FloatRegister, ComplexRegister]],
        mocked_qubits: Optional[int] = None,
        calculator: Optional[Calculator] = None,
        **kwargs) -> None:
    """Execute mocked qoqo operation

    Args:
        operation: The qoqo operation that is executed
        classical_registers: Classical registers used for input/output
        mocked_qubits: Number of qubits mocked in quest
        calculator: HQSBase Calculator used to replace symbolic parameters
        **kwargs: Additional keyword arguments

    Raises:
        OperationNotInBackendError: Operation not in mocked backend
    """
    tags = operation._operation_tags
    if 'GateOperation' in tags:
        _execute_GateOperation(
            operation,
            calculator, **kwargs)
    elif 'Definition' in tags:
        operation = cast(ops.Definition, operation)
        vartype = operation._vartype
        if vartype == 'float':
            classical_registers[operation._name] = FloatRegister(operation)
        elif vartype == 'bit':
            classical_registers[operation._name] = BitRegister(operation)
        elif vartype == 'int':
            classical_registers[operation._name] = FloatRegister(operation)
        elif vartype == 'complex':
            classical_registers[operation._name] = ComplexRegister(operation)
    elif 'MeasureQubit' in tags:
        operation = cast(ops.MeasureQubit, operation)
        res = np.random.randint(0, 1)
        classical_registers[operation._readout].register[operation._readout_index] = res
    elif 'PragmaRepeatedMeasurement' in tags:
        operation = cast(ops.PragmaRepeatedMeasurement, operation)
        mq = 1 if mocked_qubits is None else mocked_qubits
        classical_registers[operation._readout].register = np.random.randint(
            0, 2, size=(operation._number_measurements, mq))
    elif 'PragmaGetPauliProduct' in tags:
        operation = cast(ops.PragmaGetPauliProduct, operation)
        classical_registers[operation._readout].register = [np.random.random(1), ]
    elif 'PragmaGetOccupationProbability' in tags:
        operation = cast(ops.PragmaGetOccupationProbability, operation)
        mq = 1 if mocked_qubits is None else mocked_qubits
        classical_registers[operation._readout].register = np.random.random(mq)
    elif 'PragmaGetRotatedOccupationProbability' in tags:
        operation = cast(ops.PragmaGetRotatedOccupationProbability, operation)
        mq = 1 if mocked_qubits is None else mocked_qubits
        classical_registers[operation._readout].register = np.random.random(mq)
    elif 'PragmaPauliProdMeasurement' in tags:
        operation = cast(ops.PragmaPauliProdMeasurement, operation)
        classical_registers[operation._readout].register[
            operation._readout_index] = np.random.random()
    elif any(pragma in tags for pragma in _ALLOWED_PRAGMAS):
        pass
    else:
        raise ops.OperationNotInBackendError('Operation not in mocked backend')


def _execute_GateOperation(
        operation: ops.Operation,
        calculator: Optional[Calculator] = None,
        **kwargs) -> None:
    operation = cast(ops.GateOperation, operation)
    if operation._parametrized is True and calculator is None:
        raise ops.OperationNotInBackendError(
            'Interactive pyQuEST can not be called with symbolic parameters'
            + ', substitute parameters first')

    parameter_dict: Dict[str, CalculatorFloat] = dict()
    if calculator is not None:
        for key, sarg in operation._ordered_parameter_dict.items():
            parameter_dict[key] = calculator.parse_get(sarg.value)
    else:
        for key, sarg in operation._ordered_parameter_dict.items():
            parameter_dict[key] = CalculatorFloat(sarg).value
