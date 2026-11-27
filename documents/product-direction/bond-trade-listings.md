# Bond trade listings

**Status:** product direction, non-normative. This proposal describes trade across 0x1 clients, with the Telegram group flow as its first detailed example.

## Purpose

A Bond can list items from its inventory for other Bonds to discover, buy for seeds, or propose an exchange for. A new listing can give someone a reason to browse the seller’s other offers, reply in a city group, or return to a familiar spot on the map. For example, a rare record might bring a collector to the seller’s listings, where they find another record they have been looking for.

## Shared trade flow

1. The authenticated seller opens their own inventory, chooses an eligible item, and confirms the listing. A fixed-price listing includes a price in seeds.
2. After publication is confirmed, the item appears in the seller’s public trade inventory, which contains all of that Bond’s currently active listings. Unlisted items stay private. Web, the map, and messenger clients use the same active listings.
3. The public trade inventory is sorted by original publication time, newest first, with stable ordering when publication times match. Rarity and the listing that led the viewer there do not affect order. A newer listing moves above an older listing even when the older item is Exclusive.
4. The buyer opens an item to see its terms, then explicitly chooses to buy or make an exchange offer. Sold and withdrawn listings leave the public inventory. An old announcement still opens the seller’s current listings, with an empty state when none are active.

Core owns item eligibility, listing state and order, and the rules for completing a trade. Clients initiate actions and display the resulting state. Any client can link directly to the same seller’s public trade inventory. The listing and its announcement are unilateral. A trade requires the other Bond’s action under the applicable interaction contract and is recorded in the BondChain of the seller and buyer upon completion. Browsing, a group reply, or an unaccepted offer does not complete a trade.

## Telegram group example

1. In the city group «0x1 • Kyiv», the seller sends `/trade@nilxone_bot`. The bot opens a seller-only flow to browse eligible items and choose what to list. The seller can complete it in the text client or via the Mini App using the same Core permissions. The group sees the announcement only after publication is confirmed.
2. For an Exclusive Skryabin record listed by `0x0skai`, the group sees exactly one line of message text and one button:

   > 0x0skai виставив Exclusive платівку

   **Button:** «Подивитися»

   Item name, price, and terms appear in the trade interface. The announcement is an ordinary group message visible to the group.
3. «Подивитися» opens the complete public trade inventory of `0x0skai`. The Exclusive Skryabin record is first because it is the newest listing at that moment. If `0x0skai` lists another record before someone opens the announcement, that newer listing is first.

## Related documents

- [Carrying Inventory, Containers, and Item Loss](inventory-carrying-and-loss.md)
- [City Exploration and Avaia Participation](city-exploration-and-avaia.md)
- [Text-first Clients and Telegram Topics](text-first-telegram-topics.md)
- [BondChain Interaction Model](../04-bondchain-interaction-model.md)
- [0x1 Core and Client Architecture](../18-core-and-client-architecture.md)
