from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


model_local = ChatOllama(model="qwen:7b")
template = "{topic}"
prompt = ChatPromptTemplate.from_template(template)
chain = model_local | StrOutputParser()
print(chain.invoke("身长七尺，细眼长髯的是谁？"))

# >>> 您描述的特征符合中国古代文学作品《三国演义》中的人物关羽。关羽被塑造成英勇善战、忠贞不渝的武将形象。