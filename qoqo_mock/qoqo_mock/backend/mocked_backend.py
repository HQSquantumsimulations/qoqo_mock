"""Mocked Backend."""
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
from qoqo import Circuit
from typing import Tuple, List, Dict, Any, Optional, cast
from qoqo_mock import mocked_call_circuit


class MockedBackend(object):
    r"""Mocked backend to qoqo.

    The mocked backend mock-simulates a quantum circuit on a given device by translating the qoqo
    circuit using the qoqo_mocked interface. This interface produces random measurements coherent
    with the measured quantity. These results are then output from the run function in this backend
    and are accessible through the classical registers dictionary.
    """

    def __init__(self, number_qubits: int = 1) -> None:
        """Initialize backend.

        Args:
            number_qubits: The number of qubits to use

        """
        self.name = "mocked"
        self.number_qubits = number_qubits

    def run_circuit(
        self, circuit: Circuit
    ) -> Tuple[
        Dict[str, List[List[bool]]],
        Dict[str, List[List[float]]],
        Dict[str, List[List[complex]]],
    ]:
        """Run a circuit with the Mocked backend.

        Args:
            circuit: The circuit that is run

        Returns:
            Union[None, Dict[str, 'RegisterOutput']]

        """
        # Initializing the classical registers for calculation and output
        internal_bit_register_dict: Dict[str, List[bool]] = dict()
        internal_float_register_dict: Dict[str, List[float]] = dict()
        internal_complex_register_dict: Dict[str, List[complex]] = dict()

        output_bit_register_dict: Dict[str, List[List[bool]]] = dict()
        output_float_register_dict: Dict[str, List[List[float]]] = dict()
        output_complex_register_dict: Dict[str, List[List[complex]]] = dict()

        for bit_def in circuit.filter_by_tag("DefinitionBit"):
            internal_bit_register_dict[bit_def.name()] = [
                False for _ in range(bit_def.length())
            ]
            if bit_def.is_output():
                output_bit_register_dict[bit_def.name()] = list()

        for float_def in circuit.filter_by_tag("DefinitionFloat"):
            internal_float_register_dict[float_def.name()] = [
                0.0 for _ in range(float_def.length())
            ]
            if float_def.is_output():
                output_float_register_dict[float_def.name()] = cast(
                    List[List[float]], list()
                )

        for complex_def in circuit.filter_by_tag("DefinitionComplex"):
            internal_complex_register_dict[complex_def.name()] = [
                complex(0.0) for _ in range(complex_def.length())
            ]
            if complex_def.is_output():
                output_complex_register_dict[complex_def.name()] = cast(
                    List[List[complex]], list()
                )

        (
            internal_bit_register_dict,
            internal_float_register_dict,
            internal_complex_register_dict,
            output_bit_register_dict,
            output_complex_register_dict,
        ) = mocked_call_circuit(
            circuit=circuit,
            classical_bit_registers=internal_bit_register_dict,
            classical_float_registers=internal_float_register_dict,
            classical_complex_registers=internal_complex_register_dict,
            output_bit_register_dict=output_bit_register_dict,
            output_complex_register_dict=output_complex_register_dict,
            number_qubits=self.number_qubits,
        )

        for name, reg in output_bit_register_dict.items():
            if name in internal_bit_register_dict.keys():
                reg.append(internal_bit_register_dict[name])

        for name, reg in output_float_register_dict.items():  # type: ignore
            if name in internal_float_register_dict.keys():
                reg.append(internal_float_register_dict[name])  # type: ignore

        for name, reg in output_complex_register_dict.items():  # type: ignore
            if name in internal_complex_register_dict.keys():
                reg.append(internal_complex_register_dict[name])  # type: ignore

        return (
            output_bit_register_dict,
            output_float_register_dict,
            output_complex_register_dict,
        )

    def run_measurement_registers(
        self, measurement: Any
    ) -> Tuple[
        Dict[str, List[List[bool]]],
        Dict[str, List[List[float]]],
        Dict[str, List[List[complex]]],
    ]:
        """Run all circuits of a measurement with the Mocked backend.

        Args:
            measurement: The measurement that is run

        Returns:
            Union[None, Dict[str, 'RegisterOutput']]

        """
        # Initializing the classical registers for calculation and output

        constant_circuit = measurement.constant_circuit()
        output_bit_register_dict: Dict[str, List[List[bool]]] = dict()
        output_float_register_dict: Dict[str, List[List[float]]] = dict()
        output_complex_register_dict: Dict[str, List[List[complex]]] = dict()
        for circuit in measurement.circuits():
            if constant_circuit is None:
                run_circuit = circuit
            else:
                run_circuit = constant_circuit + circuit

            (
                tmp_bit_register_dict,
                tmp_float_register_dict,
                tmp_complex_register_dict,
            ) = self.run_circuit(run_circuit)
            output_bit_register_dict.update(tmp_bit_register_dict)
            output_float_register_dict.update(tmp_float_register_dict)
            output_complex_register_dict.update(tmp_complex_register_dict)
        return (
            output_bit_register_dict,
            output_float_register_dict,
            output_complex_register_dict,
        )

    def run_measurement(self, measurement: Any) -> Optional[Dict[str, float]]:
        """Run a circuit with the Mocked backend.

        Args:
            measurement: The measurement that is run

        Returns:
            Union[None, Dict[str, 'RegisterOutput']]

        """
        # Initializing the classical registers for calculation and output

        (
            output_bit_register_dict,
            output_float_register_dict,
            output_complex_register_dict,
        ) = self.run_measurement_registers(measurement)
        return measurement.evaluate(
            output_bit_register_dict,
            output_float_register_dict,
            output_complex_register_dict,
        )
