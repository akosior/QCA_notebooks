# QCA_notebooks
Space for executing notebooks form Quantum Computing Algorithms book

##Starting
1. Create python environment (with any name, here as an example \it qiskit_env)

python3 -m venv qiskit_env

2. Source this environment

source qiskit_env/bin/activat

3. install qiskit in the environment

pip3 install qiskit
pip3 install qiskit[visualization]
pip3 install qiskit-aer


### Chapter 2 Remarks

The 'execute' function became obsolete in qiskit 1.0. Instead one should yse 'transpile':

https://docs.quantum.ibm.com/migration-guides/qiskit-1.0-features#execute

### Other
To use 'latex' in circuit.draw you need to install poppler-utils pack

sudo apt install poppler-utils


