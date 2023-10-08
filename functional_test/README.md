# Functional test

## What is this?
This directory contains a functional test for QDTS. The test does not fully cover all the functional requirements of QDTS yet.

## How do I execute the test?

### Prerequisites
Have a network with 4 machiness. One of the machines will be the tester's workstation, while the other three will act as the classical infrastructure over which the digital twin of the QKD network will be deployed.

The configuration files assume the machines have the following IP addresses:
- 10.4.16.115
- 10.4.16.74
- 10.4.16.132

Why these annoying and non-user-friendly IP addresses? Don't ask. If your machines have different addresses, please, replace them in the following files:
- config.yaml
- functional_test.py
- inventory.yaml

The tester's workstation can have any modern version of python 3 (greater than 3.8). The other machines must have a modern version of python 3 and additionally a virtual env with python 3.6 (simulaqron won't work otherwise).
Additionally, modify the inventory.yaml file with the needed data from your machines.

In the tester's workstation install the qdts_orchestrator and the qdts_client:
```
pip install qdts_orchestrator qdts_client
```
There is no need to install any software other than the python virtual environment in the other machines.

### Execution
All the commands must be executed from the tester's workstation and in this directory

1. Execute the following commands to deploy the network
   ```
   qdts_install config.yaml inventory.yaml
   qdts_run inventory.yaml
   ```
2. Execute the test with the following command
   ```
   python functional_test.py
   ```
3. Verify all the tests run and the message "ALL TESTS OKAY!" is shown
4. Stop the network with the following command
   ```
   qdts_stop inventory.yaml
   ```

