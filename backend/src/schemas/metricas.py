from pydantic import BaseModel

class DistribuicaoRendaPorFaixa(BaseModel):
    faixa_nota: str
    qtd_renda_baixa: int
    qtd_renda_media: int
    qtd_renda_alta: int
    total_notas: int
    pct_renda_baixa: float
    pct_renda_media: float
    pct_renda_alta: float

class RespostaComparacaoRenda(BaseModel):
    dados: list[DistribuicaoRendaPorFaixa]