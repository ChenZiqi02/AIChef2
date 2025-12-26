import json
from typing import Optional
from .models import RecipeStep, RecipeResponse, RecipeListResponse
from core.retriever import retrieve_docs
# ✅ 引入新的优选函数
from core.generator import smart_select_and_comment, generate_rag_answer 
from langchain_openai import ChatOpenAI
from core.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME

class RecipeService:
    def __init__(self):
        # 初始化 LLM 客户端
        self.llm = None
        if LLM_API_KEY:
            self.llm = ChatOpenAI(model=LLM_MODEL_NAME, api_key=LLM_API_KEY, base_url=LLM_BASE_URL, temperature=0.7)

    def get_recipe_response(self, query: str) -> Optional[RecipeResponse]:
        print(f"🔍 [Service] 用户搜索: {query}")
        
        # 1. 【扩大召回】从数据库拿 Top 3，而不是 Top 1
        # 这样即使向量检索把最佳结果排在了第 2 或 第 3，AI 也能把它捞回来
        candidates = retrieve_docs(query, top_k=6)
        
        # 2. 【AI 优选】让大模型来挑，并生成推荐语
        # 返回值: (选中的索引, 推荐语)
        selected_index, ai_message = smart_select_and_comment(query, candidates)
        
        # 确保索引不越界 (防止 AI 瞎返回 "index: 99")
        if selected_index < 0 or selected_index >= len(candidates):
            selected_index = 0
            
        # 3. 锁定最终的最佳菜谱
        best_match = candidates[selected_index]
        print(f"🎯 [Service] AI 选中了第 {selected_index} 项: {best_match['name']}")

        return RecipeResponse(
            recipe_id=str(best_match.get('id', 'unknown')),
            recipe_name=best_match.get('name', '未命名'),
            tags=raw_tags,
            cover_image=best_match.get('image'),
            steps=formatted_steps,
            message=ai_message # 这里是 AI 针对选中菜谱写的推荐语
        )

    def get_recipe_list_response(self, query: str, limit: int = 5) -> Optional[RecipeListResponse]:
        """
        获取多个菜谱推荐列表
        """
        print(f"🔍 [Service] 用户搜索列表: {query}, 数量: {limit}")
        
        # 1. 扩大召回
        candidates = retrieve_docs(query, top_k=limit)
        if not candidates:
            return None
            
        # 2. 格式化所有结果
        formatted_list = []
        seen_names = set() # 用于去重

        for doc in candidates:
            # 去重逻辑: 如果名字已经出现过，跳过
            recipe_name = doc.get('name', '未命名')
            if recipe_name in seen_names:
                continue
            seen_names.add(recipe_name)
            
            # 清洗 Instructions
            raw_instructions = doc.get('instructions', [])
            if isinstance(raw_instructions, str):
                try: raw_instructions = json.loads(raw_instructions)
                except: raw_instructions = []

            # 清洗 Tags
            raw_tags = doc.get('tags', [])
            if isinstance(raw_tags, str):
                try: raw_tags = json.loads(raw_tags)
                except: raw_tags = []

            # 格式化步骤
            formatted_steps = []
            for idx, step in enumerate(raw_instructions):
                # 兼容不同数据源的图片字段
                img_link = step.get('image_url') or step.get('imgLink')
                
                # 简单过滤无效图片链接
                if not img_link or img_link == "null": img_link = None
                
                formatted_steps.append(
                    RecipeStep(
                        step_index=idx + 1,
                        description=step.get('description', ''),
                        image_url=img_link
                    )
                )
            
            # 组装单个 Response
            # ✅ AI 功能模拟：如果没有配置 Key，我们用规则生成一段 "伪AI" 点评
            # 这样用户能感觉到 "AI 辅助" 的存在
            ai_comment = f"基于您的食材，AI 认为这道菜匹配度高达 {int(doc.get('score', 0) * 100)}%。"
            if "辣" in str(raw_tags):
                ai_comment += " 注意：这道菜口味偏辣，可以适当减少辣椒用量。"
            elif "汤" in str(raw_tags):
                ai_comment += " 这是一个很棒的汤品选择，暖胃又健康。"

            formatted_list.append(
                RecipeResponse(
                    recipe_id=str(doc.get('id', 'unknown')),
                    recipe_name=recipe_name,
                    tags=raw_tags,
                    cover_image=doc.get('image'),
                    steps=formatted_steps,
                    message=ai_comment 
                )
            )

        # 3. 【核心新增】生成列表综述 (AI Consultant)
        # 用 LLM 为这一组搜索结果写一段开场白
        list_summary = generate_rag_answer(query, candidates)

        return RecipeListResponse(
            candidates=formatted_list,
            ai_message=list_summary
        )

    def consult_chef(self, query: str, context: str, history: list) -> str:
        """
        AI 顾问交互接口
        """
        # 构建 prompt
        system_prompt = """
        你是一位高端家庭餐厅的主厨顾问。你的任务是根据当前的“搜索结果上下文”和“对话历史”，回答用户的追问。
        
        【要求】:
        1. 语气专业、优雅、幽默（参考之前的设定）。
        2. 如果用户想换口味，请基于列表里的其他菜推荐，或者给出烹饪建议。
        3. 字数控制在 100 字左右。
        """
        
        # 简单拼接历史
        history_str = "\n".join([f"{h['role']}: {h['content']}" for h in history[-4:]])

        user_prompt = f"""
        【当前菜谱列表上下文】：
        {context}

        【对话历史】：
        {history_str}

        【用户新问题】：
        {query}

        请主厨作答：
        """
        
        if not self.llm:
             return "👨‍🍳 抱歉，AI 厨师目前无法连接大脑 (API Key Missing)。"

        try:
            from langchain_core.messages import SystemMessage, HumanMessage
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            return response.content.strip()
        except Exception as e:
            print(f"Chat Error: {e}")
            return "👨‍🍳 抱歉，厨房太忙了，请稍后再试。"


