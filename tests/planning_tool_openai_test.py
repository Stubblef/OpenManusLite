import asyncio
import json
from typing import List, Optional
import time

from openmanuslite.llm import LLM
from openmanuslite.schema import Message, ToolChoice
from openmanuslite.tools.planning import PlanningTool
from openmanuslite.logger import logger

async def demonstrate_planning_with_openai():
    # 创建 PlanningTool 和 LLM 实例
    planning_tool = PlanningTool()
    llm = LLM()
    
    # 1. 使用 OpenAI 创建计划
    print("1. 使用 OpenAI 创建计划")
    system_message = Message.system_message(
        "你是一个项目规划助手，需要帮助用户将需求拆分为可执行的步骤。"
        "每个步骤都应该清晰明确，并添加适当的标签来表示步骤类型。"
    )
    
    user_message = Message.user_message(
        "我需要开发一个用户登录系统，包含注册、登录、密码重置等功能。"
    )
    
    # 调用 OpenAI 并使用 PlanningTool
    response = await llm.ask_tool(
        messages=[user_message],
        system_msgs=[system_message],
        tools=[planning_tool.to_param()],
        tool_choice=ToolChoice.AUTO,
    )
    
    print("=====>>>>response:",response)
    # 处理 OpenAI 的响应
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call.function.name == "planning":
                # 解析参数
                args = json.loads(tool_call.function.arguments)
                args["plan_id"] = "login_system_plan"  # 在args中添加一个字段 plan_id
                
                # 执行规划工具
                result = await planning_tool.execute(**args)
                print(result.output)
                print("\n" + "="*50 + "\n")

    # 2. 使用 OpenAI 更新特定步骤状态
    print("2. 使用 OpenAI 更新步骤状态")
    user_message = Message.user_message(
        "我已经完成了需求分析工作，分析结果表明系统需要支持多种登录方式。"
    )
    
    response = await llm.ask_tool(
        messages=[user_message],
        system_msgs=[system_message],
        tools=[planning_tool.to_param()],
        tool_choice=ToolChoice.AUTO,
    )
    
    # 获取全部
    print("all plannings1",planning_tool._list_plans())

    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call.function.name == "planning":
                args = json.loads(tool_call.function.arguments)
                args["plan_id"] = "login_system_plan2"
                result = await planning_tool.execute(**args)
                logger.debug("**********",result.output)
                logger.debug("\n" + "="*50 + "\n")

    # 3. 使用 OpenAI 请求计划状态并获取建议
    print("3. 获取 OpenAI 对计划的分析和建议")
    user_message = Message.user_message(
        "请查看当前计划的进度，并给出下一步建议。"
    )
    
    
    
    # 首先获取当前计划状态
    plan_status = await planning_tool.execute(
        command="get",
        plan_id="login_system_plan"
    )
    
    # 将计划状态添加到用户消息中
    user_message = Message.user_message(
        f"这是当前的计划状态：\n\n{plan_status.output}\n\n"
        "请分析当前进度并给出下一步行动的建议。"
    )
    print("all plannings3",planning_tool._list_plans())
    # 获取 OpenAI 的分析和建议
    response = await llm.ask(
        messages=[user_message],
        system_msgs=[system_message]
    )
    
    print("OpenAI 的分析和建议：")
    print(response)

async def main():
    # try:
    await demonstrate_planning_with_openai()
    # except Exception as e:
    #     print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
