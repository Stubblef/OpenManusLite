import asyncio
from openmanuslite.tools.pyexec import PythonExecute

executor = PythonExecute()

code_snippet = """
print("Hello, World!")
print(2 + 2)
"""

if __name__ == "__main__":
    # Ensure the multiprocessing code is executed within this block
    result = asyncio.run(executor.execute(code_snippet))
    print(result)
