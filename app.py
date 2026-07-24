import streamlit as st
import os
import tempfile
import time
import pandas as pd
import matplotlib.pyplot as plt

from redactor import PIIRedactor

# ======================================================
# Initialize Redactor
# ======================================================

redactor = PIIRedactor()

# ======================================================
# Page Configuration
# ======================================================

st.set_page_config(
    page_title="PII Redaction Tool",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# Title
# ======================================================

st.title("🔒 Intelligent PII Redaction Tool")

st.markdown(
"""
Automatically detect and replace Personally Identifiable Information (PII)
from Microsoft Word documents while preserving document formatting.

### Supported Detection

- Regex
- spaCy
- Microsoft Presidio

### Supported Replacement

- Fake Names
- Fake Emails
- Fake Phone Numbers
- Fake Companies
- Fake Addresses
- PAN
- Credit Card
- IP Address
"""
)

st.divider()

# ======================================================
# Sidebar
# ======================================================

with st.sidebar:

    st.header("About")

    st.success(
        "Hybrid PII Detection Engine"
    )

    st.markdown(
        """
### Features

✅ Batch Detection

✅ Regex

✅ spaCy

✅ Presidio

✅ Formatting Preserved

✅ CSV Log

✅ DOCX Support

✅ Analytics Dashboard
"""
    )

# ======================================================
# Upload
# ======================================================

uploaded_file = st.file_uploader(
    "Upload DOCX Document",
    type=["docx"]
)

if uploaded_file is None:

    st.info("Please upload a DOCX file.")

    st.stop()

# ======================================================
# Temporary Directory
# ======================================================

if "temp_dir" not in st.session_state:
    st.session_state.temp_dir = tempfile.mkdtemp()

temp_dir = st.session_state.temp_dir
input_path = os.path.join(
    temp_dir,
    uploaded_file.name
)

with open(input_path, "wb") as file:

    file.write(
        uploaded_file.getbuffer()
    )

output_path = os.path.join(
    temp_dir,
    "Redacted_" + uploaded_file.name
)

log_path = os.path.join(
    temp_dir,
    "redaction_log.csv"
)

# ======================================================
# Redaction Button
# ======================================================

if st.button(
    "🚀 Start Redaction",
    use_container_width=True
):

    redactor.reset()

    progress = st.progress(0)

    status = st.empty()

    try:

        status.info("Loading document...")

        progress.progress(10)

        start_time = time.time()

        with st.spinner(
            "Detecting and Redacting PII..."
        ):

            progress.progress(30)

            redactor.redact_document(
                input_path,
                output_path,
                log_path
            )

            progress.progress(90)

        elapsed = time.time() - start_time

        progress.progress(100)

        status.success(
            f"✅ Completed in {elapsed:.2f} seconds"
        )

    except Exception as e:

        st.error(
            f"❌ {str(e)}"
        )

        st.stop()

# ======================================================
# Results
# ======================================================

if os.path.exists(output_path):

    stats = redactor.get_statistics()

    log_df = pd.DataFrame(
        redactor.get_logs()
    )

    st.divider()

    st.header("📊 Redaction Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Entities",
            stats["entities"]
        )

    with col2:

        st.metric(
            "Paragraphs",
            stats["paragraphs"]
        )

    with col3:

        st.metric(
            "Tables",
            stats["tables"]
        )

    with col4:

        st.metric(
            "Headers",
            stats["headers"]
        )

    st.divider()

    # ======================================================
    # Download Buttons
    # ======================================================

    c1, c2 = st.columns(2)

    with open(output_path, "rb") as file:

        c1.download_button(

            "📥 Download Redacted Document",

            file,

            os.path.basename(output_path),

            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",

            use_container_width=True

        )

    with open(log_path, "rb") as file:

        c2.download_button(

            "📄 Download CSV Log",

            file,

            "redaction_log.csv",

            mime="text/csv",

            use_container_width=True

        )

    st.divider()

    st.subheader("📋 Redaction Log")

    st.dataframe(

        log_df,

        use_container_width=True,

        hide_index=True

    )

    st.divider()
    # ======================================================
    # Analytics Dashboard
    # ======================================================

    st.header("📈 Analytics Dashboard")

    if len(log_df) > 0:

        # ------------------------------------------
        # Entity Counts
        # ------------------------------------------

        entity_counts = (

            log_df["Entity"]

            .value_counts()

            .reset_index()

        )

        entity_counts.columns = [

            "Entity",

            "Count"

        ]

        st.subheader("Entity Distribution")

        st.dataframe(

            entity_counts,

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        # ------------------------------------------
        # Charts
        # ------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Bar Chart")

            st.bar_chart(

                entity_counts.set_index(

                    "Entity"

                )

            )

        with col2:

            st.subheader("Pie Chart")

            fig, ax = plt.subplots(

                figsize=(6, 6)

            )

            ax.pie(

                entity_counts["Count"],

                labels=entity_counts["Entity"],

                autopct="%1.1f%%",

                startangle=90

            )

            ax.axis("equal")

            st.pyplot(fig)

        st.divider()

        # ------------------------------------------
        # Statistics
        # ------------------------------------------

        st.subheader("📊 Statistics")

        total_replacements = len(log_df)

        unique_original = (

            log_df["Original"]

            .nunique()

        )

        unique_fake = (

            log_df["Fake"]

            .nunique()

        )

        total_types = (

            log_df["Entity"]

            .nunique()

        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(

                "Total Replacements",

                total_replacements

            )

        with c2:

            st.metric(

                "Unique Original PII",

                unique_original

            )

        with c3:

            st.metric(

                "Unique Fake Values",

                unique_fake

            )

        with c4:

            st.metric(

                "Entity Types",

                total_types

            )

        st.divider()

        # ------------------------------------------
        # Search Log
        # ------------------------------------------

        st.subheader("🔍 Search Redaction Log")

        search = st.text_input(

            "Search Original or Fake Value"

        )

        if search:

            filtered = log_df[

                log_df.apply(

                    lambda row:

                    search.lower()

                    in str(row).lower(),

                    axis=1

                )

            ]

            st.dataframe(

                filtered,

                use_container_width=True,

                hide_index=True

            )

        else:

            st.dataframe(

                log_df,

                use_container_width=True,

                hide_index=True

            )

        st.divider()

        # ------------------------------------------
        # Download Analytics CSV
        # ------------------------------------------

        csv = log_df.to_csv(

            index=False

        ).encode("utf-8")

        st.download_button(

            "⬇ Download Redaction Log",

            csv,

            "redaction_log.csv",

            "text/csv",

            use_container_width=True

        )

    else:

        st.warning(

            "No PII detected in the document."

        )

    st.divider()
# ======================================================
# Performance Dashboard
# ======================================================

    st.header("⚡ Performance Dashboard")

    stats = redactor.get_statistics()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.info(
            f"""
    ### 📄 Document

    Paragraphs : **{stats['paragraphs']}**

    Tables : **{stats['tables']}**

    Headers : **{stats['headers']}**

    Footers : **{stats['footers']}**
    """
        )

    with c2:

        st.success(
            f"""
    ### 🔒 Redaction

    Entities Replaced

    # **{stats['entities']}**
    """
        )

    with c3:

        if stats["entities"] > 0:

            efficiency = round(
                stats["entities"] /
                max(stats["paragraphs"], 1),
                2
            )

        else:

            efficiency = 0

        st.warning(
            f"""
    ### 📈 Density

    PII / Paragraph

    # **{efficiency}**
    """
        )

    st.divider()

    # ======================================================
    # File Information
    # ======================================================

    st.header("📁 File Information")

    file_size = uploaded_file.size / 1024

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Original File",

            uploaded_file.name

        )

    with col2:

        st.metric(

            "Size (KB)",

            f"{file_size:.2f}"

        )

    st.divider()

    # ======================================================
    # Processing Status
    # ======================================================

    st.header("✅ Processing Status")

    st.success(
    """
    The uploaded document has been successfully processed.

    ✔ PII detected

    ✔ Fake values generated

    ✔ Formatting preserved

    ✔ CSV log generated

    ✔ Redacted document ready for download
    """
    )

    st.divider()

    # ======================================================
    # Tips
    # ======================================================

    with st.expander("💡 Tips"):

        st.markdown(
    """
    ### Supported PII

    - Person
    - Email
    - Phone
    - Company
    - Address
    - URL
    - IP Address
    - PAN
    - Credit Card
    - Date

    ### Best Results

    - DOCX documents
    - Machine-generated PDFs converted to DOCX
    - English language

    ### Large Documents

    Batch detection is automatically enabled
    for documents with hundreds of pages.
    """
        )

    st.divider()

    # ======================================================
    # Footer
    # ======================================================

    st.markdown("---")

    st.markdown(
    """
    <div style="text-align:center">

    ### 🔒 Intelligent PII Redaction Tool

    Built with

    **Streamlit • spaCy • Microsoft Presidio • Faker • Python**

    </div>
    """,
    unsafe_allow_html=True
    )