from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import PyPDFLoader
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain_openai import ChatOpenAI
#docs = loader.load()
class summarize(BaseModel):
    filename: str = Field(
        description="the file name in 'data' folder that is most appropriate for the task requested (example would be like xyz.pdf, do not include data directory), make sure to check that the user input request file name exists in the data folder, if it does not choose the most similar filename of one that does exist, but do not pass filename if it does not exist in data folder"
    )
@tool("pdf_summary", args_schema=summarize)
def pdf_summary(filename: str) -> str:
    ''' Use this tool to summarize pdf in data folder'''
    loader = PyPDFLoader("tools/data/" + filename, extract_images=True)
    docs = loader.load()
    llm = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo-1106", api_key="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"
                )
    chain = load_summarize_chain(llm, chain_type="stuff" )

    return chain.run(docs)