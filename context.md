# Project Context Documentation
## Machine Learning–Based Heart Disease Risk Prediction Platform

---

## 1. Project Overview

This project focuses on the design and development of a **machine learning–based predictive analytics platform** for the early detection of heart disease. The system utilizes patient clinical attributes such as age, blood pressure, cholesterol level, heart rate, electrocardiographic results, and related indicators to predict cardiovascular disease risk.

Unlike a basic prediction tool, the system is designed as a **scalable healthcare analytics platform** that supports:

- Individual patient risk prediction
- Explainable artificial intelligence (XAI)
- Historical report management
- Population-level analytics
- Administrative decision-support dashboards
- Optional subscription-based access model

The project combines data science, software engineering principles, and healthcare analytics to deliver an interpretable, data-driven decision-support system.

---

## 2. Problem Domain

Heart disease remains one of the leading causes of death worldwide. In many developing countries, including Sri Lanka, early detection is hindered by:

- Limited access to cardiologists
- High diagnostic costs
- Time-consuming clinical procedures
- Inadequate preventive screening
- Manual interpretation of clinical indicators

Traditional diagnostic methods often fail to capture complex, non-linear relationships between multiple risk factors. Machine learning techniques provide an effective solution by analyzing multidimensional medical data and identifying hidden patterns that support early diagnosis.

---

## 3. Project Aim

The primary aim of this project is to develop a **machine learning–based predictive analytics system** capable of identifying heart disease risk at an early stage using patient health indicators, while providing transparent and interpretable insights to support clinical decision-making.

---

## 4. Project Objectives

- Collect and preprocess patient health data from open-source datasets such as the UCI Heart Disease dataset
- Perform exploratory data analysis and feature correlation analysis
- Implement and compare multiple supervised machine learning algorithms
- Evaluate model performance using standard classification metrics
- Integrate explainable artificial intelligence for interpretability
- Develop a web-based platform for prediction and visualization
- Provide administrative analytics for population-level insights
- Support extensibility for payment and subscription models

---

## 5. Core System Concept

The system evolves beyond a simple “high/low risk output” and functions as a **health analytics platform**.

### Key Concept:
> Individual predictions generate value for patients, while aggregated data generates intelligence for administrators and healthcare planners.

---

## 6. User Roles and Platform Structure

### 6.1 Patient / User
- Enter personal health parameters
- View prediction results
- View detailed risk report
- Access historical prediction records
- Download reports (PDF/CSV)

### 6.2 Clinician / Staff
- Assist patient data entry
- Generate predictions
- Interpret explainable AI results
- Track patient risk history

### 6.3 Administrator
- View overall system analytics
- Monitor prediction trends
- Identify high-risk population groups
- Analyze dominant risk factors
- Generate summary reports
- Manage users and permissions
- Monitor platform usage

---

## 7. Platform Analytics (Admin Dashboard)

The administrative dashboard provides a “bigger picture” view of health trends similar to analytics dashboards used in large e-commerce platforms.

### Admin-level insights include:

- Distribution of risk levels (Low / Medium / High)
- Risk analysis by age category
- Risk analysis by gender
- Top contributing risk factors (global SHAP)
- Monthly and weekly prediction trends
- Identification of dominant clinical causes
- Population-level disease patterns

These analytics assist healthcare planners in identifying vulnerable groups and prioritizing preventive interventions.

---

## 8. Explainable Artificial Intelligence (XAI)

The system integrates **SHAP (SHapley Additive exPlanations)** to ensure transparency and trust.

### Explainability features:

- Global feature importance across all predictions
- Local explanation for individual patients
- Visualization of feature contribution values
- Alignment with known medical risk factors

This approach mitigates the black-box nature of machine learning models and improves adoption in healthcare environments.

---

## 9. Similar Systems Studied

To refine the proposed solution, three established cardiovascular risk systems were studied:

### 9.1 ASCVD Risk Estimator Plus (American College of Cardiology)
- Provides 10-year cardiovascular risk estimation
- Supports clinician–patient shared decision-making
- Tracks risk changes over time

### 9.2 QRISK3 Cardiovascular Risk Calculator
- Widely used in the UK healthcare system
- Considers multiple demographic and clinical variables
- Predicts long-term cardiovascular risk

### 9.3 Mayo Clinic Heart Disease Risk Tools
- Used in clinical environments
- Provides risk interpretation guidance
- Emphasizes patient education and prevention

### Key insights adopted:
- Multi-factor input analysis
- Population-level analytics
- Interpretability of risk
- Report-based decision support

---

## 10. Proposed System Enhancements Based on Lecturer Feedback

Based on lecturer guidance, the system design has been enhanced to include:

- Platform-based architecture instead of single prediction page
- Administrative analytics dashboards
- Patient prediction history tracking
- Advanced insight generation beyond high/low risk
- Similar-system–driven data structure refinement
- Expandable data input design
- Planned payment and subscription model

---

## 11. Payment Gateway Concept (Planned Feature)

The platform supports a **subscription-based business model**, although payment is not implemented at the interim stage.

### Intended use cases:
- Clinic-level subscriptions
- Premium analytics access
- Multi-user administrative dashboards

### Potential gateways:
- Stripe (global)
- PayHere (Sri Lanka)

Payment integration is defined within system architecture and future scope.

---

## 12. Technology Stack Summary

### Backend
- Python
- Scikit-learn
- Pandas
- NumPy
- SHAP
- Matplotlib
- Seaborn

### Frontend
- Streamlit
- HTML/CSS (basic styling)

### Development Tools
- Jupyter Notebook (experimentation)
- Visual Studio Code
- Git version control

---

## 13. Architecture Model

The system follows a **layered architecture**:

1. User Layer  
2. Presentation Layer  
3. Application Layer  
4. Machine Learning Layer  
5. Explainable AI Layer  
6. Data Layer  
7. Analytics & Reporting Layer  

This ensures modularity, scalability, and maintainability.

---

## 14. Machine Learning Approach

- Supervised classification models
- Multiple algorithm comparison:
  - Logistic Regression
  - Random Forest
  - Support Vector Machine
  - Gradient Boosting
- Train–test split (80:20)
- Cross-validation
- Model selection based on evaluation metrics

---

## 15. Implementation Status (Interim – 40%)

### Completed:
- Dataset acquisition
- Data preprocessing
- Feature engineering
- ML model training
- Model evaluation
- Initial explainable AI
- Basic Streamlit interface

### Partially Completed:
- Explainability visualization
- Admin analytics dashboard

### Pending:
- Full deployment
- Authentication system
- Payment gateway integration
- Advanced UI optimization

---

## 16. Testing and Verification

Testing includes:
- Data validation testing
- Preprocessing verification
- Model evaluation testing
- Explainable AI validation
- User interface testing

Test plan and test cases are documented in Chapter 3.6.

---

## 17. Academic Positioning

The project integrates:

- Data science principles
- Machine learning classification
- Explainable artificial intelligence
- Software engineering best practices
- Healthcare analytics domain knowledge

The system is designed strictly as a **decision-support platform**, not a replacement for professional medical diagnosis.

---

## 18. Future Enhancements

- Integration with electronic health records (EHR)
- Real-time patient monitoring
- Mobile application interface
- Advanced deep learning models
- Clinical trial dataset integration
- Full subscription management
- Cloud-based deployment

---

## 19. Summary

This project represents a scalable, interpretable, and data-driven healthcare analytics platform that extends beyond individual prediction to population-level insight generation. By combining predictive modelling, explainable AI, and administrative analytics, the system aligns closely with real-world healthcare decision-support environments and addresses key limitations of traditional diagnostic methods.

---

End of context.md