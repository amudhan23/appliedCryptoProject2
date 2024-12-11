import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report

# Load and preprocess data
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "block_cipher_data.csv")
data = pd.read_csv(file_path, header=None)
data.columns = ['Block_Cipher', 'Structure', 'Standard', 'Block_Length', 'CPU_Clock_Freq', 'Throughput', 'Total_Clock_Cycles', 'Util_Memory', 'Security_Level', 'Known_Vulnerabilities']

# Feature engineering
def categorize_throughput(value):
    if pd.isna(value):
        return -1
    elif value < 1:
        return 0  # Very Low
    elif 1 <= value < 10:
        return 1  # Low
    elif 10 <= value < 100:
        return 2  # Medium
    elif 100 <= value < 500:
        return 3  # High
    else:
        return 4  # Very High

def categorize_block_size(block_length):
    if pd.isna(block_length):
        return -1
    elif block_length < 64:
        return 0  # Very Small
    elif block_length == 64:
        return 1  # Small
    elif 64 < block_length < 128:
        return 2  # Medium-Small
    elif block_length == 128:
        return 3  # Medium
    elif 128 < block_length < 256:
        return 4  # Medium-Large
    elif block_length == 256:
        return 5  # Large
    else:
        return 6  # Very Large

block_size_categories = {
    0: "Very Small (< 64 bits)",
    1: "Small (64 bits)",
    2: "Medium-Small (65-127 bits)",
    3: "Medium (128 bits)",
    4: "Medium-Large (129-255 bits)",
    5: "Large (256 bits)",
    6: "Very Large (> 256 bits)"
}

data['Throughput'] = pd.to_numeric(data['Throughput'], errors='coerce')
data['Throughput_Category'] = data['Throughput'].apply(categorize_throughput)

data['Block_Length'] = pd.to_numeric(data['Block_Length'], errors='coerce')
data['Block_Size_Category'] = data['Block_Length'].apply(categorize_block_size)

# Prepare features and target
features = ['Structure', 'Block_Size_Category', 'Throughput_Category', 'Security_Level']
X = data[features]
y = data['Block_Cipher']

# Encode categorical variables
le = LabelEncoder()
for feature in X.columns:
    if X[feature].dtype == 'object':
        X[feature] = le.fit_transform(X[feature])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate model
y_pred = rf_model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"Precision: {precision_score(y_test, y_pred, average='weighted', zero_division=1):.2f}")
print(f"Recall: {recall_score(y_test, y_pred, average='weighted', zero_division=1):.2f}")
print(f"F1-score: {f1_score(y_test, y_pred, average='weighted', zero_division=1):.2f}")

report = classification_report(y_test, y_pred, zero_division=1)
print(report)

# Function to get user input and make predictions
def predict_block_cipher():
    user_input = {}
    for feature in features:
        if feature == 'Structure':
            print("Choose the structure:")
            print("1: Feistel, 2: SPN, 3: Lai-Massey, 4: Hybrid")
            choice = int(input("Enter the number: "))
            user_input[feature] = choice - 1
        elif feature == 'Block_Size_Category':
            print("Choose the block size:")
            for key, value in block_size_categories.items():
                print(f"{key + 1}: {value}")
            while True:
                choice = input("Enter the number: ")
                if choice in map(str, range(1, 8)):
                    user_input[feature] = int(choice) - 1
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 7.")
        elif feature == 'Throughput_Category':
            print("Choose the desired throughput range:")
            print("1: Very Low (< 1 Mbps), 2: Low (1 - 10 Mbps), 3: Medium (10 - 100 Mbps)")
            print("4: High (100 - 500 Mbps), 5: Very High (> 500 Mbps)")
            choice = int(input("Enter the number: "))
            user_input[feature] = choice - 1
        elif feature == 'Security_Level':
            print("Choose the security level:")
            print("1: Low, 2: Medium, 3: High")
            choice = int(input("Enter the number: "))
            user_input[feature] = choice - 1

    user_data = pd.DataFrame([user_input])
    prediction = rf_model.predict(user_data)
    return prediction[0]

# Example usage
print("Block Cipher Recommendation System")
recommended_cipher = predict_block_cipher()
print(f"Recommended Block Cipher: {recommended_cipher}")