// Copyright © 2021 HQS Quantum Simulations GmbH. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
// in compliance with the License. You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software distributed under the
// License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
// express or implied. See the License for the specific language governing permissions and
// limitations under the License.

use crate::call_operation;
use roqoqo::backends::EvaluatingBackend;
use roqoqo::operations::*;
use roqoqo::registers::{
    BitOutputRegister, BitRegister, ComplexOutputRegister, ComplexRegister, FloatOutputRegister,
    FloatRegister,
};
use roqoqo::RoqoqoBackendError;
use std::collections::HashMap;

/// Mocked backend to qoqo
///
/// Provides functions to run circuits and measurements.
/// The mocked backend mock-simulates a quantum circuit on a given device by translating the roqoqo
/// Circuit using the roqoqo_mocked interface. This interface produces random measurements coherent
/// with the measured quantity. These results are then output from the run function in this backend
/// and are accessible through the classical registers dictionary.
///
/// # Arguments
///
/// * `number_qubits` - Number of qubits in the Backend
///
#[derive(Debug, Clone, PartialEq)]
pub struct Backend {
    number_qubits: usize,
}

impl Backend {
    /// Creates new Mocked backend
    ///
    /// # Arguments
    ///
    /// * `number_qubits` - Number of qubits in the Backend
    ///
    /// # Returns
    ///
    /// * `Backend` - The new instance of Backend with the specified number of qubits
    pub fn new(number_qubits: usize) -> Self {
        Self { number_qubits }
    }
}

