<p align="center">
  <img src="https://raw.githubusercontent.com/ackerman23/decentralearn/main/Logo.jpg" alt="DecentraLearn Logo" width="200"/>
</p>

# DecentraLearn

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen)](docs/index.md)
[![Tests](https://github.com/ackerman23/decentralearn/actions/workflows/tests.yml/badge.svg)](https://github.com/ackerman23/decentralearn/actions/workflows/tests.yml)

A decentralized federated learning framework with strong privacy guarantees, built on blockchain technology.

## 🚀 Features

- **Federated Learning**
  - Decentralized model training
  - Secure model aggregation
  - Incentive mechanisms
  - Smart contract-based coordination

- **Privacy Mechanisms**
  - Differential Privacy
  - Homomorphic Encryption
  - Zero-Knowledge Proofs
  - Secure Aggregation

- **Blockchain Integration**
  - Smart contract-based verification
  - Transparent model tracking
  - Decentralized coordination
  - Incentive distribution

- **Advanced Security**
  - End-to-end encryption
  - Model integrity verification
  - Access control
  - Audit logging

## 📦 Installation

### Install via pip (Recommended)

You can install the latest release (v2.1.0) directly from PyPI:

```bash
pip install decentralearn
```

To upgrade to the latest version:

```bash
pip install --upgrade decentralearn
```

**Note:** If you encounter dependency issues (especially with `eth-tester`), try installing the beta version first:

```bash
pip install eth-tester==0.13.0b1
pip install decentralearn
```

Or install all dependencies manually:

```bash
pip install torch>=2.0.0 numpy>=1.21.0 scipy>=1.7.0 opacus>=1.1.0 phe>=1.5.0 web3>=6.0.0 eth-tester==0.13.0b1 eth-utils>=2.1.0
pip install decentralearn
```

---

### Prerequisites

- Python 3.8 or higher
- Ethereum node (e.g., Ganache for development)
- PyTorch 1.7 or higher

### Installation Steps (from source)

1. Clone the repository:
   ```bash
   git clone https://github.com/ackerman23/decentralearn
   cd decentralearn
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

## 🏁 Quick Start

1. Initialize blockchain connection:
   ```python
   from decentralearn.blockchain.client import BlockchainClient
   from decentralearn.config.blockchain_config import BlockchainConfig

   config = BlockchainConfig(
       rpc_url="http://localhost:8545",
       chain_id=1337
   )
   client = BlockchainClient(config)
   ```

2. Create and train a model:
   ```python
   from decentralearn.models.base import BaseModel
   from decentralearn.privacy import DifferentialPrivacy

   model = BaseModel()
   dp = DifferentialPrivacy(epsilon=0.1)
   # Train model with privacy
   ```

3. Upload to blockchain:
   ```python
   client.upload_model(model)
   ```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Architecture Overview](docs/architecture/overview.md)
- [API Reference](docs/api/README.md)
- [Tutorials](docs/tutorials/README.md)
- [Examples](docs/examples/README.md)
- [Development Guide](docs/development/README.md)

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

For detailed test output:
```bash
pytest -v tests/
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development/contributing.md) for details.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Creator:** Jihad GARTI (<jihad.garti2@gmail.com>)

## 📧 Support

For questions and support:

1. Check the [FAQ](docs/faq.md)
2. Open an issue on GitHub
3. Contact the maintainers

## 🙏 Acknowledgments

- PyTorch team for the deep learning framework
- Ethereum community for blockchain infrastructure
- Privacy research community for privacy-preserving techniques

## 📄 Citation

If you use DecentraLearn in your research, please cite:

```bibtex
@software{decentralearn2024,
  author = {Jihad GARTI},
  title = {DecentraLearn: A Decentralized Federated Learning Framework},
  year = {2024},
  publisher = {Jihad GARTI},
  url = {https://github.com/ackerman23/decentralearn}
}
```