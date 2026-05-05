# Streamlit Full User Form with Cloud DB Save

This project creates a Streamlit user form using core input widgets and saves submitted data to a cloud database:

- MongoDB Atlas
- Appwrite

## 1) Setup

### Prerequisites

- Python 3.10+
- A MongoDB Atlas cluster OR an Appwrite Cloud project

### Install

```powershell
pip install -r requirements.txt
```

### Configure environment

Copy `.env.example` to `.env` and fill the values for the backend you plan to use.

```powershell
Copy-Item .env.example .env
```

## 2) Run app

```powershell
streamlit run app.py
```

## 3) MongoDB Atlas notes

Use these variables in `.env`:

- `MONGODB_URI`
- `MONGODB_DB_NAME`
- `MONGODB_COLLECTION_NAME`

Ensure your Atlas network access and DB user permissions allow insert operations.

## 4) Appwrite notes

Use these variables in `.env`:

- `APPWRITE_ENDPOINT`
- `APPWRITE_PROJECT_ID`
- `APPWRITE_API_KEY`
- `APPWRITE_DATABASE_ID`
- `APPWRITE_COLLECTION_ID`

Also ensure:

- The collection has attributes that match the submitted data schema you want to store.
- The API key has database write permissions.

## 5) What the app captures

The form includes many Streamlit inputs such as:

- text input
- password input
- text area
- number input
- date input
- time input
- radio
- selectbox
- multiselect
- slider
- select slider
- color picker
- checkbox
- toggle
- file uploader (single and multiple)
- camera input
- data editor

On submit, the app stores the form payload in your selected cloud backend.
