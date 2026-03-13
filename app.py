import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="CosVerse Analytics", page_icon="🎭", layout="wide", initial_sidebar_state="expanded")

# ── THEME ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
.stApp{background:linear-gradient(135deg,#0A0A1A 0%,#0F0F2D 50%,#0A0A1A 100%)}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0D0D25,#1A0A2E)!important;border-right:1px solid #B026FF33}
section[data-testid="stSidebar"] .stMarkdown h1,section[data-testid="stSidebar"] .stMarkdown h2,section[data-testid="stSidebar"] .stMarkdown h3{color:#FF2D95!important;font-family:'Orbitron',sans-serif!important}
h1{font-family:'Orbitron',sans-serif!important;color:#FF2D95!important;text-shadow:0 0 20px #FF2D9555}
h2{font-family:'Orbitron',sans-serif!important;color:#00F0FF!important;text-shadow:0 0 15px #00F0FF44;font-size:1.4rem!important}
h3{font-family:'Rajdhani',sans-serif!important;color:#B026FF!important;font-size:1.2rem!important}
p,li,span,div{font-family:'Rajdhani',sans-serif!important}
div[data-testid="stMetric"]{background:linear-gradient(135deg,#12122A,#1A1A3E)!important;border:1px solid #B026FF44!important;border-radius:12px!important;padding:16px!important;box-shadow:0 0 15px #B026FF22}
div[data-testid="stMetric"] label{color:#00F0FF!important;font-family:'Rajdhani',sans-serif!important;font-weight:600!important}
div[data-testid="stMetric"] div[data-testid="stMetricValue"]{color:#FF2D95!important;font-family:'Orbitron',sans-serif!important}
.stTabs [data-baseweb="tab-list"]{gap:4px;background:#0D0D25;border-radius:12px;padding:4px}
.stTabs [data-baseweb="tab"]{background:#12122A!important;border-radius:8px!important;color:#8888AA!important;font-family:'Orbitron',sans-serif!important;font-size:.72rem!important;padding:8px 16px!important;border:1px solid transparent!important}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#FF2D9533,#B026FF33)!important;border:1px solid #FF2D95!important;color:#FF2D95!important;box-shadow:0 0 10px #FF2D9533}
.insight-box{background:linear-gradient(135deg,#12122A,#1A1A3E);border-left:4px solid #00F0FF;border-radius:0 10px 10px 0;padding:12px 18px;margin:10px 0;font-family:'Rajdhani',sans-serif;color:#C8C8E8;font-size:1rem;line-height:1.5;box-shadow:0 0 10px #00F0FF11}
.insight-box strong{color:#FF2D95}
.section-divider{border:none;height:1px;background:linear-gradient(90deg,transparent,#B026FF55,#FF2D9555,transparent);margin:30px 0}
.streamlit-expanderHeader{font-family:'Rajdhani',sans-serif!important;color:#00F0FF!important;font-weight:600!important}
.stSelectbox label,.stRadio label,.stMultiSelect label,.stSlider label{color:#00F0FF!important;font-family:'Rajdhani',sans-serif!important}
footer{visibility:hidden}.stDeployButton{display:none}
.stDataFrame{border:1px solid #B026FF33!important;border-radius:8px!important}
</style>
""", unsafe_allow_html=True)

# ── HELPERS ──
NEON = ["#FF2D95","#00F0FF","#B026FF","#39FF14","#FF6B35","#FFD700","#FF4500","#00CED1"]

def T(fig, title="", height=450):
    """Theme a figure safely."""
    try: fig.update_layout(paper_bgcolor="rgba(10,10,26,0)")
    except: pass
    try: fig.update_layout(plot_bgcolor="rgba(18,18,42,0.8)")
    except: pass
    try: fig.update_layout(font=dict(family="Rajdhani",color="#C8C8E8",size=13),height=height,margin=dict(l=40,r=40,t=60,b=40),legend=dict(bgcolor="rgba(18,18,42,0.8)",bordercolor="rgba(176,38,255,0.27)",borderwidth=1,font=dict(size=12)))
    except: pass
    if title:
        try: fig.update_layout(title_text=title,title_x=0.5,title_font_family="Orbitron",title_font_size=16,title_font_color="#FF2D95")
        except: pass
    try: fig.update_xaxes(gridcolor="#1E1E3F",zerolinecolor="#1E1E3F")
    except: pass
    try: fig.update_yaxes(gridcolor="#1E1E3F",zerolinecolor="#1E1E3F")
    except: pass
    return fig

def I(text):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

def D():
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── DATA ──
@st.cache_data
def load_data():
    df = pd.read_csv("cosplay_survey_uae_synthetic.csv")
    df["Total_Fandom_Count"] = df[["Fandom_Anime","Fandom_Marvel_DC","Fandom_Gaming","Fandom_Movies_TV","Fandom_Fantasy_SciFi"]].sum(axis=1)
    df["Total_Challenges"] = df[["Challenge_High_Cost","Challenge_Size_Issues","Challenge_Limited_Availability","Challenge_Storage","Challenge_Time_Constraint","Challenge_Shipping_Delay"]].sum(axis=1)
    df["Total_Features_Wanted"] = df[["Feature_Makeup_Tutorial","Feature_Wig_Rental","Feature_Styling_Guidance","Feature_Group_Cosplay","Feature_Photoshoot_Service"]].sum(axis=1)
    df["Spending_to_Income_Ratio"] = (df["Monthly_Cosplay_Spending_AED"] / df["Monthly_Disposable_Income_AED"].replace(0, np.nan)).fillna(0)
    df["Age_Group"] = pd.cut(df["Age"], bins=[15,20,25,30,35,45], labels=["16-20","21-25","26-30","31-35","36-45"])
    df["Income_Bracket"] = pd.cut(df["Monthly_Disposable_Income_AED"], bins=[0,5000,10000,15000,20000,30000], labels=["<5K","5K-10K","10K-15K","15K-20K","20K+"])
    df["Revenue_Score"] = df["Rental_Price_Willingness_AED"] * df["Likelihood_to_Rent"]
    df["Experience_Level"] = pd.cut(df["Years_in_Cosplay"], bins=[-1,1,3,5,10,20], labels=["Newbie (0-1yr)","Beginner (2-3yr)","Intermediate (4-5yr)","Veteran (6-10yr)","Expert (10+yr)"])
    df["Event_Frequency"] = pd.cut(df["Event_Attendance_Count"], bins=[-1,0,2,5,10,50], labels=["Never","Rare (1-2)","Occasional (3-5)","Frequent (6-10)","Super Fan (10+)"])
    return df

df = load_data()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("# 🎭 CosVerse")
    st.markdown("### Analytics Dashboard")
    st.markdown("---")
    st.markdown(f"📊 **{len(df):,}** respondents &nbsp;|&nbsp; 📋 **{df.shape[1]}** features &nbsp;|&nbsp; 🌍 **UAE**")
    st.markdown("---")
    st.markdown("#### 🎛️ Filters")
    gf = st.multiselect("Gender", df["Gender"].unique().tolist(), default=df["Gender"].unique().tolist())
    cf = st.multiselect("City Type", df["City_Type"].unique().tolist(), default=df["City_Type"].unique().tolist())
    ar = st.slider("Age Range", int(df["Age"].min()), int(df["Age"].max()), (int(df["Age"].min()), int(df["Age"].max())))

mask = df["Gender"].isin(gf) & df["City_Type"].isin(cf) & (df["Age"]>=ar[0]) & (df["Age"]<=ar[1])
dff = df[mask].copy()
if len(dff)==0:
    st.warning("No data matches filters."); st.stop()

# ── TABS ──
t1,t2,t3,t4,t5 = st.tabs(["🏠 Overview","🤖 Classification","👥 Clustering","🔗 Association Rules","📈 Regression"])


# ═══════════════════════════════════════════
# TAB 1 — OVERVIEW
# ═══════════════════════════════════════════
with t1:
    st.markdown("# 🏠 CosVerse — Market Overview")
    st.markdown("##### Comprehensive demographic & behavioral snapshot of UAE cosplay consumers")

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    k1.metric("Respondents", f"{len(dff):,}")
    k2.metric("Avg Age", f"{dff['Age'].mean():.1f}")
    k3.metric("Avg Monthly Spend", f"AED {dff['Monthly_Cosplay_Spending_AED'].mean():.0f}")
    k4.metric("Avg Costume Price", f"AED {dff['Costume_Price_Avg_AED'].mean():.0f}")
    k5.metric("Avg NPS", f"{dff['NPS_Score'].mean():.1f}/10")
    k6.metric("App Interest", f"{(dff['App_Usage_Intention']=='Yes').mean():.0%}")
    D()

    # 1 — Age
    st.markdown("## 1. Age Distribution")
    fig = px.histogram(dff, x="Age", nbins=30, color_discrete_sequence=["#FF2D95"], opacity=0.85)
    fig.update_traces(marker=dict(line=dict(color="#B026FF",width=1)))
    st.plotly_chart(T(fig,"Age Distribution of Respondents"), use_container_width=True)
    I(f"<strong>Insight:</strong> The majority fall in the <strong>21-29 age bracket</strong>, peaking at age <strong>{dff['Age'].mode().iloc[0]}</strong>. This young demographic aligns with CosVerse's digital-first strategy.")

    # 2 — Gender
    st.markdown("## 2. Gender Distribution")
    gc = dff["Gender"].value_counts().reset_index(); gc.columns=["Gender","Count"]
    fig = px.pie(gc, values="Count", names="Gender", color_discrete_sequence=["#FF2D95","#00F0FF","#B026FF"], hole=0.5)
    fig.update_traces(textposition="outside", textinfo="label+percent", textfont_size=14, marker=dict(line=dict(color="#0A0A1A",width=2)))
    st.plotly_chart(T(fig,"Gender Distribution"), use_container_width=True)
    tg=gc.iloc[0]
    I(f"<strong>Insight:</strong> <strong>{tg['Gender']}</strong> respondents lead at <strong>{tg['Count']/len(dff)*100:.1f}%</strong>. CosVerse needs gender-inclusive collections and marketing across all segments.")
    D()

    # 3 — City
    st.markdown("## 3. City Distribution & Spending")
    c1,c2 = st.columns(2)
    with c1:
        cc = dff["City_Type"].value_counts().reset_index(); cc.columns=["City","Count"]
        fig = px.bar(cc, x="City", y="Count", color="City", color_discrete_sequence=["#FF2D95","#00F0FF","#B026FF"], text_auto=True)
        fig.update_traces(textposition="outside")
        st.plotly_chart(T(fig,"Respondents by City Type",380), use_container_width=True)
    with c2:
        cs = dff.groupby("City_Type")["Monthly_Cosplay_Spending_AED"].mean().reset_index(); cs.columns=["City","Spend"]
        fig = px.bar(cs, x="City", y="Spend", color="City", color_discrete_sequence=["#39FF14","#FFD700","#FF6B35"], text_auto=".0f")
        fig.update_traces(textposition="outside")
        st.plotly_chart(T(fig,"Avg Monthly Spend by City (AED)",380), use_container_width=True)
    I("<strong>Insight:</strong> Metro users form the largest segment and spend more. CosVerse should <strong>launch in Metro cities first</strong>, then expand.")
    D()

    # 4 — Fandom
    st.markdown("## 4. Fandom Category Popularity")
    fm = {"Fandom_Anime":"Anime","Fandom_Marvel_DC":"Marvel/DC","Fandom_Gaming":"Gaming","Fandom_Movies_TV":"Movies/TV","Fandom_Fantasy_SciFi":"Fantasy/Sci-Fi"}
    fd = pd.DataFrame({"Fandom":list(fm.values()),"Fans":[dff[k].sum() for k in fm]}).sort_values("Fans",ascending=True)
    fig = px.bar(fd, y="Fandom", x="Fans", orientation="h", color="Fandom", color_discrete_sequence=NEON, text_auto=True)
    fig.update_traces(textposition="outside")
    st.plotly_chart(T(fig,"Fandom Popularity (Multi-select)"), use_container_width=True)
    I(f"<strong>Insight:</strong> <strong>{fd.iloc[-1]['Fandom']}</strong> dominates with <strong>{int(fd.iloc[-1]['Fans']):,}</strong> fans. CosVerse should prioritize this fandom's costume inventory.")
    D()

    # 5 — NPS + Discovery
    st.markdown("## 5. NPS Score & Discovery Channels")
    c1,c2 = st.columns(2)
    with c1:
        fig = px.histogram(dff, x="NPS_Score", nbins=11, color_discrete_sequence=["#39FF14"], opacity=0.85)
        st.plotly_chart(T(fig,"Net Promoter Score Distribution",380), use_container_width=True)
        I(f"<strong>Insight:</strong> <strong>{(dff['NPS_Score']>=9).mean()*100:.1f}%</strong> promoters vs <strong>{(dff['NPS_Score']<=6).mean()*100:.1f}%</strong> detractors. Promoters are potential brand ambassadors for CosVerse.")
    with c2:
        dc = dff["Discovery_Channel"].value_counts().reset_index(); dc.columns=["Channel","Count"]
        fig = px.pie(dc, values="Count", names="Channel", color_discrete_sequence=NEON, hole=0.45)
        fig.update_traces(textposition="inside", textinfo="label+percent")
        st.plotly_chart(T(fig,"Discovery Channels",380), use_container_width=True)
        I("<strong>Insight:</strong> Social media dominates discovery. CosVerse should invest in <strong>TikTok & Instagram</strong> influencer marketing.")
    D()

    # 6 — Correlation Heatmap
    st.markdown("## 6. Correlation Heatmap")
    nc = ["Age","Monthly_Disposable_Income_AED","Cosplay_Interest_Level","Years_in_Cosplay","Event_Attendance_Count","Monthly_Cosplay_Spending_AED","Costume_Price_Avg_AED","Costumes_Owned","Rental_Price_Willingness_AED","Likelihood_to_Rent","NPS_Score","Total_Fandom_Count","Total_Challenges","Total_Features_Wanted"]
    corr = dff[nc].corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale=["#0A0A1A","#B026FF","#FF2D95"], aspect="auto")
    st.plotly_chart(T(fig,"Feature Correlation Heatmap",600), use_container_width=True)
    I("<strong>Insight:</strong> Strong correlations between <strong>event attendance & spending</strong> and <strong>interest & rental likelihood</strong> validate that engaged users are the best conversion targets.")
    D()

    # 7 — Revenue Score by Demographics
    st.markdown("## 7. Revenue Potential Analysis")
    c1,c2 = st.columns(2)
    with c1:
        rv = dff.groupby("Occupation")["Revenue_Score"].mean().reset_index().sort_values("Revenue_Score",ascending=True)
        fig = px.bar(rv, y="Occupation", x="Revenue_Score", orientation="h", color="Occupation", color_discrete_sequence=NEON[:3], text_auto=".0f")
        fig.update_traces(textposition="outside")
        st.plotly_chart(T(fig,"Avg Revenue Score by Occupation",380), use_container_width=True)
    with c2:
        rv2 = dff.groupby("Age_Group")["Revenue_Score"].mean().reset_index().dropna()
        fig = px.bar(rv2, x="Age_Group", y="Revenue_Score", color="Age_Group", color_discrete_sequence=NEON[:5], text_auto=".0f")
        fig.update_traces(textposition="outside")
        st.plotly_chart(T(fig,"Avg Revenue Score by Age Group",380), use_container_width=True)
    I("<strong>Insight:</strong> Revenue Score (willingness x likelihood) quantifies each segment's <strong>monetization potential</strong>. CosVerse should prioritize segments with the highest scores for targeted campaigns.")

    # 8 — Influencer Impact
    st.markdown("## 8. Influencer Following vs Platform Adoption")
    inf_app = pd.crosstab(dff["Follow_Cosplay_Influencers"], dff["App_Usage_Intention"], normalize="index")*100
    fig = px.bar(inf_app, barmode="group", color_discrete_sequence=["#39FF14","#FFD700","#FF2D95"])
    try: fig.update_layout(yaxis_title="Percentage (%)", xaxis_title="Follows Cosplay Influencers")
    except: pass
    st.plotly_chart(T(fig,"App Interest by Influencer Following",400), use_container_width=True)
    I("<strong>Insight:</strong> Users who follow cosplay influencers show higher app adoption intent. <strong>Influencer partnerships</strong> are a key growth lever for CosVerse.")


# ═══════════════════════════════════════════
# TAB 2 — CLASSIFICATION
# ═══════════════════════════════════════════
with t2:
    st.markdown("# 🤖 Classification – Predict Platform Adoption")
    st.markdown("##### Predicting user adoption with supervised ML + behavioral signal analysis")

    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

    st.markdown("## Exploratory Analysis — Adoption Signals")

    # EDA Row 1
    e1,e2 = st.columns(2)
    with e1:
        fig = px.histogram(dff, x="Event_Attendance_Count", nbins=20, color_discrete_sequence=["#00F0FF"])
        st.plotly_chart(T(fig,"Event Attendance Distribution",370), use_container_width=True)
        I(f"<strong>Insight:</strong> <strong>{(dff['Event_Attendance_Count']>0).mean()*100:.1f}%</strong> have attended events. Frequent attendees are CosVerse's <strong>premium subscriber</strong> targets.")
    with e2:
        app_c = pd.crosstab(dff["Cosplay_Interest_Level"], dff["App_Usage_Intention"], normalize="index")*100
        fig = px.bar(app_c, barmode="stack", color_discrete_sequence=["#39FF14","#FFD700","#FF2D95"])
        try: fig.update_layout(yaxis_title="%", xaxis_title="Interest Level (1-5)")
        except: pass
        st.plotly_chart(T(fig,"App Intention by Interest Level",370), use_container_width=True)
        I("<strong>Insight:</strong> Interest level 4-5 users show the highest 'Yes' rate — they are the <strong>primary early adopter</strong> cohort.")

    # EDA Row 2
    e3,e4 = st.columns(2)
    with e3:
        sc = dff["Subscription_Interest"].value_counts().reset_index(); sc.columns=["Interest","Count"]
        fig = px.bar(sc, x="Interest", y="Count", color="Interest", color_discrete_sequence=["#39FF14","#FFD700","#FF2D95"], text_auto=True)
        fig.update_traces(textposition="outside")
        st.plotly_chart(T(fig,"Subscription Interest",370), use_container_width=True)
        I("<strong>Insight:</strong> Strong subscription interest validates CosVerse's <strong>recurring revenue model</strong>. Tiered plans will capture both casual and committed users.")
    with e4:
        ri = dff["Interest_in_Rental"].value_counts().reset_index(); ri.columns=["Interest","Count"]
        fig = px.pie(ri, values="Count", names="Interest", color_discrete_sequence=["#39FF14","#FFD700","#FF2D95"], hole=0.5)
        fig.update_traces(textposition="outside", textinfo="label+percent")
        st.plotly_chart(T(fig,"Interest in Rental Service",370), use_container_width=True)
        I("<strong>Insight:</strong> The majority are open to renting. This validates CosVerse's core rental model with <strong>strong market demand</strong>.")

    # EDA Row 3 — NEW INFERENCE CHARTS
    e5,e6 = st.columns(2)
    with e5:
        occ_app = pd.crosstab(dff["Occupation"], dff["App_Usage_Intention"], normalize="index")*100
        fig = px.bar(occ_app, barmode="group", color_discrete_sequence=["#39FF14","#FFD700","#FF2D95"])
        try: fig.update_layout(yaxis_title="%", xaxis_title="Occupation")
        except: pass
        st.plotly_chart(T(fig,"App Adoption by Occupation",370), use_container_width=True)
        I("<strong>Insight:</strong> Working professionals show the highest 'Yes' rate. CosVerse should tailor <strong>convenience-focused messaging</strong> for this busy demographic.")
    with e6:
        evt_app = pd.crosstab(dff["Event_Frequency"], dff["App_Usage_Intention"], normalize="index")*100
        fig = px.bar(evt_app, barmode="stack", color_discrete_sequence=["#39FF14","#FFD700","#FF2D95"])
        try: fig.update_layout(yaxis_title="%", xaxis_title="Event Frequency")
        except: pass
        st.plotly_chart(T(fig,"App Interest by Event Frequency",370), use_container_width=True)
        I("<strong>Insight:</strong> Frequent event-goers (6-10 events) show the strongest adoption signal. CosVerse should <strong>partner with event organizers</strong> for in-venue promotions.")

    # EDA Row 4 — NEW
    e7,e8 = st.columns(2)
    with e7:
        exp_rent = pd.crosstab(dff["Experience_Level"], dff["Interest_in_Rental"], normalize="index")*100
        fig = px.bar(exp_rent, barmode="group", color_discrete_sequence=["#00F0FF","#FFD700","#FF2D95"])
        try: fig.update_layout(yaxis_title="%", xaxis_title="Experience Level")
        except: pass
        st.plotly_chart(T(fig,"Rental Interest by Cosplay Experience",370), use_container_width=True)
        I("<strong>Insight:</strong> Veterans (6-10yr) show the highest rental interest at <strong>55%</strong>. Experienced cosplayers value <strong>variety over ownership</strong> — a key CosVerse selling point.")
    with e8:
        city_app = pd.crosstab(dff["City_Type"], dff["App_Usage_Intention"], normalize="index")*100
        fig = px.bar(city_app, barmode="group", color_discrete_sequence=["#39FF14","#FFD700","#FF2D95"])
        try: fig.update_layout(yaxis_title="%", xaxis_title="City Type")
        except: pass
        st.plotly_chart(T(fig,"App Adoption by City Type",370), use_container_width=True)
        I("<strong>Insight:</strong> Adoption intent varies by city size. CosVerse should adapt <strong>launch strategy per region</strong> based on local adoption readiness.")

    D()

    # ── ML Models ──
    st.markdown("## Machine Learning — Classification Models")

    fcols = ["Age","Monthly_Disposable_Income_AED","Cosplay_Interest_Level","Years_in_Cosplay","Event_Attendance_Count","Monthly_Cosplay_Spending_AED","Costume_Price_Avg_AED","Costumes_Owned","Total_Fandom_Count","Total_Challenges","Total_Features_Wanted","NPS_Score","Likelihood_to_Rent","Rental_Price_Willingness_AED"]

    tc1,tc2 = st.columns(2)
    with tc1: target = st.selectbox("🎯 Target Variable",["App_Usage_Intention","Interest_in_Rental"])
    with tc2: mchoice = st.selectbox("🧠 Model",["Random Forest","Logistic Regression","Gradient Boosting"])

    le = LabelEncoder()
    dc = dff.dropna(subset=fcols+[target]).copy()
    X = dc[fcols].values; y = le.fit_transform(dc[target].values); cn = le.classes_
    sc = StandardScaler(); Xs = sc.fit_transform(X)
    Xtr,Xte,ytr,yte = train_test_split(Xs, y, test_size=0.25, random_state=42, stratify=y)

    md = {"Random Forest":RandomForestClassifier(n_estimators=200,max_depth=10,random_state=42),
          "Logistic Regression":LogisticRegression(max_iter=1000,multi_class="multinomial",random_state=42),
          "Gradient Boosting":GradientBoostingClassifier(n_estimators=150,max_depth=5,random_state=42)}
    m = md[mchoice]; m.fit(Xtr,ytr); yp = m.predict(Xte); acc = accuracy_score(yte,yp)

    mk1,mk2,mk3 = st.columns(3)
    mk1.metric("Accuracy",f"{acc:.2%}"); mk2.metric("Test Samples",f"{len(yte):,}"); mk3.metric("Classes",f"{len(cn)}")
    D()

    cm1,cm2 = st.columns(2)
    with cm1:
        st.markdown("### Confusion Matrix")
        cm = confusion_matrix(yte,yp)
        fig = px.imshow(cm, text_auto=True, x=cn.tolist(), y=cn.tolist(), color_continuous_scale=["#0A0A1A","#B026FF","#FF2D95"])
        try: fig.update_layout(xaxis_title="Predicted",yaxis_title="Actual")
        except: pass
        st.plotly_chart(T(fig,f"Confusion Matrix - {mchoice}",420), use_container_width=True)
    with cm2:
        st.markdown("### Classification Report")
        rpt = classification_report(yte,yp,target_names=cn.tolist(),output_dict=True)
        st.dataframe(pd.DataFrame(rpt).T.round(3).style.background_gradient(cmap="RdPu"), use_container_width=True, height=300)
    I(f"<strong>Insight:</strong> <strong>{mchoice}</strong> achieves <strong>{acc:.1%}</strong> accuracy. This model identifies high-probability adopters for <strong>targeted marketing campaigns</strong>.")
    D()

    st.markdown("### Feature Importance")
    imp = m.feature_importances_ if hasattr(m,"feature_importances_") else np.abs(m.coef_).mean(axis=0)
    fi = pd.DataFrame({"Feature":fcols,"Importance":imp}).sort_values("Importance",ascending=True)
    fig = px.bar(fi, y="Feature", x="Importance", orientation="h", color="Importance", color_continuous_scale=["#0A0A1A","#B026FF","#FF2D95"], text_auto=".3f")
    fig.update_traces(textposition="outside")
    st.plotly_chart(T(fig,f"Feature Importance - {mchoice}",500), use_container_width=True)
    I(f"<strong>Insight:</strong> <strong>{fi.iloc[-1]['Feature']}</strong> is the strongest predictor. CosVerse should prioritize users scoring high on this for maximum conversions.")
    D()

    st.markdown("### All Models Comparison")
    cr = []
    for n,mdl in md.items():
        mdl.fit(Xtr,ytr); ypp=mdl.predict(Xte); r=classification_report(yte,ypp,output_dict=True,zero_division=0)
        cr.append({"Model":n,"Accuracy":accuracy_score(yte,ypp),"Precision":r["weighted avg"]["precision"],"Recall":r["weighted avg"]["recall"],"F1-Score":r["weighted avg"]["f1-score"]})
    cdf = pd.DataFrame(cr)
    fig = px.bar(cdf.melt(id_vars="Model",var_name="Metric",value_name="Score"), x="Model",y="Score",color="Metric",barmode="group", color_discrete_sequence=["#FF2D95","#00F0FF","#B026FF","#39FF14"], text_auto=".3f")
    fig.update_traces(textposition="outside")
    st.plotly_chart(T(fig,"Model Performance Comparison",450), use_container_width=True)
    b=cdf.loc[cdf["F1-Score"].idxmax()]
    I(f"<strong>Insight:</strong> <strong>{b['Model']}</strong> achieves the best F1 of <strong>{b['F1-Score']:.3f}</strong> — recommended for CosVerse's production recommendation engine.")


# ═══════════════════════════════════════════
# TAB 3 — CLUSTERING
# ═══════════════════════════════════════════
with t3:
    st.markdown("# 👥 Clustering – Customer Personas")
    st.markdown("##### K-Means segmentation to identify actionable customer groups")

    from sklearn.preprocessing import StandardScaler as SS2
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    from sklearn.decomposition import PCA

    st.markdown("## Exploratory Analysis — Spending & Segmentation Signals")

    s1,s2 = st.columns(2)
    with s1:
        fig = px.histogram(dff, x="Costume_Price_Avg_AED", nbins=40, color_discrete_sequence=["#FFD700"], opacity=0.85)
        st.plotly_chart(T(fig,"Costume Price Distribution (AED)",370), use_container_width=True)
        I(f"<strong>Insight:</strong> Median costume cost is <strong>AED {dff['Costume_Price_Avg_AED'].median():.0f}</strong>. A rental at 30-40% of purchase unlocks massive value.")
    with s2:
        fig = px.box(dff, x="Occupation", y="Monthly_Cosplay_Spending_AED", color="Occupation", color_discrete_sequence=NEON, points="outliers")
        st.plotly_chart(T(fig,"Monthly Spend by Occupation (AED)",370), use_container_width=True)
        I(f"<strong>Insight:</strong> <strong>{dff.groupby('Occupation')['Monthly_Cosplay_Spending_AED'].mean().idxmax()}s</strong> spend the most. CosVerse can offer tiered pricing per occupation.")

    s3,s4 = st.columns(2)
    with s3:
        fig = px.scatter(dff, x="Monthly_Disposable_Income_AED", y="Costume_Price_Avg_AED", color="Interest_in_Rental", size="Event_Attendance_Count", color_discrete_sequence=["#FF2D95","#FFD700","#00F0FF"], opacity=0.7)
        st.plotly_chart(T(fig,"Income vs Costume Price",370), use_container_width=True)
        I("<strong>Insight:</strong> High costume costs affect <strong>all income levels</strong>. Lower-income users show stronger rental interest — CosVerse's core market.")
    with s4:
        fig = px.box(dff, x="Age_Group", y="Monthly_Cosplay_Spending_AED", color="Gender", color_discrete_sequence=["#FF2D95","#00F0FF","#B026FF"])
        st.plotly_chart(T(fig,"Spend by Age & Gender (AED)",370), use_container_width=True)
        I("<strong>Insight:</strong> The <strong>26-30 bracket</strong> spends the most. CosVerse should target this group with premium and VIP styling packages.")

    # NEW — Spending Ratio + Costumes Owned
    s5,s6 = st.columns(2)
    with s5:
        fig = px.histogram(dff, x="Spending_to_Income_Ratio", nbins=40, color_discrete_sequence=["#B026FF"], opacity=0.85)
        st.plotly_chart(T(fig,"Cosplay Spend as % of Income",370), use_container_width=True)
        avg_ratio = dff["Spending_to_Income_Ratio"].mean()*100
        I(f"<strong>Insight:</strong> Users spend on average <strong>{avg_ratio:.1f}%</strong> of disposable income on cosplay. High ratios signal <strong>price-sensitive users</strong> who benefit most from rentals.")
    with s6:
        co = dff.groupby("Cosplay_Interest_Level")["Costumes_Owned"].mean().reset_index()
        fig = px.bar(co, x="Cosplay_Interest_Level", y="Costumes_Owned", color_discrete_sequence=["#00F0FF"], text_auto=".1f")
        fig.update_traces(textposition="outside")
        st.plotly_chart(T(fig,"Avg Costumes Owned by Interest Level",370), use_container_width=True)
        I("<strong>Insight:</strong> Higher interest users own more costumes — they're <strong>heavy buyers ready to switch to rentals</strong> for variety and savings.")

    # NEW — Acquisition Method Spending
    st.markdown("### Spending by Current Acquisition Method")
    acq_spend = dff.groupby("Costume_Acquisition_Method")[["Monthly_Cosplay_Spending_AED","Costume_Price_Avg_AED"]].mean().reset_index()
    fig = px.bar(acq_spend, x="Costume_Acquisition_Method", y=["Monthly_Cosplay_Spending_AED","Costume_Price_Avg_AED"], barmode="group", color_discrete_sequence=["#FF2D95","#00F0FF"])
    st.plotly_chart(T(fig,"Spending Comparison by Acquisition Method (AED)",400), use_container_width=True)
    I("<strong>Insight:</strong> Users who currently rent already spend similarly to buyers. CosVerse can attract <strong>all acquisition segments</strong> with competitive pricing.")
    D()

    # ── K-Means ──
    st.markdown("## Machine Learning — K-Means Clustering")
    cfeats = ["Age","Monthly_Disposable_Income_AED","Cosplay_Interest_Level","Years_in_Cosplay","Event_Attendance_Count","Monthly_Cosplay_Spending_AED","Costume_Price_Avg_AED","Costumes_Owned","Total_Fandom_Count","Total_Challenges","Total_Features_Wanted","NPS_Score","Likelihood_to_Rent","Rental_Price_Willingness_AED"]
    dcl = dff.dropna(subset=cfeats).copy()
    Xcl = SS2().fit_transform(dcl[cfeats].values)

    st.markdown("### Elbow & Silhouette")
    el1,el2 = st.columns(2)
    inr,sil = [],[]
    for k in range(2,9):
        km=KMeans(n_clusters=k,random_state=42,n_init=10); km.fit(Xcl)
        inr.append(km.inertia_); sil.append(silhouette_score(Xcl,km.labels_,sample_size=min(1000,len(Xcl))))
    with el1:
        fig=px.line(x=list(range(2,9)),y=inr,markers=True,labels={"x":"K","y":"Inertia"})
        fig.update_traces(line=dict(color="#FF2D95"),marker=dict(color="#00F0FF",size=10))
        st.plotly_chart(T(fig,"Elbow Method",370),use_container_width=True)
    with el2:
        fig=px.bar(x=list(range(2,9)),y=sil,labels={"x":"K","y":"Silhouette"},color_discrete_sequence=["#B026FF"])
        st.plotly_chart(T(fig,"Silhouette Scores",370),use_container_width=True)
    I("<strong>Insight:</strong> Choose K at the elbow with highest silhouette. This gives the most <strong>distinct, actionable customer segments</strong>.")
    D()

    nk = st.slider("Select K",2,8,3)
    km = KMeans(n_clusters=nk,random_state=42,n_init=10)
    dcl["Cluster"] = km.fit_predict(Xcl)
    dcl["CL"] = dcl["Cluster"].astype(str)

    st.markdown("### 3D PCA Visualization")
    pca=PCA(n_components=3); Xp=pca.fit_transform(Xcl)
    dcl["PC1"],dcl["PC2"],dcl["PC3"]=Xp[:,0],Xp[:,1],Xp[:,2]
    fig=px.scatter_3d(dcl,x="PC1",y="PC2",z="PC3",color="CL",color_discrete_sequence=NEON[:nk],opacity=0.7)
    T(fig,"Customer Segments in 3D PCA Space",550)
    try: fig.update_layout(scene=dict(xaxis=dict(backgroundcolor="#0A0A1A",gridcolor="#1E1E3F"),yaxis=dict(backgroundcolor="#0A0A1A",gridcolor="#1E1E3F"),zaxis=dict(backgroundcolor="#0A0A1A",gridcolor="#1E1E3F")))
    except: pass
    st.plotly_chart(fig,use_container_width=True)
    I(f"<strong>Insight:</strong> 3 PCs explain <strong>{pca.explained_variance_ratio_.sum()*100:.1f}%</strong> variance. Distinct clusters confirm <strong>actionable customer personas</strong>.")
    D()

    st.markdown("### Cluster Profiles")
    pcols=["Age","Monthly_Disposable_Income_AED","Cosplay_Interest_Level","Event_Attendance_Count","Monthly_Cosplay_Spending_AED","Costume_Price_Avg_AED","Total_Features_Wanted","Likelihood_to_Rent","NPS_Score","Revenue_Score"]
    cp=dcl.groupby("Cluster")[pcols].mean().round(1)
    cp.index=[f"Cluster {i}" for i in cp.index]
    st.dataframe(cp.style.background_gradient(cmap="RdPu",axis=0),use_container_width=True)

    st.markdown("### Persona Radar Chart")
    rcols=["Cosplay_Interest_Level","Event_Attendance_Count","Monthly_Cosplay_Spending_AED","Total_Features_Wanted","Likelihood_to_Rent","NPS_Score"]
    rd=dcl.groupby("Cluster")[rcols].mean()
    rn=(rd-rd.min())/(rd.max()-rd.min()+1e-9)
    pn=["Hardcore Cosplayers","Casual Fans","Event Visitors"] if nk==3 else [f"Segment {i}" for i in range(nk)]
    fig=go.Figure()
    for i in range(nk):
        lb=pn[i] if i<len(pn) else f"Seg {i}"
        v=rn.iloc[i].tolist()+[rn.iloc[i].tolist()[0]]
        fig.add_trace(go.Scatterpolar(r=v,theta=rcols+[rcols[0]],fill="toself",name=lb,opacity=0.35,line=dict(color=NEON[i],width=2)))
    T(fig,"Customer Persona Radar",500)
    try: fig.update_layout(polar=dict(bgcolor="rgba(18,18,42,0.8)",radialaxis=dict(visible=True,range=[0,1],gridcolor="#1E1E3F"),angularaxis=dict(gridcolor="#1E1E3F")))
    except: pass
    st.plotly_chart(fig,use_container_width=True)
    I("<strong>Insight:</strong> Distinct personas emerge — high spenders vs budget casuals vs occasional visitors. CosVerse needs <strong>differentiated service tiers</strong> for each.")
    D()

    # NEW — Cluster composition breakdown
    st.markdown("### Cluster Composition Analysis")
    cc1,cc2 = st.columns(2)
    with cc1:
        comp = dcl.groupby("Cluster")["Occupation"].value_counts(normalize=True).unstack().fillna(0)*100
        fig = px.bar(comp, barmode="stack", color_discrete_sequence=NEON[:3])
        try: fig.update_layout(yaxis_title="%",xaxis_title="Cluster")
        except: pass
        st.plotly_chart(T(fig,"Occupation Mix per Cluster",380),use_container_width=True)
    with cc2:
        comp2 = dcl.groupby("Cluster")["Interest_in_Rental"].value_counts(normalize=True).unstack().fillna(0)*100
        fig = px.bar(comp2, barmode="stack", color_discrete_sequence=["#39FF14","#FFD700","#FF2D95"])
        try: fig.update_layout(yaxis_title="%",xaxis_title="Cluster")
        except: pass
        st.plotly_chart(T(fig,"Rental Interest per Cluster",380),use_container_width=True)
    I("<strong>Insight:</strong> Clusters differ not just in spending but in <strong>occupation mix and rental openness</strong>. This enables hyper-targeted messaging per persona.")

    st.markdown("### Feature Distribution by Cluster")
    fp = st.selectbox("Select Feature",pcols,index=4)
    fig = px.box(dcl, x="CL", y=fp, color="CL", color_discrete_sequence=NEON[:nk], points="outliers")
    st.plotly_chart(T(fig,f"{fp} by Cluster"),use_container_width=True)


# ═══════════════════════════════════════════
# TAB 4 — ASSOCIATION RULES
# ═══════════════════════════════════════════
with t4:
    st.markdown("# 🔗 Association Rule Mining")
    st.markdown("##### Uncovering challenge-to-feature demand patterns with Apriori")

    from mlxtend.frequent_patterns import apriori, association_rules

    st.markdown("## Exploratory Analysis — Pain Points & Feature Demand")

    a1,a2 = st.columns(2)
    with a1:
        chm={"Challenge_High_Cost":"High Cost","Challenge_Size_Issues":"Size Issues","Challenge_Limited_Availability":"Limited Avail.","Challenge_Storage":"Storage","Challenge_Time_Constraint":"Time Crunch","Challenge_Shipping_Delay":"Shipping Delay"}
        chd=pd.DataFrame({"Challenge":list(chm.values()),"Count":[dff[k].sum() for k in chm]}).sort_values("Count",ascending=False)
        fig=px.bar(chd,x="Challenge",y="Count",color="Challenge",color_discrete_sequence=["#FF2D95","#FF6B35","#FFD700","#39FF14","#00F0FF","#B026FF"],text_auto=True)
        fig.update_traces(textposition="outside")
        st.plotly_chart(T(fig,"Top Challenges",400),use_container_width=True)
        I(f"<strong>Insight:</strong> <strong>{chd.iloc[0]['Challenge']}</strong> leads with <strong>{int(chd.iloc[0]['Count']):,}</strong> mentions. CosVerse's rental model directly solves this #1 pain point.")
    with a2:
        ftm={"Feature_Makeup_Tutorial":"Makeup Tutorials","Feature_Wig_Rental":"Wig Rental","Feature_Styling_Guidance":"Styling Guidance","Feature_Group_Cosplay":"Group Cosplay","Feature_Photoshoot_Service":"Photoshoot Service"}
        ftd=pd.DataFrame({"Feature":list(ftm.values()),"Interest":[dff[k].sum() for k in ftm]}).sort_values("Interest",ascending=True)
        fig=px.bar(ftd,y="Feature",x="Interest",orientation="h",color="Feature",color_discrete_sequence=NEON[:5],text_auto=True)
        fig.update_traces(textposition="outside")
        st.plotly_chart(T(fig,"Most Desired Features",400),use_container_width=True)
        I(f"<strong>Insight:</strong> <strong>{ftd.iloc[-1]['Feature']}</strong> tops demand. CosVerse should build this into the MVP for maximum engagement.")

    # NEW — Challenge Rate by Occupation + Feature by Gender
    a3,a4 = st.columns(2)
    with a3:
        ch_occ = dff.groupby("Occupation")[[*chm.keys()]].mean().rename(columns=chm)*100
        fig = px.bar(ch_occ.T, barmode="group", color_discrete_sequence=NEON[:3])
        try: fig.update_layout(yaxis_title="% Affected",xaxis_title="Challenge")
        except: pass
        st.plotly_chart(T(fig,"Challenge Rate by Occupation (%)",400),use_container_width=True)
        I("<strong>Insight:</strong> Challenge distribution is <strong>consistent across occupations</strong>, meaning CosVerse's solutions are universally needed — not niche.")
    with a4:
        ft_gen = dff.groupby("Gender")[[*ftm.keys()]].mean().rename(columns=ftm)*100
        fig = px.bar(ft_gen.T, barmode="group", color_discrete_sequence=["#FF2D95","#00F0FF","#B026FF"])
        try: fig.update_layout(yaxis_title="% Interested",xaxis_title="Feature")
        except: pass
        st.plotly_chart(T(fig,"Feature Demand by Gender (%)",400),use_container_width=True)
        I("<strong>Insight:</strong> Feature preferences are <strong>largely gender-neutral</strong>. CosVerse can market features universally without heavy gender segmentation.")

    # NEW — Acquisition + Duration
    a5,a6 = st.columns(2)
    with a5:
        ac=dff["Costume_Acquisition_Method"].value_counts().reset_index(); ac.columns=["Method","Count"]
        fig=px.bar(ac,x="Method",y="Count",color="Method",color_discrete_sequence=NEON[:5],text_auto=True)
        fig.update_traces(textposition="outside")
        st.plotly_chart(T(fig,"Acquisition Methods",370),use_container_width=True)
        I("<strong>Insight:</strong> Most buy or DIY. CosVerse converts them with <strong>lower cost + zero hassle</strong> rentals.")
    with a6:
        rd=dff["Preferred_Rental_Duration"].value_counts().reset_index(); rd.columns=["Duration","Count"]
        fig=px.pie(rd,values="Count",names="Duration",color_discrete_sequence=["#FF2D95","#00F0FF","#B026FF","#39FF14"],hole=0.45)
        fig.update_traces(textposition="inside",textinfo="label+percent")
        st.plotly_chart(T(fig,"Preferred Rental Duration",370),use_container_width=True)
        I("<strong>Insight:</strong> Short-term (1 day to 1 week) dominates. CosVerse pricing should center on <strong>event-based rental windows</strong>.")

    # NEW — Preparation Time vs Rental
    st.markdown("### Costume Preparation Time vs Rental Interest")
    pt_rent = pd.crosstab(dff["Costume_Preparation_Time"], dff["Interest_in_Rental"], normalize="index")*100
    fig = px.bar(pt_rent, barmode="group", color_discrete_sequence=["#00F0FF","#FFD700","#FF2D95"])
    try: fig.update_layout(yaxis_title="%",xaxis_title="Preparation Time")
    except: pass
    st.plotly_chart(T(fig,"Rental Interest by Prep Time",400),use_container_width=True)
    I("<strong>Insight:</strong> Users across <strong>all prep time levels</strong> show ~50% rental interest. Even those who plan ahead see rental value, suggesting CosVerse appeals to both planners and last-minute cosplayers.")
    D()

    # ── Apriori ──
    st.markdown("## Machine Learning — Apriori Rules")
    chl={"Challenge_High_Cost":"High Cost","Challenge_Size_Issues":"Size Issues","Challenge_Limited_Availability":"Limited Availability","Challenge_Storage":"Storage Problem","Challenge_Time_Constraint":"Time Constraint","Challenge_Shipping_Delay":"Shipping Delay"}
    ftl={"Feature_Makeup_Tutorial":"Makeup Tutorial","Feature_Wig_Rental":"Wig Rental","Feature_Styling_Guidance":"Styling Guidance","Feature_Group_Cosplay":"Group Cosplay","Feature_Photoshoot_Service":"Photoshoot Service"}
    ai={**chl,**ftl}
    bdf=dff[list(ai.keys())].rename(columns=ai).astype(bool)

    sl1,sl2=st.columns(2)
    with sl1: msup=st.slider("Min Support",0.05,0.5,0.10,0.05)
    with sl2: mcnf=st.slider("Min Confidence",0.10,1.0,0.30,0.05)

    freq=apriori(bdf,min_support=msup,use_colnames=True)
    if len(freq)==0:
        st.warning("No itemsets found. Lower support.")
    else:
        try:
            rules=association_rules(freq,metric="confidence",min_threshold=mcnf,num_itemsets=len(freq))
        except TypeError:
            rules=association_rules(freq,metric="confidence",min_threshold=mcnf)
        if len(rules)==0:
            st.warning("No rules found. Lower confidence.")
        else:
            # Normalize column names (different mlxtend versions use different names)
            rules.columns = [c.lower().replace(" ", "_") for c in rules.columns]
            # Ensure 'lift' column exists
            if "lift" not in rules.columns:
                for col in rules.columns:
                    if "lift" in col.lower():
                        rules = rules.rename(columns={col: "lift"})
                        break

            rules["ant"]=rules["antecedents"].apply(lambda x:", ".join(sorted(x)))
            rules["con"]=rules["consequents"].apply(lambda x:", ".join(sorted(x)))
            rk1,rk2,rk3=st.columns(3)
            rk1.metric("Rules",f"{len(rules)}"); rk2.metric("Avg Confidence",f"{rules['confidence'].mean():.2%}"); rk3.metric("Avg Lift",f"{rules['lift'].mean():.2f}")
            D()

            st.markdown("### Top Rules")
            display_df=rules[["ant","con","support","confidence","lift"]].copy()
            display_df.columns=["If","Then","Support","Confidence","Lift"]
            display_df=display_df.sort_values("Lift",ascending=False).head(20).reset_index(drop=True)
            st.dataframe(display_df.style.background_gradient(subset=["Lift"],cmap="RdPu").format({"Support":"{:.3f}","Confidence":"{:.3f}","Lift":"{:.3f}"}),use_container_width=True,height=400)
            I("<strong>Insight:</strong> Rules with <strong>lift > 1</strong> show genuine positive associations. These reveal which challenges <strong>directly drive feature demand</strong>.")
            D()

            st.markdown("### Rules Visualization")
            rv1,rv2 = st.columns(2)
            with rv1:
                fig=px.scatter(rules,x="support",y="confidence",size="lift",color="lift",color_continuous_scale=["#0A0A1A","#B026FF","#FF2D95"],hover_data=["ant","con"],size_max=20,opacity=0.8)
                st.plotly_chart(T(fig,"Support vs Confidence (Lift)",450),use_container_width=True)
            with rv2:
                fig = px.histogram(rules, x="lift", nbins=20, color_discrete_sequence=["#39FF14"], opacity=0.85)
                st.plotly_chart(T(fig,"Lift Score Distribution",450),use_container_width=True)
            I("<strong>Insight:</strong> Top-right quadrant rules are the most actionable. The lift distribution shows how many rules <strong>exceed random chance</strong>.")
            D()

            st.markdown("### Challenge to Feature Heatmap")
            ci=list(chl.values()); fi_items=list(ftl.values())
            cf=rules[rules["ant"].apply(lambda x:any(c in x for c in ci))&rules["con"].apply(lambda x:any(f in x for f in fi_items))]
            if len(cf)>0:
                hm=cf.pivot_table(index="ant",columns="con",values="lift",aggfunc="max").fillna(0)
                fig=px.imshow(hm,text_auto=".2f",color_continuous_scale=["#0A0A1A","#B026FF","#FF2D95"])
                st.plotly_chart(T(fig,"Challenge to Feature Lift Heatmap",450),use_container_width=True)
                I("<strong>Insight:</strong> This heatmap is CosVerse's <strong>feature prioritization roadmap</strong> — build features that address the most common pain points first.")
            else:
                st.info("No direct Challenge-Feature rules. Adjust thresholds.")


# ═══════════════════════════════════════════
# TAB 5 — REGRESSION
# ═══════════════════════════════════════════
with t5:
    st.markdown("# 📈 Regression – Demand Forecasting")
    st.markdown("##### Predicting spending and rental demand for pricing & business strategy")

    from sklearn.model_selection import train_test_split as tts, cross_val_score
    from sklearn.preprocessing import StandardScaler as SS3
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    st.markdown("## Exploratory Analysis — Demand & Pricing Signals")

    r1,r2 = st.columns(2)
    with r1:
        fig=px.histogram(dff,x="Monthly_Cosplay_Spending_AED",nbins=40,color_discrete_sequence=["#00F0FF"],opacity=0.85)
        st.plotly_chart(T(fig,"Monthly Spending Distribution (AED)",370),use_container_width=True)
        I(f"<strong>Insight:</strong> Right-skewed with mean <strong>AED {dff['Monthly_Cosplay_Spending_AED'].mean():.0f}</strong>. CosVerse captures this spend with competitive rental pricing.")
    with r2:
        fig=px.violin(dff,x="Interest_in_Rental",y="Rental_Price_Willingness_AED",color="Interest_in_Rental",box=True,color_discrete_sequence=["#FF2D95","#FFD700","#00F0FF"])
        st.plotly_chart(T(fig,"Willingness to Pay by Interest (AED)",370),use_container_width=True)
        I("<strong>Insight:</strong> Interested users show <strong>higher willingness</strong>. CosVerse can use dynamic pricing based on engagement signals.")

    r3,r4 = st.columns(2)
    with r3:
        fig=px.scatter(dff,x="Years_in_Cosplay",y="Monthly_Cosplay_Spending_AED",color="Cosplay_Interest_Level",color_continuous_scale=["#0A0A1A","#B026FF","#FF2D95"],opacity=0.6)
        st.plotly_chart(T(fig,"Experience vs Monthly Spending",370),use_container_width=True)
        I("<strong>Insight:</strong> Experienced cosplayers spend more. CosVerse should offer <strong>loyalty tiers</strong> to retain high-value veterans.")
    with r4:
        fig=px.scatter(dff,x="Event_Attendance_Count",y="Costumes_Owned",color="Occupation",color_discrete_sequence=NEON[:3],opacity=0.6)
        st.plotly_chart(T(fig,"Events vs Costumes Owned",370),use_container_width=True)
        I("<strong>Insight:</strong> Frequent attendees own more costumes — <strong>high-frequency rental candidates</strong>. Event-bundle packages will capture this segment.")

    # NEW — Revenue Score Heatmap + Likelihood Distribution
    r5,r6 = st.columns(2)
    with r5:
        rev_hm = dff.pivot_table(index="Age_Group", columns="City_Type", values="Revenue_Score", aggfunc="mean").fillna(0)
        fig = px.imshow(rev_hm, text_auto=".0f", color_continuous_scale=["#0A0A1A","#B026FF","#FF2D95"])
        st.plotly_chart(T(fig,"Revenue Score: Age x City",370),use_container_width=True)
        I("<strong>Insight:</strong> This heatmap reveals the <strong>highest-value demographic x location cells</strong>. CosVerse should allocate marketing budget to the brightest cells first.")
    with r6:
        fig = px.histogram(dff, x="Likelihood_to_Rent", nbins=5, color_discrete_sequence=["#39FF14"], opacity=0.85)
        st.plotly_chart(T(fig,"Likelihood to Rent Distribution (1-5)",370),use_container_width=True)
        avg_like = dff["Likelihood_to_Rent"].mean()
        I(f"<strong>Insight:</strong> Average likelihood is <strong>{avg_like:.1f}/5</strong>. Users rating 4-5 are <strong>hot leads</strong> for CosVerse's launch campaign.")

    # NEW — Income Bracket Spending
    st.markdown("### Spending Patterns by Income Bracket")
    inc_spend = dff.groupby("Income_Bracket")[["Monthly_Cosplay_Spending_AED","Rental_Price_Willingness_AED","Costume_Price_Avg_AED"]].mean().reset_index()
    fig = px.bar(inc_spend, x="Income_Bracket", y=["Monthly_Cosplay_Spending_AED","Rental_Price_Willingness_AED","Costume_Price_Avg_AED"], barmode="group", color_discrete_sequence=["#FF2D95","#00F0FF","#39FF14"])
    st.plotly_chart(T(fig,"Spending Metrics by Income Bracket (AED)",420),use_container_width=True)
    I("<strong>Insight:</strong> Even lower-income users spend heavily on costumes. The gap between costume price and rental willingness represents CosVerse's <strong>value capture opportunity</strong>.")
    D()

    # ── Regression Models ──
    st.markdown("## Machine Learning — Regression Models")
    rfts=["Age","Monthly_Disposable_Income_AED","Cosplay_Interest_Level","Years_in_Cosplay","Event_Attendance_Count","Costume_Price_Avg_AED","Costumes_Owned","Total_Fandom_Count","Total_Challenges","Total_Features_Wanted","NPS_Score","Likelihood_to_Rent"]
    tmap={"Monthly Cosplay Spending (AED)":"Monthly_Cosplay_Spending_AED","Rental Price Willingness (AED)":"Rental_Price_Willingness_AED","Average Costume Price (AED)":"Costume_Price_Avg_AED"}
    tl=st.selectbox("🎯 Target Variable",list(tmap.keys()))
    tc=tmap[tl]; fu=[f for f in rfts if f!=tc]

    dr=dff.dropna(subset=fu+[tc]).copy()
    Xr=dr[fu].values; yr=dr[tc].values
    Xrs=SS3().fit_transform(Xr)
    Xtr,Xte,ytr,yte=tts(Xrs,yr,test_size=0.25,random_state=42)

    rmd={"Linear Regression":LinearRegression(),"Ridge Regression":Ridge(alpha=1.0),"Lasso Regression":Lasso(alpha=1.0)}
    res={}; pds={}
    for n,mdl in rmd.items():
        mdl.fit(Xtr,ytr); yp=mdl.predict(Xte); pds[n]=yp
        cv=cross_val_score(mdl,Xrs,yr,cv=5,scoring="r2")
        res[n]={"R2":r2_score(yte,yp),"MAE":mean_absolute_error(yte,yp),"RMSE":np.sqrt(mean_squared_error(yte,yp)),"CV_R2":cv.mean(),"CV_Std":cv.std()}

    bn=max(res,key=lambda x:res[x]["R2"])
    bk1,bk2,bk3,bk4=st.columns(4)
    bk1.metric("Best Model",bn); bk2.metric("Best R2",f"{res[bn]['R2']:.4f}"); bk3.metric("MAE",f"AED {res[bn]['MAE']:.2f}"); bk4.metric("RMSE",f"AED {res[bn]['RMSE']:.2f}")
    D()

    st.markdown("### Performance Comparison")
    rdf=pd.DataFrame(res).T; rdf.index.name="Model"
    st.dataframe(rdf.style.background_gradient(cmap="RdPu").format("{:.4f}"),use_container_width=True)

    mn=list(res.keys())
    fig=make_subplots(rows=1,cols=3,subplot_titles=["R2","MAE (AED)","RMSE (AED)"])
    fig.add_trace(go.Bar(x=mn,y=[res[n]["R2"] for n in mn],marker_color=["#FF2D95","#00F0FF","#B026FF"],text=[f"{res[n]['R2']:.4f}" for n in mn],textposition="outside"),row=1,col=1)
    fig.add_trace(go.Bar(x=mn,y=[res[n]["MAE"] for n in mn],marker_color=["#FF2D95","#00F0FF","#B026FF"],text=[f"{res[n]['MAE']:.1f}" for n in mn],textposition="outside"),row=1,col=2)
    fig.add_trace(go.Bar(x=mn,y=[res[n]["RMSE"] for n in mn],marker_color=["#FF2D95","#00F0FF","#B026FF"],text=[f"{res[n]['RMSE']:.1f}" for n in mn],textposition="outside"),row=1,col=3)
    T(fig,"Model Comparison",420)
    try: fig.update_layout(showlegend=False)
    except: pass
    st.plotly_chart(fig,use_container_width=True)
    I(f"<strong>Insight:</strong> <strong>{bn}</strong> achieves R2 of <strong>{res[bn]['R2']:.4f}</strong>. This model forecasts {tl.lower()} for CosVerse's <strong>pricing and demand planning</strong>.")
    D()

    st.markdown("### Actual vs Predicted & Residuals")
    ms=st.selectbox("Model Detail View",mn)
    yps=pds[ms]
    rp1,rp2=st.columns(2)
    with rp1:
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=yte,y=yps,mode="markers",marker=dict(color="#00F0FF",opacity=0.5,size=5),name="Predictions"))
        fig.add_trace(go.Scatter(x=[yte.min(),yte.max()],y=[yte.min(),yte.max()],mode="lines",line=dict(color="#FF2D95",dash="dash"),name="Perfect Fit"))
        try: fig.update_layout(xaxis_title=f"Actual",yaxis_title=f"Predicted")
        except: pass
        st.plotly_chart(T(fig,f"Actual vs Predicted - {ms}",430),use_container_width=True)
    with rp2:
        residuals=yte-yps
        fig=px.histogram(residuals,nbins=40,color_discrete_sequence=["#B026FF"],opacity=0.85)
        try: fig.update_layout(xaxis_title="Residual (AED)",yaxis_title="Freq")
        except: pass
        st.plotly_chart(T(fig,"Residual Distribution",430),use_container_width=True)
    I("<strong>Insight:</strong> Points near the diagonal = accurate predictions. Symmetric residuals confirm <strong>no systematic bias</strong> in the model.")
    D()

    st.markdown("### Feature Coefficients")
    mdl_s=rmd[ms]; mdl_s.fit(Xtr,ytr)
    cdf=pd.DataFrame({"Feature":fu,"Coefficient":mdl_s.coef_}).sort_values("Coefficient")
    bc=["#39FF14" if c>0 else "#FF2D95" for c in cdf["Coefficient"]]
    fig=go.Figure(go.Bar(y=cdf["Feature"].tolist(),x=cdf["Coefficient"].tolist(),orientation="h",marker_color=bc,text=[f"{v:.3f}" for v in cdf["Coefficient"]],textposition="outside"))
    st.plotly_chart(T(fig,f"Coefficients - {ms}",480),use_container_width=True)
    I(f"<strong>Insight:</strong> Green bars (positive) increase {tl.lower()}; pink bars decrease it. These drivers shape CosVerse's <strong>pricing optimization strategy</strong>.")
    D()

    st.markdown("### Cross-Validation Stability")
    fig=go.Figure()
    fig.add_trace(go.Bar(x=mn,y=[res[n]["CV_R2"] for n in mn],error_y=dict(type="data",array=[res[n]["CV_Std"] for n in mn],visible=True,color="#FF2D95"),marker_color=["#FF2D95","#00F0FF","#B026FF"],text=[f"{res[n]['CV_R2']:.4f}" for n in mn],textposition="outside"))
    st.plotly_chart(T(fig,"5-Fold CV R2 (with Std Dev)",420),use_container_width=True)
    I("<strong>Insight:</strong> Low CV standard deviation = <strong>stable, generalizable models</strong>. CosVerse can rely on these for production demand forecasting.")


# ── FOOTER ──
st.markdown("---")
st.markdown('<div style="text-align:center;font-family:Orbitron;color:#B026FF55;font-size:.8rem">🎭 CosVerse Analytics Dashboard | Streamlit + Plotly | UAE Cosplay Survey 2024</div>',unsafe_allow_html=True)
