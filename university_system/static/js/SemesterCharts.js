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
                borderColor: bgColors,
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
                console.log(data)
            },
            error: (error) => {
                console.error(error)
            }
        })
    })
}
const chartData = document.getElementById('myChart1');
const endpoint = `/api/v1/grade/year/${$(chartData).data('year')}/semester/${$(chartData).data('semester')}`
ChartSetting('myChart1', 'pie', 'Courses', bgColors, [], options, endpoint,false)