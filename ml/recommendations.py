"""
Clinical recommendation engine based on risk factors and prediction results.
"""


def generate_clinical_recommendations(risk_label, risk_probability, patient_data):
    """
    Generate personalized clinical recommendations based on risk profile.
    
    Args:
        risk_label: Risk category ("Low", "Medium", "High")
        risk_probability: Probability score (0-1)
        patient_data: Dictionary with patient health metrics
    
    Returns:
        Dictionary with recommendations and key findings
    """
    
    # Extract key metrics
    age = patient_data.get('age', 0)
    sex = patient_data.get('sex', 0)
    bp = patient_data.get('trestbps', 0)
    chol = patient_data.get('chol', 0)
    fbs = patient_data.get('fbs', 0)
    thalach = patient_data.get('thalach', 0)
    exang = patient_data.get('exang', 0)
    oldpeak = patient_data.get('oldpeak', 0)
    
    sex_str = "Male" if sex == 1 else "Female"
    
    recommendations = {
        "risk_level": risk_label,
        "probability": risk_probability,
        "key_findings": [],
        "primary_recommendations": [],
        "lifestyle_modifications": [],
        "monitoring_guidelines": [],
        "warning_signs": []
    }
    
    # ============================================
    # Identify Key Risk Factors
    # ============================================
    
    if bp >= 140:
        recommendations["key_findings"].append(f"🔴 Elevated Blood Pressure: {bp} mmHg (≥140 mmHg is hypertensive)")
    elif bp >= 130:
        recommendations["key_findings"].append(f"🟠 High-Normal Blood Pressure: {bp} mmHg (monitoring needed)")
    
    if chol >= 240:
        recommendations["key_findings"].append(f"🔴 High Cholesterol: {chol} mg/dL (≥240 mg/dL is high risk)")
    elif chol >= 200:
        recommendations["key_findings"].append(f"🟠 Borderline High Cholesterol: {chol} mg/dL (200-239 mg/dL)")
    
    if fbs == 1:
        recommendations["key_findings"].append("🔴 Fasting Blood Sugar > 120 mg/dL (Diabetes/Prediabetes indicator)")
    
    if age >= 65:
        recommendations["key_findings"].append(f"🟠 Advanced Age: {age} years (increased cardiovascular risk)")
    
    if exang == 1:
        recommendations["key_findings"].append("🔴 Exercise-Induced Angina detected")
    
    if oldpeak > 2.0:
        recommendations["key_findings"].append(f"🔴 ST Segment Depression: {oldpeak} mm (possible ischemia)")
    
    # ============================================
    # Generate Recommendations Based on Risk Level
    # ============================================
    
    if risk_label == "High":
        recommendations["primary_recommendations"] = [
            "🏥 **Schedule immediate medical consultation** with a cardiologist",
            "⚠️ **Do not delay** - high risk indicates significant cardiovascular disease likelihood",
            "📋 Request comprehensive cardiac evaluation (ECG, stress test, cardiac imaging)",
            "💊 Discuss medication options with your physician (may include beta-blockers, statins, ACE inhibitors)",
            "🚑 Know your warning signs - seek emergency care if experiencing chest pain, shortness of breath, or severe fatigue"
        ]
        
        recommendations["monitoring_guidelines"] = [
            "Daily blood pressure monitoring and logging",
            "Frequent follow-up appointments (every 2-4 weeks initially)",
            "Regular EKG monitoring as recommended by cardiologist",
            "Blood work every 3-6 months to track cholesterol and glucose"
        ]
        
        recommendations["warning_signs"] = [
            "Chest pain or pressure, especially with activity",
            "Severe shortness of breath at rest or with minimal activity",
            "Fainting or severe dizziness",
            "Rapid or irregular heartbeat",
            "Unusual fatigue or weakness"
        ]
    
    elif risk_label == "Medium":
        recommendations["primary_recommendations"] = [
            "👨‍⚕️ **Schedule medical check-up** with your primary care physician",
            "🔍 Request cardiovascular risk assessment and appropriate testing",
            "💡 Implement aggressive lifestyle modifications starting immediately",
            "💊 Discuss preventive medication options with your doctor",
            "📊 Establish regular health monitoring routine"
        ]
        
        recommendations["lifestyle_modifications"] = [
            "**Diet**: Adopt DASH or Mediterranean diet, reduce sodium to <2,300 mg/day",
            "**Exercise**: 150 minutes/week moderate aerobic activity (walking, cycling, swimming)",
            "**Weight**: Aim for BMI 18.5-24.9 kg/m²",
            "**Smoking**: Quit smoking if applicable - seek cessation support",
            "**Alcohol**: Limit to 1 drink/day for women, 2 drinks/day for men",
            "**Stress**: Practice stress-reduction techniques (meditation, yoga, mindfulness)"
        ]
        
        recommendations["monitoring_guidelines"] = [
            "Blood pressure monitoring 2-3 times per week",
            "Follow-up appointment in 3 months",
            "Blood work every 6-12 months",
            "Repeat cardiovascular assessment annually"
        ]
    
    else:  # Low Risk
        recommendations["primary_recommendations"] = [
            "✅ **Maintain current healthy habits** - your risk profile is good",
            "🎯 Continue regular health check-ups annually",
            "💪 Keep up with cardiovascular fitness routine",
            "📈 Use this as a baseline - monitor for changes over time"
        ]
        
        recommendations["lifestyle_modifications"] = [
            "**Continue healthy diet**: Mediterranean or DASH diet recommended",
            "**Maintain exercise**: 150 minutes/week of moderate activity",
            "**Weight management**: Keep BMI in healthy range",
            "**Avoid smoking**: Stay tobacco-free",
            "**Moderate alcohol**: Keep within recommended limits",
            "**Stress management**: Continue healthy coping strategies"
        ]
        
        recommendations["monitoring_guidelines"] = [
            "Annual health check-ups with primary care physician",
            "Blood pressure and cholesterol screening every 5 years",
            "Reassess cardiovascular risk in 3-5 years"
        ]
    
    # ============================================
    # Personalized Risk Factor Recommendations
    # ============================================
    
    if bp >= 130:
        recommendations["lifestyle_modifications"].insert(0, f"🫀 **Blood Pressure Control**: Your BP is {bp} mmHg. Target <130/80 mmHg through diet (DASH), exercise, and stress management.")
    
    if chol >= 200:
        recommendations["lifestyle_modifications"].insert(0, f"🧈 **Cholesterol Management**: Your cholesterol is {chol} mg/dL. Reduce saturated fats, increase fiber, and consider statin therapy with your doctor.")
    
    if age >= 60:
        recommendations["lifestyle_modifications"].insert(0, "👴 **Age Consideration**: At your age, regular monitoring and preventive care are especially important.")
    
    # ============================================
    # Add General Prevention Tips
    # ============================================
    # Add General Emergency Signs if not already set
    # ============================================
    
    if not recommendations.get("warning_signs"):
        recommendations["warning_signs"] = [
            "Chest discomfort or pressure lasting more than a few minutes",
            "Shortness of breath with or without chest pain",
            "Dizziness, lightheadedness, or fainting",
            "Nausea or unusual fatigue",
            "Cold sweat, particularly with chest pain"
        ]
    
    return recommendations


