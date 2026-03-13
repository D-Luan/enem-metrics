import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import App from "./App";

vi.stubGlobal("fetch", vi.fn());

describe("EnemMetrics - Integração do App", () => {
    beforeEach(() => {
        vi.resetAllMocks();
        vi.stubEnv("VITE_API_URL", "http://localhost:8000");
    });

    it("deve exibir o estado de loading inicialmente", () => {
        vi.mocked(fetch).mockImplementation(() => new Promise(() => {}));

        render(<App />);

        expect(screen.getByText(/Carregando métricas do ENEM/i)).toBeInTheDocument();
    });

    it("deve exibir mensagem de erro se a API falhar", async () => {
        const mensagemErroApi = "Falha ao buscar os dados da API";

        vi.mocked(fetch).mockRejectedValueOnce(new Error(mensagemErroApi));

        render(<App />);

        await waitFor(() => {
            expect(screen.getByText(/Ocorreu um erro./i)).toBeInTheDocument();
            expect(screen.getByText(mensagemErroApi)).toBeInTheDocument();
        });
    });

    it("deve renderizar o gráfico quando os dados chegam", async () => {
        const mockApiPayload = {
            dados: [
                {
                    faixa_nota: "0-599",
                    qtd_renda_baixa: 1500,
                    qtd_renda_media: 3000,
                    qtd_renda_alta: 500,
                    total_notas: 5000,
                    pct_renda_baixa: 30.0,
                    pct_renda_media: 60.0,
                    pct_renda_alta: 10.0
                }
            ]
        };
        
        vi.mocked(fetch).mockResolvedValueOnce({
            ok: true,
            json: async () => mockApiPayload,
        } as Response);

        render(<App />);

        await waitFor(() => {
            expect(screen.queryByText(/Carregando métricas do ENEM/i)).not.toBeInTheDocument();
            expect(screen.getByText("Métricas do ENEM")).toBeInTheDocument();
        });
    });
});