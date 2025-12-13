from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from core.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME, GEMINI_API_KEY
import re
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# 初始化客户端 (使用 LangChain 统一接口)
llm = None

if GEMINI_API_KEY:
    print(f"✅ 尝试使用 Google Gemini API (model: gemini-2.0-flash)")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.7,
        safety_settings={
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        }
    )
elif LLM_API_KEY:
    print(f"✅ 使用 SiliconFlow API (model: {LLM_MODEL_NAME})")
    llm = ChatOpenAI(
        model=LLM_MODEL_NAME,
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
        temperature=0.4
    )

def safe_invoke(messages):
    """
    统一的 LLM 调用封装 (Strict Single Model: Gemini 2.0 Flash)
    用户指令: 不需要降级保底，只要原来的幽默效果。
    """
    if not llm:
        raise Exception("LLM Client not initialized")

    try:
        # 直接调用首选模型 (允许默认重试)
        return llm.invoke(messages)
    except Exception as e:
        print(f"❌ [SafeInvoke] Model Failed: {e}")
        # 直接抛出错误，不切换模型
        raise e

def smart_select_and_comment(query: str, candidates: list):
    """
    智能优选 Rerank (灵活版)
    不再死板过滤，而是侧重于“推荐 + 建议”
    """
    if not llm:
        return 0, "API Key 未配置，默认推荐："
    
    if not candidates:
        return 0, "没有候选菜谱。"

    # 1. 构建候选列表
    candidates_str = ""
    for i, doc in enumerate(candidates):
        snippet = doc.get('content', '')[:150].replace('\n', ' ')
        candidates_str += (
            f"选项[{i}]: {doc.get('name')}\n"
            f"   - 标签: {doc.get('tags', [])}\n"
            f"   - 简介: {snippet}...\n\n"
        )

    # =====================================================
    # ✅ 优化后的 Prompt：更像一个懂得变通的大厨
    # =====================================================
    system_prompt = """
    你是一位聪明、懂变通的私家大厨。你的任务是从给定的候选菜谱中，为用户推荐**最合适**的一道。

    【推荐逻辑】：
    1. **找最大公约数**：优先选择食材、口味最接近用户需求的菜。
    2. **灵活处理忌口**：
       - 如果用户说“不要辣”，尽量选不辣的。
       - **关键点**：如果候选项全都有辣，**不要拒绝回答！** 请选一个最容易“去辣”的菜（比如把辣椒油换成香油），并在理由里告诉用户怎么调整。
    3. **不仅是选择，更是建议**：推荐理由要告诉用户“为什么选它”或者“怎么做更符合你的要求”。

    【输出格式】：
    请直接返回一行：索引数字 ||| 推荐理由
    （例如：1 ||| 虽然原谱有辣椒，但这道菜只要不放辣椒油，依然非常鲜美，很适合您。）
    """

    user_prompt = f"""
    用户需求：【{query}】

    候选列表：
    {candidates_str}

    请做出你的选择：
    """

    try:
        # LangChain 调用
        messages = [
            ("system", system_prompt),
            ("human", user_prompt),
        ]
        
        response_msg = safe_invoke(messages)
        content = response_msg.content
        
        # --- 增强解析逻辑 ---
        # 1. 如果是列表 (Multipart)，拼接
        if isinstance(content, list):
             content = " ".join([str(c) for c in content])
        
        # 2. 如果是字典 (或类似结构)，尝试提取 text
        if isinstance(content, dict):
            content = content.get('text', str(content))
            
        # 3. 如果是字符串但看起来像字典 (Stringified Dict)
        content = str(content).strip()
        if content.startswith("{") and "text" in content:
            try:
                val = ast.literal_eval(content)
                if isinstance(val, dict) and 'text' in val:
                    content = val['text']
            except:
                pass # 解析失败就保留原样

        content = str(content).strip()

        # print(f"🤖 [Generator] AI 建议: {content}") 

        # --- 解析逻辑 (保持鲁棒性) ---
        if "|||" in content:
            index_part, reason = content.split("|||", 1)
            match = re.search(r'\d+', index_part)
            if match:
                return int(match.group()), reason.strip()
        
        # 兜底：如果 AI 直接说了数字开头
        match = re.search(r'^\d+', content)
        if match:
             return int(match.group()), f"为您推荐【{candidates[int(match.group())]['name']}】"

        # 彻底无法解析
        return 0, f"试试这道【{candidates[0]['name']}】，应该不错！"

    except Exception as e:
        print(f"❌ [Generator] 报错: {e}")
        return 0, "为您推荐以下菜谱："

def generate_rag_answer(query: str, candidates: list) -> str:
    """
    为搜索结果列表生成一段 "厨师顾问" 风格的综述
    """
    if not llm:
        return "🤖 AI 厨师正在休息（未配置 API Key），请直接查看下方菜谱。"
        
    if not candidates:
        return "抱歉，没有找到相关菜谱，我也很难为您提供建议。"

    # 1. 简要构建候选信息
    candidates_summary = ""
    for i, doc in enumerate(candidates[:5]):
        candidates_summary += f"- {doc.get('name')} (标签: {doc.get('tags')})\n"

    system_prompt = """
    你是一位高端家庭餐厅的主厨顾问。
    用户的需求可能只是几个食材名。你的任务是根据搜索到的菜谱列表，给用户一段**专业、优雅且得体**的开场建议。
    
    【推荐逻辑】：
    1.  **语气专业**：礼貌、温和、有质感（例如："为您精选了以下几道佳肴..."）。拒绝调侃或过度热情。
    2.  **总结亮点**：概括菜品特色，体现烹饪的艺术感。
    3.  **给出建议**：简要提及食材搭配或风味特点。
    4.  **幽默与互动（最高优先级）**：
        - **必须检查**：无论是否搜到了菜谱，先检查用户的输入里有没有**奇怪、离谱或调侃**的词（如“屎”、“毒药”、“混凝土”等）。
        - **混合输入处理**：如果用户输入了“巧克力和屎”，虽然有巧克力菜谱，但你**必须**先吐槽“屎”这个离谱的食材，然后再推荐巧克力！
        - **例子**：“巧克力我懂，但‘屎’是什么黑暗料理？😱 为了您的生命安全，我还是只给您推荐正常的【巧克力做】法吧...”
        - **拒绝无视**：绝对不能假装没看见离谱词只回答正常的，那样太呆板了！
    5.  **形式要求**：严禁使用 Emoji 表情符号。字数控制在 100 字以内。
    
    """

    
    user_prompt = f"""
    用户想吃/有的食材：【{query}】
    搜索到的菜谱：
    {candidates_summary}

    请给用户一段简短的高级感推荐语：
    """

    try:
        messages = [
            ("system", system_prompt),
            ("human", user_prompt),
        ]
        
        response = safe_invoke(messages)
        content = response.content
        
         # --- 增强解析逻辑 ---
        if isinstance(content, list):
             content = " ".join([str(c) for c in content])
             
        if isinstance(content, dict):
            content = content.get('text', str(content))

        content = str(content).strip()
        
        # 处理 Stringified Dict (例如 SiliconFlow/DeepSeek 偶尔返回的格式)
        if content.startswith("{") and "text" in content:
            try:
                import ast
                val = ast.literal_eval(content)
                if isinstance(val, dict) and 'text' in val:
                    content = val['text']
            except:
                pass

        print(f"✅ AI 响应内容: {content[:50]}...")
        return content
            
    except Exception as e:
        print(f"❌ [Generator] Summary 报错: {e}")
        return f"基于您的食材偏好，我为您甄选了以下几道值得尝试的美味佳肴。"
