# Identity Bot

The identity bot is the Stage 1 registration surface for 0x1. It binds one immutable canonical `pub_dress` to one Telegram user ID without claiming native cryptographic identity or custodial recovery.

## Commands

- `/start` begins registration and requests a `pub_dress` in the next message.
- `/whoami` returns the stored provider-backed identity record.
- `/recover` explains the current Telegram recovery boundary.

Registration is the database insert. Exact-handle uniqueness and one-handle-per-Telegram-account are enforced by SQLite constraints.

## Run

Set `TELOXIDE_TOKEN` and optionally `DATABASE_URL` (default: `sqlite://identity.db`), then run:

```bash
cargo run --manifest-path identity-bot/Cargo.toml
```

The bot accepts identity actions only in private chats.

## Verify

```bash
cargo fmt --manifest-path identity-bot/Cargo.toml --all -- --check
cargo clippy --manifest-path identity-bot/Cargo.toml --all-targets --all-features -- -D warnings
cargo test --manifest-path identity-bot/Cargo.toml --all-features
```

See [`../documents/04-identity.md`](../documents/04-identity.md) for the normative identity contract.

---

© 2026 aiaiaiai · aiaiaiai.org
