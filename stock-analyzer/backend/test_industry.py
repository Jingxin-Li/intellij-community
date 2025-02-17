import akshare as ak
import pandas as pd

def test_industry_data():
    """Test industry data retrieval capabilities"""
    print("Testing industry data retrieval...")
    
    # Get industry board data
    print("\n1. Industry board names:")
    industry_names = ak.stock_board_industry_name_em()
    print(industry_names.head())
    
    # Get industry details
    print("\n2. Industry board details:")
    industry_detail = ak.stock_board_industry_summary_em()
    print(industry_detail.head())
    
    # Get concept board data
    print("\n3. Concept board data:")
    concept_boards = ak.stock_board_concept_name_em()
    print(concept_boards.head())
    
    # Search for specific themes
    themes = ["人工智能", "机器人", "新能源车"]
    print("\n4. Searching for specific themes:")
    for theme in themes:
        matches = concept_boards[concept_boards["板块名称"].str.contains(theme, na=False)]
        if not matches.empty:
            print(f"\n{theme} related boards:")
            print(matches)

if __name__ == "__main__":
    test_industry_data()
