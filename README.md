# 🎭 CosVerse – Cosplay Rental & Styling Platform | Data Analytics Dashboard

## 📌 Project Overview
**CosVerse** is a digital platform concept where fans can rent professional cosplay costumes instead of buying expensive ones, along with makeup tutorials and event styling services. This project uses **data analytics** to understand customer demand, segment users, and predict platform adoption based on a UAE cosplay survey dataset (n=2000).

## 🎯 Objectives
- Perform comprehensive **Exploratory Data Analysis (EDA)** on cosplay consumer behavior in the UAE
- Apply **Machine Learning algorithms** to derive actionable business insights
- Build an interactive **Streamlit dashboard** for visual storytelling and presentation

## 🛠️ Tools & Technologies
| Category | Tools |
|----------|-------|
| Language | Python 3.10+ |
| Dashboard | Streamlit |
| Visualization | Plotly |
| ML & Analytics | Scikit-learn, MLxtend, SciPy |
| Data Processing | Pandas, NumPy |

## 📊 Dashboard Structure (5 Tabs)

### Tab 1: 🏠 Overview (8 Visualizations)
- KPI metrics, Age/Gender/City distributions, Fandom popularity
- NPS & Discovery channels, Correlation heatmap
- Revenue potential analysis by demographics
- Influencer following impact on platform adoption

### Tab 2: 🤖 Classification – Predict Platform Adoption (12+ Charts)
- **EDA**: Event attendance, app intent by interest level, subscription/rental interest
- **Inference**: Adoption by occupation, event frequency, experience level, city type
- **Models**: Random Forest, Logistic Regression, Gradient Boosting
- **Outputs**: Confusion matrix, classification report, feature importance, model comparison

### Tab 3: 👥 Clustering – Customer Personas (14+ Charts)
- **EDA**: Costume price, spending by occupation, income vs spending, age-gender spend
- **Inference**: Spending-to-income ratio, costumes by interest, acquisition method spending
- **Models**: K-Means with Elbow & Silhouette analysis
- **Outputs**: 3D PCA, cluster profiles, radar chart, composition analysis

### Tab 4: 🔗 Association Rule Mining (10+ Charts)
- **EDA**: Challenges, features, acquisition methods, rental duration
- **Inference**: Challenge rate by occupation, feature demand by gender, prep time vs rental
- **Models**: Apriori with adjustable support/confidence
- **Outputs**: Rules table, scatter plot, lift distribution, challenge-feature heatmap

### Tab 5: 📈 Regression – Demand Forecasting (12+ Charts)
- **EDA**: Spending distribution, rental willingness, experience vs spending
- **Inference**: Revenue score heatmap, likelihood distribution, income bracket spending
- **Models**: Linear, Ridge, Lasso Regression
- **Outputs**: R²/MAE/RMSE comparison, actual vs predicted, residuals, coefficients, CV stability

## 📂 Project Structure
```
CosVerse-Analytics/
├── app.py                              # Main Streamlit application (1100+ lines)
├── cosplay_survey_uae_synthetic.csv    # Survey dataset (n=2000, 39 features)
├── requirements.txt                    # Python dependencies
└── README.md                           # Project documentation
```

## 🚀 How to Run

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation
```bash
git clone https://github.com/<your-username>/CosVerse-Analytics.git
cd CosVerse-Analytics
pip install -r requirements.txt
streamlit run app.py
```

### Deploy on Streamlit Cloud
1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set `app.py` as the main file
5. Deploy!

## 📈 Dataset
**2,000 survey responses** from UAE cosplay enthusiasts with **39 features**: demographics, fandom preferences, spending habits, challenges, and platform interest indicators.

## 👥 Author
CosVerse Analytics Team

## 📄 License
Academic and educational purposes.
