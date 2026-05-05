import json
import os
import importlib
from datetime import datetime
from typing import Any, Dict, List, Optional, cast

import streamlit as st
from dotenv import load_dotenv

try:
    from appwrite.client import Client
    from appwrite.exception import AppwriteException
    from appwrite.id import ID
    try:
        Tables = getattr(importlib.import_module("appwrite.services.tables"), "Tables", None)
    except Exception:
        Tables = None
    try:
        Databases = getattr(importlib.import_module("appwrite.services.databases"), "Databases", None)
    except Exception:
        Databases = None
except ImportError:
    Client = None
    AppwriteException = Exception
    ID = None
    Tables = None
    Databases = None

load_dotenv()

st.set_page_config(page_title="Support Ticket System", page_icon="🎫", layout="centered")

# ── Hide Streamlit chrome for a cleaner look ──────────────────────────────────
st.markdown("""
<style>
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1rem !important; max-width: 720px; }
</style>
""", unsafe_allow_html=True)


# ── Appwrite helpers ──────────────────────────────────────────────────────────

def _file_meta(uploaded_file: Optional[Any]) -> Optional[Dict[str, Any]]:
    if not uploaded_file:
        return None
    return {"name": uploaded_file.name, "type": uploaded_file.type, "size": uploaded_file.size}


def _files_meta(uploaded_files: List[Any]) -> List[Dict[str, Any]]:
    files_meta = [_file_meta(f) for f in uploaded_files if f]
    return [meta for meta in files_meta if meta is not None]


def _response_id(response: Any, default: str = "created") -> str:
    if isinstance(response, dict):
        for key in ("$id", "$uid", "id"):
            value = response.get(key)
            if value:
                return str(value)

    for attr_name in ("$id", "$uid", "id"):
        try:
            value = getattr(response, attr_name)
        except Exception:
            continue
        if value:
            return str(value)

    return default


def save_to_appwrite(document: Dict[str, Any]) -> str:
    s = {}
    try:
        if hasattr(st, "secrets") and "appwrite" in st.secrets:
            s = dict(st.secrets["appwrite"])
    except Exception:
        s = {}

    endpoint = s.get("endpoint") or os.getenv("APPWRITE_ENDPOINT", "")
    project_id = s.get("project_id") or os.getenv("APPWRITE_PROJECT_ID", "")
    api_key = s.get("api_key") or os.getenv("APPWRITE_API_KEY", "")
    database_id = s.get("database_id") or os.getenv("APPWRITE_DATABASE_ID", "")
    collection_id = s.get("collection_id") or os.getenv("APPWRITE_COLLECTION_ID", "")

    if not all([endpoint, project_id, api_key, database_id, collection_id]):
        raise ValueError(
            "Appwrite configuration is missing. "
            "Set Streamlit secrets under [appwrite] or the APPWRITE_* environment variables."
        )

    appwrite_document = {
        "submitted_at": document.get("submitted_at"),
        "full_name": document.get("full_name", ""),
        "email": document.get("email", ""),
        "db_backend": document.get("db_backend", "Appwrite"),
        "payload_json": json.dumps(document, default=str),
    }

    if Client is None:
        raise RuntimeError("Appwrite SDK not installed. Run: pip install appwrite")

    if Tables is not None:
        client = Client().set_endpoint(endpoint).set_project(project_id).set_key(api_key)
        tables_factory = cast(Any, Tables)
        tables = tables_factory(client)
        try:
            resp = tables.create_row(database_id=database_id, collection_id=collection_id, data=appwrite_document)
        except TypeError:
            resp = tables.create_row(database_id, collection_id, appwrite_document)
        return _response_id(resp)

    if Databases is not None:
        if ID is None:
            raise RuntimeError("Appwrite SDK ID helper is unavailable.")
        client = Client().set_endpoint(endpoint).set_project(project_id).set_key(api_key)
        databases_factory = cast(Any, Databases)
        databases = databases_factory(client)
        try:
            resp = databases.create_document(
                database_id=database_id,
                collection_id=collection_id,
                document_id=ID.unique(),
                data=appwrite_document,
            )
        except Exception:
            resp = databases.create_document(database_id, collection_id, ID.unique(), appwrite_document)
        return _response_id(resp)

    raise RuntimeError("Appwrite SDK installed but neither Tables nor Databases service is available.")


