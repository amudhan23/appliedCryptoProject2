import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import os
import numpy as np

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Construct the full path to the CSV file
file_path = os.path.join(desktop_path, "block_cipher_data.csv")

# Read the CSV file without headers
data = pd.read_csv(file_path, header=None)

def categorize_throughput(value):
    if pd.isna(value):
        return -1  # or any other value to represent missing data
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

throughput_categories = {
    0: "Very Low (< 1 Mbps)",
    1: "Low (1 - 10 Mbps)",
    2: "Medium (10 - 100 Mbps)",
    3: "High (100 - 500 Mbps)",
    4: "Very High (> 500 Mbps)"
}

# Assign column names
data.columns = ['Block_Cipher', 'Structure', 'Standard', 'Block_Length', 'CPU_Clock_Freq', 'Throughput', 'Total_Clock_Cycles', 'Util_Memory', 'Security_Level', 'Known_Vulnerabilities']

print(data.columns)

# Prepare the features and target
features = ['Structure', 'Block_Length', 'Throughput', 'Security_Level']
X = data[features]
y = data['Block_Cipher']

# X['Throughput'] = pd.to_numeric(X['Throughput'], errors='coerce')
X.loc[:, 'Throughput'] = pd.to_numeric(X['Throughput'], errors='coerce')

# Encode categorical variables
le = LabelEncoder()
# Instead of:
# X['Standard'] = (X['Standard'] != 'No').astype(int)

# Use:
# X.loc[:, 'Standard'] = (X['Standard'] != 'No').astype(int)
X = X.apply(lambda col: le.fit_transform(col) if col.dtype == 'object' else col)

# Create and train the decision tree
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X, y)

# Function to get user input and make predictions
def predict_block_cipher():
    user_input = {}
    for feature in features:
        if feature == 'Structure':
            while True:
                print("Choose the structure:")
                print("1: Feistel, 2: SPN, 3: Lai-Massey, 4: Hybrid")
                choice = input("Enter the number: ")
                if choice in ['1', '2', '3', '4']:
                    user_input[feature] = int(choice) - 1
                    break
                else:
                    print("Invalid input. Please enter 1, 2, 3, or 4.")
        # elif feature == 'Standard':
        #     while True:
        #         print("Does the cipher have a standard?")
        #         print("1: Yes")
        #         print("2: No")
        #         choice = input("Enter the number: ")
        #         if choice in ['1', '2']:
        #             user_input[feature] = 1 if choice == '1' else 0
        #             break
        #         else:
        #             print("Invalid input. Please enter 1 or 2.")
        elif feature == 'Block_Length':
            user_input[feature] = int(input("Enter block length in bits: "))
        elif feature == 'Throughput':
            print("Choose the desired throughput range:")
            for key, value in throughput_categories.items():
                print(f"{key + 1}: {value}")
            while True:
                choice = input("Enter the number: ")
                if choice in map(str, range(1, 6)):
                    user_input[feature] = int(choice) - 1
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 5.")
        elif feature == 'Security_Level':
            print("Choose the security level:")
            print("1: Low, 2: Medium, 3: High")
            choice = int(input("Enter the number: "))
            user_input[feature] = choice - 1

    user_data = pd.DataFrame([user_input])
    prediction = clf.predict(user_data)
    return prediction[0]

# Example usage
print("Block Cipher Recommendation System")
recommended_cipher = predict_block_cipher()
print(f"Recommended Block Cipher: {recommended_cipher}")