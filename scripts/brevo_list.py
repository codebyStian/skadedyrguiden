"""Finner (eller lager) Brevo-lista «Skadedyrbrevet» og skriver id-en. Leser BREVO_API_KEY fra miljøet (env B eller BREVO_API_KEY)."""
import json, os, urllib.request
K = os.environ.get("B") or os.environ["BREVO_API_KEY"]
def api(path, body=None):
    r = urllib.request.Request("https://api.brevo.com/v3" + path, data=json.dumps(body).encode() if body else None,
        headers={"api-key": K, "Content-Type": "application/json", "accept": "application/json"}, method="POST" if body else "GET")
    return json.load(urllib.request.urlopen(r, timeout=30))
for l in api("/contacts/lists?limit=50").get("lists", []):
    if l["name"] == "Skadedyrbrevet":
        print(l["id"]); raise SystemExit
folders = api("/contacts/folders?limit=10").get("folders", [])
fid = folders[0]["id"] if folders else api("/contacts/folders", {"name": "Kryp.as"})["id"]
print(api("/contacts/lists", {"name": "Skadedyrbrevet", "folderId": fid})["id"])
