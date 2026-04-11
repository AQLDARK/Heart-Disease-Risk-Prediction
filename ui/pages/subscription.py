import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from ml.storage import (
    get_subscription_for_user, 
    set_subscription_for_user, 
    record_transaction,
    get_user_transactions,
    get_plan_features
)
from ml.utils import generate_pdf_report
from ui.components import card, info_box, divider, stat_card
import uuid


def generate_invoice_pdf(user, transaction, plan_features):
    """Generate PDF invoice for a transaction."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from io import BytesIO
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        styles = getSampleStyleSheet()
        custom_style = ParagraphStyle(
            'CustomStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333')
        )
        
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#00d4ff'),
            spaceAfter=6
        )
        
        story = []
        
        # Header
        story.append(Paragraph("❤️ HEART DISEASE RISK PREDICTION SYSTEM", title_style))
        story.append(Paragraph("Invoice", styles['Heading2']))
        story.append(Spacer(1, 0.3*inch))
        
        # Invoice details
        invoice_data = [
            ['Invoice #:', transaction.get('invoice_id', 'N/A'), 'Date:', datetime.now().strftime('%Y-%m-%d')],
            ['Transaction ID:', transaction.get('transaction_id', 'N/A'), 'Status:', transaction.get('status', 'N/A').upper()],
        ]
        
        invoice_table = Table(invoice_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        invoice_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#00d4ff')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        story.append(invoice_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Bill To section
        story.append(Paragraph("<b>BILL TO:</b>", styles['Heading3']))
        bill_data = [
            [f"Name: {user.get('full_name', 'N/A')}"],
            [f"Email: {user.get('email', 'N/A')}"],
            [f"User ID: {user.get('user_id', 'N/A')}"],
        ]
        story.append(Paragraph(f"<br/>".join([item[0] for item in bill_data]), custom_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Service details
        story.append(Paragraph("<b>SERVICE DETAILS:</b>", styles['Heading3']))
        
        service_data = [
            ['Description', 'Amount', 'Currency', 'Total'],
            [f"{transaction.get('plan', 'N/A')} Plan (Monthly)', '$' + str(transaction.get('amount', 0)), 
             transaction.get('currency', 'USD'), '$' + str(transaction.get('amount', 0))],
        ]
        
        service_table = Table(service_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        service_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00d4ff')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 10),
        ]))
        story.append(service_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Total
        total_data = [
            ['', 'Subtotal:', '$' + str(transaction.get('amount', 0))],
            ['', 'Tax (0%):', '$0.00'],
            ['', 'Total:', '$' + str(transaction.get('amount', 0))],
        ]
        total_table = Table(total_data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
        total_table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONT', (0, 0), (-1, 1), 'Helvetica', 9),
            ('FONT', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 2), (-1, 2), 12),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#00d4ff')),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.whitesmoke),
            ('GRID', (0, 2), (-1, 2), 1, colors.black),
        ]))
        story.append(total_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Payment method
        story.append(Paragraph(f"<b>Payment Method:</b> {transaction.get('payment_method', 'Card')}", custom_style))
        story.append(Paragraph(f"<b>Payment Date:</b> {transaction.get('created_at', 'N/A')}", custom_style))
        
        story.append(Spacer(1, 0.5*inch))
        
        # Footer
        story.append(Paragraph(
            "<i>Thank you for your business! This invoice is automatically generated by Heart Disease Risk Prediction System.</i>",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)
        ))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None


def render_subscription_page():
    """Enhanced subscription and billing page."""
    user = st.session_state["user"]
    user_id = user.get("user_id")
    
    current_plan = get_subscription_for_user(user_id)
    
    st.title("💳 Subscription & Billing")
    st.markdown("Manage your subscription plan and view billing history")
    divider()
    
    # Current Plan Info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Plan", current_plan)
    with col2:
        current_features = get_plan_features(current_plan)
        st.metric("Monthly Cost", f"${current_features['price']:.2f}")
    with col3:
        end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        st.metric("Renewal Date", end_date)
    
    st.divider()
    
    # Plan Selection
    st.markdown("### 📦 Choose Your Plan")
    
    tab1, tab2, tab3 = st.tabs(["Plans", "Billing History", "Payment Methods"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        
        # Free Plan
        with col1:
            st.markdown("""
            <div style="
                background: rgba(30, 45, 80, 0.4);
                border: 2px solid rgba(255, 200, 100, 0.5);
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
            ">
                <h3 style="color: #ffc864; margin-top: 0;">🆓 FREE</h3>
                <div style="font-size: 2rem; color: #00d4ff; font-weight: bold; margin: 1rem 0;">$0</div>
                <div style="color: #9ca3af; font-size: 0.9rem; margin-bottom: 1.5rem;">/month</div>
            </div>
            """, unsafe_allow_html=True)
            
            features_free = get_plan_features("Free")
            st.markdown(f"""
            ✅ {features_free['predictions_per_month']} predictions/month
            ✅ Basic risk assessment
            ❌ No history access
            ❌ No export features
            ❌ Limited support
            """)
            
            if current_plan != "Free":
                if st.button("Downgrade to Free", key="plan_free", use_container_width=True):
                    set_subscription_for_user(user_id, "Free")
                    record_transaction(user_id, "Free", 0, "downgrade")
                    st.success("Downgraded to Free plan")
                    st.rerun()
            else:
                st.info("Current Plan")
        
        # Standard Plan
        with col2:
            st.markdown("""
            <div style="
                background: rgba(0, 212, 255, 0.1);
                border: 2px solid rgba(0, 212, 255, 0.5);
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
            ">
                <h3 style="color: #00d4ff; margin-top: 0;">⭐ STANDARD</h3>
                <div style="font-size: 2rem; color: #00d4ff; font-weight: bold; margin: 1rem 0;">$9.99</div>
                <div style="color: #9ca3af; font-size: 0.9rem; margin-bottom: 1.5rem;">/month</div>
            </div>
            """, unsafe_allow_html=True)
            
            features_standard = get_plan_features("Standard")
            st.markdown(f"""
            ✅ {features_standard['predictions_per_month']} predictions/month
            ✅ Prediction history
            ✅ CSV export
            ✅ Explainability
            ✅ Email support
            """)
            
            if current_plan != "Standard":
                if st.button("Upgrade to Standard", key="plan_standard", use_container_width=True):
                    st.session_state["show_payment"] = True
                    st.session_state["selected_plan"] = "Standard"
                    st.rerun()
            else:
                st.info("Current Plan")
        
        # Premium Plan
        with col3:
            st.markdown("""
            <div style="
                background: rgba(34, 197, 94, 0.1);
                border: 2px solid rgba(34, 197, 94, 0.5);
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
            ">
                <h3 style="color: #22c55e; margin-top: 0;">👑 PREMIUM</h3>
                <div style="font-size: 2rem; color: #22c55e; font-weight: bold; margin: 1rem 0;">$29.99</div>
                <div style="color: #9ca3af; font-size: 0.9rem; margin-bottom: 1.5rem;">/month</div>
            </div>
            """, unsafe_allow_html=True)
            
            features_premium = get_plan_features("Premium")
            st.markdown(f"""
            ✅ Unlimited predictions
            ✅ Full history access
            ✅ Advanced export (PDF)
            ✅ SHAP explainability
            ✅ Admin analytics
            ✅ Priority support
            """)
            
            if current_plan != "Premium":
                if st.button("Upgrade to Premium", key="plan_premium", use_container_width=True):
                    st.session_state["show_payment"] = True
                    st.session_state["selected_plan"] = "Premium"
                    st.rerun()
            else:
                st.info("Current Plan")
        
        # Payment Section
        if st.session_state.get("show_payment"):
            st.divider()
            st.markdown("### 💰 Complete Your Payment")
            
            selected_plan = st.session_state.get("selected_plan", "Standard")
            plan_info = get_plan_features(selected_plan)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Plan:** {selected_plan}")
                st.markdown(f"**Amount:** ${plan_info['price']:.2f}")
            
            with col2:
                payment_method = st.selectbox(
                    "Payment Method",
                    ["Credit Card", "Debit Card", "PayPal"],
                    key="payment_method_select"
                )
            
            # Card details (simulated)
            if payment_method in ["Credit Card", "Debit Card"]:
                col1, col2 = st.columns(2)
                with col1:
                    card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456", max_chars=19)
                with col2:
                    card_expiry = st.text_input("Expiry (MM/YY)", placeholder="12/25", max_chars=5)
                
                col1, col2 = st.columns(2)
                with col1:
                    card_cvv = st.text_input("CVV", placeholder="123", max_chars=4, type="password")
                with col2:
                    st.empty()
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("💳 Process Payment", use_container_width=True, key="process_payment"):
                    # Simulate payment processing
                    with st.spinner("Processing payment..."):
                        import time
                        time.sleep(1.5)
                        
                        # Record transaction
                        transaction_info = record_transaction(
                            user_id=user_id,
                            plan=selected_plan,
                            amount=plan_info['price'],
                            payment_method=payment_method,
                            status="completed"
                        )
                        
                        # Update subscription
                        set_subscription_for_user(user_id, selected_plan)
                        st.session_state["plan"] = selected_plan
                        st.session_state["show_payment"] = False
                        
                        info_box(f"✅ Payment successful! Upgraded to {selected_plan} plan", color="success")
                        st.rerun()
            
            with col2:
                if st.button("Cancel", key="cancel_payment"):
                    st.session_state["show_payment"] = False
                    st.rerun()
    
    with tab2:
        st.markdown("### 📋 Transaction History")
        
        transactions = get_user_transactions(user_id)
        
        if transactions:
            # Create dataframe
            df_transactions = pd.DataFrame([
                {
                    "Date": t["created_at"][:10],
                    "Plan": t["plan"],
                    "Amount": f"${t['amount']:.2f}",
                    "Status": t["status"].upper(),
                    "Payment Method": t["payment_method"],
                    "Invoice": t["invoice_id"]
                }
                for t in transactions
            ])
            
            st.dataframe(df_transactions, use_container_width=True, hide_index=True)
            
            st.markdown("### 📄 Download Invoice")
            
            for transaction in transactions:
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**{transaction['plan']} Plan** - {transaction['created_at'][:10]}")
                
                with col2:
                    st.write(f"Amount: ${transaction['amount']:.2f}")
                
                with col3:
                    invoice_pdf = generate_invoice_pdf(user, transaction, get_plan_features(transaction['plan']))
                    if invoice_pdf:
                        st.download_button(
                            label="📥 PDF",
                            data=invoice_pdf,
                            file_name=f"invoice_{transaction['invoice_id']}.pdf",
                            mime="application/pdf",
                            key=f"download_{transaction['invoice_id']}"
                        )
        else:
            info_box("No transactions yet. Upgrade your plan to see billing history.", color="info")
    
    with tab3:
        st.markdown("### 💳 Payment Methods")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Available Payment Methods:**")
            st.markdown("""
            ✅ **Credit Card**
            - Visa, Mastercard, American Express
            - Secure payment via Stripe
            
            ✅ **Debit Card**
            - All major debit cards supported
            
            ✅ **PayPal**
            - Fast and secure checkout
            """)
        
        with col2:
            st.markdown("**Payment Security:**")
            st.markdown("""
            🔒 **Encrypted Transactions**
            - SSL/TLS 256-bit encryption
            
            🔒 **PCI Compliance**
            - Industry standard security
            
            🔒 **No Data Storage**
            - Card details not stored locally
            """)
        
        st.divider()
        st.markdown("**Add New Payment Method** (Coming Soon)")
        st.info("Additional payment methods will be available in future updates.")
