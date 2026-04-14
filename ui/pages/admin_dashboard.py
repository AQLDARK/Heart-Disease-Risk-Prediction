import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

from ml.storage import load_predictions
from ml.utils import load_json
from ml.storage import get_subscription
from ui.components import divider, stat_card



def render_admin_dashboard():
    st.title("📊 Admin Analytics Dashboard")
    st.markdown("Population-level heart disease risk insights and trend analysis")
    divider()

    df = load_predictions(limit=5000)

    if df.empty:
        st.warning("No prediction data available yet.")
        return

    # ============================================
    # Data Preparation
    # ============================================
    
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["date"] = df["created_at"].dt.date
    df["week"] = df["created_at"].dt.isocalendar().week
    df["month"] = df["created_at"].dt.to_period("M")

    # Age groups
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 30, 45, 60, 120],
        labels=["18–30", "31–45", "46–60", "60+"]
    )

    # Gender mapping
    df["gender"] = df["sex"].map({0: "Female", 1: "Male"})

    # ============================================
    # Overview KPI Cards
    # ============================================
    
    st.markdown("## 📈 Overview Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Predictions", len(df))
    
    with col2:
        high_risk_count = int((df["label"] == "High").sum())
        high_risk_pct = (high_risk_count / len(df)) * 100 if len(df) > 0 else 0
        st.metric("High-Risk Patients", high_risk_count, f"{high_risk_pct:.1f}%")
    
    with col3:
        medium_risk_count = int((df["label"] == "Medium").sum())
        medium_risk_pct = (medium_risk_count / len(df)) * 100 if len(df) > 0 else 0
        st.metric("Medium-Risk Patients", medium_risk_count, f"{medium_risk_pct:.1f}%")
    
    with col4:
        low_risk_count = int((df["label"] == "Low").sum())
        low_risk_pct = (low_risk_count / len(df)) * 100 if len(df) > 0 else 0
        st.metric("Low-Risk Patients", low_risk_count, f"{low_risk_pct:.1f}%")
    
    st.divider()

    # ============================================
    # Main Dashboard Tabs
    # ============================================
    
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Time Trends", "Demographics", "Risk Factors"])

    # ============================================
    # TAB 1: Overview
    # ============================================
    
    with tab1:
        col1, col2 = st.columns(2)
        
        # Risk Distribution Pie Chart
        with col1:
            st.markdown("### 🎯 Risk Distribution")
            
            risk_counts = df["label"].value_counts()
            
            fig_pie, ax_pie = plt.subplots(figsize=(8, 6))
            colors = ["#ef4444", "#f97316", "#22c55e"]  # Red, Orange, Green
            ax_pie.pie(
                risk_counts,
                labels=risk_counts.index,
                autopct="%1.1f%%",
                startangle=90,
                colors=colors[:len(risk_counts)]
            )
            ax_pie.axis("equal")
            fig_pie.patch.set_facecolor('#0f1419')
            ax_pie.set_facecolor('#0f1419')
            st.pyplot(fig_pie, use_container_width=True)
            plt.close()
        
        # Risk by Gender
        with col2:
            st.markdown("### 👥 Risk by Gender")
            
            gender_risk = (
                df.groupby(["gender", "label"])
                .size()
                .unstack(fill_value=0)
            )
            
            fig_gender, ax_gender = plt.subplots(figsize=(8, 6))
            gender_risk.plot(kind="bar", ax=ax_gender, color=["#ef4444", "#f97316", "#22c55e"])
            ax_gender.set_title("Risk Distribution by Gender", fontweight="bold", color="white", fontsize=12)
            ax_gender.set_xlabel("Gender", color="white")
            ax_gender.set_ylabel("Count", color="white")
            ax_gender.legend(title="Risk Level", labels=gender_risk.columns)
            ax_gender.tick_params(colors="white")
            fig_gender.patch.set_facecolor('#0f1419')
            ax_gender.set_facecolor('#0f1419')
            for spine in ax_gender.spines.values():
                spine.set_color('white')
            plt.xticks(rotation=0)
            st.pyplot(fig_gender, use_container_width=True)
            plt.close()

    # ============================================
    # TAB 2: Time Trends
    # ============================================
    
    with tab2:
        st.markdown("### 📅 Prediction Trends Over Time")
        
        # Number of Predictions Over Time
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Predictions Per Day")
            
            daily_predictions = df.groupby("date").size()
            
            fig_daily, ax_daily = plt.subplots(figsize=(10, 6))
            ax_daily.plot(daily_predictions.index, daily_predictions.values, marker="o", linewidth=2, markersize=6, color="#00d4ff")
            ax_daily.fill_between(daily_predictions.index, daily_predictions.values, alpha=0.3, color="#00d4ff")
            ax_daily.set_title("Daily Prediction Volume", fontweight="bold", color="white", fontsize=12)
            ax_daily.set_xlabel("Date", color="white")
            ax_daily.set_ylabel("Number of Predictions", color="white")
            ax_daily.grid(True, alpha=0.3, color="gray")
            ax_daily.tick_params(colors="white")
            fig_daily.patch.set_facecolor('#0f1419')
            ax_daily.set_facecolor('#0f1419')
            for spine in ax_daily.spines.values():
                spine.set_color('white')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig_daily, use_container_width=True)
            plt.close()
        
        with col2:
            st.markdown("#### Risk Distribution Over Time")
            
            daily_risk = (
                df.groupby(["date", "label"])
                .size()
                .unstack(fill_value=0)
            )
            
            fig_risk_trend, ax_risk_trend = plt.subplots(figsize=(10, 6))
            daily_risk.plot(kind="area", ax=ax_risk_trend, color=["#ef4444", "#f97316", "#22c55e"], alpha=0.7)
            ax_risk_trend.set_title("Risk Distribution Over Time", fontweight="bold", color="white", fontsize=12)
            ax_risk_trend.set_xlabel("Date", color="white")
            ax_risk_trend.set_ylabel("Count", color="white")
            ax_risk_trend.legend(title="Risk Level", loc="upper left")
            ax_risk_trend.tick_params(colors="white")
            ax_risk_trend.grid(True, alpha=0.3, axis="y", color="gray")
            fig_risk_trend.patch.set_facecolor('#0f1419')
            ax_risk_trend.set_facecolor('#0f1419')
            for spine in ax_risk_trend.spines.values():
                spine.set_color('white')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig_risk_trend, use_container_width=True)
            plt.close()
        
        st.divider()
        
        # Risk Probability Trends
        st.markdown("#### Average Risk Probability Over Time")
        
        daily_avg_prob = df.groupby("date")["probability"].mean()
        
        fig_prob, ax_prob = plt.subplots(figsize=(12, 6))
        ax_prob.plot(daily_avg_prob.index, daily_avg_prob.values, marker="o", linewidth=2, markersize=5, color="#0099ff")
        ax_prob.fill_between(daily_avg_prob.index, daily_avg_prob.values, alpha=0.3, color="#0099ff")
        ax_prob.axhline(y=daily_avg_prob.mean(), color="#f97316", linestyle="--", linewidth=2, label=f"Average: {daily_avg_prob.mean():.2%}")
        ax_prob.set_title("Average Risk Probability Trend", fontweight="bold", color="white", fontsize=12)
        ax_prob.set_xlabel("Date", color="white")
        ax_prob.set_ylabel("Average Probability", color="white")
        ax_prob.set_ylim(0, 1)
        ax_prob.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
        ax_prob.grid(True, alpha=0.3, color="gray")
        ax_prob.legend(loc="upper left")
        ax_prob.tick_params(colors="white")
        fig_prob.patch.set_facecolor('#0f1419')
        ax_prob.set_facecolor('#0f1419')
        for spine in ax_prob.spines.values():
            spine.set_color('white')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig_prob, use_container_width=True)
        plt.close()

    # ============================================
    # TAB 3: Demographics
    # ============================================
    
    with tab3:
        col1, col2 = st.columns(2)
        
        # Risk by Age Group
        with col1:
            st.markdown("### 📊 Risk by Age Group")
            
            age_risk = (
                df.groupby(["age_group", "label"])
                .size()
                .unstack(fill_value=0)
            )
            
            fig_age, ax_age = plt.subplots(figsize=(10, 6))
            age_risk.plot(kind="bar", ax=ax_age, color=["#ef4444", "#f97316", "#22c55e"])
            ax_age.set_title("Risk Distribution by Age Group", fontweight="bold", color="white", fontsize=12)
            ax_age.set_xlabel("Age Group", color="white")
            ax_age.set_ylabel("Count", color="white")
            ax_age.legend(title="Risk Level", labels=age_risk.columns)
            ax_age.tick_params(colors="white")
            fig_age.patch.set_facecolor('#0f1419')
            ax_age.set_facecolor('#0f1419')
            for spine in ax_age.spines.values():
                spine.set_color('white')
            plt.xticks(rotation=0)
            plt.tight_layout()
            st.pyplot(fig_age, use_container_width=True)
            plt.close()
        
        # Average Risk by Age Group
        with col2:
            st.markdown("### 📈 Average Risk Probability by Age")
            
            age_prob = df.groupby("age_group")["probability"].mean()
            
            fig_age_prob, ax_age_prob = plt.subplots(figsize=(10, 6))
            bars = ax_age_prob.bar(range(len(age_prob)), age_prob.values, color="#00d4ff", alpha=0.8, edgecolor="white", linewidth=2)
            
            # Add value labels on bars
            for bar, val in zip(bars, age_prob.values):
                height = bar.get_height()
                ax_age_prob.text(bar.get_x() + bar.get_width()/2., height,
                               f'{val:.1%}',
                               ha='center', va='bottom', fontweight='bold', color='white')
            
            ax_age_prob.set_xticks(range(len(age_prob)))
            ax_age_prob.set_xticklabels(age_prob.index)
            ax_age_prob.set_title("Average Risk Probability by Age Group", fontweight="bold", color="white", fontsize=12)
            ax_age_prob.set_xlabel("Age Group", color="white")
            ax_age_prob.set_ylabel("Average Risk Probability", color="white")
            ax_age_prob.set_ylim(0, 1)
            ax_age_prob.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
            ax_age_prob.tick_params(colors="white")
            fig_age_prob.patch.set_facecolor('#0f1419')
            ax_age_prob.set_facecolor('#0f1419')
            for spine in ax_age_prob.spines.values():
                spine.set_color('white')
            plt.tight_layout()
            st.pyplot(fig_age_prob, use_container_width=True)
            plt.close()
        
        st.divider()
        
        # Gender and Risk Probability
        st.markdown("### 👫 Risk Probability by Gender")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender_prob = df.groupby("gender")["probability"].mean()
            
            fig_gender_prob, ax_gender_prob = plt.subplots(figsize=(8, 6))
            bars = ax_gender_prob.bar(range(len(gender_prob)), gender_prob.values, color=["#f97316", "#0099ff"], alpha=0.8, edgecolor="white", linewidth=2)
            
            for bar, val in zip(bars, gender_prob.values):
                height = bar.get_height()
                ax_gender_prob.text(bar.get_x() + bar.get_width()/2., height,
                                   f'{val:.1%}',
                                   ha='center', va='bottom', fontweight='bold', color='white')
            
            ax_gender_prob.set_xticks(range(len(gender_prob)))
            ax_gender_prob.set_xticklabels(gender_prob.index)
            ax_gender_prob.set_title("Average Risk Probability by Gender", fontweight="bold", color="white", fontsize=12)
            ax_gender_prob.set_ylabel("Average Risk Probability", color="white")
            ax_gender_prob.set_ylim(0, 1)
            ax_gender_prob.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
            ax_gender_prob.tick_params(colors="white")
            fig_gender_prob.patch.set_facecolor('#0f1419')
            ax_gender_prob.set_facecolor('#0f1419')
            for spine in ax_gender_prob.spines.values():
                spine.set_color('white')
            st.pyplot(fig_gender_prob, use_container_width=True)
            plt.close()
        
        with col2:
            st.markdown("**Demographics Summary**")
            
            gender_counts = df["gender"].value_counts()
            age_group_counts = df["age_group"].value_counts().sort_index()
            
            st.write(f"**Gender Distribution:**")
            for gender, count in gender_counts.items():
                pct = (count / len(df)) * 100
                st.write(f"  • {gender}: {count} ({pct:.1f}%)")
            
            st.write(f"**Age Group Distribution:**")
            for age_group, count in age_group_counts.items():
                pct = (count / len(df)) * 100
                st.write(f"  • {age_group}: {count} ({pct:.1f}%)")

    # ============================================
    # TAB 4: Risk Factors
    # ============================================
    
    with tab4:
        st.markdown("### 🔬 Top Contributing Risk Factors")
        
        try:
            shap_dict = load_json("models/global_shap_grouped.json")

            shap_series = (
                pd.Series(shap_dict)
                .sort_values(ascending=False)
                .head(12)
            )

            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig_shap, ax_shap = plt.subplots(figsize=(10, 8))
                bars = ax_shap.barh(range(len(shap_series)), shap_series.values, color="#00d4ff", alpha=0.8, edgecolor="white", linewidth=1)
                
                ax_shap.set_yticks(range(len(shap_series)))
                ax_shap.set_yticklabels(shap_series.index)
                ax_shap.set_xlabel("Mean Absolute SHAP Value", color="white", fontweight="bold")
                ax_shap.set_title("Global Feature Importance (SHAP)", fontweight="bold", color="white", fontsize=12)
                ax_shap.tick_params(colors="white")
                fig_shap.patch.set_facecolor('#0f1419')
                ax_shap.set_facecolor('#0f1419')
                for spine in ax_shap.spines.values():
                    spine.set_color('white')
                
                # Add value labels
                for i, (idx, val) in enumerate(shap_series.items()):
                    ax_shap.text(val, i, f' {val:.4f}', va='center', color='white', fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig_shap, use_container_width=True)
                plt.close()
            
            with col2:
                st.markdown("**Feature Importance Ranking**")
                
                for rank, (feature, importance) in enumerate(shap_series.items(), 1):
                    medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
                    st.write(f"{medal} {rank}. **{feature}**")
                    st.write(f"   SHAP: {importance:.4f}")

        except FileNotFoundError:
            st.warning("Global SHAP data not found. Re-run model training to generate this analysis.")

    # ============================================
    # Footer
    # ============================================
    
    st.divider()
    st.caption(
        "✅ Dashboard generated from aggregated prediction records. "
        "Data is used for population-level healthcare planning and preventive analysis. "
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )


