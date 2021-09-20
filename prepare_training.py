"""
Usage:
    python prepare_training_data.py
    output <output-file.csv>

"""

import sys
import conf as c
from utils import (
    collect_data,
    merge_data,
    cleaning_data
)


def main():
    
    #Collect data
    data_transac,data_geo= collect_data()
    
    #Merge data
    data_to_clean=merge_data(data_transac, data_geo)
    
    #Clean data
    data_cleaned=cleaning_data(data_to_clean)
    
    data_cleaned.to_csv(c.conf['prepared_data_path'])

if __name__ == "__main__":
    main()
    sys.exit()