import hashlib
import json


def compute_card_hash(card_dict):

    clean = {
        k: v
        for k, v in card_dict.items()
        if k != "_hash"
    }

    return hashlib.md5(
        json.dumps(clean, sort_keys=True).encode()
    ).hexdigest()