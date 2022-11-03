import base64
import click
import json
from urllib.request import urlopen

from ape import accounts, project, networks
# from ape.cli import network_option, NetworkBoundCommand

def main():
    ecosystem_name = networks.provider.network.ecosystem.name
    network_name = networks.provider.network.name
    provider_name = networks.provider.name
    click.echo(f"You are connected to network '{ecosystem_name}:{network_name}:{provider_name}'.")

    deployer = accounts.test_accounts[0]
    account1 = accounts.test_accounts[1]

    circle_token = deployer.deploy(project.ERC20Factory, "Circle Token", "CIRCLETOKEN", 100, account1.address)
    print(f"Gas used: {circle_token.receipt.gas_used}")    
    # circle_token_address = circle_token.address
    print(circle_token.balanceOf(account1))

    circle_nft = deployer.deploy(project.CircleNFT, circle_token.address)
    print(f"Gas used: {circle_nft.receipt.gas_used}")    

    receipt = circle_nft.mintNFT(account1, sender=deployer)
    print(f"Gas used: {receipt.gas_used}")
    token_uri = circle_nft.tokenURI(1)

    with urlopen(token_uri) as response:
        metadata = json.loads(response.read())
    
    print(metadata)
    print("radius", metadata["radius"])

    circle_token.approve(circle_nft.address, 1**18, sender=account1)
    circle_nft.increaseRadius(1, 1**18, sender=account1)

    token_uri = circle_nft.tokenURI(1)

    with urlopen(token_uri) as response:
        metadata = json.loads(response.read())
    
    print(metadata)
    print("radius", metadata["radius"])

    return circle_nft, circle_token

if __name__ == '__main__':
    main()