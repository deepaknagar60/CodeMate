from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from constants import MODEL_NAME,OPENAI_API_KEY
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from ..utils import prompt
from constants import MODEL_NAME,OPENAI_API_KEY




directory = './uploads/CodeDoc'


qa_prompt = prompt.prompt

def run(file_path,question):
    # loader = DirectoryLoader(directory)
    # documents = loader.load()
    
    with open(file_path, 'r') as f:
        content = f.read()

    # Wrap the content in a Document object
    document = Document(page_content=content, metadata={"source": file_path})
    documents = [document]

    text_splitter = CharacterTextSplitter(
    separator=".",
    chunk_size=4000,
    chunk_overlap=0,
    )
    
    docs = text_splitter.split_documents(documents)
  
    embeddings = OpenAIEmbeddings(
        model=MODEL_NAME,
        openai_api_key= OPENAI_API_KEY
    )
    
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model_name='gpt-3.5-turbo',
            temperature=0.1
        )
        
    chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
            chain_type_kwargs={"prompt": qa_prompt}, 
           
        )
    
    
    result = chain.invoke(question)
    answer = result.get( "result",'') 
    
    return answer
     
     
     
     

  
    




