import os
from decouple import config
from datetime import date

def set_environment_variables(project_name: str = "") -> None:
    if not project_name:
        project_name = f"Test_{date.today()}"

    os.environ["ANTHROPIC_API_KEY"] = str(config("api_key",
                                                 default="api_key"))
    os.environ["OPENAI_API_KEY"] = str(config("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",
                                              default="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"))
    os.environ["LANGCHAIN_API_KEY"] = str(config("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",
                                                 default="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"))
    os.environ["LANGCHAIN_PROJECT"] = project_name
    os.environ['TAVILY_API_KEY'] = str(
        config("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", default="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"))


    print("API KEYS LOAED AND TRACING SET WITH PROJECT NAME", project_name)
