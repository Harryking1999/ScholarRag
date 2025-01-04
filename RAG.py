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
from langchain.vectorstores import Chroma
from langchain.chains import VectorDBQA
import os

persist_directory = 'embeddings'
model_local = ChatOllama(model="qwen:7b")

# 1. 读取文件并分词
documents = TextLoader("data/corpus.txt",encoding="utf-8").load()
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=100, chunk_overlap=0)
doc_splits = text_splitter.split_documents(documents)

# 2. 获取 Embedding
# embeddings = OllamaEmbeddings(model='nomic-embed-text')
embeddings = OpenAIEmbeddings() # Need to configure OPENAI_API_KEY in system variable

# 2.1 嵌入并存储到 Runtime memory
vectorstore = DocArrayInMemorySearch.from_documents(doc_splits, embeddings)
retriever = vectorstore.as_retriever()

# 3.1 使用 Cached Memory 向模型提问
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

# # docs = vectorstore.similarity_search(query)
# # print(docs)

print(chain.invoke(query))


# 2.2 嵌入并存储到 Disk
# 从文本块生成嵌入，并将嵌入存储在Chroma向量数据库中，同时设置数据库持久化路径。
vectordb = Chroma.from_documents(doc_splits, embeddings, persist_directory=persist_directory)
# 将数据库的当前状态写入磁盘，以便在后续重启时加载和使用。
vectordb.persist()

# 3.2 使用 VectorDB 生成
# 使用本地矢量数据库创建矢量数据库实例
vectordb = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings())

qa = VectorDBQA.from_chain_type(llm=model_local, chain_type="stuff", vectorstore=vectordb)
query = "身长七尺，细眼长髯的是谁？"
result = qa.run(query)

print(result)


# >>> nomic-embed-text - 根据描述，身长七尺，细眼长髯的人物是曹操（玄德）。

# >>> OpenAI Embedding - 符合身长七尺，细眼长髯描述的的人物是关羽。