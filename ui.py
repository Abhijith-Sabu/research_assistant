from datetime import datetime
import streamlit as st
import os
from main import build_prompt,parser
from smolagents.agents import CodeAgent
from smolagents import InferenceClientModel,HfApiModel
from smolagents import DuckDuckGoSearchTool, LiteLLMModel,FinalAnswerTool,WikipediaSearchTool
from pathlib import Path
from datetime import datetime
from tools import save_to_txt
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
import json
import fpdf
import base64
research_text = st.text_area("Enter the topic you want to research",placeholder="hammer head sharks?")
hf_token = st.text_input("Enter your HF access token",type="password")
button_style = """
    <style>
        .download-button {
            background: linear-gradient(135deg, #ff4b2b, #ff416c);
            color: white;
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .download-button:hover {
            background: linear-gradient(135deg, #e33e26, #e0355c);
        }
    </style>
"""

def create_pdf(text):
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=12)
    pdf.multi_cell(0, 10 ,text)
    pdf_output = pdf.output(dest='S').encode('latin-1')
    return pdf_output


if hf_token:
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token
    st.success("HuggingFace token set")


def llm_model(hf_token,user_input):
    # user_input =input("what can we research about?  ")
    full_promt =build_prompt(user_query=user_input,format_instructions=parser.get_format_instructions())
    model = InferenceClientModel(
            max_tokens=2096,
            temperature=0.5,
            model_id='Qwen/Qwen2.5-Coder-32B-Instruct'
            ,# it is possible that this model may be overloaded  Qwen/Qwen2.5-Coder-32B-Instruct
            custom_role_conversions=None,
            api_key=hf_token
            )

    agent = CodeAgent(
        model=model,
        tools=[DuckDuckGoSearchTool(),FinalAnswerTool(),save_to_txt,WikipediaSearchTool()],
    )

    result = agent.run(full_promt)
    # print(f"raw response :{result}")
    try:
        structured_response = parser.parse(json.dumps(result))
        return (structured_response.dict().get(k) for k in ["summary","sources","topic"])
        # return structured_response.dict().get("summary")
        # print(structured_response.dict().get("summary"))
    except Exception as e:
        return f"Parsing failed,{e}"
        # print("Parsing failed",e)

if st.button("Research"):
    
    with st.spinner("Reasearching...."):
        result= llm_model(hf_token,research_text)
        if isinstance(result,str):
            st.error(result)
        else:
            summary , sources ,topic= result
            st.session_state["summary"]=summary
            st.session_state['sources']= sources
            st.session_state["topic"]=topic

if "summary" in st.session_state:


    st.subheader("Here's your result.")
    st.write(st.session_state['summary'])
    if st.button("sources"):
        st.write(st.session_state['sources'])


    pdf_bytes = create_pdf(st.session_state['summary'])
    b64_pdf = base64.b64encode(pdf_bytes).decode()
    href = f'''{button_style} <a href="data:application/octet-stream;base64,{b64_pdf}" 
        download="{st.session_state["topic"]}.pdf" class="download-button">📄 Download Review</a>'''
    st.markdown(href, unsafe_allow_html=True)

