// Copyright © 2021-2023 HQS Quantum Simulations GmbH. All Rights Reserved.
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
//
//! Testing the roqoqo-mock Interface

use num_complex::Complex64;
use roqoqo::registers::{
    BitOutputRegister, BitRegister, ComplexOutputRegister, ComplexRegister, FloatRegister,
};
use roqoqo::{operations::*, Circuit};
use roqoqo_mock::call_circuit;
use std::collections::HashMap;

/// Test that MeasureQubit returns the correct type of result
#[test]
fn test_measure_qubit() {
    let mut circuit = Circuit::new();
    circuit += DefinitionBit::new("ro".to_string(), 1, true);
    circuit += PauliX::new(0);
    circuit += MeasureQubit::new(0, "ro".to_string(), 1);
    let (bit_registers, _f, _c, _bo, _co) = call_circuit(&circuit, empty_regs(), 2).unwrap();
    assert!(bit_registers.contains_key("ro"));
    let out_reg = bit_registers.get("ro").unwrap();
    assert_eq!(out_reg.len(), 1);
}

/// Test that PragmaRepeatedMeasurement returns the correct type of result
#[test]
fn test_pragma_repeated_measurement() {
    let mut circuit = Circuit::new();
    circuit += DefinitionBit::new("ro".to_string(), 1, true);
    circuit += PauliX::new(0);
    circuit += PragmaRepeatedMeasurement::new("ro".to_string(), 20, Some(HashMap::new()));
    let (_b, _f, _c, output_bit_registers, _co) = call_circuit(&circuit, empty_regs(), 2).unwrap();
    assert!(output_bit_registers.contains_key("ro"));
    let out_reg = output_bit_registers.get("ro").unwrap();
    assert_eq!(out_reg.len(), 20);
    for reg in out_reg.iter() {
        assert_eq!(reg.len(), 2);
    }
}

/// Test that PragmaGetPauliProduct returns the correct type of result
#[test]
fn test_pragma_get_pauli_product() {
    let mut circuit = Circuit::new();
    circuit += DefinitionBit::new("ro".to_string(), 1, true);
    circuit += PauliX::new(0);
    circuit += PragmaGetPauliProduct::new(HashMap::new(), "ro".to_string(), Circuit::new());
    let (_b, float_registers, _c, _bo, _co) = call_circuit(&circuit, empty_regs(), 2).unwrap();
    assert!(float_registers.contains_key("ro"));
    let out_reg = float_registers.get("ro").unwrap();
    assert_eq!(out_reg.len(), 1);
    for reg in out_reg.iter() {
        assert!(reg.abs() < 1.0);
    }
}

/// Test that PragmaGetOccupationProbability returns the correct type of result
#[test]
fn test_pragma_get_occupation_proba() {
    let mut circuit = Circuit::new();
    circuit += DefinitionBit::new("ro".to_string(), 1, true);
    circuit += PauliX::new(0);
    circuit += PragmaGetOccupationProbability::new("ro".to_string(), None);
    let (_b, float_registers, _c, _bo, _co) = call_circuit(&circuit, empty_regs(), 2).unwrap();
    assert!(float_registers.contains_key("ro"));
    let out_reg = float_registers.get("ro").unwrap();
    assert_eq!(out_reg.len(), 2);
    for reg in out_reg.iter() {
        assert!(reg.abs() < 1.0);
    }
}

/// Test that PragmaGetStateVector returns the correct type of result
#[test]
fn test_pragma_get_statevector() {
    let mut circuit = Circuit::new();
    circuit += DefinitionBit::new("ro".to_string(), 1, true);
    circuit += PauliX::new(0);
    circuit += PragmaGetStateVector::new("ro".to_string(), None);
    let (_b, _f, complex_registers, _bo, _co) = call_circuit(&circuit, empty_regs(), 2).unwrap();
    assert!(complex_registers.contains_key("ro"));
    let out_reg = complex_registers.get("ro").unwrap();
    assert_eq!(out_reg.len(), 4);
    for reg in out_reg.iter() {
        assert!(reg.re.abs() < 1.0);
        assert!(reg.im.abs() < 1.0);
    }
}

/// Test that PragmaGetDensityMatrix returns the correct type of result
#[test]
fn test_pragma_get_density_matrix() {
    let zero = Complex64::new(0.0, 0.0);
    let one = Complex64::new(1.0, 0.0);
    let mut circuit = Circuit::new();
    circuit += DefinitionBit::new("ro".to_string(), 1, true);
    circuit += PauliX::new(0);
    circuit += PragmaGetDensityMatrix::new("ro".to_string(), None);
    let (_b, _f, _c, _bo, complex_output_registers) =
        call_circuit(&circuit, empty_regs(), 2).unwrap();
    assert!(complex_output_registers.contains_key("ro"));
    let out_reg = complex_output_registers.get("ro").unwrap();
    assert_eq!(out_reg.len(), 4);
    for reg in out_reg.iter() {
        assert_eq!(reg.len(), 4);
        for val in reg.iter() {
            assert!(*val == zero || *val == one)
        }
    }
}

type BitMap = HashMap<String, BitRegister>;
type FloatMap = HashMap<String, FloatRegister>;
type ComplexMap = HashMap<String, ComplexRegister>;
type BitOutputMap = HashMap<String, BitOutputRegister>;
type ComplexOutputMap = HashMap<String, ComplexOutputRegister>;
/// Helper function for the creation of the empty registers for the call_circuit function
fn empty_regs() -> (BitMap, FloatMap, ComplexMap, BitOutputMap, ComplexOutputMap) {
    let bit_register_dict: HashMap<String, BitRegister> = HashMap::new();
    let float_register_dict: FloatMap = HashMap::new();
    let complex_register_dict: ComplexMap = HashMap::new();
    let output_bit_register_dict: BitOutputMap = HashMap::new();
    let output_complex_register_dict: ComplexOutputMap = HashMap::new();

    (
        bit_register_dict,
        float_register_dict,
        complex_register_dict,
        output_bit_register_dict,
        output_complex_register_dict,
    )
}
