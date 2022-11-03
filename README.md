# circle-nft
A dynamic on-chain SVG NFT

# Development

## Prerequisites

* Python 3.10 or higher.


## Environment

This repository uses ape/apeworx. To get started create a and activate a virtualenv using pyenv (recommended) or execute:
```
python3 -m virtualenv venv3
source venv3/bin/activate
```
and install the requirements:
```
pip install -r requirements.txt
```

Then install ape's required plugins:
```
ape plugins install .
```

## Working with ape

Compile the contracts:
```
ape compile
```

Compile and deploy the contracts locally:
```
ape run deploy_circle_nft --network ethereum:local:test
```
