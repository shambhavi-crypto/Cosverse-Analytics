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

### Tab 1: 🏠 Overview
- KPI metrics (respondents, avg age, avg spend, NPS, app interest)
- Age, Gender, City distributions
- Fandom category popularity
- NPS & Discovery channel analysis
- Correlation heatmap across all numeric features

### Tab 2: 🤖 Classification – Predict Platform Adoption
- **EDA**: Event attendance, app usage intention by interest level, subscription interest, rental interest
- **Target Variables**: `App_Usage_Intention` and `Interest_in_Rental`
- **Models**: Random Forest, Logistic Regression, Gradient Boosting
- **Outputs**: Confusion matrix, classification report, feature importance, model comparison

### Tab 3: 👥 Clustering – Customer Personas
- **EDA**: Costume price distribution, spending by occupation, income vs spending, age-gender spending
- **Algorithm**: K-Means Clustering with Elbow & Silhouette analysis
- **Outputs**: 3D PCA visualization, cluster profiles table, radar chart, feature distributions

### Tab 4: 🔗 Association Rule Mining
- **EDA**: Challenges faced, desired features, acquisition methods, rental duration preferences
- **Algorithm**: Apriori with adjustable support/confidence
- **Outputs**: Rules table, scatter plot (support vs confidence vs lift), challenge-to-feature heatmap

### Tab 5: 📈 Regression – Demand Forecasting
- **EDA**: Spending distribution, rental willingness, experience vs spending, events vs costumes
- **Models**: Linear Regression, Ridge Regression, Lasso Regression
- **Outputs**: R²/MAE/RMSE comparison, actual vs predicted, residuals, feature coefficients, cross-validation

## 📂 Project Structure
```
CosVerse-Analytics/
├── app.py                              # Main Streamlit application
├── cosplay_survey_uae_synthetic.csv    # Survey dataset (n=2000)
├── requirements.txt                    # Python dependencies
└── README.md                           # Project documentation
```

## 🚀 How to Run

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation
```bash
# Clone the repository
git clone https://github.com/<your-username>/CosVerse-Analytics.git
cd CosVerse-Analytics

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

### Deploy on Streamlit Cloud
1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set `app.py` as the main file
5. Deploy!

## 📈 Dataset Description
The dataset contains **2,000 survey responses** from UAE-based cosplay enthusiasts and fans with **39 features** including demographics, fandom preferences, spending habits, challenges, and platform interest indicators.

## 👥 Author
CosVerse Analytics Team

## 📄 License
This project is for academic and educational purposes.
