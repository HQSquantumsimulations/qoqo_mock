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
//! Testing the roqoqo-mock Backend

use num_complex::Complex64;
use roqoqo::prelude::*;
use roqoqo::{operations::*, Circuit};
use roqoqo_mock::Backend;
use roqoqo_test::prepare_monte_carlo_gate_test;
use std::collections::HashMap;

/// Test simple circuit with a Definition, a GateOperation and a PragmaRepeatedOperation
#[test]
fn run_simple_circuit_measure_qubit() {
    let backend = Backend::new(2_usize);
    let mut circuit = Circuit::new();
    circuit += DefinitionBit::new("ro".to_string(), 1, true);
    circuit += PauliX::new(0);
    circuit += MeasureQubit::new(0, "ro".to_string(), 0);
    let (bit_registers, _float_registers, _complex_registers) =
        backend.run_circuit_iterator(circuit.iter()).unwrap();
    assert!(bit_registers.contains_key("ro"));
    let out_reg = bit_registers.get("ro").unwrap();
    assert_eq!(out_reg.len(), 1);
    for reg in out_reg.iter() {
        assert_eq!(reg.len(), 1);
    }
}

/// Test simple circuit with a Definition, a GateOperation and a PragmaRepeatedOperation
#[test]
fn run_simple_circuit_repeated_meas() {
    let backend = Backend::new(2_usize);
    let mut circuit = Circuit::new();
    circuit += DefinitionBit::new("ro".to_string(), 2, true);
    circuit += RotateX::new(0, std::f64::consts::FRAC_PI_2.into());
    circuit += PauliX::new(1);
    circuit += PragmaRepeatedMeasurement::new("ro".to_string(), 20, None);
    let (bit_registers, _float_registers, _complex_registers) =
        backend.run_circuit(&circuit).unwrap();
    assert!(bit_registers.contains_key("ro"));
    let out_reg = bit_registers.get("ro").unwrap();
    assert_eq!(out_reg.len(), 20);
    for reg in out_reg.iter() {
        assert_eq!(reg.len(), 2);
    }
}

/// Test simple circuit with a Definition, a GateOperation and a PragmaRepeatedOperation
#[test]
fn run_simple_circuit_get_pauli_product() {
    let backend = Backend::new(2_usize);
    let mut circuit = Circuit::new();
    circuit += DefinitionFloat::new("ro".to_string(), 2, true);
    circuit += RotateX::new(0, std::f64::consts::FRAC_PI_2.into());
    circuit += PauliX::new(1);
    circuit += PragmaGetPauliProduct::new(HashMap::new(), "ro".to_string(), Circuit::new());
    let (_bit_registers, float_registers, _complex_registers) =
        backend.run_circuit(&circuit).unwrap();
    assert!(float_registers.contains_key("ro"));
    let out_reg = float_registers.get("ro").unwrap();
    assert_eq!(out_reg.len(), 1);
    for reg in out_reg.iter() {
        assert_eq!(reg.len(), 1);
        for val in reg {
            assert!(val.abs() < 1.0);
        }
    }
}

/// Test simple circuit with a Definition, a GateOperation and a PragmaRepeatedOperation
#[test]
fn run_simple_circuit_get_occupation_proba() {
    let backend = Backend::new(2_usize);
    let mut circuit = Circuit::new();
    circuit += DefinitionFloat::new("ro".to_string(), 2, true);
    circuit += RotateX::new(0, std::f64::consts::FRAC_PI_2.into());
    circuit += PauliX::new(1);
    circuit += PragmaGetOccupationProbability::new("ro".to_string(), None);
    let (_bit_registers, float_registers, _complex_registers) =
        backend.run_circuit(&circuit).unwrap();
    assert!(float_registers.contains_key("ro"));
    let out_reg = float_registers.get("ro").unwrap();
    assert_eq!(out_reg.len(), 1);
    for reg in out_reg.iter() {
        assert_eq!(reg.len(), 2);
        for val in reg {
            assert!(val.abs() < 1.0);
        }
    }
}

