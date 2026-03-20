# Active Directory Stale Account Auditor

A Python script that reads a CSV export of Active Directory users and identifies accounts that haven't logged in within the last 90 days. Results are exported to a new CSV for review.

Built with `pandas` for efficient column-level operations on large user datasets.

---

## Requirements

- Python 3.x
- pandas

Install pandas if needed:
```bash
pip install pandas
```

---

## Usage

Place `audit_stale_accounts.py` in the same directory as your users CSV, then run:

```bash
python audit_stale_accounts.py
```

The script will prompt you to enter the filename:
```
Enter file name: users.csv
```

---

## Getting the Input CSV

On a Windows domain controller, export the required data using PowerShell:

```powershell
Get-ADUser -Filter {Enabled -eq $true} -Properties DisplayName, LastLogonDate |
Select-Object UserPrincipalName, DisplayName, LastLogonDate |
Export-Csv -Path "users.csv" -NoTypeInformation
```

The script expects a CSV with these headers:

| Header | Description |
|---|---|
| `UserPrincipalName` | User's login name (e.g. jsmith@company.com) |
| `DisplayName` | User's full name |
| `LastLogonTimestamp` | Last login date/time in ISO 8601 format |

---

## Output

A file named `stale_accounts_audit.csv` is created in the same directory, containing only the flagged accounts:

| UserPrincipalName | DisplayName | LastLogonTimestamp | DaysSinceLastLogon |
|---|---|---|---|
| bjones@company.com | Bob Jones | 2024-06-20 09:00:00+00:00 | 274 |
| dwilson@company.com | David Wilson | 2023-11-05 11:10:00+00:00 | 501 |

A summary is also printed to the terminal:
```
Audit complete. 2 stale account(s) found (inactive > 90 days).
Results exported to: stale_accounts_audit.csv
```

> **Note:** If `stale_accounts_audit.csv` already exists, it will be overwritten on each run. If the file is open in Excel, close it before running the script.

---

## Configuration

The stale account threshold is defined as a constant at the top of the script and can be adjusted as needed:

```python
STALE_THRESHOLD_DAYS = 90
```
