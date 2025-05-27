const path = require('path');
const fs = require('fs');
const solc = require('solc');

function findImports(importPath) {
  try {
    // Handle local imports
    if (importPath.startsWith('./')) {
      const localPath = path.resolve(__dirname, importPath);
      return {
        contents: fs.readFileSync(localPath, 'utf8')
      };
    }
    
    // Handle node_modules imports
    const nodeModulesPath = importPath.startsWith('@') ? 
      require.resolve(importPath) : 
      require.resolve(`@openzeppelin/contracts/${importPath}`);
    return {
      contents: fs.readFileSync(nodeModulesPath, 'utf8')
    };
  } catch (error) {
    return { error: 'File not found' };
  }
}

// Get all Solidity files in the directory
const contractFiles = fs.readdirSync(__dirname)
  .filter(file => file.endsWith('.sol'));

// Create input object for all contracts
const input = {
  language: 'Solidity',
  sources: {},
  settings: {
    outputSelection: {
      '*': {
        '*': [
          'abi',
          'evm.bytecode.object',
          'evm.deployedBytecode.object',
          'evm.methodIdentifiers'
        ]
      }
    },
    optimizer: {
      enabled: true,
      runs: 200
    }
  }
};

// Add each contract to the sources
contractFiles.forEach(file => {
  const contractPath = path.resolve(__dirname, file);
  const source = fs.readFileSync(contractPath, 'utf8');
  input.sources[file] = { content: source };
});

try {
  const output = JSON.parse(solc.compile(JSON.stringify(input), { import: findImports }));

  // Check for compilation errors
  if (output.errors) {
    const hasError = output.errors.some(error => error.severity === 'error');
    if (hasError) {
      console.error('Compilation errors:', output.errors);
      process.exit(1);
    } else {
      console.warn('Compilation warnings:', output.errors);
    }
  }

  // Create artifacts directory if it doesn't exist
  const artifactsDir = path.resolve(__dirname, 'artifacts');
  if (!fs.existsSync(artifactsDir)) {
    fs.mkdirSync(artifactsDir);
  }

  // Write each compiled contract to a file
  for (const [sourceFile, contracts] of Object.entries(output.contracts)) {
    for (const [contractName, contractOutput] of Object.entries(contracts)) {
      // Format the output to include both deployment and runtime bytecode
      const formattedOutput = {
        abi: contractOutput.abi,
        bytecode: contractOutput.evm.bytecode.object,
        deployedBytecode: contractOutput.evm.deployedBytecode.object,
        methodIdentifiers: contractOutput.evm.methodIdentifiers
      };

      fs.writeFileSync(
        path.resolve(artifactsDir, `${contractName}.json`),
        JSON.stringify(formattedOutput, null, 2)
      );

      console.log(`Contract ${contractName} compiled successfully!`);
    }
  }
} catch (error) {
  console.error('Compilation failed:', error);
  process.exit(1);
} 