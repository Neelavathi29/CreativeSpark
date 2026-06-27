document.addEventListener('DOMContentLoaded', function() {
    Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";
    Chart.defaults.plugins.legend.labels.usePointStyle = true;

    const scoresChart = document.getElementById('scoresChart');
    if (scoresChart) {
        const innov = parseFloat(scoresChart.dataset.innovation) || 0;
        const feas = parseFloat(scoresChart.dataset.feasibility) || 0;
        const market = parseFloat(scoresChart.dataset.market) || 0;
        const scala = parseFloat(scoresChart.dataset.scalability) || 0;

        new Chart(scoresChart, {
            type: 'bar',
            data: {
                labels: ['Innovation', 'Feasibility', 'Market Potential', 'Scalability'],
                datasets: [{
                    label: 'Score',
                    data: [innov, feas, market, scala],
                    backgroundColor: [
                        'rgba(255, 205, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(153, 102, 255, 0.8)'
                    ],
                    borderColor: [
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)',
                        'rgb(153, 102, 255)'
                    ],
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, max: 100, grid: { display: false } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    const statusChart = document.getElementById('statusChart');
    if (statusChart) {
        const labels = JSON.parse(statusChart.dataset.labels || '[]');
        const values = JSON.parse(statusChart.dataset.values || '[]');
        const colors = {
            'Draft': 'rgba(108, 117, 125, 0.8)',
            'Submitted': 'rgba(13, 202, 240, 0.8)',
            'Under Review': 'rgba(255, 193, 7, 0.8)',
            'Approved': 'rgba(25, 135, 84, 0.8)',
            'Rejected': 'rgba(220, 53, 69, 0.8)',
            'Incubating': 'rgba(13, 110, 253, 0.8)',
            'Launched': 'rgba(111, 66, 193, 0.8)'
        };

        const bgColors = labels.map(l => colors[l] || 'rgba(108, 117, 125, 0.8)');

        new Chart(statusChart, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: bgColors,
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }

    const categoryChart = document.getElementById('categoryChart');
    const reportStatusChart = document.getElementById('reportStatusChart');
    const reportIndustryChart = document.getElementById('reportIndustryChart');

    [categoryChart, reportStatusChart, reportIndustryChart].forEach(function(chartEl) {
        if (chartEl) {
            try {
                const labels = JSON.parse(chartEl.dataset.labels || '[]');
                const values = JSON.parse(chartEl.dataset.values || '[]');
                const colors = [
                    'rgba(108, 99, 255, 0.8)', 'rgba(255, 101, 132, 0.8)',
                    'rgba(75, 192, 192, 0.8)', 'rgba(255, 205, 86, 0.8)',
                    'rgba(54, 162, 235, 0.8)', 'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 159, 64, 0.8)', 'rgba(201, 203, 207, 0.8)'
                ];

                new Chart(chartEl, {
                    type: 'pie',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: values,
                            backgroundColor: colors.slice(0, labels.length),
                            borderWidth: 2,
                            borderColor: '#fff'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'bottom', labels: { padding: 15 } }
                        }
                    }
                });
            } catch(e) {}
        }
    });

    const radarChart = document.getElementById('radarChart');
    if (radarChart) {
        new Chart(radarChart, {
            type: 'radar',
            data: {
                labels: ['Innovation', 'Feasibility', 'Market Potential', 'Scalability', 'Risk'],
                datasets: [{
                    label: 'Evaluation Scores',
                    data: [
                        parseInt(radarChart.dataset.innovation) || 0,
                        parseInt(radarChart.dataset.feasibility) || 0,
                        parseInt(radarChart.dataset.market) || 0,
                        parseInt(radarChart.dataset.scalability) || 0,
                        parseInt(radarChart.dataset.risk) || 0
                    ],
                    backgroundColor: 'rgba(108, 99, 255, 0.2)',
                    borderColor: 'rgba(108, 99, 255, 0.8)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(108, 99, 255, 1)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: { stepSize: 20 }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    const trendsChart = document.getElementById('trendsChart');
    if (trendsChart) {
        try {
            const labels = JSON.parse(trendsChart.dataset.labels || '[]');
            const values = JSON.parse(trendsChart.dataset.values || '[]');
            new Chart(trendsChart, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Growth Rate (%)',
                        data: values,
                        backgroundColor: 'rgba(75, 192, 192, 0.8)',
                        borderColor: 'rgb(75, 192, 192)',
                        borderWidth: 2,
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, grid: { display: false } },
                        x: { grid: { display: false } }
                    }
                }
            });
        } catch(e) {}
    }

    const marketSizeChart = document.getElementById('marketSizeChart');
    if (marketSizeChart) {
        try {
            const labels = JSON.parse(marketSizeChart.dataset.labels || '[]');
            const values = JSON.parse(marketSizeChart.dataset.values || '[]');
            new Chart(marketSizeChart, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: [
                            'rgba(108, 99, 255, 0.8)', 'rgba(255, 101, 132, 0.8)',
                            'rgba(75, 192, 192, 0.8)', 'rgba(255, 205, 86, 0.8)',
                            'rgba(54, 162, 235, 0.8)', 'rgba(153, 102, 255, 0.8)'
                        ],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: 'bottom' } }
                }
            });
        } catch(e) {}
    }

    const financialChart = document.getElementById('financialChart');
    if (financialChart) {
        try {
            var labels = JSON.parse(financialChart.dataset.labels || '[]');
            var rev = JSON.parse(financialChart.dataset.revenue || '[]');
            var costs = JSON.parse(financialChart.dataset.costs || '[]');
            var profit = JSON.parse(financialChart.dataset.profit || '[]');
            new Chart(financialChart, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        { label: 'Revenue', data: rev, backgroundColor: 'rgba(75, 192, 192, 0.8)', borderRadius: 4 },
                        { label: 'Costs', data: costs, backgroundColor: 'rgba(255, 99, 132, 0.8)', borderRadius: 4 },
                        { label: 'Profit', data: profit, backgroundColor: 'rgba(255, 205, 86, 0.8)', borderRadius: 4 }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: 'bottom' } },
                    scales: { y: { beginAtZero: true } }
                }
            });
        } catch(e) {}
    }

    const competitorChart = document.getElementById('competitorChart');
    if (competitorChart) {
        var our = parseInt(competitorChart.dataset.our) || 0;
        var c1 = parseInt(competitorChart.dataset.c1) || 0;
        var c2 = parseInt(competitorChart.dataset.c2) || 0;
        var c3 = parseInt(competitorChart.dataset.c3) || 0;
        new Chart(competitorChart, {
            type: 'radar',
            data: {
                labels: ['Innovation', 'Market Fit', 'Scalability', 'Team', 'Funding'],
                datasets: [
                    { label: 'Your Startup', data: [our, our-5, our-10, our-8, our-12], backgroundColor: 'rgba(255, 205, 86, 0.2)', borderColor: 'rgb(255, 205, 86)', borderWidth: 2 },
                    { label: 'Leader A', data: [c1, c1-3, c1-8, c1+5, c1+10], backgroundColor: 'rgba(75, 192, 192, 0.2)', borderColor: 'rgb(75, 192, 192)', borderWidth: 2 },
                    { label: 'Competitor B', data: [c2, c2-5, c2-10, c2-3, c2-5], backgroundColor: 'rgba(54, 162, 235, 0.2)', borderColor: 'rgb(54, 162, 235)', borderWidth: 2 }
                ]
            },
            options: { responsive: true, scales: { r: { beginAtZero: true, max: 100 } } }
        });
    }
});
