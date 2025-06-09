#-----------------------------------------------------------------
# Step 0: Import packages and modules
#-----------------------------------------------------------------
import streamlit as st 
import pandas as pd
from pathlib import Path
import asyncio
import os
from agents import Agent, Runner, WebSearchTool, function_tool, ItemHelpers
from openai import OpenAI
from dotenv import load_dotenv
from docx import Document
from docx.shared import Inches
import xlrd

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Well-being economy analysis tool',
    layout="wide",
)
st.header(":green[Well-being economy analysis tool]")

#-----------------------------------------------------------------
# Step 1: Get OpenAI API key
#-----------------------------------------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key= OPENAI_API_KEY)

#-----------------------------------------------------------------
# Step 2: Define tools for agent
#-----------------------------------------------------------------

# Populating variables on "indicators.xls" and "countries_WHO_Euro.csv" files
countries_WHOEURO = pd.read_excel(Path(__file__).parent/'data/countries_WHO_Euro.xls') 
countries_df = pd.DataFrame(countries_WHOEURO)

#country selection
selected_country= st.selectbox(
     ''':green[*For which country would you like to produce a report?**]''', countries_df['Countries.full_name'], index=None)

if ((st.button ("Produce Country profile")) & (selected_country != None)):


#-----------------------------------------------------------------
# Step 3: Define agents
#-----------------------------------------------------------------
    with st.spinner("Generation in progress... Country: "+ selected_country):
        response = client.responses.create (
        model="gpt-4.1-mini",
        input = "You are a senior local politician who has to prepare a 3 years plan about health services to be provided in a country. The country to focus is " + selected_country + "." + selected_country + """ has a number of laws and regulation related to health promotion and health services. Collect them for your reference. 
            Your scope is to create a document with a different vision of health. Health is both a foundation and a goal of well-being economies. Health systems are not only economic sectors in their own right—employing millions and generating social value—but also key enablers of human development, social cohesion, and environmental sustainability. 
            The vision will strengthen national capacities to generate, govern, and use health-related data to inform policies that promote equitable, resilient, and prosperous societies. The vision works on 4 well-being capitals: Human well-being, Social well-being, Planetary well-being, Economic well-being. 
            Potential actions and activities carried by stakeholders to promote well-being are also being mentiones in the WHO 'Well-being economy: a policy toolkit' (2024).
            Collect significant data on """ + selected_country + """ around the 4 well-being capitals and indicators (where possible disaggregated by sex, gender, and age) what are the key points to be considered in a three year health plan through well-being lens? Provide a 5 page long report points for action for each well-being capital with content reference and data sources. Expand points in relation to health laws and policies. Don't include simulated data. 
            Expand key actions for each well-being capital by reasoning the choice with the recommendations. Please include at least one chart for each well-being capital. 
            Do not add introductions or conclusions. No AI disclaimers or pleasantries.""")
    
        st.write (response.output_text)
    
#-----------------------------------------------------------------
# Step 4: Define helper functions
#-----------------------------------------------------------------


#-----------------------------------------------------------------
# Step 5: Saving output to a Word file
#-----------------------------------------------------------------

def save_to_word_file(what, filename):
    document = Document()
    document.add_paragraph(what)
    
    try:
        document.save(filename)
        print(f"Content successfully saved to '{filename}'")
    except Exception as e:
        print(f"Error saving document: {e}")


# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
#    #content = response.output_text
#    save_to_word_file(content, "Moldova.docx")

