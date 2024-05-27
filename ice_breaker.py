from typing import Tuple
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from third_party.linkedin import scrape_linkedin_profile
from agents.linkedin_lookupagent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary

def ice_break_with(name: str)-> Tuple[Summary, str]:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data= scrape_linkedin_profile(linkedin_profile_url=linkedin_url)
    # linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/diyar-alyasiri/", mock=True)

    summary_template= """
    Given the Linkedin infomration {information} about a person I want you to create:
    1. A Short Summary
    2. Two interesting facts about them
    \n{format_instructions}
    """
   

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template,
                                        partial_variables={"format_instructions": summary_parser.get_format_instructions()})

    llm= ChatOpenAI(temperature=0, model_name="gpt-4o")

    # chain= LLMChain(llm=llm, prompt=summary_prompt_template)

    sequence = summary_prompt_template | llm | summary_parser


    # res=chain.invoke(input={"information":information})

    # print(res)
    
    # try:
    #     result:Summary = sequence.invoke({"information": linkedin_data})
    #     print(result)
    # except Exception as e:
    #     print(f"An error occurred: {e}")

    result:Summary = sequence.invoke({"information": linkedin_data})
    
    return result, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()
    print('Ice Breaker Enter')
    ice_break_with(name="Diyar Alyasiri Linkedin")


   
