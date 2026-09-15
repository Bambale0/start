# Integration Adapters

External providers are implemented behind typed ports.

Planned provider classes:

- AccountingProvider
- EDOProvider
- BankProvider
- EmailProvider
- TelephonyProvider
- MessengerProvider
- StorageProvider

Every adapter defines authentication, timeout, retry, rate-limit, idempotency, webhook, reconciliation and observability behavior.

Provider-specific payloads remain inside the adapter boundary.
