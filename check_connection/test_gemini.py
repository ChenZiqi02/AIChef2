import os
from dotenv import load_dotenv, find_dotenv
import sys

# 1. 尝试加载环境变量
env_file = find_dotenv(filename='.env', raise_error_if_not_found=True)
print(f"📄 正在加载环境变量文件: {env_file}")
load_dotenv(env_file)

key = os.getenv("GEMINI_API_KEY")
if not key:
    print("❌ 错误: .env 文件中未找到 GEMINI_API_KEY")
    sys.exit(1)
print(f"🔑 检测到 Key: {key[:5]}******{key[-4:]}")

print("\n📡 正在尝试连接 Google Gemini...")

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=key,
        temperature=0.7
    )
    
    response = llm.invoke("Hello, are you working? Please reply with 'Yes, I am working!'.")
    print("\n✅ 连接成功！Gemini 回复：")
    print("-" * 30)
    print(response.content)
    print("-" * 30)
    
except ImportError:
    print("❌ 错误: 缺少依赖库。请运行: pip install langchain-google-genai")
except Exception as e:
    print(f"\n❌ 连接失败: {str(e)}")
