import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from imblearn.over_sampling import SMOTE

from sklearn.tree import DecisionTreeClassifier

# Load and preprocess data
project_dir = os.getcwd()
file_path = os.path.join(project_dir, "block_cipher_data.csv")
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
features = ['Standard', 'Security_Level', 'Throughput_Category','Structure', 'Block_Size_Category']
X = data[features]
y = data['Block_Cipher']

# Encode categorical variables
le = LabelEncoder()
for feature in X.columns:
    if X[feature].dtype == 'object':
        X.loc[:, feature] = le.fit_transform(X[feature])

# Decision tree test
model = DecisionTreeClassifier()
model.fit(X,y)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=1)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=1)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=1)

#print(X)
#print(y)
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-score: {f1:.2f}")

#report = classification_report(y_test, y_pred, zero_division=1)
#print(classification_report)


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

'''
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
        cipher_data['Score'] += 10  # Boost scores for standardized ciphers

    best_match = cipher_data.sort_values(by='Score', ascending=False).iloc[0]

    return best_match['Block_Cipher']
'''

# new added def
def answer(user_input):
    return model.predict(user_input)

def predict_block_cipher():
    user_input = {}
    for feature in features:
        if feature == 'Standard':
            while True:
                #added for explanation to non-expert user
                print("In block ciphers, standard refers to encryption algo that are widely recognized as secure, interoperable, and reliable, having undergone rigorous evaluation.")
                print("Non-standard algos, while potentially useful, generally lack the same level of scrutiny and global adoption.")
                #print("Is the block cipher standard?")
                print("For the blockcipher you want to apply, which one statisfies your expectation?")
                #print("1: Yes, 2: No")
                print("1: Standard, 2: Non-standard")
                choice = int(input("Enter the number: "))
                if choice == 1:  # If the user chooses '1', set Standard to 1
                    user_input[feature] = 1
                    break
                elif choice == 2:  # If the user chooses '2', set Standard to 0
                    user_input[feature] = 0
                    break
                else:
                    print("Invalid input. Please enter '1' for Yes or '2' for No.")
        elif feature == 'Throughput_Category':
            #added for explanation to non-expert user
            print("The throughput of a block cipher refers to the rate at which the cipher can encrypt or decrypt data. ")
            print("Throughput is an important metric for evaluating the performance of a block cipher, especially in applications that require fast encryption and decryption of large amounts of data, such as in secure communication or file encryption systems.")
            print("Please choose your desired throughput range:")
            print("1: Very Low (< 1 Mbps), 2: Low (1 - 10 Mbps), 3: Medium (10 - 100 Mbps)")
            print("4: High (100 - 500 Mbps), 5: Very High (> 500 Mbps)")
            while True:
                choice = int(input("Enter the number: "))
                if 1 <= choice <= 5:  # Valid choices between 1 and 4
                    user_input[feature] = choice - 1  # Mapping to 0-indexed
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 5.")
        elif feature == 'Security_Level':
            #added for explanation to non-expert user
            print("The security level of a block cipher is a measure of its resistance to cryptographic attacks, typically expressed in terms of the *computational* effort required to break it.")
            print("This effort is usually quantified as the number of operations or resources (e.g., time, memory) needed to compromise the cipher's security, such as finding the encryption key or recovering plaintext without knowing the key.")
            print("Please choose your desired security level:")
            print("1: Low, 2: Medium, 3: High, 4: Unkown")
            while True:
                choice = int(input("Enter the number: "))
                if 1 <= choice <= 3:  # Valid choices between 1 and 4
                    #user_input[feature] = choice - 1  # Mapping to 0-indexed
                    user_input[feature] = choice + 1
                    break
                elif choice == 4:
                    user_input[feature] = -1
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 3.")
        elif feature == 'Structure':
            #added for explanation to non-expert user
            print("The structure of a block cipher is a framework that determines how the plaintext input is processed into ciphertext using a secret key.")
            print("Choose the structure (or skip if no preference):")
            print("1: Feistel, 2: SPN, 3: Lai-Massey, 4: Hybrid, 5: Any (No preference)")
            while True:
                choice = int(input("Enter the number: "))
                if choice == 5:  # No preference for structure
                    user_input[feature] = -1
                    break
                elif 1 <= choice <= 4:  # Valid choices between 1 and 4
                    #user_input[feature] = choice - 1  # Mapping to 0-indexed
                    user_input[feature] = choice
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 5.")
        elif feature == 'Block_Size_Category':
            #added for explanation to non-expert user
            print("The block size of a block cipher is the fixed length (in bits) of the data blocks it encrypts or decrypts in a single operation. It is a fundamental parameter of a block cipher that influences its security, efficiency, and practical usage.")
            print("Please choose your desired block size:")
            #print("Choose the block size:")
            for key, value in block_size_categories.items():
                print(f"{key + 1}: {value}")
            while True:
                choice = input("Enter the number: ")
                if choice in map(str, range(1, 8)):
                    user_input[feature] = int(choice) - 1
                    #user_input[feature] = int(choice)
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 7.")


    # Refine the prediction based on the user input
    user_data = pd.DataFrame([user_input])
    print(user_data)
    #prediction = refine_recommendation(user_input, data)  # Use refined recommendation function
    prediction = answer(user_data)
    return prediction


print("Block Cipher Recommendation System")
while True :
    recommended_cipher = predict_block_cipher()
    print(f"Recommended Block Cipher: {recommended_cipher}")
    print("Do you want to continue : 1.yes 2.no")
    continueChoice = int(input("Enter the number: "))
    if continueChoice==1:
        continue
    else:
        break
    