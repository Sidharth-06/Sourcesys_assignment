# Streamlit Support Ticket System

A clean Streamlit app for submitting support tickets and saving them directly to Appwrite.

## Features

- Native Streamlit form with a dark UI
- Contact details, issue classification, priority, and resolution preferences
- File uploads for screenshots, logs, and supporting documents
- Appwrite-only persistence using the Python SDK
- Ticket preview before submission

## Project Structure

- `app.py` - main Streamlit application
- `data_viz_app.py` - Streamlit dashboard for visualizing uploaded data
- `requirements.txt` - Python dependencies
- `.env.example` - sample Appwrite configuration
- `appwrite.config.json` - Appwrite CLI configuration

## Setup

### 1. Install dependencies

```powershell
py -3.10 -m pip install -r requirements.txt
```

### 2. Configure Appwrite credentials

Copy the sample environment file and fill in your Appwrite values:

```powershell
Copy-Item .env.example .env
```

You can also use Streamlit secrets instead of `.env` by creating `.streamlit/secrets.toml`:

```toml
[appwrite]
endpoint = "https://fra.cloud.appwrite.io/v1"
project_id = "YOUR_PROJECT_ID"
api_key = "YOUR_API_KEY"
database_id = "YOUR_DATABASE_ID"
collection_id = "YOUR_COLLECTION_ID"
```

## Run

```powershell
streamlit run app.py
```

To open the visualization dashboard instead, run:

```powershell
streamlit run data_viz_app.py
```

If you want to make the app reachable on your local network, use:

```powershell
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## Appwrite Requirements

Make sure the Appwrite collection or table has fields that match the ticket payload. The app stores:

- `submitted_at`
- `full_name`
- `email`
- `phone`
- `company`
- `ticket_type`
- `priority`
- `category`
- `date_issue_started`
- `subject`
- `description`
- `impact_level`
- `affected_systems`
- `can_reproduce`
- `preferred_contact_method`
- `urgency`
- `subscribe_updates`
- `agree_followup`
- `error_log`
- `additional_files`

## Notes

- The app uses Appwrite SDK calls only.
- If you change the Appwrite schema, update the database/table attributes accordingly.
- The form is designed to be practical for helpdesk or internal support use.
