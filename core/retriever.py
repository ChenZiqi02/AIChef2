from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from core.config import DB_PATH_V3, EMBEDDING_MODEL_NAME, COLLECTION_NAME
import torch

class VectorDBManager:
    """
    单例模式管理数据库连接，防止重复加载模型导致内存爆炸
    """
    _instance = None
    _vector_store = None

    @classmethod
    def get_vector_store(cls):
        if cls._vector_store is None:
            print(f"🔄 [Retriever] 正在初始化向量库: {DB_PATH_V3}")
            try:
                if torch.backends.mps.is_available():
                    device = "mps"
                elif torch.cuda.is_available():
                    device = "cuda"
                else:
                    device = "cpu"
                embeddings = HuggingFaceEmbeddings(
                    model_name=EMBEDDING_MODEL_NAME,
                    model_kwargs={'device': device},
                    encode_kwargs={'normalize_embeddings': True}
                )
                # ⚠️ collection_name 必须和你 ingest 入库时的一致！
                # 之前我们用的是 "recipe_collection_v3"
                cls._vector_store = Chroma(
                    collection_name=COLLECTION_NAME, 
                    embedding_function=embeddings,
                    persist_directory=DB_PATH_V3
                )
                print("✅ [Retriever] 向量库加载完成")
            except Exception as e:
                print(f"❌ [Retriever] 数据库加载失败: {e}")
                return None
        return cls._vector_store


def retrieve_docs(query: str, top_k: int = 4, score_threshold: float = 1.0, preferences: dict = None):
    """
    检索核心函数
    :param preferences: 用户偏好字典，例如 {"dislikes": ["香菜", "辣"]}
    """
    db = VectorDBManager.get_vector_store()
    if not db:
        return []

    # 执行检索
    results = db.similarity_search_with_score(query, k=top_k)
    
    # 格式化结果
    filtered_results = []
    print(f"🔎 [Retriever] 检索到 {len(results)} 条，阈值: {score_threshold}")
    
    for doc, score in results:
        print(f"   - {doc.metadata.get('name')} (Score: {score:.4f})")
        # 恢复正常的阈值过滤
        if score <= score_threshold:
            filtered_results.append({
                "id": doc.metadata.get('id', ''),          # 建议加上 ID
                "name": doc.metadata.get('name', '未知'),
                "tags": doc.metadata.get('tags', ''),
                "image": doc.metadata.get('image', ''),
                
                # ✅【新增关键修改】提取步骤数据
                "instructions": doc.metadata.get('instructions', []), 
                
                "content": doc.page_content,
                "score": score
            })
            
    # --- 后置过滤 (Post-Retrieval Filtering) based on User Preferences ---
    if preferences:
        final_results = []
        dislikes = preferences.get("dislikes", [])
        allergies = preferences.get("allergies", [])
        
        # 将不喜欢和过敏源合并检查
        avoid_list = [x.lower() for x in (dislikes + allergies) if x]
        
        if avoid_list:
            print(f"🛑 [Retriever] 正在过滤用户忌口: {avoid_list}")
            for res in filtered_results:
                # 检查菜品名称、标签和内容是否包含忌口词
                text_to_check = (res['name'] + str(res['tags']) + res['content']).lower()
                
                is_safe = True
                for word in avoid_list:
                    if word in text_to_check:
                        print(f"   -> 剔除 '{res['name']}' (包含忌口: {word})")
                        is_safe = False
                        break
                
                if is_safe:
                    final_results.append(res)
            return final_results

    return filtered_results