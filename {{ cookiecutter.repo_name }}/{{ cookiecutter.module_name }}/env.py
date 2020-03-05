from pathlib import Path

PACKAGE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = PACKAGE_DIR.parent
DATA_DIR = PROJECT_DIR / "data"

if __name__ == "__main__":
    print(
        f"""
    package dir: {str(PACKAGE_DIR)}
    project dir: {str(PROJECT_DIR)}
    data dir   : {str(DATA_DIR)}
    """
    )
