"""Test qoqo mocked backend"""
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
from qoqo_mock import (
    MockedBackend
)
from hqsbase.qonfig import Qonfig


@pytest.mark.parametrize(
    'measurement',
    [(ops.MeasureQubit(qubit=0, readout='ro', readout_index=0), int),
     (ops.PragmaRepeatedMeasurement(readout='ro', number_measurements=10), np.ndarray),
     (ops.PragmaGetPauliProduct(pauli_product=[1, 2], readout='ro'), np.ndarray),
     (ops.PragmaGetOccupationProbability(readout='ro'), np.float64),
     (ops.PragmaGetRotatedOccupationProbability(readout='ro'), np.float64),
     (ops.PragmaPauliProdMeasurement(readout='ro'), float)])
def test_mocked_backend(measurement):
    """Test mocked backend"""
    circuit = Circuit()
    circuit += ops.Definition(name='ro', vartype='float', length=1, is_output=True)
    circuit += ops.PauliX(qubit=0)
    circuit += measurement[0]

    mocked = MockedBackend(circuit=circuit,
                           number_qubits=2,
                           number_measurements=1,
                           device=None,
                           mocked_qubits=None)

    results = mocked.run()['ro'].register[0]
    assert isinstance(results[0], measurement[1])

    config = mocked.to_qonfig()
    json = config.to_json()
    config2 = Qonfig.from_json(json)
    mocked2 = config2.to_instance()


if __name__ == '__main__':
    pytest.main(sys.argv)
