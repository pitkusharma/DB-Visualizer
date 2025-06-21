# 🧠 DB Visualizer

DB Visualizer harnesses the power of Large Language Models (LLMs) to let users **query and visualize data** from their database using **plain English**.

Users connect their database by providing connection details through the app's UI. Once connected, they can ask **complex queries** in natural language, and the app — powered by LLMs — takes care of query generation and result visualization.

---

## 🚀 Features

- 🌐 Connect to your own SQL database easily
- 💬 Ask questions in plain English
- 🤖 LLM (Gemini) generates the correct SQL queries
- 📊 View graph, plot & tabular data results directly in the app
- 🐞 Debug-friendly with Pycharm compatibility

---

## 🛠️ Tech Stack

- **Python**
- **LangChain**
- **Google Gemini LLM**
- **SQLAlchemy**
- **Streamlit**

---

## 📁 Project Structure

```
DB-Visualizer/
├── src/               # All core source code
├── notebooks/         # Notebook versions of the app for easy testing & prototyping
├── debug.py           # Run Streamlit via PyCharm for easier debugging
├── requirements.txt   # Python package dependencies
└── .env               # Must be created manually for API keys (not included in repo)
```

---

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/pitkusharma/DB-Visualizer.git
cd DB-Visualizer

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required libraries
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

You must create a `.env` file in the project root with your credentials, like:

```
GEMINI_API_KEY=your_gemini_api_key
```

---

## 🚦 Usage

```bash
# Run the Streamlit app
streamlit run src/app.py  # Or whichever your main file is
```

Then open your browser to: [http://localhost:8501](http://localhost:8501)

---

## 🧪 Notebooks

The `notebooks/` directory contains the same code in Jupyter format for easy experimentation and debugging. Ideal for building and iterating before pushing changes to the app.

---

## 🐞 Debugging

You can run `debug.py` directly in PyCharm to test the Streamlit app outside the CLI interface. This enables breakpoints and a smoother dev experience.

---

## 📸 Preview

![image](https://github.com/user-attachments/assets/f9f8cee8-940c-4b27-a589-c6e5e52b9e8b)

Query: 
1) I want you to group countries by the language spoken, 
2) Now I want you to calculate the total number of people in each country that speaks this language, for that you will use population from country and percentage from country language table. sum the values to get total number of people for each language who speaks the language
3) show top 25 result
4) show plot and graph

![image](https://github.com/user-attachments/assets/027a3837-0ef7-40c9-88b1-7818ee68216a)



---

## 🙋‍♂️ Author

- [Arun Sharma](https://github.com/pitkusharma)

---

## 📃 License

This project is open-source and available under the [MIT License](LICENSE).
