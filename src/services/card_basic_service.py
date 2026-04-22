from src.utils.card_hasher import compute_card_hash


class CardBasicService:

    def __init__(self, repository):
        self._repository = repository

    def save_card_service(self, card):
        new_hash = compute_card_hash(card.to_dict)
        card.set_attributes("_hash", new_hash)
        self._repository.save_card(card)
        print(f"Service: Carta {card.name} validata e inviata al salvataggio.")

    def delete_card_service(self, card_id : str):
        self._repository.delete_card(card_id)

    def get_all_cards_service(self):
        return self._repository.get_all_cards()

    def get_card_by_id_service(self, card_id : str):
        return self._repository.get_card_by_id(card_id)


    def get_hash_map(self):
        hash_map = {}
        cards = self._repository.get_all_cards()

        for card in cards:
            card_data = card.to_dict
            card_id = card_data.get("id")

            current_hash = card_data.get("_hash")

            if not current_hash:
                current_hash = compute_card_hash(card_data)
                card.set_attributes("_hash", current_hash)

                self._repository.save_card(card)

            hash_map[card_id] = current_hash

        return hash_map

    def sync_cards(self, remote_cards):
        """Logica di sincronizzazione centralizzata."""
        local_cards = self.get_all_cards_service()

        local_map = {str(c.id): c for c in local_cards}
        remote_map = {str(c.id): c for c in remote_cards}

        local_ids = set(local_map.keys())
        remote_ids = set(remote_map.keys())

        # --- CREATE ---
        for cid in (remote_ids - local_ids):
            card = remote_map[cid]
            # Usa set_attributes per coerenza con il dominio
            card.set_attributes("_hash", compute_card_hash(card.to_dict))
            self._repository.save_card(card)

        # --- UPDATE ---
        for cid in (remote_ids & local_ids):
            remote_card = remote_map[cid]
            local_card = local_map[cid]
            remote_hash = compute_card_hash(remote_card.to_dict)

            if local_card.get_attributes("_hash") != remote_hash:
                remote_card.set_attributes("_hash", remote_hash)
                self._repository.save_card(remote_card)

        # --- DELETE ---
        for cid in (local_ids - remote_ids):
            self._repository.delete_card(cid)
