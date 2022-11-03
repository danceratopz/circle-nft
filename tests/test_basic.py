import pytest


@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def receiver(accounts):
    return accounts[1]


@pytest.fixture(scope="session")
def circle_token(owner, receiver, project):
    return owner.deploy(
        project.ERC20Factory, "Circle Token", "CIRCLETOKEN", 100**18, receiver
    )


@pytest.fixture(scope="session")
def circle_nft(owner, project, circle_token):
    return owner.deploy(project.CircleNFT, circle_token.address)


def test_mint(receiver, owner, circle_nft):
    circle_nft.mintNFT(receiver, sender=owner)
    radius = circle_nft.getRadius(1)
    assert radius == 0


def test_increase_radius(receiver, owner, circle_token, circle_nft):
    circle_nft.mintNFT(receiver, sender=owner)
    token_id = circle_nft.getLastTokenID()
    amount = 2**18
    circle_token.approve(circle_nft.address, amount, sender=receiver)
    circle_nft.increaseRadius(token_id, amount, sender=receiver)
    assert circle_nft.getRadius(token_id) == amount


def test_decrease_radius(receiver, owner, circle_token, circle_nft):
    circle_nft.mintNFT(receiver, sender=owner)
    token_id = circle_nft.getLastTokenID()
    amount = 2**18
    circle_token.approve(circle_nft.address, amount, sender=receiver)
    circle_nft.increaseRadius(token_id, amount, sender=receiver)
    radius = circle_nft.getRadius(token_id)
    amount = 1**18
    circle_nft.decreaseRadius(token_id, amount, sender=receiver)
    assert radius - amount == circle_nft.getRadius(token_id)
