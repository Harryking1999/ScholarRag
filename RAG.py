from langchain_community.document_loaders import TextLoader
from langchain_community import embeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
import os


model_local = ChatOllama(model="qwen:7b")

# 1. 读取文件并分词
documents = TextLoader("data/corpus.txt",encoding="utf-8").load()
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=100, chunk_overlap=0)
doc_splits = text_splitter.split_documents(documents)

# 2. 嵌入并存储
# embeddings = OllamaEmbeddings(model='nomic-embed-text')
embeddings = OpenAIEmbeddings() # Need to configure OPENAI_API_KEY in system variable
vectorstore = DocArrayInMemorySearch.from_documents(doc_splits, embeddings)
retriever = vectorstore.as_retriever()

# 3. 向模型提问
template = """基于以下上下文回答问题：
{context}
问题是: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model_local
    | StrOutputParser()
)
query = "身长七尺，细眼长髯的是谁？"

# docs = vectorstore.similarity_search(query)
# print(docs)

print(chain.invoke(query))


# >>> nomic-embed-text - 根据描述，身长七尺，细眼长髯的人物是曹操（玄德）。

# >>> OpenAI Embedding - 符合身长七尺，细眼长髯描述的的人物是关羽。