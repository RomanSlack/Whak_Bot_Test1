from langchain.tools import tool
import subprocess
from pydantic import BaseModel, Field
import numexpr as ne

class Calculator(BaseModel):
    expression: str = Field(
        description="Math equation to be solved. It requires numexpr syntax"
    )


@tool("calculator", args_schema=Calculator)
def calculator(expression: str) -> str:
    """Use this tool for math operations. It requires numexpr syntax. Use it when you need to do math operations, for complex math use this to calculate for each of the steps. Be sure syntax is correct."""
    print(f'SOLVING EXPRESSION: {expression}')

    def _run(self, expression: str):
        try:
            print("calc works")
            return ne.evaluate(expression).item()
        except Exception:
            return "This is not a numexpr valid syntax. Try a different syntax."

    def _arun(self, radius: int):
        raise NotImplementedError("This tool does not support async")


