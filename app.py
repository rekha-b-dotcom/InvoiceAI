import streamlit as st
import pandas as pd
import json
from openai import OpenAI
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO
from datetime import date
import random

# ---------------- UI STYLE ----------------

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

h1 {
    color: #1f2937;
    font-size: 42px;
    font-weight: 700;
}

h2, h3 {
    color: #1f2937;
}

.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 20px;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
}

.stTextArea textarea {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# Page setup
st.set_page_config(
    page_title="InvoiceAI",
    page_icon="🧾"
)

st.set_page_config(
    page_title="InvoiceAI",
    page_icon="🧾",
    layout="wide"
)

with st.sidebar:
    st.header("🧾 InvoiceAI")

    st.write("### Features")
    st.write("🤖 AI-powered extraction")
    st.write("💰 Automatic price lookup")
    st.write("🧮 GST calculation")
    st.write("👀 Human review")
    st.write("📄 PDF invoice")
    st.write("💬 WhatsApp sharing")

    st.divider()
    st.caption("Built for the Kodnexus AI Build Battle")

    # Dashboard
    st.markdown("""
<div style="
    margin-top: 25px;
    padding: 20px;
    border-radius: 12px;
    background-color: white;
    border: 1px solid #e5e7eb;
">
    <h2 style="margin-bottom: 5px;">🧾 Invoice Preview</h2>
    <p style="color: #6b7280; margin-top: 0;">
        Review the generated invoice before approving it.
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("### 📊 Invoice Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👤 Customer",
        "Ready"
    )

with col2:
    if st.session_state.get("approved", False):
        st.metric("🧾 Status", "Approved")
    else:
        st.metric("🧾 Status", "Draft")

with col3:
    if "grand_total" in st.session_state:
        st.metric(
            "💰 Total",
            f"₹{st.session_state['grand_total']:,.2f}"
        )
    else:
        st.metric("💰 Total", "—")

st.divider()

st.caption("Built for the Kodnexus AI Build Battle")
st.markdown("""
<div style="
    padding: 25px;
    border-radius: 15px;
    background: linear-gradient(135deg, #111827, #374151);
    margin-bottom: 20px;
">
    <h1 style="color: white; margin-bottom: 5px;">
        🧾 InvoiceAI
    </h1>
    <p style="color: #d1d5db; font-size: 18px; margin-bottom: 0;">
        AI-powered invoice automation from customer messages
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    text-align: center;
    padding: 12px;
    margin-bottom: 20px;
    border-radius: 10px;
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    font-size: 15px;
">
    💬 Customer Message
    &nbsp; → &nbsp;
    🤖 Extract Details
    &nbsp; → &nbsp;
    💰 Price Lookup
    &nbsp; → &nbsp;
    👀 Human Review
    &nbsp; → &nbsp;
    📄 Invoice
</div>
""", unsafe_allow_html=True)
st.write(
    "Turn a simple customer message into a professional invoice "
    "with automatic service extraction, price lookup, GST calculation, "
    "human review, PDF generation and WhatsApp sharing."
)

st.divider()
st.subheader("Smart Invoice Generator")
st.write("Turn a customer message into a professional invoice.")

st.info(
    "💬 Customer Message  →  🤖 Extract Details  →  "
    "💰 Price Lookup  →  👀 Review  →  📄 Invoice"
)

# Load price list
prices = pd.read_csv("pricing.csv")

# Customer message
st.markdown("### 1️⃣ Customer Requirement")

customer_message = st.text_area(
    "Enter the customer's message:",
    height=180,
    placeholder="Example: Hi, I'm Rahul. My email is rahul@gmail.com. I need 2 website designs and 3 logo designs."
)

# AI extraction
if st.button("✨ Extract Details", type="primary"):

    if customer_message.strip() == "":
        st.warning("Please enter a customer message.")

    else:
        import re

        name_match = re.search(
            r"(?:I'm|I am|My name is)\s+([A-Za-z ]+?)(?:\.|,| My email)",
            customer_message,
            re.IGNORECASE
        )

        if name_match:
            name = name_match.group(1).strip()
        else:
            name = ""

        email_match = re.search(
            r"[\w\.-]+@[\w\.-]+\.\w+",
            customer_message
        )

        if email_match:
            email = email_match.group(0)
        else:
            email = ""

        services = []

        # Website Design
        website_match = re.search(
            r"(\d+)\s+(?:website designs?|websites?)",
            customer_message,
            re.IGNORECASE
        )

        if website_match:
            services.append({
                "service": "Website Design",
                "quantity": int(website_match.group(1))
            })

        # AI Video Consulting
        ai_video_match = re.search(
            r"(\d+)\s+(?:AI Video Consulting|AI Video Consulting services?)",
            customer_message,
            re.IGNORECASE
        )

        if ai_video_match:
            services.append({
                "service": "AI Video Consulting",
                "quantity": int(ai_video_match.group(1))
            })

        # Logo Design
        logo_match = re.search(
            r"(\d+)\s+(?:logo designs?|logos?)",
            customer_message,
            re.IGNORECASE
        )

        if logo_match:
            services.append({
                "service": "Logo Design",
                "quantity": int(logo_match.group(1))
            })

        # Poster Design
        poster_match = re.search(
            r"(\d+)\s+(?:poster designs?|posters?)",
            customer_message,
            re.IGNORECASE
        )

        if poster_match:
            services.append({
                "service": "Poster Design",
                "quantity": int(poster_match.group(1))
            })

        # Social Media Post
        social_match = re.search(
            r"(\d+)\s+(?:social media posts?|social posts?)",
            customer_message,
            re.IGNORECASE
        )

        if social_match:
            services.append({
                "service": "Social Media Post",
                "quantity": int(social_match.group(1))
            })

        customer = {
            "name": name,
            "email": email,
            "services": services,
            "notes": customer_message
        }

        st.session_state["customer"] = customer

        st.success("Customer details extracted successfully! 🎉")

            
# Display extracted information
if "customer" in st.session_state:

    customer = st.session_state["customer"]

    st.markdown("### 2️⃣ AI Extracted Details")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Customer Name**")
        st.write(customer["name"])

    with col2:
        st.write("**Email**")
        st.write(customer["email"])

    st.write("**Notes**")
    st.write(customer["notes"])

    # Price lookup
    st.markdown("### 3️⃣ Price Lookup")

    invoice_items = []
    missing_items = []

    for item in customer["services"]:

        service_name = item["service"]
        quantity = int(item["quantity"])

        matches = prices[
            prices["service"].str.lower() == service_name.lower()
        ]

        if len(matches) > 0:

            price = float(matches.iloc[0]["price"])
            total = price * quantity

            invoice_items.append({
                "Service": service_name,
                "Quantity": quantity,
                "Unit Price": price,
                "Total": total
            })

        else:
            missing_items.append(service_name)

    # Missing prices
    if missing_items:

        st.warning("⚠️ Price not found for:")

        for service in missing_items:
            st.write("• " + service)

        st.info("Human review is required. The AI will not invent a price.")

    # Display prices
    if invoice_items:

        st.markdown("### 💰 Services Found")

        invoice_table = pd.DataFrame(invoice_items)

        st.dataframe(
            invoice_table,
            use_container_width=True,
            hide_index=True
        )

        subtotal = sum(
            item["Total"] for item in invoice_items
        )

        st.metric(
            "Subtotal",
            f"₹{subtotal:,.2f}"
        )

        st.session_state["invoice_items"] = invoice_items
        st.session_state["subtotal"] = subtotal


        # -----------------------------
# -----------------------------
# INVOICE CALCULATION
# -----------------------------

if "subtotal" in st.session_state:

    st.markdown("### 🧾 Invoice Summary")

    subtotal = st.session_state["subtotal"]

    # GST
    gst_rate = 18
    gst_amount = subtotal * gst_rate / 100

    # Final amount
    grand_total = subtotal + gst_amount

    st.write(f"**Subtotal:** ₹{subtotal:,.2f}")
    st.write(f"**GST (18%):** ₹{gst_amount:,.2f}")

    st.markdown(
    f"""
    <div style="
        background-color: #ffffff;
        border: 2px solid #111827;
        border-radius: 12px;
        padding: 18px;
        margin-top: 15px;
        text-align: right;
    ">
        <span style="font-size: 16px; color: #6b7280;">
            GRAND TOTAL
        </span>
        <br>
        <span style="font-size: 30px; font-weight: 700;">
            ₹{grand_total:,.2f}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

    st.session_state["gst"] = gst_amount
    st.session_state["grand_total"] = grand_total


# -----------------------------
# REVIEW AND APPROVAL
# -----------------------------

if "grand_total" in st.session_state:

    st.markdown("### 👀 Review Invoice")

    st.write("Please check the details before approving the invoice.")

    if st.button("✅ Approve Invoice", type="primary"):

        st.session_state["approved"] = True

        st.success("Invoice approved successfully! 🎉")
        st.markdown("### 👀 Invoice Review")

if st.session_state.get("approved", False):
    st.success("🟢 Invoice Approved")
else:
    st.warning("🟡 Invoice Pending Review")


# -----------------------------
# APPROVED MESSAGE
# -----------------------------

if st.session_state.get("approved", False):

    st.markdown("## ✅ Invoice Approved")

    st.write("The invoice is ready to be generated.")


    # -----------------------------
# PDF INVOICE
# -----------------------------

if st.session_state.get("approved", False):

    if st.button("📄 Generate Invoice PDF"):

        pdf_buffer = BytesIO()

        pdf = canvas.Canvas(pdf_buffer, pagesize=A4)

        width, height = A4

        # Invoice title
        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawString(30 * mm, height - 30 * mm, "INVOICE")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(30 * mm, height - 40 * mm, "InvoiceAI")

        # Invoice number
        invoice_number = f"INV-{date.today().year}-{random.randint(1000, 9999)}"

        pdf.setFont("Helvetica", 10)
        pdf.drawString(
            140 * mm,
            height - 35 * mm,
            f"Invoice No: {invoice_number}"
        )

        pdf.drawString(
            140 * mm,
            height - 42 * mm,
            f"Date: {date.today().strftime('%d %B %Y')}"
        )

        # Customer
        customer = st.session_state["customer"]

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(30 * mm, height - 65 * mm, "Bill To")

        pdf.setFont("Helvetica", 11)
        pdf.drawString(
            30 * mm,
            height - 73 * mm,
            customer["name"]
        )

        pdf.drawString(
            30 * mm,
            height - 80 * mm,
            customer["email"]
        )

        # Table heading
        y = height - 105 * mm

        pdf.setFont("Helvetica-Bold", 10)

        pdf.drawString(30 * mm, y, "Service")
        pdf.drawString(100 * mm, y, "Qty")
        pdf.drawString(120 * mm, y, "Unit Price")
        pdf.drawString(155 * mm, y, "Total")

        # Services
        y -= 8 * mm

        pdf.setFont("Helvetica", 10)

        for item in st.session_state["invoice_items"]:

            pdf.drawString(
                30 * mm,
                y,
                item["Service"]
            )

            pdf.drawString(
                100 * mm,
                y,
                str(item["Quantity"])
            )

            pdf.drawString(
                120 * mm,
                y,
                f"₹{item['Unit Price']:,.2f}"
            )

            pdf.drawString(
                155 * mm,
                y,
                f"₹{item['Total']:,.2f}"
            )

            y -= 8 * mm

        # Totals
        subtotal = st.session_state["subtotal"]
        gst = st.session_state["gst"]
        grand_total = st.session_state["grand_total"]

        y -= 10 * mm

        pdf.setFont("Helvetica", 11)

        pdf.drawString(
            120 * mm,
            y,
            "Subtotal:"
        )

        pdf.drawString(
            155 * mm,
            y,
            f"₹{subtotal:,.2f}"
        )

        y -= 8 * mm

        pdf.drawString(
            120 * mm,
            y,
            "GST (18%):"
        )

        pdf.drawString(
            155 * mm,
            y,
            f"₹{gst:,.2f}"
        )

        y -= 10 * mm

        pdf.setFont("Helvetica-Bold", 13)

        pdf.drawString(
            120 * mm,
            y,
            "Grand Total:"
        )

        pdf.drawString(
            155 * mm,
            y,
            f"₹{grand_total:,.2f}"
        )

        # Notes
        y -= 20 * mm

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(30 * mm, y, "Notes")

        pdf.setFont("Helvetica", 10)

        y -= 7 * mm

        pdf.drawString(
            30 * mm,
            y,
            customer["notes"]
        )

        # Footer
        pdf.setFont("Helvetica", 9)

        pdf.drawString(
            30 * mm,
            20 * mm,
            "Thank you for your business!"
        )

        pdf.save()

        pdf_buffer.seek(0)

        st.success("Invoice PDF generated successfully! 🎉")

        st.download_button(
            label="⬇️ Download Invoice PDF",
            data=pdf_buffer,
            file_name="InvoiceAI_INV-2026-001.pdf",
            mime="application/pdf"
        )

        # -----------------------------
# WHATSAPP
# -----------------------------

if st.session_state.get("approved", False):

    customer = st.session_state["customer"]
    grand_total = st.session_state["grand_total"]

    whatsapp_message = (
        f"Hello {customer['name']},\n\n"
        f"Your invoice from InvoiceAI is ready.\n"
        f"Total amount: ₹{grand_total:,.2f}\n\n"
        f"Thank you for your business!"
    )

    import urllib.parse

    whatsapp_url = (
        "https://wa.me/?text="
        + urllib.parse.quote(whatsapp_message)
    )

    st.markdown(
        f'<a href="{whatsapp_url}" target="_blank">'
        f'<button>💬 Send Invoice on WhatsApp</button>'
        f'</a>',
        unsafe_allow_html=True
    )