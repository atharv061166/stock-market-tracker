async function fetchStockData() {
    const symbol = document.getElementById('symbol').value;
    const stockDataDiv = document.getElementById('stock-data');
    const stockChartCanvas = document.getElementById('stockChart');

    // Clear previous data
    stockDataDiv.innerHTML = '';
    stockChartCanvas.style.display = 'none';

    if (!symbol) {
        stockDataDiv.innerHTML = '<p>Please enter a stock symbol</p>';
        return;
    }

    try {
        const response = await fetch(`/api/stocks/${symbol}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        displayStockData(data);
        updateChart(data);
    } catch (error) {
        console.error('Error fetching stock data:', error);
        stockDataDiv.innerHTML = `<p>Error fetching stock data: ${error.message}</p>`;
    }
}

function displayStockData(data) {
    const stockDataDiv = document.getElementById('stock-data');
    if (data.error) {
        stockDataDiv.innerHTML = `<p>Error: ${data.error}</p>`;
    } else {
        stockDataDiv.innerHTML = `
            <h2>${data.symbol}</h2>
            <p>Date: ${data.date}</p>
            <p>Open: ${data.open}</p>
            <p>High: ${data.high}</p>
            <p>Low: ${data.low}</p>
            <p>Close: ${data.close}</p>
            <p>Volume: ${data.volume}</p>
        `;
    }
}

function updateChart(data) {
    const ctx = document.getElementById('stockChart').getContext('2d');
    const dates = data.historical_data.map(entry => new Date(entry.date));
    const closingPrices = data.historical_data.map(entry => entry.close);

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: `${data.symbol} Stock Price`,
                data: closingPrices,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero: false
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    enabled: true
                }
            }
        }
    });

    // Show the chart
    document.getElementById('stockChart').style.display = 'block';
}