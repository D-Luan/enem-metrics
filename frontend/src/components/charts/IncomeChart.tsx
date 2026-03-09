import { Bar, BarChart, CartesianGrid, XAxis, YAxis, LabelList } from "recharts";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ChartContainer, ChartLegend, ChartLegendContent, type ChartConfig } from "@/components/ui/chart";
import type { MetricaRenda } from "@/App";

interface IncomeChartProps {
    dados: MetricaRenda[];
}

const chartConfig = {
    pct_renda_baixa: {
        label: "Renda Baixa",
        color: "#60a5fa",
    },
    pct_renda_media: {
        label: "Renda Média",
        color: "#3b82f6",
    },
    pct_renda_alta: {
        label: "Renda Alta",
        color: "#1d4ed8",
    }
} satisfies ChartConfig;

export function IncomeChart({ dados }: IncomeChartProps) {
    return (
        <Card className="w-full">
            <CardHeader>
                <CardTitle>Desigualdade de Renda por Nota</CardTitle>
                <CardDescription>Distribuição percentual de renda familiar em cada faixa de nota do ENEM</CardDescription>
            </CardHeader>

            <CardContent>
                <ChartContainer config={chartConfig} className="h-[400px] w-full">
                    <BarChart accessibilityLayer data={dados} layout="vertical" margin={{ top: 0, right: 20, left: 0, bottom: 20 }} barCategoryGap="20%">
                        <CartesianGrid horizontal={true} vertical={true} strokeDasharray="3 3" opacity={0.5}/>
                        <XAxis type="number" domain={[0, 100]} ticks={[0, 20, 40, 60, 80, 100]} tickLine={true} axisLine={true} tickFormatter={(value) => `${value}%`}/>
                        <YAxis type="category" dataKey="faixa_nota" tickLine={true} axisLine={true} width={70} />

                        <ChartLegend content={<ChartLegendContent className="text-base font-medium mt-2 gap-6" />} />

                        <Bar dataKey={"pct_renda_baixa"} stackId={"a"} fill="var(--color-pct_renda_baixa)">
                            <LabelList dataKey="pct_renda_baixa" position="center" fill="#ffffff" fontSize={12} fontWeight="bold" formatter={(val: number) => `${val}%`} />
                        </Bar>
                        <Bar dataKey={"pct_renda_media"} stackId={"a"} fill="var(--color-pct_renda_media)">
                            <LabelList dataKey="pct_renda_media" position="center" fill="#ffffff" fontSize={12} fontWeight="bold" formatter={(val: number) => `${val}%`} />
                        </Bar>
                        <Bar dataKey={"pct_renda_alta"} stackId={"a"} fill="var(--color-pct_renda_alta)">
                            <LabelList dataKey="pct_renda_alta" position="center" fill="#ffffff" fontSize={12} fontWeight="bold" formatter={(val: number) => `${val}%`} />
                        </Bar>
                    </BarChart>
                </ChartContainer>
            </CardContent>
        </Card>
    );
}