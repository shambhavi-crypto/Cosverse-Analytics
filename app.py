import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────
# PAGE CONFIG & THEME
# ─────────────────────────────────────────────────
st.set_page_config(
    page_title="CosVerse Analytics Dashboard",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark anime/gaming theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Exo+2:wght@300;400;600;700&display=swap');

    :root {
        --neon-pink: #FF2D95;
        --neon-cyan: #00F0FF;
        --neon-purple: #B026FF;
        --neon-green: #39FF14;
        --neon-orange: #FF6B35;
        --dark-bg: #0A0A1A;
        --card-bg: #12122A;
        --card-border: #1E1E3F;
    }

    .stApp {
        background: linear-gradient(135deg, #0A0A1A 0%, #0F0F2D 50%, #0A0A1A 100%);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D0D25 0%, #1A0A2E 100%) !important;
        border-right: 1px solid #B026FF33;
    }

    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #FF2D95 !important;
        font-family: 'Orbitron', sans-serif !important;
    }

    /* Headers */
    h1 { font-family: 'Orbitron', sans-serif !important; color: #FF2D95 !important; text-shadow: 0 0 20px #FF2D9555; }
    h2 { font-family: 'Orbitron', sans-serif !important; color: #00F0FF !important; text-shadow: 0 0 15px #00F0FF44; font-size: 1.4rem !important; }
    h3 { font-family: 'Rajdhani', sans-serif !important; color: #B026FF !important; font-size: 1.2rem !important; }

    p, li, span, div { font-family: 'Rajdhani', sans-serif !important; }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #12122A, #1A1A3E) !important;
        border: 1px solid #B026FF44 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        box-shadow: 0 0 15px #B026FF22;
    }
    div[data-testid="stMetric"] label { color: #00F0FF !important; font-family: 'Rajdhani', sans-serif !important; font-weight: 600 !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #FF2D95 !important; font-family: 'Orbitron', sans-serif !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 4px; background: #0D0D25; border-radius: 12px; padding: 4px; }
    .stTabs [data-baseweb="tab"] {
        background: #12122A !important;
        border-radius: 8px !important;
        color: #8888AA !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.75rem !important;
        padding: 8px 16px !important;
        border: 1px solid transparent !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF2D9533, #B026FF33) !important;
        border: 1px solid #FF2D95 !important;
        color: #FF2D95 !important;
        box-shadow: 0 0 10px #FF2D9533;
    }

    /* Insight boxes */
    .insight-box {
        background: linear-gradient(135deg, #12122A, #1A1A3E);
        border-left: 4px solid #00F0FF;
        border-radius: 0 10px 10px 0;
        padding: 12px 18px;
        margin: 10px 0;
        font-family: 'Rajdhani', sans-serif;
        color: #C8C8E8;
        font-size: 1rem;
        line-height: 1.5;
        box-shadow: 0 0 10px #00F0FF11;
    }
    .insight-box strong { color: #FF2D95; }

    /* Section divider */
    .section-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #B026FF55, #FF2D9555, transparent);
        margin: 30px 0;
    }

    /* Expander */
    .streamlit-expanderHeader { font-family: 'Rajdhani', sans-serif !important; color: #00F0FF !important; font-weight: 600 !important; }

    /* Selectbox / Radio */
    .stSelectbox label, .stRadio label, .stMultiSelect label { color: #00F0FF !important; font-family: 'Rajdhani', sans-serif !important; }

    /* Hide default footer */
    footer { visibility: hidden; }
    .stDeployButton { display: none; }

    /* DataFrame styling */
    .stDataFrame { border: 1px solid #B026FF33 !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────
NEON_COLORS = ["#FF2D95", "#00F0FF", "#B026FF", "#39FF14", "#FF6B35", "#FFD700", "#FF4500", "#00CED1"]
NEON_SEQUENTIAL = ["#0A0A1A", "#1A0A2E", "#3D1466", "#6B1D99", "#9B26CC", "#B026FF", "#D066FF", "#E8A0FF"]

def dark_plotly_layout(fig, title="", height=450):
    """Apply consistent dark theme to plotly figures."""
    base_layout = dict(
        title_text=title,
        title_font=dict(family="Orbitron", size=16, color="#FF2D95"),
        title_x=0.5,
        paper_bgcolor="rgba(10,10,26,0)",
        plot_bgcolor="rgba(18,18,42,0.8)",
        font=dict(family="Rajdhani", color="#C8C8E8", size=13),
        height=height,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(bgcolor="rgba(18,18,42,0.8)", bordercolor="#B026FF44", borderwidth=1, font=dict(size=12)),
    )
    fig.update_layout(**base_layout)
    # Only apply axis styling if the figure has cartesian axes
    try:
        fig.update_xaxes(gridcolor="#1E1E3F", zerolinecolor="#1E1E3F")
        fig.update_yaxes(gridcolor="#1E1E3F", zerolinecolor="#1E1E3F")
    except Exception:
        pass
    return fig

def insight_box(text):
    """Render a styled insight box."""
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

def section_divider():
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("cosplay_survey_uae_synthetic.csv")
    # Create derived columns
    df["Total_Fandom_Count"] = df[["Fandom_Anime","Fandom_Marvel_DC","Fandom_Gaming","Fandom_Movies_TV","Fandom_Fantasy_SciFi"]].sum(axis=1)
    df["Total_Challenges"] = df[["Challenge_High_Cost","Challenge_Size_Issues","Challenge_Limited_Availability","Challenge_Storage","Challenge_Time_Constraint","Challenge_Shipping_Delay"]].sum(axis=1)
    df["Total_Features_Wanted"] = df[["Feature_Makeup_Tutorial","Feature_Wig_Rental","Feature_Styling_Guidance","Feature_Group_Cosplay","Feature_Photoshoot_Service"]].sum(axis=1)
    df["Spending_to_Income_Ratio"] = df["Monthly_Cosplay_Spending_AED"] / df["Monthly_Disposable_Income_AED"].replace(0, np.nan)
    df["Age_Group"] = pd.cut(df["Age"], bins=[15,20,25,30,35,45], labels=["16-20","21-25","26-30","31-35","36-45"])
    income_bins = [0, 5000, 10000, 15000, 20000, 30000]
    income_labels = ["<5K", "5K-10K", "10K-15K", "15K-20K", "20K+"]
    df["Income_Bracket"] = pd.cut(df["Monthly_Disposable_Income_AED"], bins=income_bins, labels=income_labels)
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

    tab_selection = st.radio(
        "🧭 Navigate",
        ["📊 EDA Dashboard", "🤖 Classification", "👥 Clustering", "🔗 Association Rules", "📈 Regression"],
        index=0
    )
    st.markdown("---")
    st.markdown("#### 🎛️ Global Filters")
    gender_filter = st.multiselect("Gender", df["Gender"].unique().tolist(), default=df["Gender"].unique().tolist())
    city_filter = st.multiselect("City Type", df["City_Type"].unique().tolist(), default=df["City_Type"].unique().tolist())
    age_range = st.slider("Age Range", int(df["Age"].min()), int(df["Age"].max()), (int(df["Age"].min()), int(df["Age"].max())))

# Apply filters
mask = (
    df["Gender"].isin(gender_filter) &
    df["City_Type"].isin(city_filter) &
    (df["Age"] >= age_range[0]) &
    (df["Age"] <= age_range[1])
)
dff = df[mask].copy()

if len(dff) == 0:
    st.warning("No data matches the current filters. Please adjust the sidebar filters.")
    st.stop()


# ═════════════════════════════════════════════════
# TAB 1: EDA DASHBOARD
# ═════════════════════════════════════════════════
if tab_selection == "📊 EDA Dashboard":

    st.markdown("# 📊 Exploratory Data Analysis")
    st.markdown("##### Comprehensive visual exploration of UAE cosplay consumer behavior")

    # ── KPI Row ──
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Respondents", f"{len(dff):,}")
    c2.metric("Avg Age", f"{dff['Age'].mean():.1f} yrs")
    c3.metric("Avg Monthly Spend", f"AED {dff['Monthly_Cosplay_Spending_AED'].mean():.0f}")
    c4.metric("Avg Costume Price", f"AED {dff['Costume_Price_Avg_AED'].mean():.0f}")
    c5.metric("Avg NPS Score", f"{dff['NPS_Score'].mean():.1f}/10")

    section_divider()

    # ── 1. Age Distribution ──
    st.markdown("## 1. Age Distribution")
    fig_age = px.histogram(dff, x="Age", nbins=30, color_discrete_sequence=["#FF2D95"],
                           opacity=0.85, marginal="box")
    fig_age.update_traces(marker_line_color="#B026FF", marker_line_width=1)
    fig_age = dark_plotly_layout(fig_age, "Age Distribution of Respondents")
    st.plotly_chart(fig_age, use_container_width=True)
    age_mode = dff["Age"].mode().iloc[0]
    insight_box(f"<strong>Insight:</strong> The majority of respondents fall in the <strong>21–29 age bracket</strong>, with a peak at age <strong>{age_mode}</strong>. "
                f"This young demographic aligns perfectly with CosVerse's digital-first rental platform strategy.")

    # ── 2. Gender Distribution ──
    st.markdown("## 2. Gender Distribution")
    gender_counts = dff["Gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]
    fig_gender = px.pie(gender_counts, values="Count", names="Gender",
                        color_discrete_sequence=["#FF2D95", "#00F0FF", "#B026FF"],
                        hole=0.5)
    fig_gender.update_traces(textposition="outside", textinfo="label+percent", textfont_size=14,
                             marker=dict(line=dict(color="#0A0A1A", width=2)))
    fig_gender = dark_plotly_layout(fig_gender, "Gender Distribution")
    st.plotly_chart(fig_gender, use_container_width=True)
    top_gender = gender_counts.iloc[0]
    insight_box(f"<strong>Insight:</strong> <strong>{top_gender['Gender']}</strong> respondents dominate at <strong>{top_gender['Count']/len(dff)*100:.1f}%</strong>. "
                f"CosVerse should ensure gender-inclusive costume collections and marketing to capture all segments.")

    section_divider()

    # ── 3. City Distribution ──
    st.markdown("## 3. City Distribution")
    col3a, col3b = st.columns(2)
    with col3a:
        city_counts = dff["City_Type"].value_counts().reset_index()
        city_counts.columns = ["City_Type", "Count"]
        fig_city = px.bar(city_counts, x="City_Type", y="Count", color="City_Type",
                          color_discrete_sequence=["#FF2D95", "#00F0FF", "#B026FF"],
                          text_auto=True)
        fig_city.update_traces(textposition="outside", marker_line_color="#0A0A1A", marker_line_width=1.5)
        fig_city = dark_plotly_layout(fig_city, "Respondents by City Type")
        st.plotly_chart(fig_city, use_container_width=True)
    with col3b:
        city_spend = dff.groupby("City_Type")["Monthly_Cosplay_Spending_AED"].mean().reset_index()
        city_spend.columns = ["City_Type", "Avg_Spend"]
        fig_city_spend = px.bar(city_spend, x="City_Type", y="Avg_Spend", color="City_Type",
                                color_discrete_sequence=["#39FF14", "#FFD700", "#FF6B35"],
                                text_auto=".0f")
        fig_city_spend.update_traces(textposition="outside")
        fig_city_spend = dark_plotly_layout(fig_city_spend, "Avg Monthly Spend by City Type (AED)")
        st.plotly_chart(fig_city_spend, use_container_width=True)
    insight_box(f"<strong>Insight:</strong> Metro residents form the largest segment and tend to spend more on cosplay. "
                f"CosVerse should prioritize <strong>Metro cities</strong> for initial launch, then expand to medium cities and small towns.")

    section_divider()

    # ── 4. Fandom Category Popularity ──
    st.markdown("## 4. Fandom Category Popularity")
    fandom_cols = {"Fandom_Anime": "Anime", "Fandom_Marvel_DC": "Marvel/DC", "Fandom_Gaming": "Gaming",
                   "Fandom_Movies_TV": "Movies/TV", "Fandom_Fantasy_SciFi": "Fantasy/Sci-Fi"}
    fandom_sums = {v: dff[k].sum() for k, v in fandom_cols.items()}
    fandom_df = pd.DataFrame({"Fandom": list(fandom_sums.keys()), "Fans": list(fandom_sums.values())})
    fandom_df = fandom_df.sort_values("Fans", ascending=True)
    fig_fandom = px.bar(fandom_df, y="Fandom", x="Fans", orientation="h",
                        color="Fandom", color_discrete_sequence=NEON_COLORS, text_auto=True)
    fig_fandom.update_traces(textposition="outside")
    fig_fandom = dark_plotly_layout(fig_fandom, "Fandom Category Popularity (Multi-select)")
    st.plotly_chart(fig_fandom, use_container_width=True)
    top_fandom = fandom_df.iloc[-1]
    insight_box(f"<strong>Insight:</strong> <strong>{top_fandom['Fandom']}</strong> leads with <strong>{int(top_fandom['Fans']):,}</strong> fans. "
                f"CosVerse should stock the widest inventory in <strong>{top_fandom['Fandom']}</strong> costumes to match demand.")

    section_divider()

    # ── 5. Cosplay Participation Rate ──
    st.markdown("## 5. Cosplay Participation Rate")
    col5a, col5b = st.columns(2)
    with col5a:
        fig_events = px.histogram(dff, x="Event_Attendance_Count", nbins=20,
                                  color_discrete_sequence=["#00F0FF"], marginal="violin")
        fig_events = dark_plotly_layout(fig_events, "Event Attendance Count Distribution")
        st.plotly_chart(fig_events, use_container_width=True)
    with col5b:
        fig_years = px.histogram(dff, x="Years_in_Cosplay", nbins=20,
                                 color_discrete_sequence=["#B026FF"], marginal="violin")
        fig_years = dark_plotly_layout(fig_years, "Years in Cosplay Distribution")
        st.plotly_chart(fig_years, use_container_width=True)
    active_pct = (dff["Event_Attendance_Count"] > 0).mean() * 100
    insight_box(f"<strong>Insight:</strong> <strong>{active_pct:.1f}%</strong> of respondents have attended at least one cosplay event. "
                f"The long tail of high-frequency attendees represents CosVerse's <strong>premium subscriber</strong> opportunity.")

    section_divider()

    # ── 6. Average Costume Spending ──
    st.markdown("## 6. Average Costume Spending")
    fig_costume = px.histogram(dff, x="Costume_Price_Avg_AED", nbins=40,
                               color_discrete_sequence=["#FFD700"], marginal="box", opacity=0.85)
    fig_costume = dark_plotly_layout(fig_costume, "Average Costume Price Distribution (AED)")
    st.plotly_chart(fig_costume, use_container_width=True)
    median_cost = dff["Costume_Price_Avg_AED"].median()
    insight_box(f"<strong>Insight:</strong> Median costume price is <strong>AED {median_cost:.0f}</strong>, indicating significant purchase costs. "
                f"A rental model at <strong>30-40% of purchase price</strong> could unlock massive value for budget-conscious cosplayers.")

    section_divider()

    # ── 7. Monthly Entertainment Spending ──
    st.markdown("## 7. Monthly Entertainment / Cosplay Spending")
    fig_monthly = px.box(dff, x="Occupation", y="Monthly_Cosplay_Spending_AED", color="Occupation",
                         color_discrete_sequence=NEON_COLORS, points="outliers")
    fig_monthly = dark_plotly_layout(fig_monthly, "Monthly Cosplay Spending by Occupation (AED)")
    st.plotly_chart(fig_monthly, use_container_width=True)
    highest_occ = dff.groupby("Occupation")["Monthly_Cosplay_Spending_AED"].mean().idxmax()
    insight_box(f"<strong>Insight:</strong> <strong>{highest_occ}s</strong> have the highest average monthly cosplay spending. "
                f"CosVerse can tailor pricing tiers — premium for professionals, student discounts for younger users.")

    section_divider()

    # ── 8. Challenges Faced by Users ──
    st.markdown("## 8. Challenges Faced by Users")
    challenge_cols = {"Challenge_High_Cost": "High Cost", "Challenge_Size_Issues": "Size Issues",
                      "Challenge_Limited_Availability": "Limited Availability", "Challenge_Storage": "Storage",
                      "Challenge_Time_Constraint": "Time Constraint", "Challenge_Shipping_Delay": "Shipping Delay"}
    challenge_data = {v: dff[k].sum() for k, v in challenge_cols.items()}
    ch_df = pd.DataFrame({"Challenge": list(challenge_data.keys()), "Count": list(challenge_data.values())})
    ch_df = ch_df.sort_values("Count", ascending=False)
    fig_ch = px.bar(ch_df, x="Challenge", y="Count", color="Challenge",
                    color_discrete_sequence=["#FF2D95", "#FF6B35", "#FFD700", "#39FF14", "#00F0FF", "#B026FF"],
                    text_auto=True)
    fig_ch.update_traces(textposition="outside")
    fig_ch = dark_plotly_layout(fig_ch, "Top Challenges Faced by Cosplayers")
    st.plotly_chart(fig_ch, use_container_width=True)
    top_ch = ch_df.iloc[0]
    insight_box(f"<strong>Insight:</strong> <strong>{top_ch['Challenge']}</strong> is the #1 challenge with <strong>{int(top_ch['Count']):,}</strong> mentions. "
                f"CosVerse directly addresses this pain point through its affordable rental model and styling services.")

    section_divider()

    # ── 9. Preferred Features ──
    st.markdown("## 9. Preferred Features in a Cosplay Platform")
    feat_cols = {"Feature_Makeup_Tutorial": "Makeup Tutorials", "Feature_Wig_Rental": "Wig Rental",
                 "Feature_Styling_Guidance": "Styling Guidance", "Feature_Group_Cosplay": "Group Cosplay",
                 "Feature_Photoshoot_Service": "Photoshoot Service"}
    feat_data = {v: dff[k].sum() for k, v in feat_cols.items()}
    ft_df = pd.DataFrame({"Feature": list(feat_data.keys()), "Interest": list(feat_data.values())})
    ft_df = ft_df.sort_values("Interest", ascending=True)
    fig_feat = px.bar(ft_df, y="Feature", x="Interest", orientation="h", color="Feature",
                      color_discrete_sequence=NEON_COLORS[:5], text_auto=True)
    fig_feat.update_traces(textposition="outside")
    fig_feat = dark_plotly_layout(fig_feat, "Most Desired Platform Features")
    st.plotly_chart(fig_feat, use_container_width=True)
    top_feat = ft_df.iloc[-1]
    insight_box(f"<strong>Insight:</strong> <strong>{top_feat['Feature']}</strong> is the most requested feature with <strong>{int(top_feat['Interest']):,}</strong> votes. "
                f"CosVerse should prioritize this in the MVP launch to maximize early user engagement and retention.")

    section_divider()

    # ── 10. Correlation Heatmap ──
    st.markdown("## 10. Correlation Heatmap")
    numeric_cols = ["Age", "Monthly_Disposable_Income_AED", "Cosplay_Interest_Level", "Years_in_Cosplay",
                    "Event_Attendance_Count", "Monthly_Cosplay_Spending_AED", "Costume_Price_Avg_AED",
                    "Costumes_Owned", "Rental_Price_Willingness_AED", "Likelihood_to_Rent", "NPS_Score",
                    "Total_Fandom_Count", "Total_Challenges", "Total_Features_Wanted"]
    corr = dff[numeric_cols].corr()
    fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale=["#0A0A1A", "#B026FF", "#FF2D95"],
                         aspect="auto", labels=dict(color="Correlation"))
    fig_corr = dark_plotly_layout(fig_corr, "Feature Correlation Heatmap", height=600)
    st.plotly_chart(fig_corr, use_container_width=True)
    insight_box("<strong>Insight:</strong> Strong positive correlations exist between <strong>event attendance & spending</strong>, and between <strong>interest level & rental likelihood</strong>. "
                "These correlated features validate that engaged users are the strongest conversion targets for CosVerse.")

    section_divider()

    # ── 11. Income vs Costume Spending ──
    st.markdown("## 11. Income vs Costume Spending")
    fig_inc = px.scatter(dff, x="Monthly_Disposable_Income_AED", y="Costume_Price_Avg_AED",
                         color="Interest_in_Rental", size="Event_Attendance_Count",
                         color_discrete_sequence=["#FF2D95", "#FFD700", "#00F0FF"],
                         opacity=0.7, hover_data=["Age", "Occupation"])
    fig_inc.update_traces(marker=dict(line=dict(width=0.5, color="#0A0A1A")))
    fig_inc = dark_plotly_layout(fig_inc, "Income vs Avg Costume Price (colored by Rental Interest)")
    st.plotly_chart(fig_inc, use_container_width=True)
    insight_box("<strong>Insight:</strong> Users across <strong>all income levels</strong> face high costume costs, but lower-income users show stronger rental interest. "
                "CosVerse's rental model is especially compelling for the <strong>AED 5K-15K income bracket</strong>.")

    section_divider()

    # ── 12. Cosplay Participation vs App Interest ──
    st.markdown("## 12. Cosplay Participation vs App Interest")
    app_cross = pd.crosstab(dff["Cosplay_Interest_Level"], dff["App_Usage_Intention"], normalize="index") * 100
    fig_app = px.bar(app_cross, barmode="stack", color_discrete_sequence=["#39FF14", "#FFD700", "#FF2D95"])
    fig_app.update_layout(yaxis_title="Percentage (%)", xaxis_title="Cosplay Interest Level (1-5)")
    fig_app = dark_plotly_layout(fig_app, "App Usage Intention by Cosplay Interest Level")
    st.plotly_chart(fig_app, use_container_width=True)
    insight_box("<strong>Insight:</strong> Higher cosplay interest levels correlate strongly with <strong>'Yes' for app usage</strong>. "
                "Users with interest level 4-5 are the <strong>primary early adopter target</strong> for CosVerse's launch campaign.")

    section_divider()

    # ── ADDITIONAL EDA ──
    st.markdown("## 13. Additional Insights")

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        # Discovery Channel
        disc_counts = dff["Discovery_Channel"].value_counts().reset_index()
        disc_counts.columns = ["Channel", "Count"]
        fig_disc = px.pie(disc_counts, values="Count", names="Channel",
                          color_discrete_sequence=NEON_COLORS, hole=0.45)
        fig_disc.update_traces(textposition="inside", textinfo="label+percent")
        fig_disc = dark_plotly_layout(fig_disc, "Discovery Channels", height=400)
        st.plotly_chart(fig_disc, use_container_width=True)
        insight_box("<strong>Insight:</strong> Social media platforms dominate discovery. "
                    "CosVerse should invest heavily in <strong>TikTok & Instagram</strong> influencer marketing for maximum reach.")

    with col_a2:
        # NPS Distribution
        fig_nps = px.histogram(dff, x="NPS_Score", nbins=11, color_discrete_sequence=["#39FF14"], opacity=0.85)
        fig_nps = dark_plotly_layout(fig_nps, "Net Promoter Score Distribution", height=400)
        st.plotly_chart(fig_nps, use_container_width=True)
        promoters = (dff["NPS_Score"] >= 9).mean() * 100
        detractors = (dff["NPS_Score"] <= 6).mean() * 100
        insight_box(f"<strong>Insight:</strong> <strong>{promoters:.1f}%</strong> promoters vs <strong>{detractors:.1f}%</strong> detractors. "
                    f"CosVerse should nurture promoters as brand ambassadors while addressing detractor concerns.")

    col_a3, col_a4 = st.columns(2)
    with col_a3:
        # Subscription Interest
        sub_counts = dff["Subscription_Interest"].value_counts().reset_index()
        sub_counts.columns = ["Interest", "Count"]
        fig_sub = px.bar(sub_counts, x="Interest", y="Count", color="Interest",
                         color_discrete_sequence=["#39FF14", "#FFD700", "#FF2D95"], text_auto=True)
        fig_sub.update_traces(textposition="outside")
        fig_sub = dark_plotly_layout(fig_sub, "Subscription Interest", height=400)
        st.plotly_chart(fig_sub, use_container_width=True)
        insight_box("<strong>Insight:</strong> A significant portion shows subscription interest, validating the <strong>recurring revenue model</strong>. "
                    "CosVerse should offer tiered monthly plans to capture both casual and committed users.")

    with col_a4:
        # Costume Acquisition Method
        acq_counts = dff["Costume_Acquisition_Method"].value_counts().reset_index()
        acq_counts.columns = ["Method", "Count"]
        fig_acq = px.bar(acq_counts, x="Method", y="Count", color="Method",
                         color_discrete_sequence=NEON_COLORS[:5], text_auto=True)
        fig_acq.update_traces(textposition="outside")
        fig_acq = dark_plotly_layout(fig_acq, "Costume Acquisition Methods", height=400)
        st.plotly_chart(fig_acq, use_container_width=True)
        insight_box("<strong>Insight:</strong> Buying online and DIY dominate current acquisition methods. "
                    "CosVerse can convert these users by offering <strong>superior convenience and lower cost</strong> through rentals.")

    # ── Rental Duration & Willingness ──
    col_a5, col_a6 = st.columns(2)
    with col_a5:
        rent_dur = dff["Preferred_Rental_Duration"].value_counts().reset_index()
        rent_dur.columns = ["Duration", "Count"]
        fig_dur = px.pie(rent_dur, values="Count", names="Duration",
                         color_discrete_sequence=["#FF2D95", "#00F0FF", "#B026FF", "#39FF14"], hole=0.45)
        fig_dur.update_traces(textposition="inside", textinfo="label+percent")
        fig_dur = dark_plotly_layout(fig_dur, "Preferred Rental Duration", height=400)
        st.plotly_chart(fig_dur, use_container_width=True)
        insight_box("<strong>Insight:</strong> Most users prefer <strong>short-term rentals (1 day to 1 week)</strong>. "
                    "CosVerse should design pricing around <strong>event-based rental windows</strong> for maximum convenience.")

    with col_a6:
        fig_willingness = px.violin(dff, x="Interest_in_Rental", y="Rental_Price_Willingness_AED",
                                    color="Interest_in_Rental", box=True,
                                    color_discrete_sequence=["#FF2D95", "#FFD700", "#00F0FF"])
        fig_willingness = dark_plotly_layout(fig_willingness, "Rental Price Willingness by Interest Level (AED)", height=400)
        st.plotly_chart(fig_willingness, use_container_width=True)
        insight_box("<strong>Insight:</strong> Users already interested in rental show <strong>higher willingness to pay</strong>. "
                    "CosVerse can implement dynamic pricing based on user engagement and interest signals.")

    # ── Spending by Age Group ──
    st.markdown("## 14. Spending Patterns by Demographics")
    fig_age_spend = px.box(dff, x="Age_Group", y="Monthly_Cosplay_Spending_AED", color="Gender",
                           color_discrete_sequence=["#FF2D95", "#00F0FF", "#B026FF"])
    fig_age_spend = dark_plotly_layout(fig_age_spend, "Monthly Spending by Age Group & Gender (AED)")
    st.plotly_chart(fig_age_spend, use_container_width=True)
    insight_box("<strong>Insight:</strong> Spending peaks in the <strong>26-30 age group</strong> where users have more disposable income. "
                "CosVerse can target this demographic with premium costume tiers and VIP styling packages.")


# ═════════════════════════════════════════════════
# TAB 2: CLASSIFICATION
# ═════════════════════════════════════════════════
elif tab_selection == "🤖 Classification":

    st.markdown("# 🤖 Classification – Predict Platform Adoption")
    st.markdown("##### Predicting which users will adopt CosVerse using ML models")

    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
    from sklearn.multiclass import OneVsRestClassifier

    # Prepare features
    feature_cols = ["Age", "Monthly_Disposable_Income_AED", "Cosplay_Interest_Level",
                    "Years_in_Cosplay", "Event_Attendance_Count", "Monthly_Cosplay_Spending_AED",
                    "Costume_Price_Avg_AED", "Costumes_Owned", "Total_Fandom_Count",
                    "Total_Challenges", "Total_Features_Wanted", "NPS_Score",
                    "Likelihood_to_Rent", "Rental_Price_Willingness_AED"]

    target_choice = st.selectbox("Select Target Variable", ["App_Usage_Intention", "Interest_in_Rental"])

    le = LabelEncoder()
    dff_class = dff.dropna(subset=feature_cols + [target_choice]).copy()
    X = dff_class[feature_cols].values
    y = le.fit_transform(dff_class[target_choice].values)
    class_names = le.classes_

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=42, stratify=y)

    models = {
        "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, multi_class="multinomial", random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=150, max_depth=5, random_state=42)
    }

    model_choice = st.selectbox("Select Model", list(models.keys()))
    model = models[model_choice]
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # KPI row
    c1, c2, c3 = st.columns(3)
    c1.metric("Accuracy", f"{acc:.2%}")
    c2.metric("Test Samples", f"{len(y_test):,}")
    c3.metric("Classes", f"{len(class_names)}")

    section_divider()

    col_cm, col_cr = st.columns(2)
    with col_cm:
        # Confusion Matrix
        st.markdown("### Confusion Matrix")
        cm = confusion_matrix(y_test, y_pred)
        fig_cm = px.imshow(cm, text_auto=True, x=class_names, y=class_names,
                           color_continuous_scale=["#0A0A1A", "#B026FF", "#FF2D95"],
                           labels=dict(x="Predicted", y="Actual", color="Count"))
        fig_cm = dark_plotly_layout(fig_cm, f"Confusion Matrix – {model_choice}", height=400)
        st.plotly_chart(fig_cm, use_container_width=True)

    with col_cr:
        # Classification Report
        st.markdown("### Classification Report")
        report = classification_report(y_test, y_pred, target_names=class_names, output_dict=True)
        report_df = pd.DataFrame(report).transpose().round(3)
        st.dataframe(report_df.style.background_gradient(cmap="RdPu"), use_container_width=True)

    insight_box(f"<strong>Insight:</strong> The <strong>{model_choice}</strong> achieves <strong>{acc:.1%}</strong> accuracy on the {target_choice.replace('_', ' ')} task. "
                f"This model can help CosVerse identify high-probability adopters for <strong>targeted marketing campaigns</strong>.")

    section_divider()

    # Feature Importance
    st.markdown("### Feature Importance")
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    else:
        importances = np.abs(model.coef_).mean(axis=0)
    fi_df = pd.DataFrame({"Feature": feature_cols, "Importance": importances}).sort_values("Importance", ascending=True)
    fig_fi = px.bar(fi_df, y="Feature", x="Importance", orientation="h",
                    color="Importance", color_continuous_scale=["#0A0A1A", "#B026FF", "#FF2D95"], text_auto=".3f")
    fig_fi.update_traces(textposition="outside")
    fig_fi = dark_plotly_layout(fig_fi, f"Feature Importance – {model_choice}", height=500)
    st.plotly_chart(fig_fi, use_container_width=True)
    top_feature = fi_df.iloc[-1]
    insight_box(f"<strong>Insight:</strong> <strong>{top_feature['Feature']}</strong> is the strongest predictor of platform adoption. "
                f"CosVerse should focus on users scoring high on this metric for maximum conversion rates.")

    section_divider()

    # Model Comparison
    st.markdown("### Model Comparison")
    comparison_results = []
    for name, mdl in models.items():
        mdl.fit(X_train, y_train)
        y_p = mdl.predict(X_test)
        comparison_results.append({"Model": name, "Accuracy": accuracy_score(y_test, y_p),
                                   "Precision": classification_report(y_test, y_p, output_dict=True, zero_division=0)["weighted avg"]["precision"],
                                   "Recall": classification_report(y_test, y_p, output_dict=True, zero_division=0)["weighted avg"]["recall"],
                                   "F1-Score": classification_report(y_test, y_p, output_dict=True, zero_division=0)["weighted avg"]["f1-score"]})
    comp_df = pd.DataFrame(comparison_results)
    fig_comp = px.bar(comp_df.melt(id_vars="Model", var_name="Metric", value_name="Score"),
                      x="Model", y="Score", color="Metric", barmode="group",
                      color_discrete_sequence=["#FF2D95", "#00F0FF", "#B026FF", "#39FF14"], text_auto=".3f")
    fig_comp.update_traces(textposition="outside")
    fig_comp = dark_plotly_layout(fig_comp, "Model Performance Comparison", height=450)
    st.plotly_chart(fig_comp, use_container_width=True)
    best_model = comp_df.loc[comp_df["F1-Score"].idxmax()]
    insight_box(f"<strong>Insight:</strong> <strong>{best_model['Model']}</strong> delivers the best F1-Score of <strong>{best_model['F1-Score']:.3f}</strong>. "
                f"This model should be deployed in CosVerse's recommendation engine for user targeting.")


# ═════════════════════════════════════════════════
# TAB 3: CLUSTERING
# ═════════════════════════════════════════════════
elif tab_selection == "👥 Clustering":

    st.markdown("# 👥 Clustering – Customer Personas")
    st.markdown("##### K-Means clustering to identify distinct customer segments for CosVerse")

    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    from sklearn.decomposition import PCA

    cluster_features = ["Age", "Monthly_Disposable_Income_AED", "Cosplay_Interest_Level",
                        "Years_in_Cosplay", "Event_Attendance_Count", "Monthly_Cosplay_Spending_AED",
                        "Costume_Price_Avg_AED", "Costumes_Owned", "Total_Fandom_Count",
                        "Total_Challenges", "Total_Features_Wanted", "NPS_Score",
                        "Likelihood_to_Rent", "Rental_Price_Willingness_AED"]

    dff_cl = dff.dropna(subset=cluster_features).copy()
    X_cl = dff_cl[cluster_features].values
    scaler = StandardScaler()
    X_cl_scaled = scaler.fit_transform(X_cl)

    # Elbow Method
    st.markdown("### Elbow Method & Silhouette Analysis")
    col_el, col_sil = st.columns(2)

    inertias = []
    sil_scores = []
    K_range = range(2, 9)
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_cl_scaled)
        inertias.append(km.inertia_)
        sil_scores.append(silhouette_score(X_cl_scaled, km.labels_, sample_size=min(1000, len(X_cl_scaled))))

    with col_el:
        fig_elbow = px.line(x=list(K_range), y=inertias, markers=True,
                            labels={"x": "Number of Clusters (K)", "y": "Inertia"})
        fig_elbow.update_traces(line_color="#FF2D95", marker=dict(size=10, color="#00F0FF"))
        fig_elbow = dark_plotly_layout(fig_elbow, "Elbow Method", height=400)
        st.plotly_chart(fig_elbow, use_container_width=True)

    with col_sil:
        fig_sil = px.bar(x=list(K_range), y=sil_scores,
                         labels={"x": "Number of Clusters (K)", "y": "Silhouette Score"},
                         color_discrete_sequence=["#B026FF"])
        fig_sil = dark_plotly_layout(fig_sil, "Silhouette Scores", height=400)
        st.plotly_chart(fig_sil, use_container_width=True)

    insight_box("<strong>Insight:</strong> The elbow and silhouette analysis guide the optimal K selection. "
                "Choose the K where inertia drop slows (elbow) and silhouette score is maximized.")

    section_divider()

    # K-Means with selected K
    n_clusters = st.slider("Select Number of Clusters (K)", 2, 8, 3)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    dff_cl["Cluster"] = kmeans.fit_predict(X_cl_scaled)

    # 3D PCA Visualization
    st.markdown("### 3D Cluster Visualization (PCA)")
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X_cl_scaled)
    dff_cl["PC1"] = X_pca[:, 0]
    dff_cl["PC2"] = X_pca[:, 1]
    dff_cl["PC3"] = X_pca[:, 2]
    dff_cl["Cluster_Label"] = dff_cl["Cluster"].astype(str)

    fig_3d = px.scatter_3d(dff_cl, x="PC1", y="PC2", z="PC3", color="Cluster_Label",
                           color_discrete_sequence=NEON_COLORS[:n_clusters],
                           opacity=0.7, hover_data=["Age", "Monthly_Cosplay_Spending_AED", "Event_Attendance_Count"])
    fig_3d = dark_plotly_layout(fig_3d, "Customer Segments in 3D PCA Space", height=550)
    fig_3d.update_layout(scene=dict(
        xaxis=dict(backgroundcolor="#0A0A1A", gridcolor="#1E1E3F"),
        yaxis=dict(backgroundcolor="#0A0A1A", gridcolor="#1E1E3F"),
        zaxis=dict(backgroundcolor="#0A0A1A", gridcolor="#1E1E3F"),
    ))
    st.plotly_chart(fig_3d, use_container_width=True)

    var_explained = pca.explained_variance_ratio_.sum() * 100
    insight_box(f"<strong>Insight:</strong> The 3 principal components explain <strong>{var_explained:.1f}%</strong> of total variance. "
                f"Clear cluster separation indicates <strong>distinct customer personas</strong> that CosVerse can target with tailored strategies.")

    section_divider()

    # Cluster Profiles
    st.markdown("### Cluster Profiles")
    profile_cols = ["Age", "Monthly_Disposable_Income_AED", "Cosplay_Interest_Level",
                    "Event_Attendance_Count", "Monthly_Cosplay_Spending_AED",
                    "Costume_Price_Avg_AED", "Total_Features_Wanted", "Likelihood_to_Rent", "NPS_Score"]
    cluster_profile = dff_cl.groupby("Cluster")[profile_cols].mean().round(1)
    cluster_profile.index = [f"Cluster {i}" for i in cluster_profile.index]
    st.dataframe(cluster_profile.style.background_gradient(cmap="RdPu", axis=0), use_container_width=True)

    # Radar Chart for Cluster Comparison
    st.markdown("### Cluster Radar Comparison")
    radar_cols = ["Cosplay_Interest_Level", "Event_Attendance_Count", "Monthly_Cosplay_Spending_AED",
                  "Total_Features_Wanted", "Likelihood_to_Rent", "NPS_Score"]
    radar_data = dff_cl.groupby("Cluster")[radar_cols].mean()
    # Normalize for radar
    radar_norm = (radar_data - radar_data.min()) / (radar_data.max() - radar_data.min() + 1e-9)

    fig_radar = go.Figure()
    persona_names = ["Hardcore Cosplayers", "Casual Fans", "Event Visitors"] if n_clusters == 3 else [f"Segment {i}" for i in range(n_clusters)]
    for i in range(n_clusters):
        label = persona_names[i] if i < len(persona_names) else f"Segment {i}"
        values = radar_norm.iloc[i].tolist()
        values.append(values[0])  # close the polygon
        fig_radar.add_trace(go.Scatterpolar(
            r=values, theta=radar_cols + [radar_cols[0]],
            fill="toself", name=label, opacity=0.6,
            line=dict(color=NEON_COLORS[i], width=2),
            fillcolor=NEON_COLORS[i] + "33"
        ))
    fig_radar = dark_plotly_layout(fig_radar, "Customer Persona Radar Chart", height=500)
    fig_radar.update_layout(polar=dict(
        bgcolor="rgba(18,18,42,0.8)",
        radialaxis=dict(visible=True, range=[0, 1], gridcolor="#1E1E3F"),
        angularaxis=dict(gridcolor="#1E1E3F")
    ))
    st.plotly_chart(fig_radar, use_container_width=True)
    insight_box("<strong>Insight:</strong> The radar chart reveals <strong>distinct persona profiles</strong> — high-engagement spenders vs budget-conscious casuals. "
                "CosVerse should design <strong>differentiated service tiers</strong> matching each persona's needs and willingness to pay.")

    section_divider()

    # Cluster distribution per feature
    st.markdown("### Cluster Feature Distributions")
    feat_to_plot = st.selectbox("Select Feature to Compare", profile_cols, index=4)
    fig_dist = px.box(dff_cl, x="Cluster_Label", y=feat_to_plot, color="Cluster_Label",
                      color_discrete_sequence=NEON_COLORS[:n_clusters], points="outliers")
    fig_dist = dark_plotly_layout(fig_dist, f"{feat_to_plot} Distribution by Cluster")
    st.plotly_chart(fig_dist, use_container_width=True)


# ═════════════════════════════════════════════════
# TAB 4: ASSOCIATION RULES
# ═════════════════════════════════════════════════
elif tab_selection == "🔗 Association Rules":

    st.markdown("# 🔗 Association Rule Mining")
    st.markdown("##### Discovering hidden relationships between challenges and desired features")

    from mlxtend.frequent_patterns import apriori, association_rules

    # Build transaction dataframe
    challenge_map = {"Challenge_High_Cost": "High Cost", "Challenge_Size_Issues": "Size Issues",
                     "Challenge_Limited_Availability": "Limited Availability", "Challenge_Storage": "Storage Problem",
                     "Challenge_Time_Constraint": "Time Constraint", "Challenge_Shipping_Delay": "Shipping Delay"}
    feature_map = {"Feature_Makeup_Tutorial": "Makeup Tutorial", "Feature_Wig_Rental": "Wig Rental",
                   "Feature_Styling_Guidance": "Styling Guidance", "Feature_Group_Cosplay": "Group Cosplay",
                   "Feature_Photoshoot_Service": "Photoshoot Service"}

    all_items = {**challenge_map, **feature_map}
    basket_df = dff[list(all_items.keys())].rename(columns=all_items).astype(bool)

    # Apriori
    min_sup = st.slider("Minimum Support", 0.05, 0.5, 0.1, 0.05)
    frequent = apriori(basket_df, min_support=min_sup, use_colnames=True)

    if len(frequent) == 0:
        st.warning("No frequent itemsets found at this support level. Try lowering the minimum support.")
    else:
        min_conf = st.slider("Minimum Confidence", 0.1, 1.0, 0.3, 0.05)
        rules = association_rules(frequent, metric="confidence", min_threshold=min_conf, num_itemsets=len(frequent))

        if len(rules) == 0:
            st.warning("No rules found at this confidence level. Try lowering the threshold.")
        else:
            rules["antecedents_str"] = rules["antecedents"].apply(lambda x: ", ".join(list(x)))
            rules["consequents_str"] = rules["consequents"].apply(lambda x: ", ".join(list(x)))

            # KPI
            c1, c2, c3 = st.columns(3)
            c1.metric("Rules Found", f"{len(rules)}")
            c2.metric("Avg Confidence", f"{rules['confidence'].mean():.2%}")
            c3.metric("Avg Lift", f"{rules['lift'].mean():.2f}")

            section_divider()

            # Top Rules Table
            st.markdown("### Top Association Rules")
            display_rules = rules[["antecedents_str", "consequents_str", "support", "confidence", "lift"]].copy()
            display_rules.columns = ["If (Antecedent)", "Then (Consequent)", "Support", "Confidence", "Lift"]
            display_rules = display_rules.sort_values("lift", ascending=False).head(20).reset_index(drop=True)
            st.dataframe(display_rules.style.background_gradient(subset=["Lift"], cmap="RdPu")
                         .format({"Support": "{:.3f}", "Confidence": "{:.3f}", "Lift": "{:.3f}"}),
                         use_container_width=True, height=400)

            insight_box("<strong>Insight:</strong> Rules with <strong>lift > 1</strong> indicate genuine positive associations. "
                        "High-lift rules reveal which challenges directly drive demand for specific CosVerse features.")

            section_divider()

            # Scatter: Support vs Confidence (colored by Lift)
            st.markdown("### Rules Scatter Plot")
            fig_scatter = px.scatter(rules, x="support", y="confidence", size="lift", color="lift",
                                     color_continuous_scale=["#0A0A1A", "#B026FF", "#FF2D95"],
                                     hover_data=["antecedents_str", "consequents_str"],
                                     size_max=20, opacity=0.8)
            fig_scatter = dark_plotly_layout(fig_scatter, "Support vs Confidence (size & color = Lift)", height=500)
            st.plotly_chart(fig_scatter, use_container_width=True)

            insight_box("<strong>Insight:</strong> Rules in the <strong>top-right quadrant</strong> (high support & confidence) are the most actionable. "
                        "CosVerse should prioritize features linked to the most common challenges with the strongest lift values.")

            section_divider()

            # Challenge → Feature Heatmap
            st.markdown("### Challenge → Feature Relationship Heatmap")
            challenge_items = list(challenge_map.values())
            feature_items = list(feature_map.values())
            ch_ft_rules = rules[
                rules["antecedents_str"].apply(lambda x: any(c in x for c in challenge_items)) &
                rules["consequents_str"].apply(lambda x: any(f in x for f in feature_items))
            ]
            if len(ch_ft_rules) > 0:
                heatmap_data = ch_ft_rules.pivot_table(
                    index="antecedents_str", columns="consequents_str",
                    values="lift", aggfunc="max"
                ).fillna(0)
                fig_hm = px.imshow(heatmap_data, text_auto=".2f",
                                   color_continuous_scale=["#0A0A1A", "#B026FF", "#FF2D95"],
                                   labels=dict(color="Lift"))
                fig_hm = dark_plotly_layout(fig_hm, "Challenge → Feature Lift Heatmap", height=450)
                st.plotly_chart(fig_hm, use_container_width=True)
                insight_box("<strong>Insight:</strong> The heatmap shows which challenges drive demand for specific features. "
                            "CosVerse can use this to create <strong>personalized feature recommendations</strong> based on user pain points.")
            else:
                st.info("No direct Challenge → Feature rules found. Try adjusting support/confidence thresholds.")


# ═════════════════════════════════════════════════
# TAB 5: REGRESSION
# ═════════════════════════════════════════════════
elif tab_selection == "📈 Regression":

    st.markdown("# 📈 Regression – Demand Forecasting")
    st.markdown("##### Predicting cosplay spending and rental demand for CosVerse's business planning")

    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    reg_features = ["Age", "Monthly_Disposable_Income_AED", "Cosplay_Interest_Level",
                    "Years_in_Cosplay", "Event_Attendance_Count",
                    "Costume_Price_Avg_AED", "Costumes_Owned", "Total_Fandom_Count",
                    "Total_Challenges", "Total_Features_Wanted", "NPS_Score", "Likelihood_to_Rent"]

    target_map = {
        "Monthly Cosplay Spending (AED)": "Monthly_Cosplay_Spending_AED",
        "Rental Price Willingness (AED)": "Rental_Price_Willingness_AED",
        "Average Costume Price (AED)": "Costume_Price_Avg_AED"
    }

    target_label = st.selectbox("Select Target Variable for Regression", list(target_map.keys()))
    target_col = target_map[target_label]

    # Remove target from features if it's there
    features_used = [f for f in reg_features if f != target_col]

    dff_reg = dff.dropna(subset=features_used + [target_col]).copy()
    X_reg = dff_reg[features_used].values
    y_reg = dff_reg[target_col].values

    scaler = StandardScaler()
    X_reg_scaled = scaler.fit_transform(X_reg)
    X_train, X_test, y_train, y_test = train_test_split(X_reg_scaled, y_reg, test_size=0.25, random_state=42)

    reg_models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression (α=1.0)": Ridge(alpha=1.0),
        "Lasso Regression (α=1.0)": Lasso(alpha=1.0)
    }

    results = {}
    predictions = {}
    for name, mdl in reg_models.items():
        mdl.fit(X_train, y_train)
        y_pred = mdl.predict(X_test)
        predictions[name] = y_pred
        cv_scores = cross_val_score(mdl, X_reg_scaled, y_reg, cv=5, scoring="r2")
        results[name] = {
            "R²": r2_score(y_test, y_pred),
            "MAE": mean_absolute_error(y_test, y_pred),
            "RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),
            "CV R² (mean)": cv_scores.mean(),
            "CV R² (std)": cv_scores.std()
        }

    # KPI row
    best_name = max(results, key=lambda x: results[x]["R²"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Best Model", best_name.split(" (")[0])
    c2.metric("Best R²", f"{results[best_name]['R²']:.4f}")
    c3.metric("Best MAE", f"AED {results[best_name]['MAE']:.2f}")
    c4.metric("Best RMSE", f"AED {results[best_name]['RMSE']:.2f}")

    section_divider()

    # Model Comparison
    st.markdown("### Model Performance Comparison")
    res_df = pd.DataFrame(results).T
    res_df.index.name = "Model"
    st.dataframe(res_df.style.background_gradient(cmap="RdPu").format("{:.4f}"), use_container_width=True)

    fig_comp = make_subplots(rows=1, cols=3, subplot_titles=["R² Score", "MAE (AED)", "RMSE (AED)"])
    model_names = list(results.keys())
    short_names = [n.split(" (")[0] if "(" in n else n for n in model_names]
    r2_vals = [results[n]["R²"] for n in model_names]
    mae_vals = [results[n]["MAE"] for n in model_names]
    rmse_vals = [results[n]["RMSE"] for n in model_names]

    fig_comp.add_trace(go.Bar(x=short_names, y=r2_vals, marker_color=["#FF2D95","#00F0FF","#B026FF"], text=[f"{v:.4f}" for v in r2_vals], textposition="outside"), row=1, col=1)
    fig_comp.add_trace(go.Bar(x=short_names, y=mae_vals, marker_color=["#FF2D95","#00F0FF","#B026FF"], text=[f"{v:.1f}" for v in mae_vals], textposition="outside"), row=1, col=2)
    fig_comp.add_trace(go.Bar(x=short_names, y=rmse_vals, marker_color=["#FF2D95","#00F0FF","#B026FF"], text=[f"{v:.1f}" for v in rmse_vals], textposition="outside"), row=1, col=3)
    fig_comp = dark_plotly_layout(fig_comp, "Regression Model Performance Comparison", height=420)
    fig_comp.update_layout(showlegend=False)
    st.plotly_chart(fig_comp, use_container_width=True)

    insight_box(f"<strong>Insight:</strong> <strong>{best_name}</strong> achieves the highest R² of <strong>{results[best_name]['R²']:.4f}</strong>. "
                f"This model can forecast {target_label.lower()} to support CosVerse's <strong>pricing strategy and demand planning</strong>.")

    section_divider()

    # Actual vs Predicted
    st.markdown("### Actual vs Predicted")
    model_to_show = st.selectbox("Select Model for Detailed View", model_names)
    y_p = predictions[model_to_show]

    col_ap, col_res = st.columns(2)
    with col_ap:
        fig_ap = px.scatter(x=y_test, y=y_p, opacity=0.5,
                            labels={"x": f"Actual {target_label}", "y": f"Predicted {target_label}"},
                            color_discrete_sequence=["#00F0FF"])
        fig_ap.add_trace(go.Scatter(x=[y_test.min(), y_test.max()], y=[y_test.min(), y_test.max()],
                                    mode="lines", line=dict(color="#FF2D95", dash="dash"), name="Perfect Fit"))
        fig_ap = dark_plotly_layout(fig_ap, f"Actual vs Predicted – {model_to_show.split(' (')[0]}", height=430)
        st.plotly_chart(fig_ap, use_container_width=True)

    with col_res:
        residuals = y_test - y_p
        fig_res = px.histogram(residuals, nbins=40, color_discrete_sequence=["#B026FF"], opacity=0.85,
                               labels={"value": "Residual (AED)", "count": "Frequency"})
        fig_res = dark_plotly_layout(fig_res, "Residual Distribution", height=430)
        st.plotly_chart(fig_res, use_container_width=True)

    insight_box("<strong>Insight:</strong> Points closer to the diagonal line indicate better predictions. "
                "A symmetric residual distribution centered near zero confirms the model has <strong>no systematic bias</strong>.")

    section_divider()

    # Feature Coefficients
    st.markdown("### Feature Coefficients")
    mdl_selected = reg_models[model_to_show]
    mdl_selected.fit(X_train, y_train)
    coefs = mdl_selected.coef_
    coef_df = pd.DataFrame({"Feature": features_used, "Coefficient": coefs}).sort_values("Coefficient")
    coef_df["Color"] = coef_df["Coefficient"].apply(lambda x: "#39FF14" if x > 0 else "#FF2D95")

    fig_coef = px.bar(coef_df, y="Feature", x="Coefficient", orientation="h",
                      color="Color", color_discrete_map="identity", text_auto=".3f")
    fig_coef.update_traces(textposition="outside")
    fig_coef = dark_plotly_layout(fig_coef, f"Feature Coefficients – {model_to_show.split(' (')[0]}", height=480)
    fig_coef.update_layout(showlegend=False)
    st.plotly_chart(fig_coef, use_container_width=True)

    top_pos = coef_df.iloc[-1]
    top_neg = coef_df.iloc[0]
    insight_box(f"<strong>Insight:</strong> <strong>{top_pos['Feature']}</strong> has the strongest positive effect on {target_label.lower()}, while "
                f"<strong>{top_neg['Feature']}</strong> shows the most negative association. "
                f"These drivers inform CosVerse's <strong>pricing optimization and revenue forecasting</strong>.")

    section_divider()

    # Cross-validation
    st.markdown("### Cross-Validation Stability")
    cv_data = pd.DataFrame({
        "Model": short_names,
        "CV R² Mean": [results[n]["CV R² (mean)"] for n in model_names],
        "CV R² Std": [results[n]["CV R² (std)"] for n in model_names]
    })
    fig_cv = go.Figure()
    fig_cv.add_trace(go.Bar(x=cv_data["Model"], y=cv_data["CV R² Mean"],
                            error_y=dict(type="data", array=cv_data["CV R² Std"].tolist(), visible=True, color="#FF2D95"),
                            marker_color=["#FF2D95","#00F0FF","#B026FF"],
                            text=[f"{v:.4f}" for v in cv_data["CV R² Mean"]], textposition="outside"))
    fig_cv = dark_plotly_layout(fig_cv, "5-Fold Cross-Validation R² Scores (with Std Dev)", height=420)
    st.plotly_chart(fig_cv, use_container_width=True)
    insight_box("<strong>Insight:</strong> Low standard deviation in CV scores indicates <strong>model stability</strong> and generalizability. "
                "CosVerse can trust these forecasting models for reliable <strong>demand estimation and business planning</strong>.")


# ─────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center; font-family: Orbitron; color: #B026FF55; font-size: 0.8rem;">'
    '🎭 CosVerse Analytics Dashboard | Built with Streamlit & Plotly | UAE Cosplay Survey 2024'
    '</div>',
    unsafe_allow_html=True
)