# ── Streamlit App ─────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
      #MainMenu, footer, header { visibility: hidden; }
      .stApp {
        background:
          radial-gradient(circle at top, rgba(56, 189, 248, 0.10), transparent 35%),
          linear-gradient(180deg, #090d14 0%, #0d1320 52%, #090d14 100%);
      }
      .block-container {
        padding-top: 1.5rem !important;
        max-width: 980px;
      }
      div[data-testid="stForm"] {
        border: 1px solid #1f2c3d;
        border-radius: 18px;
        padding: 1.5rem;
        background: rgba(11, 18, 32, 0.86);
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
      }
      div[data-testid="stForm"] label,
      div[data-testid="stForm"] p,
      div[data-testid="stForm"] span {
        color: #d9e2f0;
      }
      div[data-testid="stTextInput"] input,
      div[data-testid="stTextArea"] textarea,
      div[data-testid="stSelectbox"] div,
      div[data-testid="stMultiSelect"] div,
      div[data-testid="stDateInput"] input,
      div[data-testid="stTimeInput"] input {
        background-color: #111a27 !important;
        color: #edf4ff !important;
        border-color: #243244 !important;
      }
      .stButton > button {
        background: linear-gradient(135deg, #38bdf8 0%, #0f172a 100%);
        color: #f5f9ff;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.25rem;
      }
      .stButton > button:hover { opacity: 0.92; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Support Ticket System")
st.caption("Submit support tickets and store them directly in Appwrite.")

with st.container(border=False):
    st.markdown("### Tell us what’s happening")
    st.markdown(
        "We review every ticket and respond within your selected timeframe. The more detail you share, the faster we can help."
    )

with st.form("support_ticket_form", clear_on_submit=True):
    st.subheader("Your details")
    contact_left, contact_right = st.columns(2)
    with contact_left:
        full_name = st.text_input("Full name *", placeholder="John Smith")
        email = st.text_input("Email address *", placeholder="john@example.com")
    with contact_right:
        phone = st.text_input("Phone number", placeholder="+1 (555) 123-4567")
        company = st.text_input("Company / Organization", placeholder="Your Company")

    st.subheader("Issue type")
    issue_type = st.radio(
        "How should we categorize this ticket?",
        ["Problem", "Question", "Complaint", "Suggestion"],
        horizontal=True,
    )

    st.subheader("Priority")
    priority = st.radio(
        "How urgent is it?",
        ["Low", "Medium", "High", "Urgent"],
        horizontal=True,
    )

    st.subheader("Issue details")
    details_left, details_right = st.columns(2)
    with details_left:
        category = st.selectbox(
            "Category",
            ["Technical Issue", "Billing", "Account Access", "Feature Request", "Bug Report", "Other"],
        )
        date_issue_started = st.date_input("Date issue started", value=datetime.utcnow().date())
    with details_right:
        subject = st.text_input("Subject *", placeholder="Brief description of your issue")
        impact_level = st.slider("Impact level", min_value=1, max_value=5, value=2, step=1)

    description = st.text_area(
        "Detailed description *",
        placeholder="What happened? What did you expect? Include any error messages you received.",
        height=150,
    )

    st.subheader("Affected systems")
    affected_systems = st.multiselect(
        "Select all that apply",
        ["Dashboard", "API", "Mobile App", "Web Portal", "Integrations", "Reporting"],
        default=["Dashboard"],
    )
    can_reproduce = st.checkbox("I can reliably reproduce this issue")

    st.subheader("Attachments")
    attachment_left, attachment_right = st.columns(2)
    with attachment_left:
        error_log = st.file_uploader("Error log / screenshot", type=["txt", "log", "png", "jpg", "pdf"])
    with attachment_right:
        additional_files = st.file_uploader(
            "Additional files",
            accept_multiple_files=True,
            type=["pdf", "xlsx", "csv", "jpg", "png"],
        )

    st.subheader("Resolution preferences")
    resolution_left, resolution_right = st.columns(2)
    with resolution_left:
        preferred_contact_method = st.selectbox(
            "Preferred contact method",
            ["Email", "Phone", "In-App Notification", "No Preference"],
        )
        urgency = st.selectbox(
            "Resolution window",
            ["Within 1 week", "Within 3 days", "Within 1 day", "Immediately"],
        )
    with resolution_right:
        subscribe_updates = st.checkbox("Send me status updates by email", value=True)
        agree_followup = st.checkbox("I agree to be contacted for clarification if needed")

    submitted = st.form_submit_button("Submit support ticket")

if submitted:
    missing = []
    if not full_name.strip():
        missing.append("Full name")
    if not email.strip():
        missing.append("Email address")
    if not subject.strip():
        missing.append("Subject")
    if not description.strip():
        missing.append("Detailed description")
    if not agree_followup:
        missing.append("Agreement to be contacted")

    if missing:
        st.error("Please fill in: " + ", ".join(missing) + ".")
    else:
        submission = {
            "submitted_at": datetime.utcnow().isoformat() + "Z",
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "company": company,
            "ticket_type": issue_type,
            "priority": priority,
            "category": category,
            "date_issue_started": str(date_issue_started),
            "subject": subject,
            "description": description,
            "impact_level": int(impact_level),
            "affected_systems": affected_systems,
            "can_reproduce": can_reproduce,
            "preferred_contact_method": preferred_contact_method,
            "urgency": urgency,
            "subscribe_updates": subscribe_updates,
            "agree_followup": agree_followup,
            "error_log": _file_meta(error_log),
            "additional_files": _files_meta(additional_files),
            "db_backend": "Appwrite",
        }

        with st.expander("Ticket preview", expanded=False):
            st.json(submission)

        try:
            doc_id = save_to_appwrite(submission)
            st.success(
                f"✅ Ticket saved to Appwrite!\n\n"
                f"**Ticket ID:** {doc_id}\n\n"
                f"We'll contact {submission['email']} within {urgency.lower()}."
            )
        except Exception as exc:
            st.error(f"Appwrite save failed: {exc}")
            st.info("Check your Appwrite secrets or environment variables and try again.")