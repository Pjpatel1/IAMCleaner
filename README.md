Automatically detects and revokes unused IAM roles to enforce least privilege.  
**Aligned with Yelp's IAM team goals** (automation, access governance).

## Features
- ✅ **Detects stale roles** (unused for >90 days or never used).
- ✅ **Dry-run mode** for safe testing.
- ✅ **CSV reports** for compliance audits.
- ✅ **Simulated IAM** (no AWS needed).

## How It Works
1. Scans mock IAM roles (`mock_iam_roles.py`).
2. Flags unused roles based on `last_used` timestamp.
3. Exports results to `unused_roles.csv`.

## Run It
```bash
# Dry run (safe)
python iam_cleaner.py --dry-run

# Real execution (deletes from mock DB)
python iam_cleaner.py