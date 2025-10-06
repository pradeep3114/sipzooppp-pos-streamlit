# 🥤 Sipzooppp Point-of-Sale (POS) System

A real-time e-commerce simulator and analytics dashboard built entirely in Python using Streamlit and Pandas.

## 🎯 Project Goal

To build a functional, end-to-end data application that handles real-time data capture, state management, and basic sales analytics. This project showcases proficiency in web application development, data persistence, and data visualization.

## ✨ Key Features

| Feature | Technical Implementation | Demonstrated Skill |
| :--- | :--- | :--- |
| **Custom POS Interface** | Two-column layout with product menu and cart/checkout side-by-side. | Front-end design, Streamlit layout management. |
| **Real-Time Data Logic** | Dynamic pricing and subtotal calculations managed instantly using `st.session_state`. | State management, Python business logic. |
| **Data Persistence** | Order history (including customer details) is saved to a local CSV file, demonstrating database simulation. | Data I/O, file handling, `pandas`. |
| **Sales Analytics Dashboard** | Dedicated tab featuring Total Revenue and a "Bestselling Products" chart (`plotly`) calculated from the historical data. | Data analysis, `pandas` manipulation, data visualization. |
| **Input Validation** | Checks for non-empty customer names and 10-digit mobile numbers before allowing checkout. | User experience (UX), input validation. |

## 🛠️ Technology Stack

* **Primary Language:** Python
* **Web Framework:** Streamlit (Frontend/Web App)
* **Data Handling:** Pandas (DataFrames, persistence)
* **Visualization:** Plotly (Interactive charts)

## 🚀 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [YOUR_REPO_LINK]
    cd sipzooppp-pos-streamlit
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application:**
    ```bash
    streamlit run lemonade_app.py
    ```

---
**Author:** Pradeep Sehrawat
