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
| Visualization | Plotly, Seaborn, Matplotlib |
| ML & Analytics | Scikit-learn, MLxtend, SciPy, Statsmodels |
| Data Processing | Pandas, NumPy |

## 📊 Dashboard Tabs

### Tab 1: Exploratory Data Analysis (EDA)
- Age, Gender, City distribution
- Fandom category popularity
- Cosplay participation rate & spending analysis
- Challenges faced & preferred features
- Correlation heatmap
- Income vs Spending & Participation vs App Interest relationships
- Additional visualizations: NPS distribution, Discovery channels, Subscription interest

### Tab 2: Classification – Predict Platform Adoption
- **Target Variables**: `App_Usage_Intention` and `Interest_in_Rental`
- **Models**: Random Forest, Logistic Regression, Gradient Boosting
- **Outputs**: Confusion matrix, classification report, feature importance chart

### Tab 3: Clustering – Customer Personas
- **Algorithm**: K-Means Clustering
- **Analysis**: Elbow method, Silhouette scores, 3D cluster visualization
- **Output**: Customer persona profiles (Hardcore Cosplayers, Casual Fans, Event Visitors)

### Tab 4: Association Rule Mining
- **Algorithm**: Apriori
- **Analysis**: Challenge → Feature relationships
- **Metrics**: Support, Confidence, Lift
- **Output**: Rule table and network visualization

### Tab 5: Regression – Demand Forecasting
- **Models**: Linear Regression, Ridge Regression, Lasso Regression
- **Targets**: Monthly cosplay spending, rental willingness, costume price
- **Outputs**: R² scores, MAE comparison, actual vs predicted plots, residual analysis

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
