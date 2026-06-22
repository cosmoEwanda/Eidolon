from urllib.error import URLError

import pandas as pd


class GoogleDriveCardStorage:

    def __init__(self, card_sheet, order_sheet, cost_sheet):
        self.card_sheet = card_sheet
        self.order_sheet = order_sheet
        self.cost_sheet = cost_sheet

    def load_raw(self):
        try:
            return {
                "cards": pd.read_csv(self.card_sheet).fillna("NULL"),
                "orders": pd.read_csv(self.order_sheet).fillna("NULL"),
                "costs" : pd.read_csv(self.cost_sheet).fillna("NULL")
            }
        except URLError as e:
            raise ConnectionError("NO_INTERNET") from e

