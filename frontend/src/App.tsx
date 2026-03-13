import { useState, useEffect } from "react";
import { Layout } from "@/components/layout/Layout";
import { IncomeChart } from "./components/charts/IncomeChart";

export interface MetricaRenda {
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
        const API_URL = import.meta.env.VITE_API_URL;
        const resposta = await fetch(`${API_URL}/api/metricas/renda`);

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
      <div className="w-full max-w-4xl mx-auto min-h-96 bg-zinc-50 border border-zinc-200 rounded-lg p-4 flex flex-col justify-center">
        {loading && (
          <div className="flex justify-center items-center h-full">
             <p className="font-medium text-lg animate-pulse text-blue-500">Carregando métricas do ENEM...</p>
          </div>
        )}

        {error && (
          <div className="text-center">
            <p className="font-medium text-lg text-red-500">Ocorreu um erro.</p>
            <p className="text-sm text-red-400 mt-1">{error}</p>
          </div>
        )} 

        {!loading && !error && (
          <div className="w-full">
            <div className="w-full max-w-4xl"> 
              <IncomeChart dados={dados} />
            </div>
          </div>
        )}
      </div>
    </Layout>  
  );
}

export default App;
