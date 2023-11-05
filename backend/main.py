import asyncio
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain

from scrape.scrape import ascrape_playwright

# for local env set key as export OPENAI_API_KEY=<YOUR KEY>

housing_url = "https://hsh.sfgov.org/services/how-to-get-services/accessing-temporary-shelter/" # make this a list
resource_content = {}

if __name__ == "__main__":

    async def scrape_with_playwright(url: str, **kwargs):
        html_content = await ascrape_playwright(url)
        resource_content["housing"] = html_content
        print("html_content= " + html_content)

    asyncio.run(scrape_with_playwright(url=housing_url))

    chat_llm=ChatOpenAI(temperature=0.1, verbose=True, model="gpt-4")

    prompt_template = PromptTemplate.from_template(
        """You are a knowledgable public official, here to assist everyone with questions related to housing, food, mental health resources provided by the city of San Francisco. 
        Use the following knowledge material to help answer the question.  
        Useful resources: {material}
    
        Question: {ques}
        """
    )

    st.title('🌉 :red[AskSF]')

    tab1, tab2, tab3, tab4 = st.tabs(["Housing Resources", "Food Resources", "Mental Health Resources", "Small Business Resources"])

    with tab1:
        html_content = resource_content["housing"]
        st.subheader("Hi, thank you for reaching out. How can I help today? ")

        ques = st.text_input('Please ask your question here.')

        if ques:
            # prompt_template.format(material=html_content, ques=ques)
            chain = LLMChain(llm=chat_llm, prompt=prompt_template)
            response = chain.run({"material":html_content, "ques":ques})
            st.text_area(label ="response",value=response, height =300)

    with tab2:
        st.subheader("Hi, thank you for reaching out. How can I help today? ")

    with tab3:
        st.subheader("Hi, thank you for reaching out. How can I help today? ")

    with tab4:
        st.subheader("Hi, thank you for reaching out. How can I help today? ")