/// Test simple circuit with a Definition, a GateOperation and a PragmaRepeatedOperation
#[test]
fn run_simple_circuit_get_statevec() {
    let backend = Backend::new(2_usize);
    let mut circuit = Circuit::new();
    circuit += DefinitionComplex::new("ro".to_string(), 2, true);
    circuit += RotateX::new(0, std::f64::consts::FRAC_PI_2.into());
    circuit += PauliX::new(1);
    circuit += PragmaGetStateVector::new("ro".to_string(), None);
    let (_bit_registers, _float_registers, complex_registers) =
        backend.run_circuit(&circuit).unwrap();
    assert!(complex_registers.contains_key("ro"));
    let out_reg = complex_registers.get("ro").unwrap();
    assert_eq!(out_reg.len(), 1);
    for reg in out_reg.iter() {
        assert_eq!(reg.len(), 4);
        for val in reg.iter() {
            assert!(val.re.abs() < 1.0);
            assert!(val.im.abs() < 1.0);
        }
    }
}

/// Test simple circuit with a Definition, a GateOperation and a PragmaRepeatedOperation
#[test]
fn run_simple_circuit_get_densmat() {
    let backend = Backend::new(2_usize);
    let mut circuit = Circuit::new();
    circuit += DefinitionComplex::new("ro".to_string(), 2, true);
    circuit += RotateX::new(0, std::f64::consts::FRAC_PI_2.into());
    circuit += PauliX::new(1);
    circuit += PragmaGetDensityMatrix::new("ro".to_string(), None);
    let (_bit_registers, _float_registers, complex_registers) =
        backend.run_circuit(&circuit).unwrap();
    assert!(complex_registers.contains_key("ro"));
    let out_reg = complex_registers.get("ro").unwrap();
    assert_eq!(out_reg.len(), 4);
    let zero = Complex64::new(0.0, 0.0);
    let one = Complex64::new(1.0, 0.0);
    for reg in out_reg.iter() {
        assert_eq!(reg.len(), 4);
        for val in reg.iter() {
            assert!(*val == zero || *val == one)
        }
    }
}

/// Simply test measurement process, not that gate is translated correctly
#[test]
fn test_measurement() {
    let gate: GateOperation = PauliZ::new(0).into();
    let preparation_gates: Vec<SingleQubitGateOperation> = vec![PauliX::new(0).into()];
    let basis_rotation_gates: Vec<SingleQubitGateOperation> = vec![PauliY::new(0).into()];
    let (measurement, exp_vals) =
        prepare_monte_carlo_gate_test(gate, preparation_gates, basis_rotation_gates, None, 1, 200);
    let backend = Backend::new(1);
    let measured_exp_vals = backend.run_measurement(&measurement).unwrap().unwrap();
    for (key, val) in exp_vals.iter() {
        assert!((val - measured_exp_vals.get(key).unwrap()).abs() <= 2.0);
    }
}

/// Test full gate with stochastic application of gates
#[test]
fn test_full_simple_gate() {
    let gate: GateOperation = PauliX::new(0).into();
    let preparation_gates: Vec<SingleQubitGateOperation> = vec![
        PauliX::new(0).into(),
        PauliY::new(0).into(),
        PauliZ::new(0).into(),
    ];
    let basis_rotation_gates: Vec<SingleQubitGateOperation> = vec![
        PauliX::new(0).into(),
        RotateX::new(0, std::f64::consts::FRAC_PI_2.into()).into(),
        RotateZ::new(0, std::f64::consts::FRAC_PI_2.into()).into(),
    ];
    let (measurement, exp_vals) =
        prepare_monte_carlo_gate_test(gate, preparation_gates, basis_rotation_gates, None, 5, 200);

    let backend = Backend::new(1);
    let measured_exp_vals = backend.run_measurement(&measurement).unwrap().unwrap();
    for (key, val) in exp_vals.iter() {
        assert!((val - measured_exp_vals.get(key).unwrap()).abs() <= 2.0);
    }
}

/// Test Debug, Clone and PartialEq for Backend
#[test]
fn test_debug_clone_partialeq() {
    let backend = Backend::new(0_usize);

    // Test Debug trait
    assert_eq!(format!("{:?}", backend), "Backend { number_qubits: 0 }");

    // Test Clone trait
    assert_eq!(backend.clone(), backend);

    // PartialEq
    let backend_0 = Backend::new(0_usize);
    let backend_2 = Backend::new(2_usize);

    assert!(backend_0 == backend);
    assert!(backend == backend_0);
    assert!(backend_2 != backend);
    assert!(backend != backend_2);
}
