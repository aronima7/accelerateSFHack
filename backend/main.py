import asyncio
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain

from scrape.scrape import ascrape_playwright

# for local env set key as export OPENAI_API_KEY=<YOUR KEY>

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

resource_content = {}

def init():
    f = open("html_content.txt", "w")
    urls = {}
    urls["housing"] = housing
    urls["health"] = health
    urls["legal"] = legal
    urls["child"] = child
    urls["food"] = food
    urls["misc"] = misc

    resource_content["housing"] = []
    resource_content["health"] = []
    resource_content["legal"] = []
    resource_content["child"] = []
    resource_content["food"] = []
    resource_content["misc"] = []

    async def scrape_with_playwright(url: str, key: str):
        html_content = await ascrape_playwright(url)
        resource_content[key].append(html_content)
        f.write("\n KEY=" + key + ", URL=" + url + ", HTML= " + html_content + "\n")
        print("\n KEY=" + key + ", HTML= " + html_content + "\n")

    for key in urls:
        for url in urls[key]:
            asyncio.run(scrape_with_playwright(url=url, key=key))

    f.close()

init()

if __name__ == "__main__":

    chat_llm=ChatOpenAI(temperature=0.1, verbose=True, model="gpt-4")
    prompt_template = PromptTemplate.from_template(
        """You are a knowledgable public official, here to assist everyone with questions related to housing, food, mental health resources provided by the city of San Francisco. 
        Use the following knowledge material to help answer the question.  
        Useful resources: {material}
    
        Question: {ques}
        """
    )
    chain = LLMChain(llm=chat_llm, prompt=prompt_template)

    st.title('🌉 :red[AskSF]')

    tab1, tab2, tab3, tab4 = st.tabs(["Housing Resources", "Food Resources", "Mental Health Resources", "Small Business Resources"])

    with tab1:
        html_content = resource_content["housing"]
        st.subheader("Hi, thank you for reaching out. How can I help today? ")

        ques = st.text_input('Please ask your question here.')

        if ques:
            # prompt_template.format(material=html_content, ques=ques)
            response = chain.run({"material":html_content, "ques":ques})
            st.text_area(label ="response",value=response, height =300)

    with tab2:
        st.subheader("Hi, thank you for reaching out. How can I help today? ")

    with tab3:
        st.subheader("Hi, thank you for reaching out. How can I help today? ")

    with tab4:
        st.subheader("Hi, thank you for reaching out. How can I help today? ")
