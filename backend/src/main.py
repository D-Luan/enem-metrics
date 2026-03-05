import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Estudante:
    def __init__(self, id, renda_classificada, nota_matematica):
        self.id = id
        self.renda_classificada = renda_classificada
        self.nota_matematica = nota_matematica

def generate_mock_data(size=10000):
    estudantes = []
    for i in range(size):
        renda_val = random.randint(0, 20000)
        if renda_val > 10000:
            renda_classificada = "Renda Alta"
            nota_matematica = random.uniform(600, 1000)
        elif renda_val > 3000:
            renda_classificada = "Renda Média"
            nota_matematica = random.uniform(500, 900)
        else:
            renda_classificada = "Renda Baixa"
            nota_matematica = random.uniform(300, 800)
        estudantes.append(Estudante(i+1, renda_classificada, round(nota_matematica, 2)))
    return estudantes

def classificar_nota(nota):
    if 500 <= nota < 600: return "500-599"
    elif 600 <= nota < 700: return "600-699"
    elif 700 <= nota < 800: return "700-799"
    elif 800 <= nota < 900: return "800-899"
    elif 900 <= nota <= 1000: return "900-999"
    return None

def calcular_porcentagens(estudantes):
    labels = ["500-599", "600-699", "700-799", "800-899", "900-999"]
    dados = {
        "labels": labels,
        "datasets": [
            {"label": "Renda Alta", "data": [0] * 5},
            {"label": "Renda Média", "data": [0] * 5},
            {"label": "Renda Baixa", "data": [0] * 5}
        ]
    }
    renda_map = {"Renda Alta": 0, "Renda Média": 1, "Renda Baixa": 2}
    
    for estudante in estudantes:
        faixa_nota = classificar_nota(estudante.nota_matematica)
        if faixa_nota:
            try:
                idx_nota = labels.index(faixa_nota)
                idx_renda = renda_map[estudante.renda_classificada]
                dados["datasets"][idx_renda]["data"][idx_nota] += 1
            except ValueError:
                pass
                
    for dataset in dados["datasets"]:
        total = sum(dataset["data"])
        if total > 0:
            dataset["data"] = [round((x / total) * 100, 2) for x in dataset["data"]]
    return dados

@app.get("/")
def read_root():
    return {"status": "online", "docs_url": "/docs"}

@app.get("/api/comparacao/nota-renda")
async def comparacao_notas_rendas():
    estudantes = generate_mock_data()
    porcentagens = calcular_porcentagens(estudantes)
    return porcentagens

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)