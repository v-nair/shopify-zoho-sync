import json, logging, requests
from typing import Any, Dict, List
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from flask import Request, make_response
import config

# Set up structured logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO
)

# Shared retry strategy
RETRY_STRATEGY = Retry(
    total=3,
    backoff_factor=0.3,
    status_forcelist=[429, 500, 502, 503, 504],
    raise_on_status=False,
)

def create_session(headers: Dict) -> requests.Session:
    # Return a Session configured with the given headers and retry policy.
    session = requests.Session()
    session.headers.update(headers)
    adapter = HTTPAdapter(max_retries=RETRY_STRATEGY)
    session.mount("https://", adapter)
    return session

def get_shopify_session() -> requests.Session:
    return create_session({
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": config.SHOPIFY_ACCESS_TOKEN,
        "X-Shopify-Shop-Api-Call-Limit": "40/40"
    })

def get_zoho_session() -> requests.Session:
    return create_session({
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {config.ZOHO_ACCESS_TOKEN}",
        "X-com-zoho-organizationid": config.ZOHO_ORG_ID
    })

def fetch_json(url: str, session: requests.Session) -> Any:
    # Fetch JSON data from a given URL using the provided session
    resp = session.get(url, timeout=5)
    resp.raise_for_status() # Raise an error for bad responses
    return resp.json()

def merge_orders_with_contacts(orders: List, contacts: List) -> List:
    # one-time build of email → user
    user_map = {
        c.get("user", {}).get("email"): c["user"]
        for c in contacts
        if c.get("user", {}).get("email")
    }

    merged = []
    for order in orders:
        email = order.get("customer_email")
        user  = user_map.get(email, {})

        merged.append({
            "order_id": order.get("id"),
            "order_total": order.get("total_price"),
            "customer_email": email,
            "customer_name": user.get("name"),
            "customer_company": user.get("company"),
        })
    return merged

@functions_framework.http
def main(request: Request):
    logging.info("Fetching Shopify orders from %s", config.SHOPIFY_API_URL)
    logging.info("Fetching Zoho contacts from  %s", config.ZOHO_API_URL)

    shopify = get_shopify_session()
    zoho = get_zoho_session()

    try:
        orders = fetch_json(config.SHOPIFY_API_URL, shopify)
        contacts = fetch_json(config.ZOHO_API_URL, zoho)
    except requests.HTTPError as he:
        logging.exception("Upstream API error")
        return make_response(
            json.dumps({"error": str(he)}), 502, {"Content-Type": "application/json"}
        )
    except ValueError:
        logging.exception("Invalid JSON received")
        return make_response(
            json.dumps({"error": "Invalid JSON"}), 502, {"Content-Type": "application/json"}
        )

    if not orders:
        return make_response("", 204)

    result = merge_orders_with_contacts(orders, contacts)

    return make_response(
        json.dumps(result),
        200,
        {"Content-Type": "application/json"}
    )

if __name__ == "__main__":
    # Local test
    shopify = get_shopify_session()
    zoho = get_zoho_session()
    orders   = fetch_json(config.SHOPIFY_API_URL, shopify)
    contacts = fetch_json(config.ZOHO_API_URL, zoho)

    print(json.dumps(
        merge_orders_with_contacts(orders, contacts),
        indent=2
    ))
