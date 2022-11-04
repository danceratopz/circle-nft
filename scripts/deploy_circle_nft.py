import json
from urllib.request import urlopen

import click
from ape import accounts, convert, networks, project


class CircleNFT:
    def __init__(self, circle_nft, circle_token, owner):
        self.circle_nft = circle_nft
        self.circle_token = circle_token
        self.address = circle_nft.address
        self.owner = owner

    def increase_radius(self, token_id, token_owner, amount):
        self.circle_token.approve(self.address, amount, sender=token_owner)
        self.circle_nft.increaseRadius(token_id, amount, sender=token_owner)

    def decrease_radius(self, token_id, token_owner, amount):
        self.circle_nft.decreaseRadius(token_id, amount, sender=token_owner)

    def get_token_metadata(self, token_id):
        token_uri = self.circle_nft.tokenURI(token_id)
        with urlopen(token_uri) as f:
            metadata = json.loads(f.read())
        return metadata

    def get_token_svg(self, token_id):
        metadata = self.get_token_metadata(token_id)
        with urlopen(metadata["image"]) as f:
            svg = f.read()
        return svg


def main():
    ecosystem_name = networks.provider.network.ecosystem.name
    network_name = networks.provider.network.name
    provider_name = networks.provider.name
    click.echo(
        f"You are connected to network '{ecosystem_name}:{network_name}:{provider_name}'."
    )

    owner = accounts.test_accounts[0]
    receiver = accounts.test_accounts[1]

    circle_token = owner.deploy(
        project.ERC20Factory,
        "Circle Token",
        "CIRCLETOKEN",
        convert("200 ETH", int),
        receiver.address,
    )
    print(f"Gas used: {circle_token.receipt.gas_used}")
    print(circle_token.balanceOf(receiver))

    circle_nft = owner.deploy(project.CircleNFT, circle_token.address)
    print(f"Gas used: {circle_nft.receipt.gas_used}")

    print("Minting circle...")
    receipt = circle_nft.mintNFT(receiver, sender=owner)
    print(f"Gas used: {receipt.gas_used}")

    token_id = circle_nft.getLastTokenID()
    circle_nft_helper = CircleNFT(circle_nft, circle_token, owner)
    metadata = circle_nft_helper.get_token_metadata(token_id)
    assert int(metadata["radius"]) == circle_nft.getRadius(token_id)

    new_radius = 50
    print(f"\nIncreasing radius to {new_radius}...")
    amount = new_radius - circle_nft.getRadius(token_id)
    circle_nft_helper.increase_radius(token_id, receiver, amount)
    metadata = circle_nft_helper.get_token_metadata(token_id)
    assert int(metadata["radius"]) == circle_nft.getRadius(token_id)
    assert int(metadata["radius"]) == new_radius
    print(circle_nft_helper.get_token_svg(token_id))

    new_radius = 100
    print(f"\nIncreasing radius to {new_radius}...")
    amount = new_radius - circle_nft.getRadius(token_id)  # / 10**18
    circle_nft_helper.increase_radius(token_id, receiver, amount)
    metadata = circle_nft_helper.get_token_metadata(token_id)
    assert int(metadata["radius"]) == circle_nft.getRadius(token_id)
    assert int(metadata["radius"]) == new_radius
    print(circle_nft_helper.get_token_svg(token_id))

    new_radius = 75
    print(f"\nDecreasing radius to {new_radius}...")
    print(amount)
    amount = circle_nft.getRadius(token_id) - new_radius  # / 10**18
    circle_nft_helper.decrease_radius(token_id, receiver, amount)
    metadata = circle_nft_helper.get_token_metadata(token_id)
    assert int(metadata["radius"]) == circle_nft.getRadius(token_id)
    assert int(metadata["radius"]) == new_radius
    print(circle_nft_helper.get_token_svg(token_id))

    return circle_nft, circle_token


if __name__ == "__main__":
    main()
