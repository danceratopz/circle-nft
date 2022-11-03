// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import {Base64} from "./Base64.sol";

/// @title ERC721 Circle NFT Proof of Concept
/// @author danceratopz
/// @notice Simple ERC721 contract with dynamic token data
contract CircleNFT is ERC721, Ownable {
    using Strings for uint256;
    using Counters for Counters.Counter;
    using SafeERC20 for IERC20;
    Counters.Counter private _tokenIds;

    address erc20Address;
    mapping(uint256 => uint256) erc20Balances;
    uint256 maxRadius = 1 ether;

    constructor(address _erc20Address) ERC721("CircleNFT", "CIRCLE") {
        erc20Address = _erc20Address;
    }

    /// @notice Emitted upon a successful NFT mint.
    /// @param recipient The address that received the NFT.
    /// @param tokenId The index of the minted NFT.
    event Minted(address indexed recipient, uint256 indexed tokenId);

    /// @notice Mint a new NFT with metadata at the specified tokenURI and transfer it to the recipient.
    /// @param recipient The address to receive the newly minted NFT.
    /// @return The ID of the newly minted NFT.
    function mintNFT(address recipient)
        public
        onlyOwner
        returns (uint256)
    {
        _tokenIds.increment();
        uint256 newItemId = _tokenIds.current();
        erc20Balances[newItemId] = 0;
        _mint(recipient, newItemId);
            emit Minted(recipient, newItemId);
        return newItemId;
    }

    function getRadius(uint256 tokenId) public view returns (uint256) {
        require(_exists(tokenId), "not exist");
        return erc20Balances[tokenId];
    }

    /// @notice Helper that returns the ID last minted NFT.
    /// @return The ID of the last NFT that was minted.
    function getLastTokenID() public view returns (uint256) {
        require(_tokenIds.current() > 0, "Nothing minted, yet.");
        return _tokenIds.current();
    }

    function increaseRadius(uint256 tokenId, uint256 amount) public {
        require(_exists(tokenId), "not exist");
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        // TODO: use ceil if amount exceeds max allowed balance
        uint256 newRadius = erc20Balances[tokenId] + amount;
        require(newRadius <= maxRadius, "circle would exceed max radius");
        erc20Balances[tokenId] = newRadius;
        IERC20(erc20Address).safeTransferFrom(msg.sender, address(this), amount);
    }

    function decreaseRadius(uint256 tokenId, uint256 amount) public {
        require(_exists(tokenId), "not exist");
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        uint256 newRadius = erc20Balances[tokenId] - amount;
        require(newRadius >= 0, "circle would have neg radius");
        erc20Balances[tokenId] = newRadius;
        IERC20(erc20Address).approve(address(this), amount);
        IERC20(erc20Address).safeTransferFrom(address(this), msg.sender, amount);
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "not exist");

        string memory name = string(abi.encodePacked("Circle ", tokenId.toString()));
        string memory radius = getRadius(tokenId).toString();

        string memory jsonMetadata =  string(abi.encodePacked(
            'data:application/json;base64,',
            Base64.encode(bytes(abi.encodePacked(
                '{"name":"', name, '",',
                '"radius":"', radius, '"}')))));
        return jsonMetadata;
    }

}
