from __future__ import annotations

import unittest

from states import SessionStore


class SessionStoreTests(unittest.TestCase):
    def test_set_get_and_pop_round_trip(self) -> None:
        store = SessionStore()
        store.set(42, "user_search", field="points")

        self.assertEqual(store.get(42), {"flow": "user_search", "field": "points"})
        self.assertEqual(store.pop(42), {"flow": "user_search", "field": "points"})
        self.assertIsNone(store.get(42))

    def test_clear_removes_pending_input(self) -> None:
        store = SessionStore()
        store.set(42, "broadcast", body="hello")
        store.clear(42)

        self.assertIsNone(store.pop(42))


if __name__ == "__main__":
    unittest.main()