import os

# Function to concatenate files into a single .txt file
def concatenate_files(dir_name, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for root, dirs, files in os.walk(dir_name):
            for file in files:
                if file.endswith('.lock'): # Ignore large files that adds nothing to overall knowledge
                    continue
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        output_file.write('######## ' + file_path + '\n\n')
                        output_file.write(f.read() + '\n\n')
                except Exception as e:
                    print(f"Skipping non-text file or error reading file: {file_path} - {e}")

# Example Call
concatenate_files('./knowledge-base', 'knowledge-base.txt')