def format_recommendations_for_display(recommendations):
    """
    Format recommendations into a readable string for Streamlit display.
    
    Args:
        recommendations: Dictionary from generate_clinical_recommendations
    
    Returns:
        Formatted string for display
    """
    
    output = []
    
    # Key Findings
    if recommendations.get("key_findings"):
        output.append("### 🔍 Key Findings")
        for finding in recommendations["key_findings"]:
            output.append(f"- {finding}")
        output.append("")
    
    # Primary Recommendations
    if recommendations.get("primary_recommendations"):
        output.append("### 📋 Recommended Actions")
        for rec in recommendations["primary_recommendations"]:
            output.append(f"- {rec}")
        output.append("")
    
    # Lifestyle Modifications
    if recommendations.get("lifestyle_modifications"):
        output.append("### 🏃 Lifestyle Modifications")
        for mod in recommendations["lifestyle_modifications"]:
            output.append(f"- {mod}")
        output.append("")
    
    # Monitoring Guidelines
    if recommendations.get("monitoring_guidelines"):
        output.append("### 📅 Monitoring Guidelines")
        for guideline in recommendations["monitoring_guidelines"]:
            output.append(f"- {guideline}")
        output.append("")
    
    # Warning Signs
    if recommendations.get("warning_signs"):
        output.append("### ⚠️ Warning Signs - Seek Emergency Care If You Experience:")
        for sign in recommendations["warning_signs"]:
            output.append(f"- {sign}")
        output.append("")
    
    return "\n".join(output)


def get_risk_color(risk_label):
    """Get color code for risk level."""
    colors = {
        "Low": "#22c55e",      # Green
        "Medium": "#f97316",   # Orange
        "High": "#ef4444"      # Red
    }
    return colors.get(risk_label, "#6b7280")


def get_emergency_contact_info():
    """
    Get localized emergency contact information.
    Returns emergency services details for Sri Lanka.
    """
    return {
        "country": "Sri Lanka",
        "ambulance_number": "1990",
        "ambulance_service": "Suwa Seriya",
        "emergency_message": "For medical emergencies, call 1990 (Suwa Seriya - toll-free ambulance service) for fast pre-hospital care and emergency transport.",
        "emergency_tips": [
            "Call 1990 immediately - do not delay",
            "Provide clear location details for faster ambulance dispatch",
            "Keep the phone line open with the dispatcher",
            "If possible, have someone wait outside to guide the ambulance",
            "Never attempt to drive yourself to the hospital in an emergency"
        ]
    }



