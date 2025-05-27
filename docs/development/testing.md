# Testing Guide

This guide provides comprehensive information about testing in DecentraLearn.

## Testing Strategy

### Test Types

1. **Unit Tests**
   - Test individual components
   - Isolate dependencies
   - Fast execution
   - High coverage

2. **Integration Tests**
   - Test component interactions
   - Verify system behavior
   - Include blockchain interactions
   - Test privacy mechanisms

3. **Performance Tests**
   - Measure execution time
   - Monitor resource usage
   - Test scalability
   - Benchmark privacy overhead

## Writing Tests

### Test Structure

1. **Basic Test**
   ```python
   def test_client_registration():
       """Test client registration process."""
       client = BlockchainClient()
       address = client.register("test_client")
       assert address.startswith("0x")
   ```

2. **Test Class**
   ```python
   class TestModelVerification:
       """Test suite for model verification."""

       def setup_method(self):
           """Setup test environment."""
           self.client = BlockchainClient()
           self.model = BaseModel()

       def test_verification_success(self):
           """Test successful verification."""
           result = self.client.verify_model(self.model)
           assert result is True

       def test_verification_failure(self):
           """Test failed verification."""
           invalid_model = InvalidModel()
           with pytest.raises(VerificationError):
               self.client.verify_model(invalid_model)
   ```

### Test Fixtures

1. **Basic Fixture**
   ```python
   @pytest.fixture
   def blockchain_client():
       """Create blockchain client for testing."""
       client = BlockchainClient()
       yield client
       client.cleanup()
   ```

2. **Parameterized Fixture**
   ```python
   @pytest.fixture(params=[32, 64, 128])
   def batch_size(request):
       """Test different batch sizes."""
       return request.param
   ```

### Mocking

1. **Basic Mock**
   ```python
   def test_model_upload(mocker):
       """Test model upload with mocked blockchain."""
       mock_client = mocker.Mock()
       mock_client.upload_model.return_value = "0x123"
       
       result = upload_model(mock_client, BaseModel())
       assert result == "0x123"
   ```

2. **Mock with Side Effects**
   ```python
   def test_error_handling(mocker):
       """Test error handling in blockchain operations."""
       mock_client = mocker.Mock()
       mock_client.upload_model.side_effect = BlockchainError("Failed")
       
       with pytest.raises(BlockchainError):
           upload_model(mock_client, BaseModel())
   ```

## Running Tests

### Basic Commands

1. **Run All Tests**
   ```bash
   pytest
   ```

2. **Run Specific Tests**
   ```bash
   pytest tests/blockchain/test_client.py
   pytest tests/blockchain/test_client.py::test_registration
   ```

3. **Run with Coverage**
   ```bash
   pytest --cov=decentralearn
   pytest --cov=decentralearn --cov-report=html
   ```

### Test Configuration

1. **pytest.ini**
   ```ini
   [pytest]
   testpaths = tests
   python_files = test_*.py
   python_classes = Test*
   python_functions = test_*
   ```

2. **coverage.ini**
   ```ini
   [run]
   source = decentralearn
   omit = tests/*,setup.py

   [report]
   exclude_lines =
       pragma: no cover
       def __repr__
       raise NotImplementedError
   ```

## Test Categories

### Blockchain Tests

1. **Client Tests**
   ```python
   def test_client_connection():
       """Test blockchain connection."""
       client = BlockchainClient()
       assert client.is_connected()

   def test_transaction_signing():
       """Test transaction signing."""
       client = BlockchainClient()
       tx = client.sign_transaction({"to": "0x123"})
       assert tx["signature"] is not None
   ```

2. **Contract Tests**
   ```python
   def test_contract_deployment():
       """Test smart contract deployment."""
       client = BlockchainClient()
       contract = client.deploy_contract("ModelRegistry")
       assert contract.address is not None
   ```

### Privacy Tests

1. **Differential Privacy**
   ```python
   def test_dp_noise_addition():
       """Test differential privacy noise."""
       data = torch.randn(100)
       private_data = add_dp_noise(data, epsilon=1.0)
       assert not torch.allclose(data, private_data)
   ```

2. **Homomorphic Encryption**
   ```python
   def test_he_encryption():
       """Test homomorphic encryption."""
       data = torch.tensor([1.0, 2.0, 3.0])
       encrypted = encrypt_data(data)
       assert encrypted.shape == data.shape
   ```

### Model Tests

1. **Training Tests**
   ```python
   def test_model_training():
       """Test model training process."""
       model = BaseModel()
       dataset = CustomDataset()
       trainer = Trainer(model)
       loss = trainer.train(dataset)
       assert loss < 1.0
   ```

2. **Verification Tests**
   ```python
   def test_model_verification():
       """Test model verification."""
       model = BaseModel()
       verifier = ModelVerifier()
       result = verifier.verify(model)
       assert result["valid"] is True
   ```

## Best Practices

1. **Test Organization**
   - Group related tests
   - Use descriptive names
   - Follow test hierarchy
   - Maintain test isolation

2. **Test Quality**
   - Write meaningful tests
   - Cover edge cases
   - Test error conditions
   - Verify expected behavior

3. **Performance**
   - Minimize test duration
   - Use appropriate fixtures
   - Avoid unnecessary I/O
   - Mock external services

4. **Maintenance**
   - Keep tests up to date
   - Remove obsolete tests
   - Update test data
   - Document test changes

## See Also

- [pytest Documentation](https://docs.pytest.org/)
- [Testing Setup](setup.md)
- [Code Style Guide](code_style.md)
- [Development Guide](../development/README.md) 