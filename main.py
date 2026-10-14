from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI(title="Binary Search Cloud Run API")

# 클라이언트로부터 받을 요청 데이터 구조 정의
class SearchRequest(BaseModel):
    array: list[int]
    target: int

@app.post("/binary-search")
def binary_search_trace(req: SearchRequest):
    """
    이진 검색을 수행하고 각 단계별 상태 기록(Trace)을 반환합니다.
    시간 복잡도: O(log n)
    """
    # 입력받은 배열을 오름차순으로 정렬 (이진 검색의 전제 조건)
    arr = sorted(req.array)
    target = req.target
    
    steps = []
    low = 0
    high = len(arr) - 1
    found = False
    result_index = -1
    
    start_time = time.time()
    
    # 이진 검색 알고리즘 루프
    while low <= high:
        mid = (low + high) // 2
        current_val = arr[mid]
        
        # 현재 단계의 상태 기록
        step_info = {
            "low": low,
            "high": high,
            "mid": mid,
            "current_val": current_val,
            "status": "searching"
        }
        
        if current_val == target:
            found = True
            result_index = mid
            step_info["status"] = "found"
            steps.append(step_info)
            break
        elif current_val < target:
            step_info["status"] = "go_right" # 타겟이 더 크므로 우측 탐색
            steps.append(step_info)
            low = mid + 1
        else:
            step_info["status"] = "go_left"  # 타겟이 더 작으므로 좌측 탐색
            steps.append(step_info)
            high = mid - 1
            
    # 탐색 실패 시 최종 상태 기록
    if not found:
        steps.append({
            "low": low,
            "high": high,
            "mid": -1,
            "current_val": None,
            "status": "not_found"
        })
        
    elapsed_time = (time.time() - start_time) * 1000 # 밀리초(ms) 변환
    
    return {
        "array": arr,
        "target": target,
        "found": found,
        "index": result_index,
        "steps": steps,
        "complexity": "O(log n)",
        "execution_time_ms": round(elapsed_time, 2)
    }
