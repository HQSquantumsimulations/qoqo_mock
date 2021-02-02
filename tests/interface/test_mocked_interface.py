"""Test qoqo mocked interface"""
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
import pytest
import sys
import numpy as np
import numpy.testing as npt
from qoqo import operations as ops
from qoqo import Circuit
from qoqo.operations import OperationNotInBackendError
from typing import (
    Dict,
    Optional,
    cast
)
from hqsbase.calculator import Calculator
from copy import copy
from qoqo_mock import (
    mocked_call_circuit,
)


@pytest.mark.parametrize("init", [
    ops.Bogoliubov,
    ops.CNOT,
    ops.ControlledPauliY,
    ops.ControlledPauliZ,
    ops.ControlledPhaseShift,
    ops.FSwap,
    ops.Fsim,
    ops.Qsim,
    ops.GivensRotation,
    ops.GivensRotationLittleEndian,
    ops.ISwap,
    ops.InvSqrtISwap,
    ops.MolmerSorensenXX,
    ops.VariableMSXX,
    ops.PMInteraction,
    ops.ComplexPMInteraction,
    ops.SWAP,
    ops.SqrtISwap,
    ops.XY,
    ops.TwoQubitGateOperation,
    ops.SingleQubitGateOperation,
    ops.SingleQubitGate,
    ops.Hadamard,
    ops.PauliX,
    ops.PauliY,
    ops.PauliZ,
    ops.TGate,
    ops.SGate,
    ops.SqrtPauliX,
    ops.InvSqrtPauliX,
    ops.RotateX,
    ops.RotateY,
    ops.RotateZ,
    ops.RotateAroundSphericalAxis,
    ops.W,
    ops.PragmaSetNumberOfMeasurements,
    ops.PragmaSetStateVector,
    ops.PragmaSetDensityMatrix,
    ops.PragmaNoise,
    ops.PragmaDamping,
    ops.PragmaDephasing,
    ops.PragmaDepolarise,
    ops.PragmaRandomNoise,
    ops.PragmaRepeatGate,
    ops.PragmaBoostNoise,
    ops.PragmaOverrotation,
    ops.PragmaStop,
    ops.PragmaSleep,
    ops.PragmaParameterSubstitution,
    ops.PragmaGlobalPhase,
    ops.MeasureQubit,
    ops.PragmaRepeatedMeasurement,
    ops.PragmaGetStateVector,
    ops.PragmaGetDensityMatrix,
    ops.PragmaGetOccupationProbability,
    ops.PragmaPauliProdMeasurement,
    ops.PragmaGetRotatedOccupationProbability,
    ops.PragmaGetPauliProduct
])
def test_all_operations(init: ops.Operation):
    """Test all operations with mocked interface"""
    op = init
    kwargs = {'theta': -np.pi / 2,
              'spherical_phi': np.pi / 2,
              'spherical_theta': np.pi,
              'alpha_r': 1,
              'alpha_i': 0,
              'beta_r': 1,
              'beta_i': 0,}
    tags = op._operation_tags
    if 'GateOperation' in tags:
        op = cast(ops.GateOperation, op)
        if op.number_of_qubits() == 1:
            operation = op(qubit=0, **kwargs)
        else:
            operation = op(control=1, qubit=0, **kwargs)
    elif 'PragmaSetStateVector' in tags:
        operation = op(statevec=np.array([0, 1]))
    elif 'PragmaSetDensityMatrix' in tags:
        operation = op(density_matrix=np.array([0, 1, 0, 0]))
    elif 'MeasureQubit' in tags:
        operation = op(qubit=0, readout='ro', readout_index=0)
    elif 'PragmaGetPauliProduct' in tags:
        operation = op(pauli_product=np.array([0, 1]))
    else:
        operation = op()

    circuit = Circuit()
    circuit += ops.Definition(name='ro', length=1)
    circuit += operation
    mocked_call_circuit(circuit=circuit, classical_registers={})


if __name__ == '__main__':
    pytest.main(sys.argv)
