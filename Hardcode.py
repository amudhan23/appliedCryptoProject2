import pandas as pd

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

def recommend_cipher():
    # Load the CSV data
    file_path = 'block_cipher_data.csv'
    data = pd.read_csv(file_path)
    
    data['Throughput'] = pd.to_numeric(data['Throughput'], errors='coerce')
    data['Throughput_Category'] = data['Throughput'].apply(categorize_throughput)
    #print(data)
    # Start with all rows as potential answers
    remaining_choices = data

    # Define the questions and corresponding column names
    questions = {
        "In block ciphers, standard refers to encryption algo that are widely recognized as secure, interoperable, and reliable, having undergone rigorous evaluation. Non-standard algos, while potentially useful, generally lack the same level of scrutiny and global adoption. \nStandard (Yes/No)": "Standard",
        "The structure of a block cipher is a framework that determines how the plaintext input is processed into ciphertext using a secret key. \nStructure (Feistel/SPN/Lai-Massey/Nested SPN/Type3-Feistel/SPN and Feistel)": "Structure",
        "The block size of a block cipher is the fixed length (in bits) of the data blocks it encrypts or decrypts in a single operation. It is a fundamental parameter of a block cipher that influences its security, efficiency, and practical usage. \nBlock Length (64/96/128/64,96,128/4096/)": "Block_Length",
        "The security level of a block cipher is a measure of its resistance to cryptographic attacks, typically expressed in terms of the *computational* effort required to break it. This effort is usually quantified as the number of operations or resources (e.g., time, memory) needed to compromise the cipher's security, such as finding the encryption key or recovering plaintext without knowing the key. \nSecurity Level (High/Medium/Low/-)": "Security_Level",
        "The throughput of a block cipher refers to the rate at which the cipher can encrypt or decrypt data. Throughput is an important metric for evaluating the performance of a block cipher, especially in applications that require fast encryption and decryption of large amounts of data, such as in secure communication or file encryption systems.\n Throughput (Value is smaller than 1 Mbps, 0 \nValue is between 1(included) and 10(excluded) Mbps, 1 \nValue is between 10(included) and 100(excluded) Mbps,2 \nValue is between 100(included) and 500(excluded) Mbps, 3 \nValue is larger than 500 Mpbs, 4)":"Throughput_Category"
    }

    print("Answer the following questions to determine the recommended block cipher:")
    
    # Ask questions and filter choices
    for question, column in questions.items():
        # Display current remaining choices
        if len(remaining_choices) == 1:
            break  # Stop asking questions if only one choice remains

        # Get user input
        answer = input(f"{question}: ").strip()

        # Filter the remaining choices
        remaining_choices = remaining_choices[remaining_choices[column].astype(str) == answer]

        # If no matches are found
        if remaining_choices.empty:
            print("No matching cipher found based on the inputs provided.")
            return

    # Determine the result
    if len(remaining_choices) == 1:
        # One match found
        result = remaining_choices.iloc[0]["Block_Cipher"]
        print(f"The recommended block cipher is: {result}")
    else:
        # Multiple matches remaining
        print("Multiple potential matches found:")
        print(remaining_choices["Block_Cipher"].tolist())

# Run the program
recommend_cipher()
