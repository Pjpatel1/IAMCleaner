from datetime import datetime, timedelta

# Mock database of IAM roles and their last usage
mock_iam_roles = {
    "developer-role": {
        "policies": ["s3-read-only", "ec2-describe-instances"],
        "last_used": "2024-01-15",  # Over 90 days ago (stale)
    },
    "admin-role": {
        "policies": ["admin-full-access"],
        "last_used": "2024-03-28",  # Recently used (safe)
    },
    "ci-cd-role": {
        "policies": ["code-deploy", "lambda-invoke"],
        "last_used": None,  # Never used (high risk)
    }
}