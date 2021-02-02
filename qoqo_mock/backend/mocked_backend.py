"""Mocked Backend"""
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
from qoqo.registers import (
    RegisterOutput,
    BitRegister,
    FloatRegister,
    ComplexRegister,
    add_register
)
from qoqo.backends import BackendBaseClass
from qoqo import operations as ops
from qoqo import Circuit
from typing import (
    Union,
    Optional,
    Dict,
    cast
)
from qoqo.devices import DeviceBaseClass
from hqsbase.calculator import (
    CalculatorFloat
)
from hqsbase.qonfig import Qonfig
from hqsbase.calculator import Calculator
from qoqo_mock import mocked_call_circuit


class MockedBackend(BackendBaseClass):
    r"""Mocked backend to qoqo

    The mocked backend mock-simulates a quantum circuit on a given device by translating the qoqo
    circuit using the qoqo_mocked interface. This interface produces random measurements coherent
    with the measured quantity. These results are then output from the run function in this backend
    and are accessible through the classical registers dictionary.
    """

    _qonfig_defaults_dict = {
        'circuit': {'doc': 'The circuit that is run',
                    'default': None},
        'number_qubits': {'doc': 'The number of qubits to use',
                          'default': 1},
        'substitution_dict': {'doc': 'Substitution dictionary used to replace symbolic parameters',
                              'default': None},
        'number_measurements': {'doc': 'The number of measurement repetitions',
                                'default': 1},
        'device': {'doc': 'The device specification',
                   'default': None},
        'mocked_qubits': {'doc': 'Number of qubits mocked in quest',
                          'default': None},
    }

    def __init__(self,
                 circuit: Optional[Circuit] = None,
                 number_qubits: int = 1,
                 substitution_dict: Optional[Dict[str, float]] = None,
                 number_measurements: int = 1,
                 device: Optional[DeviceBaseClass] = None,
                 mocked_qubits: Optional[int] = None,
                 **kwargs) -> None:
        """Initialize backend

        Args:
            circuit: The circuit that is run on the backend
            number_qubits: The number of qubits to use
            substitution_dict: The substitution dictionary used to replace symbolic parameters
            number_measurements: The number of measurement repetitions
            device: The device specification
            mocked_qubits: Number of qubits mocked in quest
            **kwargs: Additional keyword arguments
        """
        self.name = "mocked"
        self.number_qubits = number_qubits
        self.substitution_dict: Optional[Dict[str, float]] = substitution_dict
        self.number_measurements = number_measurements
        self.device = device
        self.mocked_qubits = mocked_qubits
        self.kwargs = kwargs
        self.qubit_names = getattr(self.device, '_qubit_names', None)
        super().__init__(circuit=circuit,
                         device=self.device,
                         number_qubits=number_qubits,
                         **kwargs)

    @classmethod
    def from_qonfig(cls,
                    config: Qonfig['MockedBackend']
                    ) -> 'MockedBackend':
        """Create Instance from Qonfig

        Args:
            config: Qonfig of class

        Returns:
            MockedBackend
        """
        if isinstance(config['device'], Qonfig):
            init_device = config['device'].to_instance()
        else:
            init_device = cast(Optional[DeviceBaseClass], config['device'])
        if isinstance(config['circuit'], Qonfig):
            init_circuit = config['circuit'].to_instance()
        else:
            init_circuit = cast(Optional[Circuit], config['circuit'])
        return cls(circuit=init_circuit,
                   number_qubits=config['number_qubits'],
                   substitution_dict=config['substitution_dict'],
                   number_measurements=config['number_measurements'],
                   device=init_device,
                   mocked_qubits=config['mocked_qubits'],
                   )

    def to_qonfig(self) -> 'Qonfig[MockedBackend]':
        """Create Qonfig from Instance

        Returns:
            Qonfig[MockedBackend]
        """
        config = Qonfig(self.__class__)
        if self._circuit is not None:
            config['circuit'] = self._circuit.to_qonfig()
        else:
            config['circuit'] = self._circuit
        config['number_qubits'] = self.number_qubits
        config['substitution_dict'] = self.substitution_dict
        config['number_measurements'] = self.number_measurements
        if self.device is not None:
            config['device'] = self.device.to_qonfig()
        else:
            config['device'] = self.device
        config['mocked_qubits'] = self.mocked_qubits

        return config

    def run(self, **kwargs) -> Union[None, Dict[str, 'RegisterOutput']]:
        """Run Backend

        Args:
            **kwargs: Additional keyword arguments

        Returns:
            Union[None, Dict[str, 'RegisterOutput']]
        """
        # Initializing the classical registers for calculation and output
        internal_register_dict: Dict[str, Union[BitRegister,
                                                FloatRegister, ComplexRegister]] = dict()
        output_register_dict: Dict[str, RegisterOutput] = dict()
        for definition in self.circuit._definitions:
            add_register(internal_register_dict, output_register_dict, definition)

        if self.substitution_dict is None:
            calculator = None
        else:
            calculator = Calculator()
            self.substitution_dict = cast(Dict[str, float], self.substitution_dict)
            for name, val in self.substitution_dict.items():
                calculator.set(name, val)

        global_phase = 0
        for op in self.circuit:
            op = cast(ops.Operation, op)
            if 'PragmaGlobalPhase' in op._operation_tags:
                op = cast(ops.PragmaGlobalPhase, op)
                if calculator is not None:
                    global_phase += CalculatorFloat(calculator.parse_get(op.phase.value))
                else:
                    op = global_phase + CalculatorFloat(op.phase).value

        mocked_call_circuit(
            circuit=self.circuit,
            classical_registers=internal_register_dict,
            mocked_qubits=self.mocked_qubits,
            calculator=calculator,
            **kwargs)

        for name, reg in internal_register_dict.items():
            if reg.is_output:
                # Extending output register when register is repeated measurement bit register
                if (internal_register_dict[name].vartype == 'bit'
                        and hasattr(reg.register[0], '__iter__')):
                    output_register_dict[name].extend(reg)
                else:
                    output_register_dict[name].append(reg)

        # Overwriting global phase
        if 'global_phase' in output_register_dict.keys() and global_phase != 0:
            output_register_dict['global_phase'].register = [[global_phase]]

        return output_register_dict
