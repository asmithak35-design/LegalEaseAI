
import streamlit as st
import requests
from datetime import date

API_URL = "http://127.0.0.1:8000/generate"

st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️",
    layout="centered"
)

st.title("⚖️ LegalEase AI")
st.subheader("AI-Powered Legal Document Generator")
st.write("Generate a draft legal document using AI.")

document_type = st.selectbox(
    "Select Document Type",
    [
        "Rental Agreement",
        "Employment Agreement",
        "Non-Disclosure Agreement",
        "Service Agreement",
        "Partnership Agreement",
        "General Legal Document"
    ]
)

party_one = st.text_input("First Party Name")
party_two = st.text_input("Second Party Name")
effective_date = st.date_input(
    "Effective Date",
    value=date.today()
)
terms = st.text_area(
    "Terms and Conditions",
    placeholder="Enter the important terms...",
    height=150
)

if st.button("Generate Document", type="primary"):
    if not party_one.strip() or not party_two.strip() or not terms.strip():
        st.warning("Please fill in all required fields.")
    else:
        payload = {
            "document_type": document_type,
            "party_one": party_one,
            "party_two": party_two,
            "terms": terms,
            "effective_date": str(effective_date)
        }

        try:
            with st.spinner("Generating your document..."):
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=120
                )

            if response.ok:
                document = response.json()["document"]

                st.session_state["legal_document"] = document
                st.success("Document generated successfully!")

            else:
                st.error(f"API Error: {response.text}")

        except requests.RequestException as error:
            st.error(
                "Could not connect to the backend. "
                "Please start the backend first."
            )
            st.caption(str(error))

if "legal_document" in st.session_state:
    st.subheader("Generated Document")

    edited_document = st.text_area(
        "Edit your document here",
        value=st.session_state["legal_document"],
        height=350,
        key="edited_document"
    )

    st.download_button(
        "Download as TXT",
        data=edited_document,
        file_name="legal_document.txt",
        mime="text/plain"
    )

    st.info(
        "This is an AI-generated draft, not legal advice. "
        "Ask a qualified lawyer to review it before use."
    )
