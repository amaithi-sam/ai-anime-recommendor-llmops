import pandas as pd 

class AnimeDataLoader():

    def __init__(self, original_csv: str, processed_csv : str):
        self.original_csv_path = original_csv 
        self.processed_csv_path = processed_csv 

    def load_and_process(self):
        df = pd.read_csv(self.original_csv_path, encoding = "utf-8", error_bad_lines=False).dropna()
        required_cols = {'Name', 'Genres', 'sypnopsis'}
        missing = required_cols - set(df.columns)

        if missing:
            raise ValueError("Missing column in csv file")
        
        df['combined_info'] = (
            "Title: " + df['Name'] + "Overview: " + df['sypnopsis'] + "Genres: " + df['Genres']
        )


        df[['combined_info']].to_csv(self.processed_csv_path, index=False, encoding = 'utf-8')
        

        