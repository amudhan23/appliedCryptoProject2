# Applied Crypto Project 2

This project is a **Block Cipher Recommendation System** based on user input and machine learning. It uses various cipher attributes (such as throughput, block size, and security level) to suggest the most appropriate block cipher based on user preferences.

## Features
- User-friendly input prompts for block cipher features.
- Uses a Random Forest Classifier to recommend a cipher.
- Handles class imbalance using **SMOTE**.
- Allows users to choose whether to continue providing input or exit the program.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/amudhan23/appliedCryptoProject2.git
    ```

2. Navigate into the project directory:

    ```bash
    cd appliedCryptoPro2
    ```

3. Install the necessary dependencies using **pip**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To use the Block Cipher Recommendation System:

1. Ensure your dataset (`block_cipher_data.csv`) is in the project directory.
2. Run the Python script to start the recommendation system:

    ```bash
    python decisionTree.py
    ```

3. Follow the prompts to input cipher preferences, and the system will recommend the most suitable block cipher.


## Acknowledgments

- The implementation uses **Random Forest** from `scikit-learn`.
- Papers : https://ieeexplore.ieee.org/document/9924700

