import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Define constants
NUM_RECORDS = 1000  # Number of records to generate
PRIORITIES = ["Low", "Medium", "High", "Critical"]
STATUSES = ["Open", "In Progress", "Resolved"]
SERVICES = ["Payment Service", "Auth Service", "Database B", "Notification Service"]
APPS = ["Online Banking App", "Mobile Banking App", "Backend API"]
ENVIRONMENTS = ["Production", "Staging", "Development"]
KB_ARTICLES = [f"KB{str(i).zfill(3)}" for i in range(1, 101)]  # KB001 to KB100

# Define realistic incident titles and descriptions
INCIDENT_TITLES = [
    "High CPU usage on {service}",
    "Memory leak in {service}",
    "{service} connection timeout",
    "API latency spike in {service}",
    "Failed transactions in {service}",
    "{service} not responding",
    "Database deadlock in {service}",
    "Notification failure in {service}",
]

INCIDENT_DESCRIPTIONS = [
    "Users are experiencing high latency when accessing {service}.",
    "{service} is consuming excessive memory, causing system slowdowns.",
    "Connection attempts to {service} are timing out.",
    "API requests to {service} are failing with 500 errors.",
    "Transactions in {service} are failing due to database issues.",
    "{service} is unresponsive, causing service degradation.",
    "A deadlock in {service} is blocking critical operations.",
    "Notifications from {service} are not being delivered to users.",
]

# Function to generate a single incident record
def generate_incident():
    service = random.choice(SERVICES)
    app = random.choice(APPS)
    incident_id = f"INC{fake.unique.random_int(min=1, max=999999):06}"
    title = random.choice(INCIDENT_TITLES).format(service=service)
    description = random.choice(INCIDENT_DESCRIPTIONS).format(service=service)
    priority = random.choices(PRIORITIES, weights=[0.4, 0.3, 0.2, 0.1])[0]  # Higher weight for Low/Medium
    status = random.choice(STATUSES)
    reported_by = fake.name()
    reported_date = fake.date_time_between(start_date="-1y", end_date="now")
    resolved_by = fake.name() if status == "Resolved" else None
    resolved_date = (
        fake.date_time_between(start_date=reported_date, end_date="now")
        if status == "Resolved"
        else None
    )
    resolution_notes = (
        f"Restarted {service}." if status == "Resolved" and random.random() > 0.5 else
        f"Fixed memory leak in {service}." if status == "Resolved" and random.random() > 0.5 else
        f"Resolved database deadlock in {service}." if status == "Resolved" else None
    )
    cpu_usage = round(random.uniform(10, 100), 2)
    memory_usage = round(random.uniform(10, 100), 2)
    related_incidents = (
        f"INC{fake.unique.random_int(min=1, max=999999):06}, INC{fake.unique.random_int(min=1, max=999999):06}"
        if random.random() > 0.7 and status != "Open"
        else None
    )
    kb_article_id = random.choice(KB_ARTICLES) if random.random() > 0.5 else None

    return {
        "incident_id": incident_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": status,
        "reported_by": reported_by,
        "reported_date": reported_date,
        "resolved_by": resolved_by,
        "resolved_date": resolved_date,
        "resolution_notes": resolution_notes,
        "affected_app": app,
        "affected_microservice": service,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "related_incidents": related_incidents,
        "kb_article_id": kb_article_id,
    }

# Generate data
data = []
for _ in range(NUM_RECORDS):
    data.append(generate_incident())

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("realistic_incident_data_1000.csv", index=False)

print(f"Generated {NUM_RECORDS} records and saved to 'realistic_incident_data_1000.csv'.")