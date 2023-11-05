import asyncio
from sentence_transformers import SentenceTransformer
from langchain.embeddings import OpenAIEmbeddings
import openai
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
import html2text

from scrape.scrape import ascrape_playwright

# model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = OpenAIEmbeddings()

housing = [
    "https://hsh.sfgov.org/services/how-to-get-services/accessing-temporary-shelter/"
]

health = [
    "https://healthysanfrancisco.org",
    "https://hsfconnect-portal.redmane-cloud.us",
    "https://www.sfhsa.org/services/health/medi-cal/check-your-medi-cal-eligibility",
    "https://www.coveredca.com/support/using-my-plan/parents-covered-ca-kids-cchip/",
]

legal = ["https://docs.google.com/document/d/1tVWqVovjLKhEF0gYZ5KHcUXDr3gx9nxx21EV9fai9-4/edit"]

child = ["https://www.dcyf.org/initiatives", "https://www.dcyf.org/contact"]

food = ["https://www.sfhsa.org/our-services/food/programma-calfresh", "https://www.sfhsa.org/services/food/calfresh/applying-calfresh/checking-your-eligibility"]

misc = ["https://www.projecthomelessconnect.org"]

resource_content = []

store = None

def init_embeddings():
    urls = {}
    urls["housing"] = housing
    # urls["health"] = health
    # urls["legal"] = legal
    # urls["child"] = child
    # urls["food"] = food
    # urls["misc"] = misc

    async def scrape_with_playwright(url: str, key: str):
        html_content = await ascrape_playwright(url)
        text = html2text.html2text(html_content)
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=200, chunk_overlap=30
        )
        texts = text_splitter.split_text(text)
        print("\n KEY=" + key + ", HTML= " + html_content + "\n")
        return texts

    for key in urls:
        for url in urls[key]:
            texts = asyncio.run(scrape_with_playwright(url=url, key=key))
            resource_content.append(texts)
            print(resource_content)

    return texts
    # Load html content into vector database (ChromaDB)
    # store = Chroma.from_texts(resource_content, embeddings, collection_name='public_resources')
    # vectorstore_info = VectorStoreInfo(
    #     name="exec-public_resources",
    #     description="public resources",
    #     vectorstore=store
    # )
    # toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
    # chat_llm=ChatOpenAI(temperature=0.1, verbose=True, model="gpt-4")
    # agent_executor = create_vectorstore_agent(
    #     llm=chat_llm,
    #     toolkit=toolkit,
    #     verbose=True
    # )



def find_match(store, input):
    # input_em = embeddings.embed_query(input)
    result = store.similarity_search(input)
    return result

def query_refiner(conversation, query):
    response = openai.Completion.create(
        # model="text-davinci-003",
        model="gpt-3.5-turbo-instruct",
        prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text']

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):

        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
    return conversation_string
