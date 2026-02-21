import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

const GraficoEnem = () => {
    const [porcentagens, setPorcentagens] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/comparacao/nota-renda')
            .then(response => {
                setPorcentagens(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Erro ao carregar os dados:', error);
                setError("Erro ao carregar dados.");
                setLoading(false);
            });
    }, []);

    if (loading) return <div style={{padding: '20px'}}>Carregando gráfico...</div>;
    if (error) return <div style={{color: 'red', padding: '20px'}}>{error}</div>;
    if (!porcentagens) return null;

    const cores = {
        'Renda Alta': 'rgba(255, 99, 132, 0.6)',   
        'Renda Média': 'rgba(54, 162, 235, 0.6)',  
        'Renda Baixa': 'rgba(75, 192, 192, 0.6)'   
    };

    const chartData = {
        labels: porcentagens.labels,
        datasets: porcentagens.datasets.map(dataset => ({
            label: dataset.label,
            data: dataset.data,
            backgroundColor: cores[dataset.label] || 'gray',
            borderColor: cores[dataset.label] || 'black',   
            borderWidth: 1
        }))
    };

    const options = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Distribuição de Notas por Faixa de Renda (%)',
                font: {
                    size: 18
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label += context.parsed.y + '%';
                        }
                        return label;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Porcentagem de Estudantes (%)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Faixas de Nota'
                }
            }
        },
        layout: {
            padding: {
                top: 10,
                bottom: 10,
                left: 10,
                right: 10
            }
        }
    };

    return (
        <div style={{ 
            margin: '0 auto',
            padding: '20px', 
            width: '90%',           
            maxWidth: '1000px',     
            minWidth: '0',          
            position: 'relative',   
            boxShadow: '0 4px 12px rgba(0,0,0,0.1)', 
            borderRadius: '8px', 
            backgroundColor: '#fff'
        }}>
            <h2 style={{ textAlign: 'center', color: '#333' }}>Comparação ENEM</h2>
            <p style={{ textAlign: 'center', color: '#666', marginBottom: '20px' }}>
                Proporção de estudantes por faixa de nota em cada grupo de renda.
            </p>
            <Bar data={chartData} options={options} />
        </div>
    );
};

export default GraficoEnem;