from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from typing import List

app = FastAPI(title="MLBB Counter-Pick API")

# Разрешаем фронтенду подключаться к бэкенду
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Загружаем базу данных героев
with open("heroes_data.json", "r", encoding="utf-8") as f:
    HEROES_DB = json.load(f)

class DraftRequest(BaseModel):
    enemy_team: List[int] # Список ID врагов
    our_team: List[int]   # Список ID союзников

@app.get("/api/heroes")
def get_all_heroes():
    return [{"id": h["id"], "name": h["name"], "role": h["role"], "lane": h["lane"]} for h in HEROES_DB]

# РЕЖИМ 1х1: Контрпик на линию
@app.get("/api/counter/lane")
def get_lane_counter(enemy_id: int, lane: str):
    recommendations = []
    for hero in HEROES_DB:
        if hero["lane"] == lane:
            for c in hero.get("counters", []):
                if c["enemy_id"] == enemy_id:
                    recommendations.append({
                        "hero_name": hero["name"],
                        "weight": c["weight"],
                        "reason": c["reason"]
                    })
    
    # Сортируем по силе контры
    recommendations.sort(key=lambda x: x["weight"], reverse=True)
    return recommendations

# РЕЖИМ 5х5: Умный подбор под драфт
@app.post("/api/counter/draft")
def get_draft_recommendations(req: DraftRequest):
    scores = {}
    
    # Считаем свободные роли в нашей команде
    taken_roles = []
    for my_id in req.our_team:
        hero = next((h for h in HEROES_DB if h["id"] == my_id), None)
        if hero: taken_roles.append(hero["role"])
            
    # Анализируем каждого врага
    for enemy_id in req.enemy_team:
        for hero in HEROES_DB:
            # Исключаем тех, кого уже пикнули
            if hero["id"] in req.enemy_team or hero["id"] in req.our_team:
                continue
                
            for c in hero.get("counters", []):
                if c["enemy_id"] == enemy_id:
                    if hero["id"] not in scores:
                        scores[hero["id"]] = {"hero": hero, "score": 0, "reasons": []}
                    
                    # Начисляем очки за контру
                    scores[hero["id"]]["score"] += c["weight"]
                    scores[hero["id"]]["reasons"].append(f"Хорош против {hero['name']}: {c['reason']}")

    # Формируем ответ по приоритетным ролям
    result = []
    sorted_scores = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    
    for item in sorted_scores:
        h = item["hero"]
        # Делаем пометку, если роль в команде еще не занята (это приоритет!)
        priority = "РЕКОМЕНДУЕТСЯ (Роль свободна)" if h["role"] not in taken_roles else "Возможный добор"
        
        result.append({
            "name": h["name"],
            "role": h["role"],
            "lane": h["lane"],
            "status": priority,
            "reasons": item["reasons"][:2] # отдаем топ-2 причины
        })
        
    return result[:5] # Возвращаем ТОП-5 идеальных кандидатов

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)