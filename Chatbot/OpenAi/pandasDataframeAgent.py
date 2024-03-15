import os
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
import matplotlib.pyplot as plt


def process_dataframe_with_natural_language(df: pd.DataFrame, query):
    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo-0125"),
        df,
        verbose=False,
        return_intermediate_steps=True,
        agent_type=AgentType.OPENAI_FUNCTIONS
    )
    return agent.invoke(query + " Make sure the results are expressed in English and return results not code.")

def retrieve_generated_plot():
    try:
        with open('plot.png', 'rb') as file:
            png_data = file.read()
        os.remove('plot.png')
        return png_data
    except FileNotFoundError:
        print("File not found.")
        return None

def visualize_data_with_natural_language(df: pd.DataFrame, query: str):
    # Initialize agent with the DataFrame
    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-0125"),
        df,
        agent_type=AgentType.OPENAI_FUNCTIONS
    )

    # Invoke the agent with the query
    response = agent.invoke(query + " Store the generated plot as plot.png, overwright it if a file already exists.")

    plot_data = retrieve_generated_plot()
    return plot_data

#
#
#
# os.chdir("../..")
#
# dataset = DatasetManager.get_datasets_by_dataset_id("55dda4fb-0fa5-4311-b628-c388a24240d0")
#
# visualize_data_with_natural_language(dataset,
#                                      "plot the evolution of data over the years")

# # Print the textual representation of the plot
# print("Textual representation of the plot:")
# print(plot)
#
# # Inspect the PNG image data
# print("PNG image data:")
# print(plot_image)
#
# # You can also save the PNG image data to a file for further inspection
# with open("plot_image.png", "wb") as f:
#     f.write(plot_image)
# def visualize_data_with_natural_language(df: pd.DataFrame, query):
#     agent = create_pandas_dataframe_agent(
#         ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-0125"),
#         df,
#         verbose=False,
#         agent_type=AgentType.OPENAI_FUNCTIONS
#     )
#     full_query = f"{query} functions=[setPlotFunctionSpecs], function_call={{'name': 'setPlotParameters'}}"
#     return agent.invoke(full_query)

#
# agent2 = create_pandas_dataframe_agent(
#     ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-0125"),
#     dataset,
#     # verbose=True,
#     return_intermediate_steps=True,
#     agent_type=AgentType.OPENAI_FUNCTIONS
# )
#
# while True:
#     user_input = input("Enter your query: ")  # Prompt the user for input
#     output = agent2.invoke(user_input)  # Invoke the agent with user input
#     # Extracting relevant information from the output dictionary
#     query = output['input']
#     result = output['output']
#     intermediate_steps = output['intermediate_steps']
#
#     # Printing the query
#     print("Query: ", query)
#
#     # Printing intermediate steps
#     print("\nIntermediate Steps:")
#     for step in intermediate_steps:
#         print(step)
#
#     # Printing the result
#     print("\nResult:")
#     print(result)
