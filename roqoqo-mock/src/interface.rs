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
//
//! The roqoqo-mock Interface translates qoqo Operations and applies the corresponding Mocked operation on the Circuit

use num_complex::Complex64;
use rand::Rng;
use roqoqo::operations::*;
use roqoqo::registers::{
    BitOutputRegister, BitRegister, ComplexOutputRegister, ComplexRegister, FloatRegister,
};
use roqoqo::Circuit;
use roqoqo::RoqoqoBackendError;
use std::collections::HashMap;

// Pragma operations that are ignored by backend and do not throw an error
const ALLOWED_OPERATIONS: &'static [&'static str; 14] = &[
    "PragmaSetNumberOfMeasurements",
    "PragmaSetStateVector",
    "PragmaSetDensityMatrix",
    "PragmaNoise",
    "PragmaDamping",
    "PragmaDepolarise",
    "PragmaDephasing",
    "PragmaRandomNoise",
    "PragmaRepeatGate",
    "PragmaBoostNoise",
    "PragmaOverrotation",
    "PragmaStop",
    "PragmaSleep",
    "PragmaGlobalPhase",
];

/// Executes mocked qoqo Circuit.
///
/// The Mocked interface is an interface which mock-simulates a quantum circuit. The quantum
/// gates are not applied and the measurements produce random results coherent with the
/// measured quantity.
///
/// # Arguments
///
/// * `circuit` - The qoqo Circuit that is executed.
/// * `registers` - The five registers used in the Interface:
///                 (1) HashMap containing bit readout values.
///                 (2) HashMap containing float readout values.
///                 (3) HashMap containing complex readout values.
///                 (4) HashMap containing a register for each repetition of the circuit (bit readout values).
///                 (5) HashMap containing a register for each repetition of the circuit (complex readout values).
/// * `number_qubits: Number of qubits mocked.
///
/// # Returns
///
/// * `Ok(HashMap<String, BitRegister>, HashMap<String, FloatRegister>, HashMap<String, ComplexRegister>, HashMap<String, BitOutputRegister>, HashMap<String, ComplexOutputRegister>) - The five input registers with the readouts from the operations in the Circuit.
/// * `Err(RoqoqoBackendError)` - Operation not supported by Mocked backend.
///
/// # Example
/// ```
/// use roqoqo::{Circuit, operations::{DefinitionBit, PauliX, MeasureQubit}};
/// use roqoqo_mock::call_circuit;
/// use std::collections::HashMap;
///
/// let mut circuit = Circuit::new();
/// circuit += DefinitionBit::new("ro".to_string(), 1, true);
/// circuit += PauliX::new(0);
/// circuit += MeasureQubit::new(0, "ro".to_string(), 1);
/// let (bit_registers, _f, _c, _bo, _co) = call_circuit(
///     &circuit,
///     (HashMap::new(), HashMap::new(), HashMap::new(), HashMap::new(), HashMap::new()),
///     2,
/// )
/// .unwrap();
///
/// assert!(bit_registers.contains_key("ro"));
/// let out_reg = bit_registers.get("ro").unwrap();
/// assert_eq!(out_reg.len(), 1);
/// for reg in out_reg.iter() {
///     assert!(*reg || !*reg);
/// }
/// ```
///
pub fn call_circuit(
    circuit: &Circuit,
    mut registers: (
        HashMap<String, BitRegister>,
        HashMap<String, FloatRegister>,
        HashMap<String, ComplexRegister>,
        HashMap<String, BitOutputRegister>,
        HashMap<String, ComplexOutputRegister>,
    ),
    number_qubits: usize,
) -> Result<
    (
        HashMap<String, BitRegister>,
        HashMap<String, FloatRegister>,
        HashMap<String, ComplexRegister>,
        HashMap<String, BitOutputRegister>,
        HashMap<String, ComplexOutputRegister>,
    ),
    RoqoqoBackendError,
