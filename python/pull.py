import requests
import pandas as pd
from auth import headers, ZAP_DOMAIN

def main():
    skipTokenParams = requests.get(
        "https://zap-api-production.herokuapp.com/projects"
    ).json()["meta"]["skipTokenParams"]
    nextlink = f"{ZAP_DOMAIN}/api/data/v9.1/dcp_projects?{skipTokenParams}"
    counter = 0

    while nextlink != "":
        result = requests.get(nextlink, headers=headers).json()
        pd.DataFrame(result["value"]).to_csv(f"dump_{counter}.csv", index=False)
        counter += 1
        nextlink = result.get("@odata.nextLink", "")

if __name__ == "__main__":
    main()