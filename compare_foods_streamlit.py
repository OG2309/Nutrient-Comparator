import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

API_KEY = "YOUR KEY"
st.set_page_config(page_title="Food Nutrient Comparator", layout="wide")

# Dark mode visuals
plt.style.use('dark_background')
sns.set_theme(style="darkgrid", palette="colorblind")

def get_food_nutrients(food_name):
    search_url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={API_KEY}&query={food_name}&pageSize=1"
    res = requests.get(search_url).json()
    if 'foods' not in res or not res['foods']:
        return None

    fdc_id = res['foods'][0]['fdcId']
    desc = res['foods'][0]['description']
    detail_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}?api_key={API_KEY}"
    food_data = requests.get(detail_url).json()

    nutrients = {
        'Description': desc,
        'Carbohydrates (g)': None,
        'Proteins (g)': None,
        'Fats (g)': None
    }

    for n in food_data['foodNutrients']:
        name = n.get('nutrient', {}).get('name', '')
        amount = n.get('amount', 0)
        if 'Carbohydrate' in name:
            nutrients['Carbohydrates (g)'] = amount
        elif 'Protein' in name:
            nutrients['Proteins (g)'] = amount
        elif 'Total lipid' in name:
            nutrients['Fats (g)'] = amount

    return nutrients

def make_suggestion(n1, n2):
    score1 = (n1['Proteins (g)'] or 0) - (n1['Fats (g)'] or 0)*0.5 + (n1['Carbohydrates (g)'] or 0)*0.2
    score2 = (n2['Proteins (g)'] or 0) - (n2['Fats (g)'] or 0)*0.5 + (n2['Carbohydrates (g)'] or 0)*0.2
    return n1['Description'] if score1 > score2 else n2['Description'] if score2 > score1 else "Both are similar"

st.title("🍽️ Food Nutrient Comparator (Dark Mode)")
st.markdown("Compare any two food items by carbs, proteins, and fats in real time per 100g serving.")

with st.form("food_form"):
    col1, col2 = st.columns(2)
    with col1:
        food1 = st.text_input("Enter First Food", value="Almond Butter")
    with col2:
        food2 = st.text_input("Enter Second Food", value="Peanut Butter")
    submitted = st.form_submit_button("Compare")

if submitted:
    n1 = get_food_nutrients(food1)
    n2 = get_food_nutrients(food2)

    if not n1 or not n2:
        st.error("One or both foods not found. Try simpler or different names.")
    else:
        df = pd.DataFrame({
            'Nutrient': ['Carbohydrates (g)', 'Proteins (g)', 'Fats (g)'],
            n1['Description']: [n1['Carbohydrates (g)'], n1['Proteins (g)'], n1['Fats (g)']],
            n2['Description']: [n2['Carbohydrates (g)'], n2['Proteins (g)'], n2['Fats (g)']],
        })

        df_melted = pd.melt(df, id_vars='Nutrient', var_name='Product', value_name='Amount')

        st.subheader("📊 Nutrient Comparison")
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.barplot(data=df_melted, y='Nutrient', x='Amount', hue='Product', ax=ax)
        ax.set_xlabel("Amount per 100g")
        ax.set_ylabel("Nutrient")
        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f', color='white')
        st.pyplot(fig)

        # 🥧 Pie Charts with improved visuals
        st.subheader("🥧 Macronutrient Distribution")
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        labels = ['Carbohydrates (g)', 'Proteins (g)', 'Fats (g)']
        colors = sns.color_palette("pastel")

        values1 = [n1[l] or 0 for l in labels]
        values2 = [n2[l] or 0 for l in labels]

        wedges1, texts1, autotexts1 = axes[0].pie(
            values1, labels=labels, autopct='%1.1f%%', startangle=140,
            colors=colors, textprops={'color': 'white'}, wedgeprops=dict(edgecolor='black')
        )
        axes[0].set_title(n1['Description'], color='white')

        wedges2, texts2, autotexts2 = axes[1].pie(
            values2, labels=labels, autopct='%1.1f%%', startangle=140,
            colors=colors, textprops={'color': 'white'}, wedgeprops=dict(edgecolor='black')
        )
        axes[1].set_title(n2['Description'], color='white')

        fig.patch.set_facecolor('#0e1117')
        st.pyplot(fig)

        st.subheader("🧠 Summary")
        for nutrient in df['Nutrient']:
            v1 = df[n1['Description']][df['Nutrient'] == nutrient].values[0] or 0
            v2 = df[n2['Description']][df['Nutrient'] == nutrient].values[0] or 0
            if v1 > v2:
                st.markdown(f"- **{nutrient}**: {n1['Description']} has **{v1 - v2:.1f} more**")
            elif v2 > v1:
                st.markdown(f"- **{nutrient}**: {n2['Description']} has **{v2 - v1:.1f} more**")
            else:
                st.markdown(f"- **{nutrient}**: Equal in both")

        # 🏆 Healthier Choice Box with Off-White Background
        st.markdown("### 🏆 Healthier Choice")
        better = make_suggestion(n1, n2)
        st.markdown(
            f"<div style='border: 3px solid green; padding: 20px; border-radius: 10px; "
            f"background-color: #fdfaf4; font-size: 24px; color: black; text-align: center;'>"
            f"✅ <strong>{better}</strong> may be the healthier choice based on its macronutrient profile."
            f"</div>",
            unsafe_allow_html=True
        )
