# Nutrient-Comparator
This is a casual project that compares two foods based on carbs, Protein and Fats
# 🥗 Food Nutrient Comparator (Streamlit App)

Compare the **macronutrient profiles** of two foods in real-time using the USDA FoodData Central API. Get insights into **carbohydrates, proteins, and fats per 100g** and discover which food might be the healthier choice — all through a sleek dark-themed Streamlit interface.

---

## ✨ Features

🔍 **Live USDA API Integration**  
🎨 **Dark Mode Visuals** with vibrant bar and pie charts  
📊 **Side-by-Side Comparison** of Proteins, Fats, and Carbs  
🧠 **Healthier Choice Recommendation** with clean design  
📱 **Mobile-friendly** and intuitive user interface  
✅ No manual data entry — just type in food names!

---

## 🚀 Getting Started

pip install streamlit requests pandas matplotlib seaborn
🔑 Get a USDA API Key
Sign up at: https://fdc.nal.usda.gov/api-key-signup.html

Copy the key

Open compare_foods_app.py and paste it:

python
Copy
Edit
API_KEY = "your key"


🏃 Run the app
bash
Copy
Edit
streamlit run compare_foods_app.py
The app will launch in your browser at http://localhost:8501.



🧪 Example Inputs
Try comparing:
"Almond Butter" vs "Peanut Butter"
"Oats" vs "Cornflakes"
"Chicken Breast" vs "Paneer"



🧠 What You'll See
📊 Bar chart showing amounts of each macronutrient
🥧 Pie charts for nutrient proportions per food
💡 A Healthier Choice suggestion based on balance and totals


```bash
git clone https://github.com/your-username/food-nutrient-comparator.git
cd food-nutrient-comparator
