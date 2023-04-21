# import os

# env_var = "OPENAI_API_KEY"

# if env_var in os.environ:
#     print(os.environ[env_var])
# else:
#     print(f"{env_var} is not defined in the environment")

from langchain.llms import OpenAI
llm = OpenAI(model_name="text-ada-001", n=2, best_of=2)
print( llm("Tell me a joke") )