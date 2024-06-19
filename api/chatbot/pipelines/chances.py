# TODO: create pipeline for determining chances of getting into a school
from llama_index.core.query_pipeline import (
    QueryPipeline,
    InputComponent,
)
from llama_index.core import PromptTemplate
from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core.llms import LLM

# what are my chances pipeline:
# determine school(s)
# determine student's information relevant to admission
# determine admissions data for each school
# determine weightings for each school
# ask LLM to make decisions

determine_schools_prompt_tmpl = PromptTemplate(
    "Based on this input and chat history, determine which schools the user would like to know their chances of admission at:\n"
    "\n\n"
    "{input}"
    "\n\n"
    "{chat_history}"
)

determine_factors_tmpl = PromptTemplate(
    "Give a breakdown of importance of what academic and nonacademic factors the admissions commitee considers for admission at the following schools:"
    "\n\n"
    "{schools}"
)

determine_test_scores_tmpl = PromptTemplate(
    "Give a breakdown of standardized test scores for admitted applicants at the following schools:"
    "\n\n"
    "{schools}"
)

determine_gpa_tmpl = PromptTemplate(
    "Give a breakdown of GPAs and class rank of admitted applicants at the following schools:"
    "\n\n"
    "{schools}"
)

determine_chances_tmpl = PromptTemplate(
    "Based on what factors the schools deem important, the GPAs and class ranks of the schools,\n"
    "the test scores at the schools, and what the student has shared about themselves in the input\n"
    "and chat history, make your best judgement at whether or not the student has a good chance of admission\n"
    "at these institutions.\n"
    "\n\n"
    "Input:\n"
    "{input}"
    "\n\n"
    "Chat History:\n"
    "{chat_history}"
    "\n\n"
    "Admission Factor Information:\n"
    "{factors}"
    "\n\n"
    "GPA and Class Rank Information:\n"
    "{gpas}"
    "\n\n"
    "Standardized Test Score Information:\n"
    "{test_scores}"
    "\n\n"
)

input_component = InputComponent()


def create_chances_query_chain(llm: LLM, cds_query_engine: BaseQueryEngine):
    chances_query_modules = {
        "input": input_component,
        "determine_schools_prompt": determine_schools_prompt_tmpl,
        "determine_factors_tmpl": determine_factors_tmpl,
        "determine_test_scores_tmpl": determine_test_scores_tmpl,
        "determine_gpa_tmpl": determine_gpa_tmpl,
        "determine_schools": llm,
        "determine_factors": cds_query_engine,
        "determine_test_scores": cds_query_engine,
        "determine_gpa": cds_query_engine,
        "determine_chances_tmpl": determine_chances_tmpl,
        "determine_chances": llm,
    }

    qp = QueryPipeline(verbose=True)

    qp.add_modules(chances_query_modules)
    qp.add_link("input", "determine_schools_prompt", src_key="input", dest_key="input")
    qp.add_link(
        "input",
        "determine_schools_prompt",
        src_key="chat_history",
        dest_key="chat_history",
    )
    qp.add_link("determine_schools_prompt", "determine_schools")
    qp.add_link("determine_schools", "determine_factors_tmpl")
    qp.add_link("determine_schools", "determine_test_scores_tmpl")
    qp.add_link("determine_schools", "determine_gpa_tmpl")
    qp.add_link("determine_factors_tmpl", "determine_factors")
    qp.add_link("determine_test_scores_tmpl", "determine_test_scores")
    qp.add_link("determine_gpa_tmpl", "determine_gpa")
    qp.add_link("input", "determine_chances_tmpl", src_key="input", dest_key="input")
    qp.add_link(
        "input",
        "determine_chances_tmpl",
        src_key="chat_history",
        dest_key="chat_history",
    )
    qp.add_link("determine_factors", "determine_chances_tmpl", dest_key="factors")
    qp.add_link("determine_test_scores", "determine_chances_tmpl", dest_key="gpas")
    qp.add_link("determine_gpa", "determine_chances_tmpl", dest_key="test_scores")
    qp.add_link("determine_chances_tmpl", "determine_chances")

    return qp
    # await chances_query_chain.arun(
    #     input="Are my chances nyu?", chat_history=["I have a 3.75 gpa and a 1490 on my sat"]
    # )
