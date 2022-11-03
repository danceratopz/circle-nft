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
        project.ERC20Factory, "Circle Token", "CIRCLETOKEN", 100, receiver
    )


@pytest.fixture(scope="session")
def circle_nft(owner, project, circle_token):
    return owner.deploy(project.CircleNFT, circle_token.address)


def test_mint(receiver, owner, circle_nft):
    circle_nft.mintNFT(receiver, sender=owner)
    radius = circle_nft.getRadius(1)
    assert radius == 0
