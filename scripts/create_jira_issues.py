import os
from jira import JIRA

# Read env vars injected by GitHub Actions
EMAIL = os.getenv("JIRA_EMAIL")
TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = os.getenv("JIRA_URL")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "SCRUM")
 # default to SCRUM

def get_jira_client():
    if not (EMAIL and TOKEN and JIRA_URL):
        raise RuntimeError("Missing Jira credentials. Check env vars.")
    return JIRA(server=JIRA_URL, basic_auth=(EMAIL, TOKEN))

def create_issue(summary, description, issue_type="Task"):
    jira = get_jira_client()
    issue_dict = {
        "project": {"key": PROJECT_KEY},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
    }
    issue = jira.create_issue(fields=issue_dict)
    print(f"Created issue: {issue.key}")
    return issue

if __name__ == "__main__":
    tasks = [
        ("Implement User Entity", "Develop User model + unit tests."),
        ("Implement Product Entity", "Develop Product model + unit tests."),
        ("Implement CartItem Entity", "Develop CartItem model + unit tests."),
        ("Write Integration Tests", "Test User–Cart–Product relationships."),
    ]

    for title, desc in tasks:
        create_issue(title, desc)
