import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from imblearn.over_sampling import SMOTE

# Load and preprocess data
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "block_cipher_data.csv")
data = pd.read_csv(file_path, header=None)
data.columns = ['Block_Cipher', 'Structure', 'Standard', 'Block_Length', 'CPU_Clock_Freq', 'Throughput',
                'Total_Clock_Cycles', 'Util_Memory', 'Security_Level', 'Known_Vulnerabilities']

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
features = ['Structure', 'Block_Size_Category', 'Throughput_Category', 'Security_Level', 'Standard']
X = data[features]
y = data['Block_Cipher']

# Encode categorical variables
le = LabelEncoder()
for feature in X.columns:
    if X[feature].dtype == 'object':
        X[feature] = le.fit_transform(X[feature])

# Handle class imbalance with SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Split the resampled data
X_train_res, X_test_res, y_train_res, y_test_res = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Train the Random Forest model
rf_model_resampled = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model_resampled.fit(X_train_res, y_train_res)

# Evaluate the model
y_pred_res = rf_model_resampled.predict(X_test_res)
accuracy_res = accuracy_score(y_test_res, y_pred_res)
precision_res = precision_score(y_test_res, y_pred_res, average='weighted', zero_division=1)
recall_res = recall_score(y_test_res, y_pred_res, average='weighted', zero_division=1)
f1_res = f1_score(y_test_res, y_pred_res, average='weighted', zero_division=1)

print(f"Accuracy: {accuracy_res:.2f}")
print(f"Precision: {precision_res:.2f}")
print(f"Recall: {recall_res:.2f}")
print(f"F1-score: {f1_res:.2f}")

# Detailed classification report
report = classification_report(y_test_res, y_pred_res, zero_division=1)
print(report)

# Block Cipher Recommendation System
block_size_categories = {
    0: "Very Small (< 64 bits)",
    1: "Small (64 bits)",
    2: "Medium-Small (65-127 bits)",
    3: "Medium (128 bits)",
    4: "Medium-Large (129-255 bits)",
    5: "Large (256 bits)",
    6: "Very Large (> 256 bits)"
}


# Refining recommendation logic with emphasis on standardization
def refine_recommendation(user_input, cipher_data):
    """
    Refines the recommendation logic to prioritize matches for the user's criteria.

    Args:
    user_input: Dict of user preferences (Structure, Block Size, Throughput, Security Level, Standard)
    cipher_data: DataFrame containing block cipher characteristics

    Returns:
    Recommended block cipher based on refined rules
    """
    # Assign weights to criteria for prioritization, emphasizing 'Standard' more
    criteria_weights = {'Structure': 5, 'Block_Size_Category': 3, 'Throughput_Category': 2, 'Security_Level': 1,
                        'Standard': 6}

    def score_cipher(row):
        """
        Scores a cipher based on closeness to user input.
        Higher scores indicate better matches.
        """
        score = 0
        for key, weight in criteria_weights.items():
            if row[key] == user_input[key]:
                score += weight
        return score

    cipher_data['Score'] = cipher_data.apply(score_cipher, axis=1)

    # If the user prefers a standardized cipher, prioritize those
    if user_input['Standard'] == 1:  # User selected "Yes" for Standard
        cipher_data = cipher_data[cipher_data['Standard'] == 1]  # Filter only standard ciphers
        cipher_data['Score'] += 10  # Boost scores for standardized ciphers

    # Check if the filtered data is empty
    if cipher_data.empty:
        print("No ciphers match your preferences. Please adjust your selection.")
        return None

    # If data is not empty, proceed with sorting and recommending
    best_match = cipher_data.sort_values(by='Score', ascending=False).iloc[0]

    return best_match['Block_Cipher']




def predict_block_cipher():
    user_input = {}
    for feature in features:
        if feature == 'Structure':
            print("Choose the structure (or skip if no preference):")
            print("1: Feistel, 2: SPN, 3: Lai-Massey, 4: Hybrid, 5: Any (No preference)")
            while True:
                choice = int(input("Enter the number: "))
                if choice == 5:  # No preference for structure
                    user_input[feature] = -1
                    break
                elif 1 <= choice <= 4:  # Valid choices between 1 and 4
                    user_input[feature] = choice - 1  # Mapping to 0-indexed
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 5.")
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
        elif feature == 'Standard':
            print("Is the block cipher standard?")
            print("1: Yes, 2: No")
            while True:
                choice = int(input("Enter the number: "))
                if choice == 1:  # Yes
                    user_input[feature] = 1
                    break
                elif choice == 2:  # No
                    user_input[feature] = 0
                    break
                else:
                    print("Invalid input. Please enter 1 (Yes) or 2 (No).")

    # Refine the prediction based on the user input
    user_data = pd.DataFrame([user_input])
    prediction = refine_recommendation(user_input, data)  # Use refined recommendation function
    return prediction


print("Block Cipher Recommendation System")
recommended_cipher = predict_block_cipher()
print(f"Recommended Block Cipher: {recommended_cipher}")
