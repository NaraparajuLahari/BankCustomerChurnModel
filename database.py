import sqlite3

DB_NAME = 'customer_churn.db'

def init_db():
    """Initialize the database and create the predictions table if it does not exist."""
    conn = sqlite3.connect(DB_NAME)  
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Geography TEXT,
            Gender TEXT,
            CreditScore INTEGER,
            Age INTEGER,
            Tenure INTEGER,
            Balance REAL,
            NumOfProducts INTEGER,
            HasCrCard INTEGER,
            IsActiveMember INTEGER,
            EstimatedSalary REAL,
            CustomerFeedback INTEGER DEFAULT 0,
            Churn INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_prediction(data, prediction):
    """Save a customer's prediction data into the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO predictions 
        (Geography, Gender, CreditScore, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, CustomerFeedback, Churn)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data["Geography"],
            data["Gender"],
            data["CreditScore"],
            data["Age"],
            data["Tenure"],
            data["Balance"],
            data["NumOfProducts"],
            data["HasCrCard"],
            data["IsActiveMember"],
            data["EstimatedSalary"],
            data.get("CustomerFeedback", 0),  # Default to 0 if missing
            prediction
        ))
        conn.commit()

def get_all_predictions():
    """Retrieve all stored predictions from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM predictions')
        data = cursor.fetchall()
    return data

# Initialize the database when script runs
init_db()