> {
    for op in circuit.iter() {
        registers = call_operation(op, registers, number_qubits)?;
    }
    Ok(registers)
}

/// Executes mocked qoqo operation.
///
/// # Arguments
///
/// * `operation` - The qoqo Operation that is executed.
/// * `registers` - The five registers used in the Interface:
///                 (1) HashMap containing bit readout values.
///                 (2) HashMap containing float readout values.
///                 (3) HashMap containing complex readout values.
///                 (4) HashMap containing a register for each repetition of the circuit (bit readout values).
///                 (5) HashMap containing a register for each repetition of the circuit (complex readout values).
/// * `number_qubits: Number of qubits mocked.
///
/// # Returns
///
/// * `Ok(HashMap<String, BitRegister>, HashMap<String, FloatRegister>, HashMap<String, ComplexRegister>, HashMap<String, BitOutputRegister>, HashMap<String, ComplexOutputRegister>) - The five input registers with the readouts from the operation.
/// * `Err(RoqoqoBackendError)` - Operation not supported by Mocked backend.
///
pub fn call_operation(
    operation: &Operation,
    registers: (
        HashMap<String, BitRegister>,
        HashMap<String, FloatRegister>,
        HashMap<String, ComplexRegister>,
        HashMap<String, BitOutputRegister>,
        HashMap<String, ComplexOutputRegister>,
    ),
    number_qubits: usize,
) -> Result<
    (
        HashMap<String, BitRegister>,
        HashMap<String, FloatRegister>,
        HashMap<String, ComplexRegister>,
        HashMap<String, BitOutputRegister>,
        HashMap<String, ComplexOutputRegister>,
    ),
    RoqoqoBackendError,
