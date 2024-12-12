import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def consolidate_docs(base_dir: str = 'knowledge-base') -> None:
    """Consolidate documentation into separate files"""
    try:
        # Consolidate ApeWorX docs
        ape_content = []
        ape_base = Path(base_dir) / 'apeworx'
        
        # Main ApeWorX docs
        if (ape_base).exists():
            for file in ape_base.glob('*.txt'):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        ape_content.append(f"### {file.name}\n{f.read()}\n")
                except Exception as e:
                    logger.error(f"Error reading {file}: {e}")

        # Subdirectories
        for subdir in ['commands', 'methoddocs', 'userguides']:
            subdir_path = ape_base / subdir
            if subdir_path.exists():
                ape_content.append(f"\n## {subdir.upper()}\n")
                for file in subdir_path.rglob('*.txt'):
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            ape_content.append(f"### {file.name}\n{f.read()}\n")
                    except Exception as e:
                        logger.error(f"Error reading {file}: {e}")

        # Write consolidated ApeWorX docs
        with open('ape_docs.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(ape_content))
        logger.info("ApeWorX documentation consolidated successfully")

        # Consolidate Vyper docs
        vyper_content = []
        vyper_base = Path(base_dir) / 'vyper'
        
        if vyper_base.exists():
            for file in vyper_base.rglob('*.txt'):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        vyper_content.append(f"### {file.name}\n{f.read()}\n")
                except Exception as e:
                    logger.error(f"Error reading {file}: {e}")

        # Write consolidated Vyper docs
        with open('vyper_docs.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(vyper_content))
        logger.info("Vyper documentation consolidated successfully")

    except Exception as e:
        logger.error(f"Error consolidating documentation: {e}")
        raise

if __name__ == '__main__':
    consolidate_docs()