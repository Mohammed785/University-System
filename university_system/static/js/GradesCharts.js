var ctx = document.getElementById('myChart1').getContext('2d');
var myChart1 = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    plugins:[],
    options: {
        scales: {
            y: {
                suggestedMax: 100,
                beginAtZero: true
            }
        },
        plugins:{
            legend:{
                labels:{
                    font:{
                        size:15,
                        family:'sans-serif'
                    },
                },
            },
        },
        
    }
});

var endpoint = 'api/';//there a code paramter here
window.addEventListener('DOMContentLoaded',(e)=>{
    $.ajax({
        method:'GET',
        url:endpoint,
        success:(data)=>{
            myChart1.data.labels = data.labels;
            myChart1.data.datasets[0].data = data.data;
            myChart1.update();
        },
        error:(error)=>{
            console.error(error)
        }
    })
})