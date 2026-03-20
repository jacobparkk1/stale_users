import pandas as pd
import os
from datetime import datetime, timezone

# Configuration
timestamp = datetime.now().strftime("%Y-%m-%d")
OUTPUT_FILE = f"stale_accounts_audit_{timestamp}.csv"
STALE_THRESHOLD_DAYS = 90

def audit_stale_accounts():

	# Receive and verify filename
    input_file = input("Enter file name: ")
    if not os.path.exists(input_file): # 
        print(f"Error: '{input_file}' not found.")
        return

    # Load the CSV
    df = pd.read_csv(input_file)

    # Parse LastLogonTimestamp as datetime (UTC-aware)
    df["LastLogonDate"] = pd.to_datetime(df["LastLogonDate"], utc=True)

    # Get current UTC time
    now = datetime.now(timezone.utc)

    # Calculate days since last logon
    df["DaysSinceLastLogon"] = (now - df["LastLogonDate"]).dt.days

    # Filter for stale accounts (>90 days since logon)
    stale_df = df[df["DaysSinceLastLogon"] > STALE_THRESHOLD_DAYS].copy()

    # Reorder columns for the output report
    output_df = stale_df[["UserPrincipalName", "DisplayName", "LastLogonDate", "DaysSinceLastLogon"]]

    # Export to CSV
    output_df.to_csv(OUTPUT_FILE, index=False)

    # Summary
    print(f"Audit complete. {len(output_df)} stale account(s) found (inactive > {STALE_THRESHOLD_DAYS} days).")
    print(f"Results exported to: {OUTPUT_FILE}")

if __name__ == "__main__":
    audit_stale_accounts()