> {
    let mut bit_register_dict = registers.0;
    let mut float_register_dict = registers.1;
    let mut complex_register_dict = registers.2;
    let mut output_bit_register_dict = registers.3;
    let mut output_complex_register_dict = registers.4;

    match operation {
        Operation::MeasureQubit(op) => {
            let res: bool = rand::random();
            bit_register_dict.insert(op.readout().to_string(), vec![res]);
            Ok((
                bit_register_dict,
                float_register_dict,
                complex_register_dict,
                output_bit_register_dict,
                output_complex_register_dict,
            ))
        }
        Operation::PragmaRepeatedMeasurement(op) => {
            let mut all_res: Vec<Vec<bool>> = Vec::new();
            for _i in 0..*op.number_measurements() {
                let res: Vec<bool> = (0..number_qubits).map(|_| rand::random()).collect();
                all_res.push(res)
            }
            output_bit_register_dict.insert(op.readout().to_string(), all_res);
            Ok((
                bit_register_dict,
                float_register_dict,
                complex_register_dict,
                output_bit_register_dict,
                output_complex_register_dict,
            ))
        }
        Operation::PragmaGetPauliProduct(op) => {
            let mut rng = rand::thread_rng();
            let res: f64 = rng.gen::<f64>();
            float_register_dict.insert(op.readout().to_string(), vec![res]);
            Ok((
                bit_register_dict,
                float_register_dict,
                complex_register_dict,
                output_bit_register_dict,
                output_complex_register_dict,
            ))
        }
        Operation::PragmaGetOccupationProbability(op) => {
            let mut rng = rand::thread_rng();
            let res: Vec<f64> = (0..number_qubits).map(|_| rng.gen::<f64>()).collect();
            float_register_dict.insert(op.readout().to_string(), res);
            Ok((
                bit_register_dict,
                float_register_dict,
                complex_register_dict,
                output_bit_register_dict,
                output_complex_register_dict,
            ))
        }
        Operation::PragmaGetStateVector(op) => {
            let mut rng = rand::thread_rng();
            let shape = 2usize.pow(number_qubits as u32);
            let res_real: Vec<f64> = (0..shape).map(|_| rng.gen::<f64>()).collect();
            let res_imag: Vec<f64> = (0..shape).map(|_| rng.gen::<f64>()).collect();
            let mut normalise: f64 = 0.0;
            let mut res_all: Vec<Complex64> = Vec::new();
            for (real, imag) in res_real.iter().zip(res_imag.iter()) {
                let number = Complex64::new(*real, *imag);
                res_all.push(number);
                normalise += number.norm_sqr();
            }
            let mut res_normalised: Vec<Complex64> = Vec::new();
            for number in res_all {
                res_normalised.push(number / normalise);
            }

            complex_register_dict.insert(op.readout().to_string(), res_normalised);
            Ok((
                bit_register_dict,
                float_register_dict,
                complex_register_dict,
                output_bit_register_dict,
                output_complex_register_dict,
            ))
        }
        Operation::PragmaGetDensityMatrix(op) => {
            let mut rng = rand::thread_rng();
            let res_qubits: Vec<usize> = (0..number_qubits).map(|_| rng.gen_range(0..2)).collect();

            let mut statevec: Vec<Vec<Complex64>>;
            let matrix_0: Vec<Vec<Complex64>> =
                vec![vec![Complex64::new(1.0, 0.0), Complex64::new(0.0, 0.0)]];
            let matrix_1: Vec<Vec<Complex64>> =
                vec![vec![Complex64::new(0.0, 0.0), Complex64::new(1.0, 0.0)]];
            if res_qubits[0] == 0 {
                statevec = matrix_0.clone();
            } else {
                statevec = matrix_1.clone();
            }
            for i in 1..number_qubits {
                if res_qubits[i] == 0 {
                    statevec = kronecker_fn(&statevec, &matrix_0);
                } else {
                    statevec = kronecker_fn(&statevec, &matrix_1);
                }
            }
            let mut statevec_to_row: Vec<Complex64> = Vec::new();
            let mut statevec_column: Vec<Vec<Complex64>> = Vec::new();
            for value in statevec[0].iter() {
                statevec_to_row.push(*value);
                statevec_column.push(vec![*value]);
            }
            let statevec_row = vec![statevec_to_row];
            let density_matrix = kronecker_fn(&statevec_row, &statevec_column);

            output_complex_register_dict.insert(op.readout().to_string(), density_matrix);
            Ok((
                bit_register_dict,
                float_register_dict,
                complex_register_dict,
                output_bit_register_dict,
                output_complex_register_dict,
            ))
        }
        _ => {
            if ALLOWED_OPERATIONS.contains(&operation.hqslang())
                || operation.tags().contains(&"GateOperation")
                || operation.tags().contains(&"Definition")
            {
                Ok((
                    bit_register_dict,
                    float_register_dict,
                    complex_register_dict,
                    output_bit_register_dict,
                    output_complex_register_dict,
                ))
            } else {
                Err(RoqoqoBackendError::OperationNotInBackend {
                    backend: "Mock",
                    hqslang: operation.hqslang(),
                })
            }
        }
    }
}

fn kronecker_fn(a: &Vec<Vec<Complex64>>, b: &Vec<Vec<Complex64>>) -> Vec<Vec<Complex64>> {
    let m = a.len();
    let n = a[0].len();
    let p = b.len();
    let q = b[0].len();
    let rtn = m * p;
    let ctn = n * q;
    let mut r = zero_matrix(rtn, ctn);

    for i in 0..m {
        for j in 0..n {
            for k in 0..p {
                for l in 0..q {
                    r[p * i + k][q * j + l] = a[i][j] * b[k][l];
                }
            }
        }
    }
    r
}

fn zero_matrix(rows: usize, cols: usize) -> Vec<Vec<Complex64>> {
    let mut matrix = Vec::with_capacity(cols);
    for _ in 0..rows {
        let mut col: Vec<Complex64> = Vec::with_capacity(rows);
        for _ in 0..cols {
            col.push(Complex64::new(0.0, 0.0));
        }
        matrix.push(col);
    }
    matrix
}
