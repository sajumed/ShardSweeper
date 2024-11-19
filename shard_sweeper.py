import requests

OPENSEA_API = "https://api.opensea.io/api/v1/assets"

def fetch_nfts(address, chain='ethereum'):
    params = {
        "owner": address,
        "order_direction": "desc",
        "offset": 0,
        "limit": 50
    }
    if chain == "polygon":
        params["asset_contract_address"] = "0x...polygon_contract"
    response = requests.get(OPENSEA_API, params=params)
    result = response.json()
    assets = result.get("assets", [])
    return [
        {
            "name": asset.get("name"),
            "token_id": asset.get("token_id"),
            "collection": asset.get("collection", {}).get("name"),
            "rarity_rank": asset.get("rarity_rank", "N/A"),
            "description": asset.get("description", ""),
        }
        for asset in assets
    ]

def sweep(addresses):
    report = []
    for chain in ["ethereum", "polygon"]:
        for addr in addresses.get(chain, []):
            nfts = fetch_nfts(addr, chain)
            rare_nfts = [n for n in nfts if n['rarity_rank'] != "N/A" and int(n['rarity_rank']) <= 100]
            for nft in rare_nfts:
                report.append({
                    "address": addr,
                    "chain": chain,
                    **nft
                })
    return report

if __name__ == "__main__":
    addresses = {
        "ethereum": ["0x742d35Cc6634C0532925a3b844Bc454e4438f44e"],
        "polygon": ["0x560fC6F6e81B636db99C5EEA556dBd3b103b62eD"]
    }
    found = sweep(addresses)
    for item in found:
        print(f"[{item['chain']}] {item['address']}: {item['collection']} #{item['token_id']} — {item['name']} (Rarity: {item['rarity_rank']})\nОписание: {item['description']}\n")