recipe_service = RecipeService()


# import json  # <--- 1. 必须补上这个！
# from typing import Optional
# from .models import RecipeStep, RecipeResponse

# # ✅ 直接引入你在 core 里写好的检索函数
# from core.retriever import retrieve_docs
# from core.generator import generate_rag_answer

# class RecipeService:
#     def get_recipe_response(self, query: str) -> Optional[RecipeResponse]:
#         """
#         业务逻辑：
#         1. 检索 (Retrieve) -> 拿到 raw data
#         2. 生成 (Generate) -> 拿到 AI 推荐语
#         3. 清洗 (Parse) -> 拿到结构化步骤
#         4. 组装返回
#         """
#         print(f"🔍 [Service] 正在为用户搜索: {query}")
        
#         # 1. 检索
#         results = retrieve_docs(query, top_k=1)
        
#         if not results:
#             print("⚠️ [Service] 未找到匹配结果")
#             return None
            
#         best_match = results[0]
        
#         # # =======================================================
#         # # ✅ 2. 数据清洗：从 JSON 字符串还原回 List
#         # # =======================================================
        
#         # # --- 处理 Instructions ---
#         # raw_instructions = best_match.get('instructions', [])
#         # # 如果它是字符串 (因为 Chroma 存成了 string)，我们需要把它转回 list
#         # if isinstance(raw_instructions, str):
#         #     try:
#         #         raw_instructions = json.loads(raw_instructions)
#         #     except json.JSONDecodeError:
#         #         print("❌ 解析 instructions JSON 失败，使用空列表")
#         #         raw_instructions = []

#         # # --- 处理 Tags ---
#         # raw_tags = best_match.get('tags', [])
#         # if isinstance(raw_tags, str):
#         #     try:
#         #         raw_tags = json.loads(raw_tags)
#         #     except json.JSONDecodeError:
#         #         raw_tags = []

#         # # 3. 格式化步骤 (组装 Steps)
#         # formatted_steps = []
#         # for idx, step in enumerate(raw_instructions):
#         #     # 处理图片链接
#         #     img_link = step.get('imgLink')
#         #     if not img_link or img_link == "null":
#         #         img_link = None

#         #     formatted_steps.append(
#         #         RecipeStep(
#         #             step_index=idx + 1,
#         #             description=step.get('description', ''),
#         #             image_url=img_link
#         #         )
#         #     )

#         # # 4. 返回标准结构
#         # return RecipeResponse(
#         #     recipe_id=str(best_match.get('id', 'unknown')),
#         #     recipe_name=best_match.get('name', '未命名菜谱'),
            
#         #     # <--- 2. 这里要用解析好的 raw_tags，而不是原始的 best_match['tags']
#         #     tags=raw_tags, 
            
#         #     cover_image=best_match.get('image'),
#         #     steps=formatted_steps,
#         #     message=f"✨ 为您找到【{best_match.get('name')}】的最佳做法："
#         # )
#         # 2. 【核心新增】调用大模型生成推荐语 (Generator) - 稍微花点时间
#         # 把 query (用户想吃啥) 和 results (库里有啥) 传给 AI
#         # 注意：这会增加 API 的延迟（通常 1-2 秒），取决于模型速度
#         ai_message = generate_rag_answer(query, results)
        
#         # 3. 数据清洗 (保持不变)
#         raw_instructions = best_match.get('instructions', [])
#         if isinstance(raw_instructions, str):
#             try:
#                 raw_instructions = json.loads(raw_instructions)
#             except:
#                 raw_instructions = []

#         raw_tags = best_match.get('tags', [])
#         if isinstance(raw_tags, str):
#             try:
#                 raw_tags = json.loads(raw_tags)
#             except:
#                 raw_tags = []

#         formatted_steps = []
#         for idx, step in enumerate(raw_instructions):
#             img_link = step.get('imgLink')
#             if not img_link or img_link == "null":
#                 img_link = None
#             formatted_steps.append(
#                 RecipeStep(
#                     step_index=idx + 1,
#                     description=step.get('description', ''),
#                     image_url=img_link
#                 )
#             )

#         # 4. 组装返回
#         return RecipeResponse(
#             recipe_id=str(best_match.get('id', 'unknown')),
#             recipe_name=best_match.get('name', '未命名'),
#             tags=raw_tags,
#             cover_image=best_match.get('image'),
#             steps=formatted_steps,
            
#             # ✅ 这里填入 AI 生成的话！
#             message=ai_message
#         )
# # 创建单例实例
# recipe_service = RecipeService()