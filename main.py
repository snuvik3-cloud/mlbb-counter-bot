from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="MLBB Counter-Pick API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === ОГРОМНАЯ БАЗА ГЕРОЕВ И КОНТРПИКОВ ===
HEROES_DB: Dict[str, dict] = {
    # ---------------- УБИЙЦЫ (JUNGLE) ----------------
    "Fanny": {
        "role": "Assassin", "lane": "Jungle",
        "counters": {
            "Khufra": "Сфера Хуфры блокирует полеты на тросах при столкновении.",
            "Minsitthar": "Ультимейт отключает использование тросов.",
            "Saber": "Моментально ловит в ульт до начала полета.",
            "Eudora": "Стан из кустов и прокаст сбривают Фанни до реакции."
        }
    },
    "Nolan": {
        "role": "Assassin", "lane": "Jungle",
        "counters": {
            "Chou": "Выпинывает Нолана из порталов и сбивает комбо.",
            "Kaja": "Подавляет ультой, игнорируя очищение Нолана.",
            "Khufra": "Контролем не дает быстро раскастоваться."
        }
    },
    "Ling": {
        "role": "Assassin", "lane": "Jungle",
        "counters": {
            "Minsitthar": "Снимает со стены и связывает ультой.",
            "Khufra": "Сбивает со стены прыжком или блокирует рывки.",
            "Saber": "Ждет спуска со стены и выдает ваншот."
        }
    },
    "Gusion": {
        "role": "Assassin", "lane": "Jungle",
        "counters": {
            "Lolita": "Щит блокирует все летящие кинжалы Гуся.",
            "Chou": "Прерывает рывок Гуся пинком.",
            "Lancelot": "Уворачивается от кинжалов неуязвимостью."
        }
    },
    "Lancelot": {
        "role": "Assassin", "lane": "Jungle",
        "counters": {
            "Phoveus": "Каждый рывок Ланселота заряжает ульту Фовеуса.",
            "Khufra": "Сбивает бесконечные рывки сферой."
        }
    },
    "Hayabusa": {
        "role": "Assassin", "lane": "Jungle",
        "counters": {
            "Saber": "Ловит в ульт до того, как Хаябуса уйдет в тень.",
            "Chou": "Легко уходит от ульты Хаябусы рывками.",
            "Sun": "Ульта Хаябусы распыляется на клонов Сана."
        }
    },
    "Joy": {
        "role": "Assassin", "lane": "Exp/Jungle",
        "counters": {
            "Minsitthar": "Запрещает рывки Джой в ульте, ломая её ритм.",
            "Franco": "Подавление игнорирует её иммунитет к контролю."
        }
    },
    "Saber": {
        "role": "Assassin", "lane": "Jungle",
        "counters": {
            "Argus": "Прожимает ульту на бессмертие в ответ на ульт Сабера.",
            "Diggie": "Снимает стан Сабера ультой."
        }
    },

    # ---------------- СТРЕЛКИ (GOLD) ----------------
    "Claude": {
        "role": "Marksman", "lane": "Gold",
        "counters": {
            "Belerick": "Возвращает огромный урон от ульты Клода обратно.",
            "Lolita": "Щит полностью съедает все выстрелы Клода.",
            "Saber": "Ловит Клода в прыжке на ульте."
        }
    },
    "Wanwan": {
        "role": "Marksman", "lane": "Gold",
        "counters": {
            "Phoveus": "Прыжки Ванван активируют ульту Фовеуса.",
            "Kaja": "Подавляет танец и не дает нажать очищение.",
            "Khufra": "Блокирует прыжки, не давая сбить метки."
        }
    },
    "Karrie": {
        "role": "Marksman", "lane": "Gold",
        "counters": {
            "Lolita": "Блокирует чистый урон от сфер Кэрри.",
            "Lunox": "Перестреливает по урону за счет темной ульты.",
            "Belerick": "Провоцирует и убивает возвратом урона."
        }
    },
    "Moskov": {
        "role": "Marksman", "lane": "Gold",
        "counters": {
            "Belerick": "Высокая скорость атаки Москова убивает его об пассивку Белерика.",
            "Lolita": "Блокирует автоатаки."
        }
    },
    "Bruno": {
        "role": "Marksman", "lane": "Gold",
        "counters": {
            "Lolita": "Сбивает щитом мячи Бруно.",
            "Natalia": "Немота и дым заставляют Бруно промахиваться."
        }
    },
    "Beatrix": {
        "role": "Marksman", "lane": "Gold",
        "counters": {
            "Natalia": "Легко вырезает из инвиза.",
            "Lolita": "Блокирует выстрелы из снайперки и пулемета."
        }
    },
    "Melissa": {
        "role": "Marksman", "lane": "Gold",
        "counters": {
            "Franco": "Притягивает Мелиссу хуком прямо из её купола.",
            "Yve": "Достает замедлением и уроном сквозь купол."
        }
    },
    "Lesley": {
        "role": "Marksman", "lane": "Gold",
        "counters": {
            "Aldous": "Ульта открывает Лесли в инвизе и ваншотает.",
            "Saber": "Дает моментальный прокаст из кустов."
        }
    },

    # ---------------- ТАНКИ / РОУМ (ROAM) ----------------
    "Khufra": {
        "role": "Tank", "lane": "Roam",
        "counters": {
            "Diggie": "Дает иммунитет команде к прыжку Хуфры.",
            "Valir": "Отталкивает Хуфру вторым скиллом."
        }
    },
    "Tigreal": {
        "role": "Tank", "lane": "Roam",
        "counters": {
            "Diggie": "Снимает стяжку Тигриала ультой.",
            "Akai": "Расталкивает Тигриала вертушкой во время каста."
        }
    },
    "Franco": {
        "role": "Tank", "lane": "Roam",
        "counters": {
            "Lylia": "Постоянно мансит и харасит Франко, не давая дать хук.",
            "Johnson": "Если Франко хукнет Джонсона, это убьет команду Франко."
        }
    },
    "Atlas": {
        "role": "Tank", "lane": "Roam",
        "counters": {
            "Diggie": "Полностью контрит ульту Атласа.",
            "Valir": "Останавливает Атласа, когда тот выходит из мехи."
        }
    },
    "Estes": {
        "role": "Support", "lane": "Roam",
        "counters": {
            "Baxia": "Антихил срезает всё лечение Эстеса.",
            "Luo Yi": "Взрывает команду Эстеса за то, что они стоят толпой."
        }
    },
    "Angela": {
        "role": "Support", "lane": "Roam",
        "counters": {
            "Baxia": "Режет щиты Ангелы.",
            "Kaja": "Вытягивает цель Ангелы в фокус."
        }
    },
    "Diggie": {
        "role": "Support", "lane": "Roam",
        "counters": {
            "Hilda": "Легко убивает хилого Дигги на первых минутах.",
            "Natalia": "Шотает Дигги до того, как он нажмет ульту."
        }
    },

    # ---------------- БОЙЦЫ (EXP) ----------------
    "Chou": {
        "role": "Fighter", "lane": "Exp",
        "counters": {
            "Phoveus": "Рывки Чоу спамят ульту Фовеуса.",
            "Minsitthar": "Отключает рывки в ульте.",
            "Gatotkaca": "Слишком много физ-дефа для Чоу."
        }
    },
    "Yin": {
        "role": "Fighter", "lane": "Exp",
        "counters": {
            "Argus": "Убивает Иня в его же арене.",
            "Tigreal": "Ловит Иня на вкате."
        }
    },
    "Yu Zhong": {
        "role": "Fighter", "lane": "Exp",
        "counters": {
            "Baxia": "Срезает отхил от пассивки дракона.",
            "Dyrroth": "Перебивает дракона на линии со старта."
        }
    },
    "Dyrroth": {
        "role": "Fighter", "lane": "Exp",
        "counters": {
            "Guinevere": "Подбрасывает Диррота во время его долгого каста.",
            "Thamuz": "Сильнее в лобовой дуэли за счет отхила."
        }
    },
    "Martis": {
        "role": "Fighter", "lane": "Exp/Jungle",
        "counters": {
            "Kaja": "Подавление игнорирует иммунитет Мартиса.",
            "Franco": "Подавляет ультой, не давая крутиться."
        }
    },
    "Aldous": {
        "role": "Fighter", "lane": "Exp",
        "counters": {
            "Chou": "Выпинывает Алдоса под башню.",
            "Twilight Armor": "Предмет режет огромный урон Алдоса.",
            "Akai": "Отталкивает Алдоса при прилете."
        }
    },
    "Terizla": {
        "role": "Fighter", "lane": "Exp",
        "counters": {
            "Valir": "Держит медленного Теризлу на расстоянии.",
            "Karrie": "Пробивает чистым уроном сквозь его жир."
        }
    },

    # ---------------- МАГИ (MID) ----------------
    "Lunox": {
        "role": "Mage", "lane": "Mid",
        "counters": {
            "Saber": "Взрывает Лунокс до светлого ульта.",
            "Helcurt": "Сайленс не дает переключить фазы."
        }
    },
    "Luo Yi": {
        "role": "Mage", "lane": "Mid",
        "counters": {
            "Saber": "Ловит на ошибке позиционирования.",
            "Lancelot": "Уворачивается от инь-янь навыков."
        }
    },
    "Nana": {
        "role": "Mage", "lane": "Mid",
        "counters": {
            "Helcurt": "Сайленс не дает Нане сбежать.",
            "Lancelot": "Забирает пассивку и добивает рывком."
        }
    },
    "Lylia": {
        "role": "Mage", "lane": "Mid",
        "counters": {
            "Saber": "Ваншотает до отмотки здоровья.",
            "Kaja": "Держит в ульте, не давая нажать тапки."
        }
    },
    "Novaria": {
        "role": "Mage", "lane": "Mid",
        "counters": {
            "Ling": "Быстро долетает на бэклайн и вырезает.",
            "Fanny": "Настигает на любой дистанции."
        }
    },
    "Pharsa": {
        "role": "Mage", "lane": "Mid",
        "counters": {
            "Chou": "Сбивает каст ульты пинком.",
            "Kadita": "Ныряет прямо под Фарсу и взрывает."
        }
    },
    "Kadita": {
        "role": "Mage", "lane": "Mid",
        "counters": {
            "Lylia": "Легко уходит от прокаста Кадиты тапком.",
            "Franco": "Подавляет ультой, когда она выныривает."
        }
    },
    "Valentina": {
        "role": "Mage", "lane": "Mid",
        "counters": {
            "Yve": "Если Валентина украдет ульту Ив, Ив всё равно перебьет её.",
            "Pharsa": "Перестреливает Валентину с безопасного расстояния."
        }
    }
}

