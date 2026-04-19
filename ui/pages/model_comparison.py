import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from ml.utils import load_json
from ui.components import card, info_box, divider, stat_card, inject_page_background


def render_model_comparison():
    """Display model performance comparison dashboard."""
    inject_page_background("analytics")
    
    st.title("🤖 Model Comparison")
    st.markdown("Compare performance metrics across all trained models")
    divider()
    
    try:
        # Load metrics
        metrics = load_json("models/metrics.json")
        best_model_name = metrics.get("best_model", "LogisticRegression")
        all_models = metrics.get("all_models", {})
        
        if not all_models:
            st.error("No model metrics found. Please train models first.")
            return
        
        # ============================================
        # 1. Models Summary Cards
        # ============================================
        st.markdown("### 📊 Models Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Models", len(all_models))
        
        with col2:
            best_accuracy = all_models[best_model_name]["accuracy"]
            st.metric("Best Accuracy", f"{best_accuracy:.2%}")
        
        with col3:
            avg_accuracy = np.mean([m["accuracy"] for m in all_models.values()])
            st.metric("Average Accuracy", f"{avg_accuracy:.2%}")
        
        with col4:
            st.metric("Best Model", best_model_name)
        
        st.divider()
        
        # ============================================
        # 2. Metrics Comparison Table
        # ============================================
        st.markdown("### 📋 Detailed Metrics Comparison")
        
        # Prepare data for comparison table
        comparison_data = []
        for model_name, metrics_data in all_models.items():
            comparison_data.append({
                "Model": model_name,
                "Accuracy": f"{metrics_data['accuracy']:.4f}",
                "Precision": f"{metrics_data['precision']:.4f}",
                "Recall": f"{metrics_data['recall']:.4f}",
                "F1-Score": f"{metrics_data['f1']:.4f}",
                "ROC-AUC": f"{metrics_data['roc_auc']:.4f}"
            })
        
        df_comparison = pd.DataFrame(comparison_data)
        
        # Highlight best model
        def highlight_best(row):
            if row["Model"] == best_model_name:
                return ['background-color: rgba(34, 197, 94, 0.3)'] * len(row)
            return [''] * len(row)
        
        st.dataframe(
            df_comparison.style.apply(highlight_best, axis=1),
            use_container_width=True,
            hide_index=True
        )
        
        st.caption(f"✅ {best_model_name} is the best performing model (highlighted in green)")
        
        st.divider()
        
        # ============================================
        # 3. Visualizations
        # ============================================
        st.markdown("### 📈 Performance Visualizations")
        
        tab1, tab2, tab3 = st.tabs(["Accuracy", "F1-Score", "ROC-AUC"])
        
        # Prepare data for visualizations
        model_names = list(all_models.keys())
        accuracies = [all_models[m]["accuracy"] for m in model_names]
        f1_scores = [all_models[m]["f1"] for m in model_names]
        roc_aucs = [all_models[m]["roc_auc"] for m in model_names]
        
        # Tab 1: Accuracy Comparison
        with tab1:
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#22c55e' if m == best_model_name else '#00d4ff' for m in model_names]
            bars = ax.bar(model_names, accuracies, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
            
            # Add value labels on bars
            for bar, acc in zip(bars, accuracies):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{acc:.2%}',
                       ha='center', va='bottom', fontweight='bold', color='white')
            
            ax.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
            ax.set_xlabel('Model', fontsize=12, fontweight='bold')
            ax.set_title('Model Accuracy Comparison', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylim(0, 1)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.set_facecolor('#0f1419')
            fig.patch.set_facecolor('#0f1419')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')
            
            st.pyplot(fig, use_container_width=True)
            plt.close()
        
        # Tab 2: F1-Score Comparison
        with tab2:
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#22c55e' if m == best_model_name else '#0099ff' for m in model_names]
            bars = ax.bar(model_names, f1_scores, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
            
            # Add value labels on bars
            for bar, f1 in zip(bars, f1_scores):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{f1:.4f}',
                       ha='center', va='bottom', fontweight='bold', color='white')
            
            ax.set_ylabel('F1-Score', fontsize=12, fontweight='bold')
            ax.set_xlabel('Model', fontsize=12, fontweight='bold')
            ax.set_title('Model F1-Score Comparison', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylim(0, 1)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.set_facecolor('#0f1419')
            fig.patch.set_facecolor('#0f1419')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')
            
            st.pyplot(fig, use_container_width=True)
            plt.close()
        
        # Tab 3: ROC-AUC Comparison
        with tab3:
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#22c55e' if m == best_model_name else '#f97316' for m in model_names]
            bars = ax.bar(model_names, roc_aucs, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
            
            # Add value labels on bars
            for bar, auc in zip(bars, roc_aucs):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{auc:.4f}',
                       ha='center', va='bottom', fontweight='bold', color='white')
            
            ax.set_ylabel('ROC-AUC Score', fontsize=12, fontweight='bold')
            ax.set_xlabel('Model', fontsize=12, fontweight='bold')
            ax.set_title('Model ROC-AUC Comparison', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylim(0, 1)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.set_facecolor('#0f1419')
            fig.patch.set_facecolor('#0f1419')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')
            
            st.pyplot(fig, use_container_width=True)
            plt.close()
        
        st.divider()
        
        # ============================================
        # 4. Best Model Analysis
        # ============================================
        st.markdown("### 🏆 Best Model Analysis")
        
        best_metrics = all_models[best_model_name]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Accuracy",
                f"{best_metrics['accuracy']:.2%}",
                delta=f"+{(best_metrics['accuracy'] - np.mean(accuracies))*100:.1f}% vs avg"
            )
        
        with col2:
            st.metric(
                "Precision",
                f"{best_metrics['precision']:.2%}"
            )
        
        with col3:
            st.metric(
                "Recall",
                f"{best_metrics['recall']:.2%}"
            )
        
        with col4:
            st.metric(
                "F1-Score",
                f"{best_metrics['f1']:.4f}"
            )
        
        st.divider()
        
        # ============================================
        # 5. Model Selection Explanation
        # ============================================
        st.markdown("### 📝 Why This Model Was Selected")
        
        card(
            f"✅ {best_model_name}",
            f"""
            <p><strong>Selection Criteria:</strong></p>
            <ul>
                <li><strong>Balanced Performance:</strong> This model achieved the highest balanced score across all metrics.</li>
                <li><strong>Accuracy:</strong> {best_metrics['accuracy']:.2%} - Best accuracy among all models.</li>
                <li><strong>Reliability:</strong> High ROC-AUC score ({best_metrics['roc_auc']:.4f}) indicates excellent discrimination ability.</li>
                <li><strong>Precision & Recall:</strong> Well-balanced precision ({best_metrics['precision']:.2%}) and recall ({best_metrics['recall']:.2%}).</li>
                <li><strong>Clinical Relevance:</strong> High recall ensures fewer false negatives, critical for medical diagnosis.</li>
            </ul>
            <p><strong>Deployment Status:</strong> This model is currently deployed in production for risk predictions.</p>
            """,
            icon="🎯"
        )
        
        # ============================================
        # 6. Model Comparison Summary
        # ============================================
        st.markdown("### 📊 Comparative Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Model Rankings by Accuracy:**")
            accuracy_ranking = sorted(
                [(name, all_models[name]['accuracy']) for name in all_models.keys()],
                key=lambda x: x[1],
                reverse=True
            )
            for idx, (model, acc) in enumerate(accuracy_ranking, 1):
                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "  "
                st.write(f"{medal} {idx}. **{model}**: {acc:.2%}")
        
        with col2:
            st.markdown("**Model Rankings by ROC-AUC:**")
            roc_ranking = sorted(
                [(name, all_models[name]['roc_auc']) for name in all_models.keys()],
                key=lambda x: x[1],
                reverse=True
            )
            for idx, (model, auc) in enumerate(roc_ranking, 1):
                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "  "
                st.write(f"{medal} {idx}. **{model}**: {auc:.4f}")
        
        st.divider()
        
        # ============================================
        # 7. Model Specifications
        # ============================================
        st.markdown("### ⚙️ Model Specifications")
        
        model_info = {
            "LogisticRegression": {
                "Type": "Linear Classification",
                "Best For": "Interpretability, speed",
                "Parameters": "L2 regularization, max_iter=1000"
            },
            "RandomForest": {
                "Type": "Ensemble (Tree-based)",
                "Best For": "Feature importance, non-linearity",
                "Parameters": "n_estimators=100, max_depth=10"
            },
            "SVM_RBF": {
                "Type": "Support Vector Machine",
                "Best For": "Non-linear boundaries, small datasets",
                "Parameters": "kernel=RBF, C=1.0, gamma=auto"
            },
            "GradientBoosting": {
                "Type": "Ensemble (Boosting)",
                "Best For": "Sequential error correction",
                "Parameters": "n_estimators=100, learning_rate=0.1"
            }
        }
        
        selected_spec = st.selectbox(
            "Select a model to view specifications:",
            list(model_info.keys())
        )
        
        if selected_spec in model_info:
            spec = model_info[selected_spec]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Model Type:**\n{spec['Type']}")
            
            with col2:
                st.write(f"**Use Case:**\n{spec['Best For']}")
            
            with col3:
                st.write(f"**Parameters:**\n{spec['Parameters']}")
    
    except Exception as e:
        st.error(f"Error loading model comparison: {str(e)}")
        st.info("Please ensure metrics.json exists in the models directory.")
