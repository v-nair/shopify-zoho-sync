## Shopify + Zoho Data Sync

### 1. Approach

- **Fetch** orders from Shopify mock API and contacts from Zoho mock API via HTTPS.
- **Build** an in-memory map of email → user details for O(1) lookups.
- **Merge** each order with its customer by email, emitting a list of unified JSON objects.
- **Local Testing** via `python main.py` (prints sample output)



### 2. GCP Architecture

- Trigger: Cloud Scheduler → Pub/Sub → Cloud Function (HTTP subscription).

- Storage: Store the function's output JSON in a Cloud Storage bucket or load into BigQuery manually.

- Secrets: Manage API endpoints and tokens in Secret Manager, injected as environment variables.

```text
[Cloud Scheduler] (cron)
        ↓ Pub/Sub topic
   [Cloud Function]
        ↓ (HTTP response with merged JSON)
   [Cloud Storage / BigQuery]
```

### 3. Local Setup & Running
# 1. Create and activate a venv
python3 -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Populate .env in project root

# 4. Run locally
functions-framework --target=main


### 4. Sample Output (output.json)
```text
[
  {
    "order_id": 1,
    "order_total": "99.95",
    "customer_email": "sanjeev@example.com",
    "customer_name": "Sanjeev Gupta",
    "customer_company": "Innovate Inc."
  }
]
```

### output.json
[
  {
    "order_id": 1,
    "order_total": "99.95",
    "customer_email": "sanjeev@example.com",
    "customer_name": "Sanjeev Gupta",
    "customer_company": "Innovate Inc."
  }
]