<img src="qoqo_Logo_vertical_color.png" alt="qoqo logo" width="300" />

# qoqo-mock

Mocking backend for the qoqo/roqoqo quantum toolkit by [HQS Quantum Simulations](https://quantumsimulations.de).

This repository contains two components:

* The qoqo_mock backend for the qoqo python interface to roqoqo
* The roqoqo_mock backend for roqoqo directly

## qoqo-mock

[![Documentation Status](https://readthedocs.org/projects/qoqo_mock/badge/?version=latest)](https://qoqo_mock.readthedocs.io/en/latest/?badge=latest)
[![GitHub Workflow Status](https://github.com/HQSquantumsimulations/qoqo_mock/workflows/ci_tests/badge.svg)](https://github.com/HQSquantumsimulations/qoqo_mock/actions)
[![PyPI](https://img.shields.io/pypi/v/qoqo_mock)](https://pypi.org/project/qoqo_mock/)
![PyPI - License](https://img.shields.io/pypi/l/qoqo_mock)
[![PyPI - Format](https://img.shields.io/pypi/format/qoqo_mock)](https://pypi.org/project/qoqo_mock/)

Mocking backend for the qoqo quantum toolkit by [HQS Quantum Simulations](https://quantumsimulations.de).

qoqo-mock provides a mocked benchmarking backend for qoqo.
qoqo circuits can be sent to the mock backend and all steps of a full hardware backend are applied, except calling actual quantum hardware. Measurements return random results.  
This backend is designed purely for benchmarking purposes.

A source distribution now exists but requires a Rust install with a rust version > 1.47 and a maturin version { >= 0.12, <0.13 } in order to be built.

## roqoqo-mock

[![Crates.io](https://img.shields.io/crates/v/roqoqo-mock)](https://crates.io/crates/roqoqo-mock)
[![GitHub Workflow Status](https://github.com/HQSquantumsimulations/qoqo_mock/workflows/ci_tests/badge.svg)](https://github.com/HQSquantumsimulations/qoqo_mock/actions)
[![docs.rs](https://img.shields.io/docsrs/roqoqo-mock)](https://docs.rs/roqoqo-mock/)
![Crates.io](https://img.shields.io/crates/l/roqoqo-mock)

Mocking backend for the roqoqo quantum toolkit by [HQS Quantum Simulations](https://quantumsimulations.de).

roqoqo-mock provides a mocked benchmarking backend for roqoqo.
roqoqo circuits can be sent to the mock backend and all steps of a full hardware backend are applied, except calling actual quantum hardware. Measurements return random results.  
This backend is designed purely for benchmarking purposes.

## General Notes

This software is still in the beta stage. Functions and documentation are not yet complete and breaking changes can occur.

## Contributing

We welcome contributions to the project. If you want to contribute code, please have a look at CONTRIBUTE.md for our code contribution guidelines.
