

from src.vector_store import VectorStoreBuilder
from config.config import GROQ_API_KEY, MODEL_NAME

from utils.logger import get_logger
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_groq import ChatGroq 
from src.prompt_template import get_anime_prompt 


logger = get_logger(__name__)


    

logger.info("Initiating recommender pipeline")

vector_builder = VectorStoreBuilder(csv_path="", persis_dir='chroma_db')

retriever = vector_builder.load_vector_store().as_retriever()

    
llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME, temperature = 0.3)
prompt = get_anime_prompt()

print(prompt)

# self.qa_chain = RetrievalQA.from_chain_type(
#     llm = self.llm,
#     chain_type = "stuff",
#     retriever = retriever,
#     return_source_documents = True,
#     chain_type_kwargs = {"prompt": self.prompt}
# )
combine_docs_chain = create_stuff_documents_chain(
llm=llm,
prompt=prompt
)
qa_chain = create_retrieval_chain(
retriever=retriever,
combine_docs_chain=combine_docs_chain)


result = qa_chain.invoke({'input': 'school kind of anime'})

print(result)
logger.info(result)



