import { useState, useEffect } from "react";
import { Layout } from "@/components/layout/Layout";

interface MetricaRenda {
  faixa_nota: string;
  qtd_renda_baixa: number;
  qtd_renda_media: number;
  qtd_renda_alta: number;
  total_notas: number;
  pct_renda_baixa: number;
  pct_renda_media: number;
  pct_renda_alta: number;
}

interface ApiResposta {
  dados: MetricaRenda[];
}

function App() {
  const [dados, setDados] = useState<MetricaRenda[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function buscarMetricas() {
      try {
        const resposta = await fetch("http://127.0.0.1:8000/api/metricas/renda");

        if (!resposta.ok) {
          throw new Error("Falha ao buscar os dados da API");
        }

        const json = await resposta.json() as ApiResposta;
        setDados(json.dados);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
          return;
        }

        setError("Ocorreu um erro desconhecido.");
      } finally {
        setLoading(false);
      }
    }

    buscarMetricas();
  }, []);
  
  return (
    <Layout>
      <div className="w-full max-w-4xl mx-auto h-96 bg-white border-2 border-zinc-700 rounded-lg flex flex-col items-center justify-center">
        {loading && (
          <p className="font-medium text-lg animate-pulse text-blue-500">Carregando métricas do ENEM</p>
        )}

        {error && (
          <div className="text-center">
            <p className="font-medium text-lg text-red-500">Ocorre um erro.</p>
            <p className="text-sm text-red-400 mt-1">{error}</p>
          </div>
        )} 

        {!loading && !error && (
          <div className="text-center flex flex-col items-center">
            <p className="font-medium text-lg text-zinc-800">Dados carregados com sucesso!</p>
            <p className="text-sm mt-2 text-zinc-500">{dados.length} faixas de notas da API recebidas.</p>
          </div>
        )}
      </div>
    </Layout>  
  );
}

export default App;
