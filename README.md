## Shopify + Zoho Data Sync

### 1. Approach

- **Fetch** orders from Shopify mock API and contacts from Zoho mock API via HTTPS.
- **Build** an in-memory map of email → user details for O(1) lookups.
- **Merge** each order with its customer by email, emitting a list of unified JSON objects.
- **Local Testing** via `python main.py` (prints sample output)

### 2. GCP Architecture

```plaintext
[Cloud Scheduler] (cron)
        ↓ Pub/Sub topic
   [Cloud Function]
        ↓ (HTTP response with merged JSON)
   [Cloud Storage / BigQuery]
```plaintext

- Trigger: Cloud Scheduler → Pub/Sub → Cloud Function (HTTP subscription).

- Storage: Store the function's output JSON in a Cloud Storage bucket or load into BigQuery manually.

- Secrets: Manage API endpoints and tokens in Secret Manager, injected as environment variables.

