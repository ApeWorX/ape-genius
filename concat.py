import os
from pathlib import Path
import mimetypes

def is_text_file(file_path):
    """Check if a file is likely to be a text file based on its mimetype and extension."""
    mime_type, _ = mimetypes.guess_type(file_path)
    text_extensions = {'.txt', '.md', '.py', '.js', '.sol', '.yml', '.yaml', '.json', '.toml', '.ini', '.cfg'}
    
    # Check file extension
    if Path(file_path).suffix.lower() in text_extensions:
        return True
    
    # Check mime type
    if mime_type and mime_type.startswith('text/'):
        return True
        
    return False

def is_excluded_file(file_path):
    """Check if the file should be excluded based on patterns."""
    excluded_patterns = {
        '.lock',
        '.pyc',
        '__pycache__',
        '.git',
        '.env',
        '.venv',
        'node_modules',
        '.DS_Store'
    }
    
    path_parts = Path(file_path).parts
    return any(pattern in path_parts or file_path.endswith(pattern) for pattern in excluded_patterns)

def concatenate_files(dir_name, output_filename):
    """
    Concatenate all text files in a directory into a single knowledge base file.
    
    Args:
        dir_name (str): Source directory containing the files to concatenate
        output_filename (str): Output file path for the concatenated content
    """
    dir_path = Path(dir_name)
    output_path = Path(output_filename)
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    processed_files = 0
    skipped_files = 0
    
    with open(output_path, 'w', encoding='utf-8') as output_file:
        # Add header to the knowledge base
        output_file.write(f"# Knowledge Base\nGenerated from: {dir_path.absolute()}\n\n")
        
        # Walk through directory
        for file_path in sorted(dir_path.rglob('*')):
            if not file_path.is_file() or is_excluded_file(str(file_path)):
                continue
                
            rel_path = file_path.relative_to(dir_path)
            
            try:
                if not is_text_file(str(file_path)):
                    skipped_files += 1
                    continue
                    
                # Try to read the file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                    # Only write non-empty files
                    if content:
                        output_file.write(f'{"#" * 4} {rel_path}\n\n')
                        output_file.write(f'{content}\n\n')
                        processed_files += 1
                        
            except UnicodeDecodeError:
                print(f"Skipping binary file: {rel_path}")
                skipped_files += 1
            except Exception as e:
                print(f"Error processing {rel_path}: {str(e)}")
                skipped_files += 1
    
    print(f"\nKnowledge Base Generation Complete:")
    print(f"- Processed files: {processed_files}")
    print(f"- Skipped files: {skipped_files}")
    print(f"- Output file: {output_path.absolute()}")

if __name__ == '__main__':
    # Example usage
    concatenate_files('./knowledge-base', 'knowledge-base.txt')