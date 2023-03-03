"""Test qoqo mocked interface"""
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
import pytest
import sys
import numpy as np
from qoqo import operations as ops
from qoqo import Circuit
from typing import Any
from qoqo_mock import mocked_call_circuit


@pytest.mark.parametrize(
    "op",
    [
        ops.Bogoliubov(1, 0, 0.01, 0.02),
        ops.CNOT(1, 0),
        ops.ControlledPauliY(1, 0),
        ops.ControlledPauliZ(1, 0),
        ops.ControlledPhaseShift(1, 0, 0.01),
        ops.FSwap(1, 0),
        ops.Fsim(1, 0, 0.01, 0.02, 0.03),
        ops.Qsim(1, 0, 0.01, 0.02, 0.03),
        ops.GivensRotation(1, 0, 0.01, 0.02),
        ops.GivensRotationLittleEndian(0, 1, 0.01, 0.02),
        ops.ISwap(1, 0),
        ops.InvSqrtISwap(1, 0),
        ops.MolmerSorensenXX(1, 0),
        ops.VariableMSXX(1, 0, 0.01),
        ops.PMInteraction(1, 0, 0.01),
        ops.ComplexPMInteraction(1, 0, 0.01, 0.02),
        ops.SWAP(1, 0),
        ops.SqrtISwap(1, 0),
        ops.XY(1, 0, 0.01),
        ops.SpinInteraction(1, 0, 0.01, 0.02, 0.003),
        ops.SingleQubitGate(0, 0.1, 0.0, 0.0, 0.0, 0.0),
        ops.Hadamard(0),
        ops.PauliX(0),
        ops.PauliY(0),
        ops.PauliZ(0),
        ops.TGate(0),
        ops.SGate(0),
        ops.SqrtPauliX(0),
        ops.InvSqrtPauliX(0),
        ops.RotateX(0, 0.01),
        ops.RotateY(0, 0.01),
        ops.RotateZ(0, 0.01),
        ops.RotateAroundSphericalAxis(0, 0.01, 0.02, 0.03),
        ops.PragmaSetNumberOfMeasurements(20, "ro"),
        ops.PragmaSetStateVector(np.array([0, 1], dtype=complex)),
        ops.PragmaSetDensityMatrix(np.array([[0, 0], [0, 1]], dtype=complex)),
        ops.PragmaDamping(0, 0.005, 0.02),
        ops.PragmaDephasing(0, 0.005, 0.02),
        ops.PragmaDepolarising(0, 0.005, 0.02),
        ops.PragmaRandomNoise(0, 0.005, 0.02, 0.01),
        ops.PragmaGeneralNoise(
            0, 0.005, np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float)
        ),
        ops.PragmaConditional("ro", 0, Circuit()),
        ops.PragmaRepeatGate(3),
        ops.PragmaBoostNoise(0.004),
        ops.PragmaStopParallelBlock([0, 1], 0.002),
        ops.PragmaSleep([0, 1], 0.002),
        ops.PragmaActiveReset(0),
        ops.PragmaGlobalPhase(0.03),
        ops.MeasureQubit(0, "ro", 0),
        ops.PragmaRepeatedMeasurement("ro", 20, {}),
        ops.PragmaGetStateVector("ro", Circuit()),
        ops.PragmaGetDensityMatrix("ro", Circuit()),
        ops.PragmaGetOccupationProbability("ro", Circuit()),
        ops.PragmaGetPauliProduct({}, "ro", Circuit()),
        ops.PragmaStartDecompositionBlock([0, 1], {}),
        ops.PragmaStopDecompositionBlock([0, 1]),
        ops.InputSymbolic("other", 0),
    ],
)
def test_all_operations(op: Any):
    """Test all operations with mocked interface"""
    circuit = Circuit()
    circuit += ops.DefinitionFloat(name="ro", length=1, is_output=False)
    circuit += ops.DefinitionBit(name="ro", length=1, is_output=False)
    circuit += ops.DefinitionComplex(name="ro", length=1, is_output=False)
    circuit += ops.DefinitionUsize(name="ro", length=1, is_output=False)
    circuit += op
    mocked_call_circuit(
        circuit=circuit,
        classical_bit_registers={},
        classical_float_registers={},
        classical_complex_registers={},
        output_bit_register_dict={},
        output_complex_register_dict={},
        number_qubits=1,
    )


if __name__ == "__main__":
    pytest.main(sys.argv)
