import re
from itertools import combinations
def main():
   # Reading letter values from the values.txt file
    with open('values.txt', 'r') as file:
        values_content = file.readlines()
    letter_values = {line.split()[0]: int(line.split()[1]) for line in values_content}

    # Processing names and writing the results to the output file
    input_file_path = 'file.txt'
    name_abbreviations = process_names_corrected(input_file_path, letter_values)
    output_file_path = 'output_abbrevs.txt'
    write_results_to_file(name_abbreviations, output_file_path)
# Function to calculate the score of a letter
def calculate_score(word, idx, letter_values):
    if idx == 0:
        return 0
    elif idx == len(word) - 1 and word[idx] != 'E':
        return 5
    elif idx == len(word) - 1 and word[idx] == 'E':
        return 20
    else:
        position_value = 1 if idx == 1 else 2 if idx == 2 else 3
        return position_value + letter_values[word[idx]]

# Function to get the abbreviation score
def get_abbreviation_score(name, abbreviation_indices, letter_values):
    score = 0
    word_start_idx = 0
    for word in name.split():
        for idx in abbreviation_indices:
            if word_start_idx <= idx < word_start_idx + len(word):
                score += calculate_score(word, idx - word_start_idx, letter_values)
        word_start_idx += len(word)
    return score

# Function to get all possible abbreviations for a name
def get_all_abbreviations(name, letter_values):
    name = re.sub(r"[^a-zA-Z\s]", "", name).upper()
    words = name.split()
    concatenated_name = "".join(words)
    abbreviations = combinations(range(1, len(concatenated_name)), 2)
    abbreviations = [(0, *abbr) for abbr in abbreviations]
    abbreviation_scores = {
        ''.join(concatenated_name[i] for i in abbr): get_abbreviation_score(name, abbr, letter_values)
        for abbr in abbreviations
    }
    print (abbreviation_scores)
    return abbreviation_scores

# Function to process names and ensure each name has a valid abbreviation listed
def process_names_corrected(input_file_path, letter_values):
    with open(input_file_path, 'r') as file:
        names = file.read().splitlines()

    # Get all possible abbreviations for each name
    all_name_abbreviations = {
        name: get_all_abbreviations(name, letter_values) for name in names
    }

    # Identify common abbreviations and exclude them
    all_abbreviations = [abbr for abbreviations in all_name_abbreviations.values() for abbr in abbreviations]
    excluded_abbreviations = {abbr for abbr in all_abbreviations if all_abbreviations.count(abbr) > 1}
    print(excluded_abbreviations)
    # Filter out the common abbreviations and get the best ones for each name
    filtered_name_abbreviations = {}
    for name, abbreviations in all_name_abbreviations.items():
        filtered_abbreviations = {abbr: score for abbr, score in abbreviations.items() if abbr not in excluded_abbreviations}
        
        min_score = min(filtered_abbreviations.values(),default=0)
        best_abbreviations = [abbr for abbr, score in filtered_abbreviations.items() if score == min_score]
        filtered_name_abbreviations[name] = (best_abbreviations, min_score)
    print(filtered_name_abbreviations)
    return filtered_name_abbreviations
    
# Function to write the results to the output file
def write_results_to_file(name_abbreviations, output_file_path):
   with open(output_file_path, 'w') as file:
        for name, (abbreviations, min_score) in name_abbreviations.items():
            file.write(name + '\n')
            for abbreviation in abbreviations:
                # Write each abbreviation with its score, followed by a semicolon
                file.write(f'{abbreviation}:{min_score} ')
            file.write('\n')
if __name__ == "__main__":
    main()

