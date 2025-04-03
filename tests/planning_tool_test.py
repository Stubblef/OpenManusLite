import asyncio
from openmanuslite.tools.planning import PlanningTool

async def demonstrate_planning_tool():
    # 创建 PlanningTool 实例
    planning_tool = PlanningTool()
    
    # 1. 创建一个新计划
    print("1. 创建一个新计划")
    result = await planning_tool.execute(
        command="create",
        plan_id="plan_001",
        title="开发一个新的网站功能",
        steps=[
            "[ANALYSIS] 分析需求和技术可行性",
            "[DESIGN] 设计系统架构和数据模型",
            "[CODE] 实现核心功能",
            "[TEST] 编写和执行测试用例",
            "[DEPLOY] 部署到测试环境"
        ]
    )
    print(result.output)
    print("\n" + "="*50 + "\n")

    # 2. 获取计划详情
    print("2. 查看计划详情")
    result = await planning_tool.execute(
        command="get",
        plan_id="plan_001"
    )
    print(result.output)
    print("\n" + "="*50 + "\n")

    # 3. 标记第一步为进行中
    print("3. 标记第一步为进行中")
    result = await planning_tool.execute(
        command="mark_step",
        plan_id="plan_001",
        step_index=0,
        step_status="in_progress",
        step_notes="已开始分析用户需求"
    )
    print(result.output)
    print("\n" + "="*50 + "\n")

    # 4. 完成第一步
    print("4. 完成第一步并添加备注")
    result = await planning_tool.execute(
        command="mark_step",
        plan_id="plan_001",
        step_index=0,
        step_status="completed",
        step_notes="需求分析完成，技术方案可行"
    )
    print(result.output)
    print("\n" + "="*50 + "\n")

    # 5. 开始第二步
    print("5. 开始第二步")
    result = await planning_tool.execute(
        command="mark_step",
        plan_id="plan_001",
        step_index=1,
        step_status="in_progress"
    )
    print(result.output)
    print("\n" + "="*50 + "\n")

    # 6. 列出所有计划
    print("6. 列出所有计划")
    result = await planning_tool.execute(command="list")
    print(result.output)

# 运行示例
if __name__ == "__main__":
    asyncio.run(demonstrate_planning_tool())