/// Trait for Backends that can evaluate measurements to expectation values.
///
/// # Example
/// ```
/// use roqoqo::{Circuit, backends::EvaluatingBackend, operations::*};
/// use roqoqo_mock::Backend;
///
/// let backend = Backend::new(2_usize);
/// let mut circuit = Circuit::new();
/// circuit += DefinitionBit::new("ro".to_string(), 2, true);
/// circuit += RotateX::new(0, std::f64::consts::FRAC_PI_2.into());
/// circuit += PauliX::new(1);
/// circuit += PragmaRepeatedMeasurement::new("ro".to_string(), None, 20);
/// let (bit_registers, _float_registers, _complex_registers) =
///     backend.run_circuit(&circuit).unwrap();
/// assert!(bit_registers.contains_key("ro"));
/// let out_reg = bit_registers.get("ro").unwrap();
/// assert_eq!(out_reg.len(), 20);
/// for reg in out_reg.iter() {
///     assert_eq!(reg.len(), 2);
/// }
/// ```
///
impl EvaluatingBackend for Backend {
    /// Runs a circuit with the backend.
    ///
    /// A circuit is passed to the roqoqo-mock backend and executed.
    /// During execution values are written to and read from classical registers
    /// ([crate::registers::BitRegister], [crate::registers::FloatRegister] and [crate::registers::ComplexRegister]).
    /// To produce sufficient statistics for evaluating expectationg values,
    /// circuits have to be run multiple times.
    /// The results of each repetition are concatenated in OutputRegisters
    /// ([crate::registers::BitOutputRegister], [crate::registers::FloatOutputRegister] and [crate::registers::ComplexOutputRegister]).  
    ///
    /// # Arguments
    ///
    /// * `circuit` - The circuit that is run on the backend.
    ///
    /// # Returns
    ///
    /// `RegisterResult` - The output registers written by the evaluated circuits.
    fn run_circuit_iterator<'a>(
        &self,
        circuit: impl Iterator<Item = &'a Operation>,
    ) -> Result<
        (
            HashMap<String, BitOutputRegister>,
            HashMap<String, FloatOutputRegister>,
            HashMap<String, ComplexOutputRegister>,
        ),
        RoqoqoBackendError,
    > {
        let mut internal_bit_registers: HashMap<String, BitRegister> = HashMap::new();
        let mut internal_float_registers: HashMap<String, FloatRegister> = HashMap::new();
        let mut internal_complex_registers: HashMap<String, ComplexRegister> = HashMap::new();
        let mut bit_registers: HashMap<String, BitOutputRegister> = HashMap::new();
        let mut float_registers: HashMap<String, FloatOutputRegister> = HashMap::new();
        let mut complex_registers: HashMap<String, ComplexOutputRegister> = HashMap::new();
        let mut registers = (
            internal_bit_registers.clone(),
            internal_float_registers.clone(),
            internal_complex_registers.clone(),
            bit_registers.clone(),
            complex_registers.clone(),
        );

        for op in circuit {
            match op {
                Operation::DefinitionBit(def) => {
                    internal_bit_registers.insert(def.name().clone(), Vec::new());
                    if *def.is_output() {
                        bit_registers.insert(def.name().clone(), Vec::new());
                    }
                }
                Operation::DefinitionFloat(def) => {
                    internal_float_registers.insert(def.name().clone(), Vec::new());
                    if *def.is_output() {
                        float_registers.insert(def.name().clone(), Vec::new());
                    }
                }
                Operation::DefinitionComplex(def) => {
                    internal_complex_registers.insert(def.name().clone(), Vec::new());
                    if *def.is_output() {
                        complex_registers.insert(def.name().clone(), Vec::new());
                    }
                }
                Operation::MeasureQubit(_op) => {
                    registers = call_operation(
                        op,
                        (
                            internal_bit_registers.clone(),
                            internal_float_registers.clone(),
                            internal_complex_registers.clone(),
                            bit_registers.clone(),
                            complex_registers.clone(),
                        ),
                        self.number_qubits,
                    )
                    .unwrap();
                }
                Operation::PragmaRepeatedMeasurement(_op) => {
                    registers = call_operation(
                        op,
                        (
                            internal_bit_registers.clone(),
                            internal_float_registers.clone(),
                            internal_complex_registers.clone(),
                            bit_registers.clone(),
                            complex_registers.clone(),
                        ),
                        self.number_qubits,
                    )
                    .unwrap();
                }
                Operation::PragmaGetPauliProduct(_op) => {
                    registers = call_operation(
                        op,
                        (
                            internal_bit_registers.clone(),
                            internal_float_registers.clone(),
                            internal_complex_registers.clone(),
                            bit_registers.clone(),
                            complex_registers.clone(),
                        ),
                        self.number_qubits,
                    )
                    .unwrap();
                }
                Operation::PragmaGetOccupationProbability(_op) => {
                    registers = call_operation(
                        op,
                        (
                            internal_bit_registers.clone(),
                            internal_float_registers.clone(),
                            internal_complex_registers.clone(),
                            bit_registers.clone(),
                            complex_registers.clone(),
                        ),
                        self.number_qubits,
                    )
                    .unwrap();
                }
                Operation::PragmaGetStateVector(_op) => {
                    registers = call_operation(
                        op,
                        (
                            internal_bit_registers.clone(),
                            internal_float_registers.clone(),
                            internal_complex_registers.clone(),
                            bit_registers.clone(),
                            complex_registers.clone(),
                        ),
                        self.number_qubits,
                    )
                    .unwrap();
                }
                Operation::PragmaGetDensityMatrix(_op) => {
                    registers = call_operation(
                        op,
                        (
                            internal_bit_registers.clone(),
                            internal_float_registers.clone(),
                            internal_complex_registers.clone(),
                            bit_registers.clone(),
                            complex_registers.clone(),
                        ),
                        self.number_qubits,
                    )
                    .unwrap();
                }
                _ => {}
            }
            internal_bit_registers.extend(registers.clone().0);
            internal_float_registers.extend(registers.clone().1);
            internal_complex_registers.extend(registers.clone().2);
            bit_registers.extend(registers.clone().3);
            complex_registers.extend(registers.clone().4);
        }

        for (key, mut value) in bit_registers.clone() {
            if internal_bit_registers.contains_key(&key) {
                if !internal_bit_registers
                    .get(&key)
                    .unwrap()
                    .to_vec()
                    .is_empty()
                {
                    value.push(internal_bit_registers.get(&key).unwrap().to_vec());
                    bit_registers.insert(key, value);
                }
            }
        }
        for (key, mut value) in float_registers.clone() {
            if internal_float_registers.contains_key(&key) {
                if !internal_float_registers
                    .get(&key)
                    .unwrap()
                    .to_vec()
                    .is_empty()
                {
                    value.push(internal_float_registers.get(&key).unwrap().to_vec());
                    float_registers.insert(key, value);
                }
            }
        }
        for (key, mut value) in complex_registers.clone() {
            if internal_complex_registers.contains_key(&key) {
                if !internal_complex_registers
                    .get(&key)
                    .unwrap()
                    .to_vec()
                    .is_empty()
                {
                    value.push(internal_complex_registers.get(&key).unwrap().to_vec());
                    complex_registers.insert(key, value);
                }
            }
        }

        Ok((bit_registers, float_registers, complex_registers))
    }
}
