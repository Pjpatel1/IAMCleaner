import csv
from datetime import datetime, timedelta
from argparse import ArgumentParser
from mock_iam_roles import mock_iam_roles


def send_slack_alert(unused_roles):
    """Send a formatted Slack message about unused roles."""
    if not unused_roles:
        return
    
    message = {
        "text": "🚨 *Unused IAM Roles Detected*",
        "attachments": [
            {
                "color": "#ff0000",
                "fields": [
                    {
                        "title": "Role Name",
                        "value": "\n".join([role for role, _ in unused_roles]),
                        "short": True
                    },
                    {
                        "title": "Reason",
                        "value": "\n".join([reason for _, reason in unused_roles]),
                        "short": True
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        response.raise_for_status()  # Raise error if HTTP request fails
        print("Slack alert sent successfully!")
    except Exception as e:
        print(f"Failed to send Slack alert: {e}")


def find_unused_roles(roles, threshold_days=90):
    unused_roles = []
    today = datetime.now()
    
    for role_name, details in roles.items():
        last_used = details["last_used"]
        
        if last_used is None:
            unused_roles.append((role_name, "Never used"))
            continue
            
        last_used_date = datetime.strptime(last_used, "%Y-%m-%d")
        days_unused = (today - last_used_date).days
        
        if days_unused > threshold_days:
            unused_roles.append((role_name, f"Unused for {days_unused} days"))
    
    return unused_roles

def remediate_roles(unused_roles, dry_run=True):
    for role, reason in unused_roles:
        if dry_run:
            print(f"[DRY RUN] Would revoke {role} ({reason})")
        else:
            print(f"Revoked {role} ({reason})")
            mock_iam_roles.pop(role)  # Remove from mock DB

def export_to_csv(unused_roles, filename="unused_roles.csv"):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Role Name", "Reason", "Last Used"])
        for role, reason in unused_roles:
            last_used = mock_iam_roles.get(role, {}).get("last_used", "Unknown")
            writer.writerow([role, reason, last_used])

def main():
    parser = ArgumentParser(description="IAM Role Cleanup Tool")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without deleting")
    args = parser.parse_args()

    unused = find_unused_roles(mock_iam_roles)
    send_slack_alert(unused)
    remediate_roles(unused, dry_run=args.dry_run)
    export_to_csv(unused)

if __name__ == "__main__":
    main()