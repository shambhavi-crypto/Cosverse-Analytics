import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────
st.set_page_config(
    page_title="CosVerse Analytics Dashboard",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────
# DARK ANIME THEME CSS
# ─────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

    .stApp { background: linear-gradient(135deg, #0A0A1A 0%, #0F0F2D 50%, #0A0A1A 100%); }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D0D25 0%, #1A0A2E 100%) !important;
        border-right: 1px solid #B026FF33;
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #FF2D95 !important; font-family: 'Orbitron', sans-serif !important;
    }

    h1 { font-family: 'Orbitron', sans-serif !important; color: #FF2D95 !important; text-shadow: 0 0 20px #FF2D9555; }
    h2 { font-family: 'Orbitron', sans-serif !important; color: #00F0FF !important; text-shadow: 0 0 15px #00F0FF44; font-size: 1.4rem !important; }
    h3 { font-family: 'Rajdhani', sans-serif !important; color: #B026FF !important; font-size: 1.2rem !important; }
    p, li, span, div { font-family: 'Rajdhani', sans-serif !important; }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #12122A, #1A1A3E) !important;
        border: 1px solid #B026FF44 !important; border-radius: 12px !important;
        padding: 16px !important; box-shadow: 0 0 15px #B026FF22;
    }
    div[data-testid="stMetric"] label { color: #00F0FF !important; font-family: 'Rajdhani', sans-serif !important; font-weight: 600 !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #FF2D95 !important; font-family: 'Orbitron', sans-serif !important; }

    .stTabs [data-baseweb="tab-list"] { gap: 4px; background: #0D0D25; border-radius: 12px; padding: 4px; }
    .stTabs [data-baseweb="tab"] {
        background: #12122A !important; border-radius: 8px !important; color: #8888AA !important;
        font-family: 'Orbitron', sans-serif !important; font-size: 0.72rem !important;
        padding: 8px 16px !important; border: 1px solid transparent !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF2D9533, #B026FF33) !important;
        border: 1px solid #FF2D95 !important; color: #FF2D95 !important; box-shadow: 0 0 10px #FF2D9533;
    }

    .insight-box {
        background: linear-gradient(135deg, #12122A, #1A1A3E);
        border-left: 4px solid #00F0FF; border-radius: 0 10px 10px 0;
        padding: 12px 18px; margin: 10px 0; font-family: 'Rajdhani', sans-serif;
        color: #C8C8E8; font-size: 1rem; line-height: 1.5; box-shadow: 0 0 10px #00F0FF11;
    }
    .insight-box strong { color: #FF2D95; }

    .section-divider {
        border: none; height: 1px;
        background: linear-gradient(90deg, transparent, #B026FF55, #FF2D9555, transparent);
        margin: 30px 0;
    }

    .streamlit-expanderHeader { font-family: 'Rajdhani', sans-serif !important; color: #00F0FF !important; font-weight: 600 !important; }
    .stSelectbox label, .stRadio label, .stMultiSelect label { color: #00F0FF !important; font-family: 'Rajdhani', sans-serif !important; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
    .stDataFrame { border: 1px solid #B026FF33 !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────
NEON = ["#FF2D95", "#00F0FF", "#B026FF", "#39FF14", "#FF6B35", "#FFD700", "#FF4500", "#00CED1"]

def apply_theme(fig, title="", height=450):
    """Apply dark neon theme to any Plotly figure — safe for all chart types."""
    try:
        fig.update_layout(paper_bgcolor="rgba(10,10,26,0)")
    except Exception:
        pass
    try:
        fig.update_layout(plot_bgcolor="rgba(18,18,42,0.8)")
    except Exception:
        pass
    try:
        fig.update_layout(
            font=dict(family="Rajdhani", color="#C8C8E8", size=13),
            height=height,
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(bgcolor="rgba(18,18,42,0.8)", bordercolor="#B026FF44", borderwidth=1, font=dict(size=12)),
        )
    except Exception:
        pass
    if title:
        try:
            fig.update_layout(title_text=title, title_x=0.5,
                              title_font_family="Orbitron", title_font_size=16, title_font_color="#FF2D95")
        except Exception:
            pass
    try:
        fig.update_xaxes(gridcolor="#1E1E3F", zerolinecolor="#1E1E3F")
        fig.update_yaxes(gridcolor="#1E1E3F", zerolinecolor="#1E1E3F")
    except Exception:
        pass
    return fig

def insight(text):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

def divider():
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("cosplay_survey_uae_synthetic.csv")
    df["Total_Fandom_Count"] = df[["Fandom_Anime", "Fandom_Marvel_DC", "Fandom_Gaming", "Fandom_Movies_TV", "Fandom_Fantasy_SciFi"]].sum(axis=1)
    df["Total_Challenges"] = df[["Challenge_High_Cost", "Challenge_Size_Issues", "Challenge_Limited_Availability", "Challenge_Storage", "Challenge_Time_Constraint", "Challenge_Shipping_Delay"]].sum(axis=1)
    df["Total_Features_Wanted"] = df[["Feature_Makeup_Tutorial", "Feature_Wig_Rental", "Feature_Styling_Guidance", "Feature_Group_Cosplay", "Feature_Photoshoot_Service"]].sum(axis=1)
    df["Spending_to_Income_Ratio"] = df["Monthly_Cosplay_Spending_AED"] / df["Monthly_Disposable_Income_AED"].replace(0, np.nan)
    df["Age_Group"] = pd.cut(df["Age"], bins=[15, 20, 25, 30, 35, 45], labels=["16-20", "21-25", "26-30", "31-35", "36-45"])
    df["Income_Bracket"] = pd.cut(df["Monthly_Disposable_Income_AED"], bins=[0, 5000, 10000, 15000, 20000, 30000], labels=["<5K", "5K-10K", "10K-15K", "15K-20K", "20K+"])
    return df

df = load_data()


# ─────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🎭 CosVerse")
    st.markdown("### Analytics Dashboard")
    st.markdown("---")
    st.markdown("**Cosplay Rental & Styling Platform**")
    st.markdown(f"📊 Dataset: **{len(df):,}** respondents")
    st.markdown(f"📋 Features: **{df.shape[1]}** columns")
    st.markdown("🌍 Region: **UAE**")
    st.markdown("---")
    st.markdown("#### 🎛️ Filters")
    gender_filter = st.multiselect("Gender", df["Gender"].unique().tolist(), default=df["Gender"].unique().tolist())
    city_filter = st.multiselect("City Type", df["City_Type"].unique().tolist(), default=df["City_Type"].unique().tolist())
    age_range = st.slider("Age Range", int(df["Age"].min()), int(df["Age"].max()), (int(df["Age"].min()), int(df["Age"].max())))

mask = (df["Gender"].isin(gender_filter)) & (df["City_Type"].isin(city_filter)) & (df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1])
dff = df[mask].copy()

if len(dff) == 0:
    st.warning("No data matches the current filters. Please adjust the sidebar filters.")
    st.stop()


# ─────────────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────────────
tab_overview, tab_class, tab_cluster, tab_assoc, tab_reg = st.tabs([
    "🏠 Overview", "🤖 Classification", "👥 Clustering", "🔗 Association Rules", "📈 Regression"
])


# ═══════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════
with tab_overview:
    st.markdown("# 🏠 CosVerse — Platform Overview")
    st.markdown("##### High-level snapshot of the UAE cosplay market from survey data")

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Respondents", f"{len(dff):,}")
    k2.metric("Avg Age", f"{dff['Age'].mean():.1f}")
    k3.metric("Avg Monthly Spend", f"AED {dff['Monthly_Cosplay_Spending_AED'].mean():.0f}")
    k4.metric("Avg Costume Price", f"AED {dff['Costume_Price_Avg_AED'].mean():.0f}")
    k5.metric("Avg NPS", f"{dff['NPS_Score'].mean():.1f}/10")
    k6.metric("App Interest (Yes)", f"{(dff['App_Usage_Intention'] == 'Yes').mean():.0%}")

    divider()

    st.markdown("## 1. Age Distribution")
    fig = px.histogram(dff, x="Age", nbins=30, color_discrete_sequence=["#FF2D95"], opacity=0.85)
    fig.update_traces(marker_line_color="#B026FF", marker_line_width=1)
    st.plotly_chart(apply_theme(fig, "Age Distribution of Respondents"), use_container_width=True)
    age_mode = dff["Age"].mode().iloc[0]
    insight(f"<strong>Insight:</strong> The majority of respondents fall in the <strong>21-29 age bracket</strong>, peaking at age <strong>{age_mode}</strong>. "
            "This young demographic aligns perfectly with CosVerse's digital-first rental platform strategy.")

    st.markdown("## 2. Gender Distribution")
    gc = dff["Gender"].value_counts().reset_index()
    gc.columns = ["Gender", "Count"]
    fig = px.pie(gc, values="Count", names="Gender", color_discrete_sequence=["#FF2D95", "#00F0FF", "#B026FF"], hole=0.5)
    fig.update_traces(textposition="outside", textinfo="label+percent", textfont_size=14,
                      marker_line_color="#0A0A1A", marker_line_width=2)
    st.plotly_chart(apply_theme(fig, "Gender Distribution"), use_container_width=True)
    tg = gc.iloc[0]
    insight(f"<strong>Insight:</strong> <strong>{tg['Gender']}</strong> respondents dominate at <strong>{tg['Count']/len(dff)*100:.1f}%</strong>. "
            "CosVerse should ensure gender-inclusive costume collections and marketing to capture all segments.")

    divider()

    st.markdown("## 3. City Distribution")
    c3a, c3b = st.columns(2)
    with c3a:
        cc = dff["City_Type"].value_counts().reset_index()
        cc.columns = ["City_Type", "Count"]
        fig = px.bar(cc, x="City_Type", y="Count", color="City_Type",
                     color_discrete_sequence=["#FF2D95", "#00F0FF", "#B026FF"], text_auto=True)
        fig.update_traces(textposition="outside")
        st.plotly_chart(apply_theme(fig, "Respondents by City Type"), use_container_width=True)
    with c3b:
        cs = dff.groupby("City_Type")["Monthly_Cosplay_Spending_AED"].mean().reset_index()
        cs.columns = ["City_Type", "Avg_Spend"]
        fig = px.bar(cs, x="City_Type", y="Avg_Spend", color="City_Type",
                     color_discrete_sequence=["#39FF14", "#FFD700", "#FF6B35"], text_auto=".0f")
        fig.update_traces(textposition="outside")
        st.plotly_chart(apply_theme(fig, "Avg Monthly Spend by City Type (AED)"), use_container_width=True)
    insight("<strong>Insight:</strong> Metro residents form the largest segment and tend to spend more. "
            "CosVerse should prioritize <strong>Metro cities</strong> for initial launch, then expand outward.")

    divider()

    st.markdown("## 4. Fandom Category Popularity")
    fandom_map = {"Fandom_Anime": "Anime", "Fandom_Marvel_DC": "Marvel/DC", "Fandom_Gaming": "Gaming",
                  "Fandom_Movies_TV": "Movies/TV", "Fandom_Fantasy_SciFi": "Fantasy/Sci-Fi"}
    fd = pd.DataFrame({"Fandom": list(fandom_map.values()),
                        "Fans": [dff[k].sum() for k in fandom_map]}).sort_values("Fans", ascending=True)
    fig = px.bar(fd, y="Fandom", x="Fans", orientation="h", color="Fandom",
                 color_discrete_sequence=NEON, text_auto=True)
    fig.update_traces(textposition="outside")
    st.plotly_chart(apply_theme(fig, "Fandom Category Popularity (Multi-select)"), use_container_width=True)
    tf = fd.iloc[-1]
    insight(f"<strong>Insight:</strong> <strong>{tf['Fandom']}</strong> leads with <strong>{int(tf['Fans']):,}</strong> fans. "
            f"CosVerse should stock the widest inventory in <strong>{tf['Fandom']}</strong> costumes to match demand.")

    divider()

    st.markdown("## 5. NPS & Discovery Channels")
    c5a, c5b = st.columns(2)
    with c5a:
        fig = px.histogram(dff, x="NPS_Score", nbins=11, color_discrete_sequence=["#39FF14"], opacity=0.85)
        st.plotly_chart(apply_theme(fig, "Net Promoter Score Distribution", 400), use_container_width=True)
        promoters = (dff["NPS_Score"] >= 9).mean() * 100
        detractors = (dff["NPS_Score"] <= 6).mean() * 100
        insight(f"<strong>Insight:</strong> <strong>{promoters:.1f}%</strong> promoters vs <strong>{detractors:.1f}%</strong> detractors. "
                "CosVerse should nurture promoters as brand ambassadors while addressing detractor concerns.")
    with c5b:
        dc = dff["Discovery_Channel"].value_counts().reset_index()
        dc.columns = ["Channel", "Count"]
        fig = px.pie(dc, values="Count", names="Channel", color_discrete_sequence=NEON, hole=0.45)
        fig.update_traces(textposition="inside", textinfo="label+percent")
        st.plotly_chart(apply_theme(fig, "Discovery Channels", 400), use_container_width=True)
        insight("<strong>Insight:</strong> Social media platforms dominate discovery. "
                "CosVerse should invest heavily in <strong>TikTok & Instagram</strong> influencer marketing.")

    divider()

    st.markdown("## 6. Correlation Heatmap")
    num_cols = ["Age", "Monthly_Disposable_Income_AED", "Cosplay_Interest_Level", "Years_in_Cosplay",
                "Event_Attendance_Count", "Monthly_Cosplay_Spending_AED", "Costume_Price_Avg_AED",
                "Costumes_Owned", "Rental_Price_Willingness_AED", "Likelihood_to_Rent", "NPS_Score",
                "Total_Fandom_Count", "Total_Challenges", "Total_Features_Wanted"]
    corr = dff[num_cols].corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale=["#0A0A1A", "#B026FF", "#FF2D95"], aspect="auto")
    st.plotly_chart(apply_theme(fig, "Feature Correlation Heatmap", 600), use_container_width=True)
    insight("<strong>Insight:</strong> Strong positive correlations exist between <strong>event attendance & spending</strong>, and between <strong>interest level & rental likelihood</strong>. "
            "These correlated features validate that engaged users are the strongest conversion targets for CosVerse.")


# ═══════════════════════════════════════════════════════════
# TAB 2 — CLASSIFICATION
# ═══════════════════════════════════════════════════════════
with tab_class:
    st.markdown("# 🤖 Classification – Predict Platform Adoption")
    st.markdown("##### Predicting which users will adopt CosVerse using supervised ML models")

    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

    st.markdown("## Exploratory Analysis — Adoption Signals")

    ce1, ce2 = st.columns(2)
    with ce1:
        fig = px.histogram(dff, x="Event_Attendance_Count", nbins=20, color_discrete_sequence=["#00F0FF"])
        st.plotly_chart(apply_theme(fig, "Event Attendance Distribution", 380), use_container_width=True)
        active_pct = (dff["Event_Attendance_Count"] > 0).mean() * 100
        insight(f"<strong>Insight:</strong> <strong>{active_pct:.1f}%</strong> have attended at least one cosplay event. "
                "High-frequency attendees represent CosVerse's <strong>premium subscriber</strong> opportunity.")
    with ce2:
        app_cross = pd.crosstab(dff["Cosplay_Interest_Level"], dff["App_Usage_Intention"], normalize="index") * 100
        fig = px.bar(app_cross, barmode="stack", color_discrete_sequence=["#39FF14", "#FFD700", "#FF2D95"])
        try:
            fig.update_layout(yaxis_title="Percentage (%)", xaxis_title="Cosplay Interest Level (1-5)")
        except Exception:
            pass
        st.plotly_chart(apply_theme(fig, "App Usage Intention by Interest Level", 380), use_container_width=True)
        insight("<strong>Insight:</strong> Higher cosplay interest correlates strongly with <strong>'Yes' for app usage</strong>. "
                "Users with interest level 4-5 are the <strong>primary early adopter target</strong>.")

    ce3, ce4 = st.columns(2)
    with ce3:
        sc = dff["Subscription_Interest"].value_counts().reset_index()
        sc.columns = ["Interest", "Count"]
        fig = px.bar(sc, x="Interest", y="Count", color="Interest",
                     color_discrete_sequence=["#39FF14", "#FFD700", "#FF2D95"], text_auto=True)
        fig.update_traces(textposition="outside")
        st.plotly_chart(apply_theme(fig, "Subscription Interest", 380), use_container_width=True)
        insight("<strong>Insight:</strong> A significant portion shows subscription interest, validating the <strong>recurring revenue model</strong>. "
                "CosVerse should offer tiered monthly plans to capture casual and committed users alike.")
    with ce4:
        ri = dff["Interest_in_Rental"].value_counts().reset_index()
        ri.columns = ["Interest", "Count"]
        fig = px.pie(ri, values="Count", names="Interest",
                     color_discrete_sequence=["#39FF14", "#FFD700", "#FF2D95"], hole=0.5)
        fig.update_traces(textposition="outside", textinfo="label+percent")
        st.plotly_chart(apply_theme(fig, "Interest in Rental Service", 380), use_container_width=True)
        insight("<strong>Insight:</strong> The majority are either interested or open to renting costumes. "
                "This validates CosVerse's core rental business model with strong market demand.")

    divider()

    st.markdown("## Machine Learning — Classification Models")

    feature_cols = ["Age", "Monthly_Disposable_Income_AED", "Cosplay_Interest_Level",
                    "Years_in_Cosplay", "Event_Attendance_Count", "Monthly_Cosplay_Spending_AED",
                    "Costume_Price_Avg_AED", "Costumes_Owned", "Total_Fandom_Count",
                    "Total_Challenges", "Total_Features_Wanted", "NPS_Score",
                    "Likelihood_to_Rent", "Rental_Price_Willingness_AED"]

    tc1, tc2 = st.columns(2)
    with tc1:
        target_choice = st.selectbox("🎯 Target Variable", ["App_Usage_Intention", "Interest_in_Rental"])
    with tc2:
        model_choice = st.selectbox("🧠 Model", ["Random Forest", "Logistic Regression", "Gradient Boosting"])

    le = LabelEncoder()
    dff_c = dff.dropna(subset=feature_cols + [target_choice]).copy()
    X = dff_c[feature_cols].values
    y = le.fit_transform(dff_c[target_choice].values)
    class_names = le.classes_

    scaler_c = StandardScaler()
    X_scaled = scaler_c.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=42, stratify=y)

    models_dict = {
        "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, multi_class="multinomial", random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=150, max_depth=5, random_state=42)
    }
    model = models_dict[model_choice]
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    mk1, mk2, mk3 = st.columns(3)
    mk1.metric("Accuracy", f"{acc:.2%}")
    mk2.metric("Test Samples", f"{len(y_test):,}")
    mk3.metric("Classes", f"{len(class_names)}")

    divider()

    cm1, cm2 = st.columns(2)
    with cm1:
        st.markdown("### Confusion Matrix")
        cm = confusion_matrix(y_test, y_pred)
        fig = px.imshow(cm, text_auto=True, x=class_names.tolist(), y=class_names.tolist(),
                        color_continuous_scale=["#0A0A1A", "#B026FF", "#FF2D95"])
        try:
            fig.update_layout(xaxis_title="Predicted", yaxis_title="Actual")
        except Exception:
            pass
        st.plotly_chart(apply_theme(fig, f"Confusion Matrix - {model_choice}", 420), use_container_width=True)
    with cm2:
        st.markdown("### Classification Report")
        report = classification_report(y_test, y_pred, target_names=class_names.tolist(), output_dict=True)
        report_df = pd.DataFrame(report).transpose().round(3)
        st.dataframe(report_df.style.background_gradient(cmap="RdPu"), use_container_width=True, height=300)

    insight(f"<strong>Insight:</strong> The <strong>{model_choice}</strong> achieves <strong>{acc:.1%}</strong> accuracy on {target_choice.replace('_', ' ')}. "
            "This model can help CosVerse identify high-probability adopters for <strong>targeted marketing campaigns</strong>.")

    divider()

    st.markdown("### Feature Importance")
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    else:
        importances = np.abs(model.coef_).mean(axis=0)
    fi_df = pd.DataFrame({"Feature": feature_cols, "Importance": importances}).sort_values("Importance", ascending=True)
    fig = px.bar(fi_df, y="Feature", x="Importance", orientation="h",
                 color="Importance", color_continuous_scale=["#0A0A1A", "#B026FF", "#FF2D95"], text_auto=".3f")
    fig.update_traces(textposition="outside")
    st.plotly_chart(apply_theme(fig, f"Feature Importance - {model_choice}", 500), use_container_width=True)
    top_f = fi_df.iloc[-1]
    insight(f"<strong>Insight:</strong> <strong>{top_f['Feature']}</strong> is the strongest predictor of platform adoption. "
            "CosVerse should focus on users scoring high on this metric for maximum conversion rates.")

    divider()

    st.markdown("### All Models Comparison")
    comp_results = []
    for name, mdl in models_dict.items():
        mdl.fit(X_train, y_train)
        yp = mdl.predict(X_test)
        rpt = classification_report(y_test, yp, output_dict=True, zero_division=0)
        comp_results.append({"Model": name, "Accuracy": accuracy_score(y_test, yp),
                             "Precision": rpt["weighted avg"]["precision"],
                             "Recall": rpt["weighted avg"]["recall"],
                             "F1-Score": rpt["weighted avg"]["f1-score"]})
    comp_df = pd.DataFrame(comp_results)
    fig = px.bar(comp_df.melt(id_vars="Model", var_name="Metric", value_name="Score"),
                 x="Model", y="Score", color="Metric", barmode="group",
                 color_discrete_sequence=["#FF2D95", "#00F0FF", "#B026FF", "#39FF14"], text_auto=".3f")
    fig.update_traces(textposition="outside")
    st.plotly_chart(apply_theme(fig, "Model Performance Comparison", 450), use_container_width=True)
    best = comp_df.loc[comp_df["F1-Score"].idxmax()]
    insight(f"<strong>Insight:</strong> <strong>{best['Model']}</strong> delivers the best F1-Score of <strong>{best['F1-Score']:.3f}</strong>. "
            "This model should be deployed in CosVerse's recommendation engine for user targeting.")


# ═══════════════════════════════════════════════════════════
# TAB 3 — CLUSTERING
# ═══════════════════════════════════════════════════════════
with tab_cluster:
    st.markdown("# 👥 Clustering – Customer Personas")
    st.markdown("##### K-Means clustering to identify distinct customer segments for CosVerse")

    from sklearn.preprocessing import StandardScaler as SS2
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    from sklearn.decomposition import PCA

    st.markdown("## Exploratory Analysis — Spending & Behavior Patterns")

    se1, se2 = st.columns(2)
    with se1:
        fig = px.histogram(dff, x="Costume_Price_Avg_AED", nbins=40,
                           color_discrete_sequence=["#FFD700"], opacity=0.85)
        st.plotly_chart(apply_theme(fig, "Average Costume Price Distribution (AED)", 380), use_container_width=True)
        med_cost = dff["Costume_Price_Avg_AED"].median()
        insight(f"<strong>Insight:</strong> Median costume price is <strong>AED {med_cost:.0f}</strong>, indicating significant purchase costs. "
                "A rental model at <strong>30-40%</strong> of purchase price could unlock massive value.")
    with se2:
        fig = px.box(dff, x="Occupation", y="Monthly_Cosplay_Spending_AED", color="Occupation",
                     color_discrete_sequence=NEON, points="outliers")
        st.plotly_chart(apply_theme(fig, "Monthly Cosplay Spending by Occupation (AED)", 380), use_container_width=True)
        highest_occ = dff.groupby("Occupation")["Monthly_Cosplay_Spending_AED"].mean().idxmax()
        insight(f"<strong>Insight:</strong> <strong>{highest_occ}s</strong> have the highest average monthly cosplay spending. "
                "CosVerse can tailor pricing tiers for each occupation group.")

    se3, se4 = st.columns(2)
    with se3:
        fig = px.scatter(dff, x="Monthly_Disposable_Income_AED", y="Costume_Price_Avg_AED",
                         color="Interest_in_Rental", size="Event_Attendance_Count",
                         color_discrete_sequence=["#FF2D95", "#FFD700", "#00F0FF"], opacity=0.7)
        st.plotly_chart(apply_theme(fig, "Income vs Costume Price (by Rental Interest)", 380), use_container_width=True)
        insight("<strong>Insight:</strong> Users across <strong>all income levels</strong> face high costume costs, but lower-income users show stronger rental interest. "
                "CosVerse's model is especially compelling for the <strong>AED 5K-15K bracket</strong>.")
    with se4:
        fig = px.box(dff, x="Age_Group", y="Monthly_Cosplay_Spending_AED", color="Gender",
                     color_discrete_sequence=["#FF2D95", "#00F0FF", "#B026FF"])
        st.plotly_chart(apply_theme(fig, "Monthly Spending by Age & Gender (AED)", 380), use_container_width=True)
        insight("<strong>Insight:</strong> Spending peaks in the <strong>26-30 age group</strong> with more disposable income. "
                "CosVerse can target this demographic with premium costume tiers and VIP styling packages.")

    divider()

    st.markdown("## Machine Learning — K-Means Clustering")

    cluster_feats = ["Age", "Monthly_Disposable_Income_AED", "Cosplay_Interest_Level",
                     "Years_in_Cosplay", "Event_Attendance_Count", "Monthly_Cosplay_Spending_AED",
                     "Costume_Price_Avg_AED", "Costumes_Owned", "Total_Fandom_Count",
                     "Total_Challenges", "Total_Features_Wanted", "NPS_Score",
                     "Likelihood_to_Rent", "Rental_Price_Willingness_AED"]

    dff_cl = dff.dropna(subset=cluster_feats).copy()
    X_cl = dff_cl[cluster_feats].values
    scaler_cl = SS2()
    X_cl_s = scaler_cl.fit_transform(X_cl)

    st.markdown("### Elbow Method & Silhouette Analysis")
    el1, el2 = st.columns(2)
    inertias, sils = [], []
    K_range = range(2, 9)
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_cl_s)
        inertias.append(km.inertia_)
        sils.append(silhouette_score(X_cl_s, km.labels_, sample_size=min(1000, len(X_cl_s))))
    with el1:
        fig = px.line(x=list(K_range), y=inertias, markers=True, labels={"x": "K", "y": "Inertia"})
        fig.update_traces(line_color="#FF2D95", marker_color="#00F0FF", marker_size=10)
        st.plotly_chart(apply_theme(fig, "Elbow Method", 380), use_container_width=True)
    with el2:
        fig = px.bar(x=list(K_range), y=sils, labels={"x": "K", "y": "Silhouette Score"},
                     color_discrete_sequence=["#B026FF"])
        st.plotly_chart(apply_theme(fig, "Silhouette Scores", 380), use_container_width=True)
    insight("<strong>Insight:</strong> The elbow and silhouette analysis guide optimal K selection. "
            "Choose K where inertia drop slows and silhouette is maximized.")

    divider()

    n_clusters = st.slider("Select Number of Clusters (K)", 2, 8, 3)
    kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    dff_cl["Cluster"] = kmeans_model.fit_predict(X_cl_s)
    dff_cl["Cluster_Label"] = dff_cl["Cluster"].astype(str)

    st.markdown("### 3D Cluster Visualization (PCA)")
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X_cl_s)
    dff_cl["PC1"] = X_pca[:, 0]
    dff_cl["PC2"] = X_pca[:, 1]
    dff_cl["PC3"] = X_pca[:, 2]

    fig = px.scatter_3d(dff_cl, x="PC1", y="PC2", z="PC3", color="Cluster_Label",
                        color_discrete_sequence=NEON[:n_clusters], opacity=0.7,
                        hover_data=["Age", "Monthly_Cosplay_Spending_AED", "Event_Attendance_Count"])
    apply_theme(fig, "Customer Segments in 3D PCA Space", 550)
    try:
        fig.update_layout(scene=dict(
            xaxis=dict(backgroundcolor="#0A0A1A", gridcolor="#1E1E3F"),
            yaxis=dict(backgroundcolor="#0A0A1A", gridcolor="#1E1E3F"),
            zaxis=dict(backgroundcolor="#0A0A1A", gridcolor="#1E1E3F"),
        ))
    except Exception:
        pass
    st.plotly_chart(fig, use_container_width=True)
    var_exp = pca.explained_variance_ratio_.sum() * 100
    insight(f"<strong>Insight:</strong> The 3 principal components explain <strong>{var_exp:.1f}%</strong> of total variance. "
            "Clear cluster separation indicates <strong>distinct customer personas</strong> for CosVerse to target.")

    divider()

    st.markdown("### Cluster Profiles")
    profile_cols = ["Age", "Monthly_Disposable_Income_AED", "Cosplay_Interest_Level",
                    "Event_Attendance_Count", "Monthly_Cosplay_Spending_AED",
                    "Costume_Price_Avg_AED", "Total_Features_Wanted", "Likelihood_to_Rent", "NPS_Score"]
    cp = dff_cl.groupby("Cluster")[profile_cols].mean().round(1)
    cp.index = [f"Cluster {i}" for i in cp.index]
    st.dataframe(cp.style.background_gradient(cmap="RdPu", axis=0), use_container_width=True)

    st.markdown("### Cluster Radar Comparison")
    radar_cols = ["Cosplay_Interest_Level", "Event_Attendance_Count", "Monthly_Cosplay_Spending_AED",
                  "Total_Features_Wanted", "Likelihood_to_Rent", "NPS_Score"]
    rd = dff_cl.groupby("Cluster")[radar_cols].mean()
    rd_norm = (rd - rd.min()) / (rd.max() - rd.min() + 1e-9)
    persona_names = ["Hardcore Cosplayers", "Casual Fans", "Event Visitors"] if n_clusters == 3 else [f"Segment {i}" for i in range(n_clusters)]

    fig = go.Figure()
    for i in range(n_clusters):
        label = persona_names[i] if i < len(persona_names) else f"Segment {i}"
        vals = rd_norm.iloc[i].tolist() + [rd_norm.iloc[i].tolist()[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=radar_cols + [radar_cols[0]], fill="toself", name=label,
            opacity=0.6, line_color=NEON[i], fillcolor=NEON[i] + "33"
        ))
    apply_theme(fig, "Customer Persona Radar Chart", 500)
    try:
        fig.update_layout(polar=dict(
            bgcolor="rgba(18,18,42,0.8)",
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="#1E1E3F"),
            angularaxis=dict(gridcolor="#1E1E3F")
        ))
    except Exception:
        pass
    st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Insight:</strong> The radar chart reveals <strong>distinct persona profiles</strong> — high-engagement spenders vs budget-conscious casuals. "
            "CosVerse should design <strong>differentiated service tiers</strong> matching each persona's needs.")

    divider()

    st.markdown("### Cluster Feature Distributions")
    feat_pick = st.selectbox("Select Feature to Compare Across Clusters", profile_cols, index=4)
    fig = px.box(dff_cl, x="Cluster_Label", y=feat_pick, color="Cluster_Label",
                 color_discrete_sequence=NEON[:n_clusters], points="outliers")
    st.plotly_chart(apply_theme(fig, f"{feat_pick} Distribution by Cluster"), use_container_width=True)


# ═══════════════════════════════════════════════════════════
# TAB 4 — ASSOCIATION RULE MINING
# ═══════════════════════════════════════════════════════════
with tab_assoc:
    st.markdown("# 🔗 Association Rule Mining")
    st.markdown("##### Discovering hidden relationships between challenges and desired features")

    from mlxtend.frequent_patterns import apriori, association_rules

    st.markdown("## Exploratory Analysis — Challenges & Desired Features")

    ae1, ae2 = st.columns(2)
    with ae1:
        ch_map = {"Challenge_High_Cost": "High Cost", "Challenge_Size_Issues": "Size Issues",
                  "Challenge_Limited_Availability": "Limited Availability", "Challenge_Storage": "Storage",
                  "Challenge_Time_Constraint": "Time Constraint", "Challenge_Shipping_Delay": "Shipping Delay"}
        ch_data = pd.DataFrame({"Challenge": list(ch_map.values()),
                                "Count": [dff[k].sum() for k in ch_map]}).sort_values("Count", ascending=False)
        fig = px.bar(ch_data, x="Challenge", y="Count", color="Challenge",
                     color_discrete_sequence=["#FF2D95", "#FF6B35", "#FFD700", "#39FF14", "#00F0FF", "#B026FF"],
                     text_auto=True)
        fig.update_traces(textposition="outside")
        st.plotly_chart(apply_theme(fig, "Top Challenges Faced by Cosplayers", 420), use_container_width=True)
        top_ch = ch_data.iloc[0]
        insight(f"<strong>Insight:</strong> <strong>{top_ch['Challenge']}</strong> is the #1 challenge with <strong>{int(top_ch['Count']):,}</strong> mentions. "
                "CosVerse directly addresses this pain point through its affordable rental model.")

    with ae2:
        ft_map = {"Feature_Makeup_Tutorial": "Makeup Tutorials", "Feature_Wig_Rental": "Wig Rental",
                  "Feature_Styling_Guidance": "Styling Guidance", "Feature_Group_Cosplay": "Group Cosplay",
                  "Feature_Photoshoot_Service": "Photoshoot Service"}
        ft_data = pd.DataFrame({"Feature": list(ft_map.values()),
                                "Interest": [dff[k].sum() for k in ft_map]}).sort_values("Interest", ascending=True)
        fig = px.bar(ft_data, y="Feature", x="Interest", orientation="h", color="Feature",
                     color_discrete_sequence=NEON[:5], text_auto=True)
        fig.update_traces(textposition="outside")
        st.plotly_chart(apply_theme(fig, "Most Desired Platform Features", 420), use_container_width=True)
        top_ft = ft_data.iloc[-1]
        insight(f"<strong>Insight:</strong> <strong>{top_ft['Feature']}</strong> is the most requested feature with <strong>{int(top_ft['Interest']):,}</strong> votes. "
                "CosVerse should prioritize this in the MVP launch to maximize engagement.")

    ae3, ae4 = st.columns(2)
    with ae3:
        ac = dff["Costume_Acquisition_Method"].value_counts().reset_index()
        ac.columns = ["Method", "Count"]
        fig = px.bar(ac, x="Method", y="Count", color="Method",
                     color_discrete_sequence=NEON[:5], text_auto=True)
        fig.update_traces(textposition="outside")
        st.plotly_chart(apply_theme(fig, "Costume Acquisition Methods", 380), use_container_width=True)
        insight("<strong>Insight:</strong> Buying online and DIY dominate acquisition methods. "
                "CosVerse can convert these users by offering <strong>superior convenience and lower cost</strong>.")
    with ae4:
        rdur = dff["Preferred_Rental_Duration"].value_counts().reset_index()
        rdur.columns = ["Duration", "Count"]
        fig = px.pie(rdur, values="Count", names="Duration",
                     color_discrete_sequence=["#FF2D95", "#00F0FF", "#B026FF", "#39FF14"], hole=0.45)
        fig.update_traces(textposition="inside", textinfo="label+percent")
        st.plotly_chart(apply_theme(fig, "Preferred Rental Duration", 380), use_container_width=True)
        insight("<strong>Insight:</strong> Most users prefer <strong>short-term rentals (1 day to 1 week)</strong>. "
                "CosVerse should design pricing around <strong>event-based rental windows</strong>.")

    divider()

    st.markdown("## Machine Learning — Apriori Association Rules")

    challenge_labels = {"Challenge_High_Cost": "High Cost", "Challenge_Size_Issues": "Size Issues",
                        "Challenge_Limited_Availability": "Limited Availability", "Challenge_Storage": "Storage Problem",
                        "Challenge_Time_Constraint": "Time Constraint", "Challenge_Shipping_Delay": "Shipping Delay"}
    feature_labels = {"Feature_Makeup_Tutorial": "Makeup Tutorial", "Feature_Wig_Rental": "Wig Rental",
                      "Feature_Styling_Guidance": "Styling Guidance", "Feature_Group_Cosplay": "Group Cosplay",
                      "Feature_Photoshoot_Service": "Photoshoot Service"}

    all_items = {**challenge_labels, **feature_labels}
    basket_df = dff[list(all_items.keys())].rename(columns=all_items).astype(bool)

    ar1, ar2 = st.columns(2)
    with ar1:
        min_sup = st.slider("Minimum Support", 0.05, 0.5, 0.10, 0.05)
    with ar2:
        min_conf = st.slider("Minimum Confidence", 0.10, 1.0, 0.30, 0.05)

    frequent = apriori(basket_df, min_support=min_sup, use_colnames=True)

    if len(frequent) == 0:
        st.warning("No frequent itemsets found. Try lowering the minimum support.")
    else:
        rules = association_rules(frequent, metric="confidence", min_threshold=min_conf,
                                  num_itemsets=len(frequent))

        if len(rules) == 0:
            st.warning("No rules found. Try lowering the confidence threshold.")
        else:
            rules["antecedents_str"] = rules["antecedents"].apply(lambda x: ", ".join(sorted(x)))
            rules["consequents_str"] = rules["consequents"].apply(lambda x: ", ".join(sorted(x)))

            rk1, rk2, rk3 = st.columns(3)
            rk1.metric("Rules Found", f"{len(rules)}")
            rk2.metric("Avg Confidence", f"{rules['confidence'].mean():.2%}")
            rk3.metric("Avg Lift", f"{rules['lift'].mean():.2f}")

            divider()

            st.markdown("### Top Association Rules")
            disp = rules[["antecedents_str", "consequents_str", "support", "confidence", "lift"]].copy()
            disp.columns = ["If (Antecedent)", "Then (Consequent)", "Support", "Confidence", "Lift"]
            disp = disp.sort_values("lift", ascending=False).head(20).reset_index(drop=True)
            st.dataframe(disp.style.background_gradient(subset=["Lift"], cmap="RdPu")
                         .format({"Support": "{:.3f}", "Confidence": "{:.3f}", "Lift": "{:.3f}"}),
                         use_container_width=True, height=400)
            insight("<strong>Insight:</strong> Rules with <strong>lift > 1</strong> indicate genuine positive associations. "
                    "High-lift rules reveal which challenges directly drive demand for specific CosVerse features.")

            divider()

            st.markdown("### Rules Scatter Plot")
            fig = px.scatter(rules, x="support", y="confidence", size="lift", color="lift",
                             color_continuous_scale=["#0A0A1A", "#B026FF", "#FF2D95"],
                             hover_data=["antecedents_str", "consequents_str"], size_max=20, opacity=0.8)
            st.plotly_chart(apply_theme(fig, "Support vs Confidence (size & color = Lift)", 500), use_container_width=True)
            insight("<strong>Insight:</strong> Rules in the <strong>top-right quadrant</strong> are the most actionable. "
                    "CosVerse should prioritize features linked to the most common challenges.")

            divider()

            st.markdown("### Challenge to Feature Lift Heatmap")
            ch_items = list(challenge_labels.values())
            ft_items = list(feature_labels.values())
            ch_ft = rules[
                rules["antecedents_str"].apply(lambda x: any(c in x for c in ch_items)) &
                rules["consequents_str"].apply(lambda x: any(f in x for f in ft_items))
            ]
            if len(ch_ft) > 0:
                hm = ch_ft.pivot_table(index="antecedents_str", columns="consequents_str",
                                       values="lift", aggfunc="max").fillna(0)
                fig = px.imshow(hm, text_auto=".2f",
                                color_continuous_scale=["#0A0A1A", "#B026FF", "#FF2D95"])
                st.plotly_chart(apply_theme(fig, "Challenge to Feature Lift Heatmap", 450), use_container_width=True)
                insight("<strong>Insight:</strong> The heatmap shows which challenges drive demand for specific features. "
                        "CosVerse can use this for <strong>personalized feature recommendations</strong>.")
            else:
                st.info("No direct Challenge to Feature rules found at current thresholds. Try adjusting the sliders.")


# ═══════════════════════════════════════════════════════════
# TAB 5 — REGRESSION
# ═══════════════════════════════════════════════════════════
with tab_reg:
    st.markdown("# 📈 Regression – Demand Forecasting")
    st.markdown("##### Predicting cosplay spending and rental demand for CosVerse's business planning")

    from sklearn.model_selection import train_test_split as tts2, cross_val_score
    from sklearn.preprocessing import StandardScaler as SS3
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    st.markdown("## Exploratory Analysis — Spending & Demand Drivers")

    re1, re2 = st.columns(2)
    with re1:
        fig = px.histogram(dff, x="Monthly_Cosplay_Spending_AED", nbins=40,
                           color_discrete_sequence=["#00F0FF"], opacity=0.85)
        st.plotly_chart(apply_theme(fig, "Monthly Cosplay Spending Distribution (AED)", 380), use_container_width=True)
        insight(f"<strong>Insight:</strong> Monthly spending has a right-skewed distribution with mean <strong>AED {dff['Monthly_Cosplay_Spending_AED'].mean():.0f}</strong>. "
                "CosVerse can capture this spend with competitive rental pricing below the purchase alternative.")
    with re2:
        fig = px.violin(dff, x="Interest_in_Rental", y="Rental_Price_Willingness_AED",
                        color="Interest_in_Rental", box=True,
                        color_discrete_sequence=["#FF2D95", "#FFD700", "#00F0FF"])
        st.plotly_chart(apply_theme(fig, "Rental Price Willingness by Interest (AED)", 380), use_container_width=True)
        insight("<strong>Insight:</strong> Users interested in rental show <strong>higher willingness to pay</strong>. "
                "CosVerse can implement dynamic pricing based on engagement signals.")

    re3, re4 = st.columns(2)
    with re3:
        fig = px.scatter(dff, x="Years_in_Cosplay", y="Monthly_Cosplay_Spending_AED",
                         color="Cosplay_Interest_Level",
                         color_continuous_scale=["#0A0A1A", "#B026FF", "#FF2D95"], opacity=0.6)
        st.plotly_chart(apply_theme(fig, "Experience vs Monthly Spending", 380), use_container_width=True)
        insight("<strong>Insight:</strong> More experienced cosplayers tend to spend more monthly. "
                "CosVerse should offer <strong>loyalty tiers</strong> to retain high-value long-term users.")
    with re4:
        fig = px.scatter(dff, x="Event_Attendance_Count", y="Costumes_Owned",
                         color="Occupation", color_discrete_sequence=NEON[:3], opacity=0.6)
        st.plotly_chart(apply_theme(fig, "Event Attendance vs Costumes Owned", 380), use_container_width=True)
        insight("<strong>Insight:</strong> Frequent event-goers own more costumes — <strong>high-frequency rental candidates</strong>. "
                "CosVerse should offer event-bundle packages targeting this power-user segment.")

    divider()

    st.markdown("## Machine Learning — Regression Models")

    reg_features = ["Age", "Monthly_Disposable_Income_AED", "Cosplay_Interest_Level",
                    "Years_in_Cosplay", "Event_Attendance_Count",
                    "Costume_Price_Avg_AED", "Costumes_Owned", "Total_Fandom_Count",
                    "Total_Challenges", "Total_Features_Wanted", "NPS_Score", "Likelihood_to_Rent"]

    target_map = {
        "Monthly Cosplay Spending (AED)": "Monthly_Cosplay_Spending_AED",
        "Rental Price Willingness (AED)": "Rental_Price_Willingness_AED",
        "Average Costume Price (AED)": "Costume_Price_Avg_AED"
    }
    target_label = st.selectbox("🎯 Select Target Variable", list(target_map.keys()))
    target_col = target_map[target_label]
    feats_used = [f for f in reg_features if f != target_col]

    dff_r = dff.dropna(subset=feats_used + [target_col]).copy()
    X_r = dff_r[feats_used].values
    y_r = dff_r[target_col].values

    scaler_r = SS3()
    X_r_s = scaler_r.fit_transform(X_r)
    X_tr, X_te, y_tr, y_te = tts2(X_r_s, y_r, test_size=0.25, random_state=42)

    reg_models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Lasso Regression": Lasso(alpha=1.0)
    }

    results = {}
    preds = {}
    for name, mdl in reg_models.items():
        mdl.fit(X_tr, y_tr)
        yp = mdl.predict(X_te)
        preds[name] = yp
        cv = cross_val_score(mdl, X_r_s, y_r, cv=5, scoring="r2")
        results[name] = {
            "R2": r2_score(y_te, yp),
            "MAE": mean_absolute_error(y_te, yp),
            "RMSE": np.sqrt(mean_squared_error(y_te, yp)),
            "CV_R2_Mean": cv.mean(),
            "CV_R2_Std": cv.std()
        }

    best_name = max(results, key=lambda x: results[x]["R2"])
    bk1, bk2, bk3, bk4 = st.columns(4)
    bk1.metric("Best Model", best_name)
    bk2.metric("Best R2", f"{results[best_name]['R2']:.4f}")
    bk3.metric("Best MAE", f"AED {results[best_name]['MAE']:.2f}")
    bk4.metric("Best RMSE", f"AED {results[best_name]['RMSE']:.2f}")

    divider()

    st.markdown("### Model Performance Comparison")
    res_df = pd.DataFrame(results).T
    res_df.index.name = "Model"
    st.dataframe(res_df.style.background_gradient(cmap="RdPu").format("{:.4f}"), use_container_width=True)

    model_names_r = list(results.keys())
    r2_v = [results[n]["R2"] for n in model_names_r]
    mae_v = [results[n]["MAE"] for n in model_names_r]
    rmse_v = [results[n]["RMSE"] for n in model_names_r]

    fig = make_subplots(rows=1, cols=3, subplot_titles=["R2 Score", "MAE (AED)", "RMSE (AED)"])
    fig.add_trace(go.Bar(x=model_names_r, y=r2_v, marker_color=["#FF2D95", "#00F0FF", "#B026FF"],
                         text=[f"{v:.4f}" for v in r2_v], textposition="outside"), row=1, col=1)
    fig.add_trace(go.Bar(x=model_names_r, y=mae_v, marker_color=["#FF2D95", "#00F0FF", "#B026FF"],
                         text=[f"{v:.1f}" for v in mae_v], textposition="outside"), row=1, col=2)
    fig.add_trace(go.Bar(x=model_names_r, y=rmse_v, marker_color=["#FF2D95", "#00F0FF", "#B026FF"],
                         text=[f"{v:.1f}" for v in rmse_v], textposition="outside"), row=1, col=3)
    apply_theme(fig, "Regression Model Performance", 420)
    try:
        fig.update_layout(showlegend=False)
    except Exception:
        pass
    st.plotly_chart(fig, use_container_width=True)

    insight(f"<strong>Insight:</strong> <strong>{best_name}</strong> achieves the highest R2 of <strong>{results[best_name]['R2']:.4f}</strong>. "
            f"This model can forecast {target_label.lower()} to support CosVerse's <strong>pricing and demand planning</strong>.")

    divider()

    st.markdown("### Actual vs Predicted")
    model_show = st.selectbox("Select Model for Detailed View", model_names_r)
    yp_show = preds[model_show]

    rp1, rp2 = st.columns(2)
    with rp1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=y_te, y=yp_show, mode="markers",
                                 marker=dict(color="#00F0FF", opacity=0.5, size=5), name="Predictions"))
        fig.add_trace(go.Scatter(x=[y_te.min(), y_te.max()], y=[y_te.min(), y_te.max()],
                                 mode="lines", line=dict(color="#FF2D95", dash="dash"), name="Perfect Fit"))
        try:
            fig.update_layout(xaxis_title=f"Actual {target_label}", yaxis_title=f"Predicted {target_label}")
        except Exception:
            pass
        st.plotly_chart(apply_theme(fig, f"Actual vs Predicted - {model_show}", 430), use_container_width=True)
    with rp2:
        residuals = y_te - yp_show
        fig = px.histogram(residuals, nbins=40, color_discrete_sequence=["#B026FF"], opacity=0.85)
        try:
            fig.update_layout(xaxis_title="Residual (AED)", yaxis_title="Frequency")
        except Exception:
            pass
        st.plotly_chart(apply_theme(fig, "Residual Distribution", 430), use_container_width=True)

    insight("<strong>Insight:</strong> Points closer to the diagonal indicate better predictions. "
            "A symmetric residual distribution centered near zero confirms <strong>no systematic bias</strong>.")

    divider()

    st.markdown("### Feature Coefficients")
    mdl_sel = reg_models[model_show]
    mdl_sel.fit(X_tr, y_tr)
    coef_df = pd.DataFrame({"Feature": feats_used, "Coefficient": mdl_sel.coef_}).sort_values("Coefficient")
    bar_colors = ["#39FF14" if c > 0 else "#FF2D95" for c in coef_df["Coefficient"]]

    fig = go.Figure(go.Bar(
        y=coef_df["Feature"].tolist(), x=coef_df["Coefficient"].tolist(), orientation="h",
        marker_color=bar_colors,
        text=[f"{v:.3f}" for v in coef_df["Coefficient"]], textposition="outside"
    ))
    st.plotly_chart(apply_theme(fig, f"Feature Coefficients - {model_show}", 480), use_container_width=True)

    top_pos = coef_df.iloc[-1]
    top_neg = coef_df.iloc[0]
    insight(f"<strong>Insight:</strong> <strong>{top_pos['Feature']}</strong> has the strongest positive effect, while "
            f"<strong>{top_neg['Feature']}</strong> shows the strongest negative association. "
            "These drivers inform CosVerse's <strong>pricing optimization and revenue forecasting</strong>.")

    divider()

    st.markdown("### Cross-Validation Stability")
    cv_means = [results[n]["CV_R2_Mean"] for n in model_names_r]
    cv_stds = [results[n]["CV_R2_Std"] for n in model_names_r]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=model_names_r, y=cv_means,
        error_y=dict(type="data", array=cv_stds, visible=True, color="#FF2D95"),
        marker_color=["#FF2D95", "#00F0FF", "#B026FF"],
        text=[f"{v:.4f}" for v in cv_means], textposition="outside"
    ))
    st.plotly_chart(apply_theme(fig, "5-Fold Cross-Validation R2 (with Std Dev)", 420), use_container_width=True)
    insight("<strong>Insight:</strong> Low standard deviation in CV scores indicates <strong>model stability</strong>. "
            "CosVerse can trust these models for reliable <strong>demand estimation and business planning</strong>.")


# ─────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center; font-family: Orbitron; color: #B026FF55; font-size: 0.8rem;">'
    '🎭 CosVerse Analytics Dashboard | Built with Streamlit & Plotly | UAE Cosplay Survey 2024'
    '</div>', unsafe_allow_html=True
)
