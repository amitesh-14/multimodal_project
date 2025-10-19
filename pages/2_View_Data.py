# pages/2_View_Data.py
import streamlit as st
from utils import fetch_all_documents_from_db, delete_row_from_db

st.set_page_config(page_title="View Data", page_icon="📊")
st.title("📊 View Stored Data")

data = fetch_all_documents_from_db()

if data:
    # Create a header for your table
    col_headers = st.columns([3, 2, 2, 4, 1])
    headers = ["File Name", "File Type", "Upload Time", "Text Preview", "Action"]
    for col, header in zip(col_headers, headers):
        col.subheader(header)
    
    st.markdown("---")

    # Display data for each row
    for row in data:
        row_id, file_name, file_type, extracted_text, upload_time = row
        
        col_data = st.columns([3, 2, 2, 4, 1])
        col_data[0].write(file_name)
        col_data[1].write(file_type)
        col_data[2].write(upload_time)
        
        # Text Preview and Expander
        preview_text = (extracted_text[:100] + "...") if len(extracted_text) > 100 else extracted_text
        col_data[3].write(preview_text)
        with col_data[3].expander("View Full Text"):
            st.write(extracted_text)

        # Delete Button
        if col_data[4].button("Delete", key=f"delete_{row_id}"):
            delete_row_from_db(row_id)
            st.success(f"✅ Deleted '{file_name}'.")
            st.rerun()
else:
    st.info("ℹ️ No data found in the database.")