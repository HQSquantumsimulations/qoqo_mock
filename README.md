# qoqo-mock interface

[![Documentation Status](https://readthedocs.org/projects/qoqo_mock/badge/?version=latest)](https://qoqo_mock.readthedocs.io/en/latest/?badge=latest)
[![GitHub Workflow Status](https://github.com/HQSquantumsimulations/qoqo_mock/workflows/ci_tests/badge.svg)](https://github.com/HQSquantumsimulations/qoqo_mock/actions)
[![PyPI](https://img.shields.io/pypi/v/qoqo_mock)](https://pypi.org/project/qoqo_mock/)
![PyPI - License](https://img.shields.io/pypi/l/qoqo_mock)
[![PyPI - Format](https://img.shields.io/pypi/format/qoqo_mock)](https://pypi.org/project/qoqo_mock/)

Mocking interface for for the qoqo quantum toolkit by [HQS Quantum Simulations](https://quantumsimulations.de).

qoqo-mock provides a mocked benchmarking backend for qoqo.
qoqo circuits can be send to the mock backend and are all steps of a full hardware backend are applied, except calling actual quantum hardware. Measurements return random results.  
This backend is designed purely for benchmarking purposes.

This software is still in the beta stage. Functions and documentation are not yet complete and breaking changes can occur.
