import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# SALARY DATA (2024 Benchmarks)
# --------------------------
SALARY_DATA = {
    "USA": {
        "Data Scientist": {"entry": 95000, "avg": 135000, "senior": 190000, "currency": "USD"},
        "AI Engineer": {"entry": 105000, "avg": 150000, "senior": 210000, "currency": "USD"},
        "ML Engineer": {"entry": 110000, "avg": 155000, "senior": 200000, "currency": "USD"}
    },
    "UK": {
        "Data Scientist": {"entry": 45000, "avg": 70000, "senior": 100000, "currency": "GBP"},
        "AI Engineer": {"entry": 50000, "avg": 80000, "senior": 110000, "currency": "GBP"},
        "ML Engineer": {"entry": 55000, "avg": 85000, "senior": 115000, "currency": "GBP"}
    },
    "India": {
        "Data Scientist": {"entry": 900000, "avg": 1500000, "senior": 2500000, "currency": "INR"},
        "AI Engineer": {"entry": 1000000, "avg": 1800000, "senior": 3000000, "currency": "INR"},
        "ML Engineer": {"entry": 950000, "avg": 1600000, "senior": 2800000, "currency": "INR"}
    },
    "Germany": {
        "Data Scientist": {"entry": 55000, "avg": 75000, "senior": 100000, "currency": "EUR"},
        "AI Engineer": {"entry": 60000, "avg": 85000, "senior": 110000, "currency": "EUR"},
        "ML Engineer": {"entry": 58000, "avg": 80000, "senior": 105000, "currency": "EUR"}
    }
}

# --------------------------
# SALARY VISUALIZATION
# --------------------------
def show_salary_insights(country, role):
    try:
        # Get data with fallbacks
        country_data = SALARY_DATA.get(country, SALARY_DATA["USA"])
        role_data = country_data.get(role, country_data["Data Scientist"])
        
        # Create equal-length arrays
        levels = ["Entry", "Average", "Senior"]
        salaries = [role_data["entry"], role_data["avg"], role_data["senior"]]
        currencies = [role_data["currency"]] * 3  # Same currency for all levels
        
        df = pd.DataFrame({
            "Level": levels,
            "Salary": salaries,
            "Currency": currencies
        })
        
        # Create visualization
        fig = px.bar(df,
                    x="Level",
                    y="Salary",
                    color="Level",
                    title=f"{role} Salaries in {country} (2024)",
                    text="Salary")
        
        # Format currency symbols
        currency_symbol = {
            "USD": "$",
            "GBP": "£",
            "INR": "₹",
            "EUR": "€"
        }.get(role_data["currency"], "")
        
        fig.update_layout(
            yaxis_tickprefix=currency_symbol,
            uniformtext_minsize=8
        )
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Couldn't display salary data: {str(e)}")

# --------------------------
# MAIN APP
# --------------------------
def main():
    st.title("🌍 AI Salary Benchmark Tool")
    
    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("Country", list(SALARY_DATA.keys()), index=0)
    with col2:
        role = st.selectbox("Role", ["Data Scientist", "AI Engineer", "ML Engineer"], index=0)
    
    show_salary_insights(country, role)

if __name__ == "__main__":
    main()
