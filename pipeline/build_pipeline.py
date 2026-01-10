from src.data_loader import AnimeDataLoader 
from src.vector_store import VectorStoreBuilder 
from dotenv import load_dotenv 
from utils.logger import get_logger 
from utils.custom_exception import CustomException

load_dotenv()

logger = get_logger(__name__)


def main():

    try:
        logger.info("Starting to build the pipeline..")

        loader = AnimeDataLoader("data/anime_with_synopsis.csv", "data/anime_updated.csv")
        processed_csv = loader.load_and_process()
        
        logger.info("data loaded and processed..")

        vector_builder = VectorStoreBuilder(processed_csv)

        vector_builder.build_and_save_vectorstore()

        logger.info("vector store built successfully..")

        logger.info("Pipeline built successfully..")

    except Exception as e:
        logger.error(f"Error occured at builder pipeline {str(e)}")
        raise CustomException(f"Error occured in builder pipeline ", e) 
    


if __name__ == "__main__":
    main()