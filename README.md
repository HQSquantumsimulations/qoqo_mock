# qoqo-mock interface

![Read the Docs](https://img.shields.io/readthedocs/qoqo_mock)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/HQSquantumsimulations/qoqo_mock/ci_tests)
![PyPI](https://img.shields.io/pypi/v/qoqo_mock)
![PyPI - License](https://img.shields.io/pypi/l/qoqo_mock)
![PyPI - Format](https://img.shields.io/pypi/format/qoqo_mock)

Mocking interface for for the qoqo quantum toolkit by [HQS Quantum Simulations](https://quantumsimulations.de).

qoqo-mock provides a mocked benchmarking backend for qoqo.
qoqo circuits can be send to the mock backend and are all steps of a full hardware backend are applied, except calling actual quantum hardware. Measurements return random results.  
This backend is designed purely for benchmarking purposes.

This software is still in the beta stage. Functions and documentation are not yet complete and breaking changes can occur.
