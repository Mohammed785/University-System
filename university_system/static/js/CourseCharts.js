// gradient color
let width, height, gradient;
function getGradient(ctx, chartArea) {
    const chartWidth = chartArea.right - chartArea.left;
    const chartHeight = chartArea.bottom - chartArea.top;
    if (gradient === null || width !== chartWidth || height !== chartHeight) {
        width = chartWidth;
        height = chartHeight;
        gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
        gradient.addColorStop(0.2, '#102A42');
        gradient.addColorStop(1, '#0F5092');
    }
    return gradient
};

const bgColors = [
    '#0e3d8a',
    '#623d94',
    '#9a3992',
    '#c93784',
    '#eb416e',
    '#ff5c53',
    '#ff8034',
    '#ffa600'
]
const options = {
    scales: {
        y: {
            beginAtZero: true
        }
    },
    elements: {
        point: {
            radius: 5,
            borderWidth: 2
        }
    }
}
const ChartSetting = (canvasID, type, label, bgColors, plugins = [], options, endpoint, endpointFlag = true) => {
    let chartCanvas = document.getElementById(canvasID)
    let ctx = chartCanvas.getContext('2d');
    let myChart = new Chart(ctx, {
        type: type,
        data: {
            labels: [],
            datasets: [{
                label: label,
                data: [],
                backgroundColor: bgColors,
                borderColor: (context) => {
                    const chart = context.chart;
                    const { ctx, chartArea } = chart;
                    if (!chartArea) {
                        return null;
                    }
                    return getGradient(ctx, chartArea);
                },
                tension: 0.2,
                hoverOffset: 4
            }]
        },
        plugins: plugins,
        options: options
    });
    let course_Code = $(chartCanvas).data('coursecode')
    if (endpointFlag) {
        endpoint = endpoint + course_Code;
    }
    window.addEventListener('DOMContentLoaded', (e) => {
        $.ajax({
            method: 'GET',
            url: endpoint,
            success: (data) => {
                myChart.data.labels = data.labels;
                myChart.data.datasets[0].data = data.data
                myChart.update();
            },
            error: (error) => {
                console.error(error)
            }
        })
    })
}
ChartSetting('myChart1', 'line', 'Quizzes', bgColors, [], options, '/api/v1/grade/quizzes/')
ChartSetting('myChart2', 'line', 'Assignments', bgColors, [], options, '/api/v1/grade/assignments/')
ChartSetting('myChart3', 'pie', 'Grade', bgColors, [], options, '/api/v1/grade/course/')
const canvasData = document.getElementById('myChart4')
const endpoint = `/api/v1/grade/midterm/course/${$(canvasData).data('coursecode')}/${$(canvasData).data('year')}`
ChartSetting('myChart4', 'pie', 'Midterm', bgColors, [], options, endpoint, false)