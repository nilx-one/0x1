# Identity Service

The identity service is the Stage 1 registration surface for 0x1. It binds one immutable canonical `pub_dress` to one verified Telegram user ID without claiming native cryptographic identity or custodial recovery.

## Commands

- `/start` begins registration and requests a `pub_dress` in the next message.
- `/whoami` returns the stored provider-backed identity record.
- `/recover` explains the current Telegram recovery boundary.

Registration is the database insert. Exact-handle uniqueness and one-handle-per-Telegram-account are enforced by SQLite constraints.

## Telegram Mini App API

- `GET /api/v1/identity` returns the registered public identity projection.
- `POST /api/v1/identity/registration` accepts `{"discriminator":"0","slug":"sky"}` and registers `0x0sky`.
- `GET /health` reports process health without identity state.

Identity endpoints require `Authorization: tma <Telegram.WebApp.initData>`. The service verifies the Telegram HMAC, rejects duplicate fields, enforces a bounded `auth_date`, and derives the provider ID only from the verified `user` object. A collision response never discloses the existing provider binding.

## Run

Set `TELOXIDE_TOKEN` and optionally:

- `DATABASE_URL` — default `sqlite://identity.db`;
- `HTTP_BIND` — default `0.0.0.0:8080`;
- `TELEGRAM_INIT_DATA_MAX_AGE_SECONDS` — default `300`.

Then run:

```bash
cargo run --manifest-path identity-bot/Cargo.toml
```

The bot accepts identity actions only in private chats. The HTTP API accepts identity actions only after server-side Telegram Mini App authentication.

## Runtime package

[`Dockerfile`](Dockerfile) builds the combined Telegram bot and identity API. [`deploy/compose.yaml`](deploy/compose.yaml) persists SQLite state in a named volume and exposes only the private `ox1-identity:8080` edge alias. The canonical Web runtime proxies the bounded `/api/v1/identity*` surface to that alias.

CI validates the image and Compose contract but does not publish or deploy them.

## Verify

```bash
cargo fmt --manifest-path identity-bot/Cargo.toml --all -- --check
cargo clippy --manifest-path identity-bot/Cargo.toml --all-targets --all-features -- -D warnings
cargo test --manifest-path identity-bot/Cargo.toml --all-features
```

See [`../documents/04-identity.md`](../documents/04-identity.md) for the normative identity contract.

---

© 2026 aiaiaiai · aiaiaiai.org