class DraftRequest(BaseModel):
    enemy_team: List[str]
    our_team: List[str]

@app.get("/api/heroes")
def get_all_heroes():
    # Отдаем список всех имен по алфавиту для выпадающих меню
    return sorted(list(HEROES_DB.keys()))

@app.get("/api/counter/lane")
def get_lane_counter(enemy_name: str, lane: str):
    recommendations = []
    
    # Ищем, кто контрит выбранного врага на нужной линии
    for my_name, info in HEROES_DB.items():
        if info["lane"] == lane and enemy_name in info["counters"]:
            recommendations.append({
                "hero_name": my_name,
                "reason": info["counters"][enemy_name]
            })
            
    return recommendations

@app.post("/api/counter/draft")
def get_draft_recommendations(req: DraftRequest):
    scores = {}
    
    taken_roles = [HEROES_DB[name]["role"] for name in req.our_team if name in HEROES_DB]
            
    for enemy in req.enemy_team:
        for my_name, info in HEROES_DB.items():
            if my_name in req.enemy_team or my_name in req.our_team:
                continue
                
            if enemy in info["counters"]:
                if my_name not in scores:
                    scores[my_name] = {"name": my_name, "role": info["role"], "lane": info["lane"], "score": 0, "reasons": []}
                
                # Добавляем очки за каждый контрпик
                scores[my_name]["score"] += 10
                scores[my_name]["reasons"].append(f"Контрит {enemy}: {info['counters'][enemy]}")

    result = []
    sorted_scores = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    
    for item in sorted_scores:
        priority = "РЕКОМЕНДУЕТСЯ (Роль свободна)" if item["role"] not in taken_roles else "Доп. вариант (роль занята)"
        result.append({
            "name": item["name"],
            "role": item["role"],
            "lane": item["lane"],
            "status": priority,
            "reasons": item["reasons"]
        })
        
    return result[:10]  # Выводим топ-10 лучших вариантов для 5х5

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)