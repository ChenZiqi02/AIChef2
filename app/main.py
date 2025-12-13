from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 引入我们定义好的模型和服务
from .models import QueryRequest, RecipeResponse, RecipeListResponse, ConsultRequest
from .services import recipe_service

# 初始化 APP
app = FastAPI(
    title="AIChef RAG API",
    description="智能菜谱检索接口 - 返回包含步骤图的结构化数据",
    version="1.0.0"
)

# --- 跨域配置 (CORS) ---
# 允许前端 (Vue/React/小程序) 访问接口
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请改为具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    """健康检查接口"""
    return {"status": "ok", "message": "AIChef API is running!"}

@app.post("/api/search", response_model=RecipeListResponse)
async def search_recipe(request: QueryRequest):
    """
    🔍 核心搜索接口 - 支持返回列表
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="搜索词不能为空")

    # 调用 Service 层
    # 注意：为了兼容旧代码，我们先看看 service 能不能返回列表
    result = recipe_service.get_recipe_list_response(request.query, request.limit)
    
    # 404 处理
    if not result or not result.candidates:
        raise HTTPException(
            status_code=404, 
            detail=f"抱歉，暂未收录关于“{request.query}”的菜谱，请尝试其他关键词。"
        )
    
    return result

@app.post("/api/consult")
async def consult_chef_api(request: ConsultRequest):
    """
    AI 厨师交互接口
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")

    reply = recipe_service.consult_chef(request.query, request.context, request.history)
    return {"reply": reply}

# 仅用于直接调试 main.py 时使用
# 实际建议在根目录用 run.py 启动
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)