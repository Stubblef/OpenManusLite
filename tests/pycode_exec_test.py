import asyncio
from openmanuslite.tools.pyexec import PythonExecute

executor = PythonExecute()

code_snippet = """
print("Hello, World!")
print(2 + 2)
"""

result = asyncio.run(executor.execute(code_snippet))
print(result)
