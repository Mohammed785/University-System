var canvas = document.getElementById('myChart1');
var ctx = canvas.getContext('2d');
var myChart1 = new Chart(ctx,{
    type:'pie',
    data:{
        labels:[],
        datasets:[{
            label:'Semester Grades',
            data: [],
            backgroundColor:[
                '#0e3d8a',
                '#623d94',
                '#9a3992',
                '#c93784',
                '#eb416e',
                '#ff5c53',
                '#ff8034',
                '#ffa600'
            ],
            borderColor:[
                '#0e3d8a',
                '#623d94',
                '#9a3992',
                '#c93784',
                '#eb416e',
                '#ff5c53',
                '#ff8034',
                '#ffa600'
            ],
            borderWidth:1
        }]
    },
    options:{
        scales:{
            y:{
                beginAtZero:true
            }
        }
    }
});

var endpoint = 'api/2021/1ST';
window.addEventListener('DOMContentLoaded',(e)=>{
    $.ajax({
        method:'GET',
        url:endpoint,
        success:(data)=>{
            myChart1.data.labels = data.labels;
            myChart1.data.datasets[0].data = data.data;
            myChart1.update();
        },
        error:(error)=>console.error(error)
    })
})
canvas.addEventListener('click',(ev)=>{
    const activePoints = myChart1.getElementsAtEventForMode(ev, 'nearest', { intersect: true }, true);
    if(activePoints.length){
        const point = activePoints[0];
        var label = myChart1.data.labels[point.index];
        var value = myChart1.data.datasets[point.datasetIndex].data[point.index];
        console.log(label + ' Has Been Clicked And Its Values ' + value);
    }
})