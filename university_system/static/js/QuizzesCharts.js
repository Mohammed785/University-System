{
    // gradient color
    let width,height,gradient;
    function getGradient(ctx,chartArea){
        const chartWidth = chartArea.right - chartArea.left;
        const chartHeight = chartArea.bottom - chartArea.top;
        if (gradient===null||width!==chartWidth||height!==chartHeight){
            width = chartWidth;
            height = chartHeight;
            gradient = ctx.createLinearGradient(0,chartArea.bottom,0,chartArea.top);
            gradient.addColorStop(0.2,'#102A42');
            gradient.addColorStop(1,'#0F5092');
        }
        return gradient
    };

    let ctx = document.getElementById('myChart1').getContext('2d');
    let myChart1 = new Chart(ctx, {
        type:'line',
        data:{
            labels:[],
            datasets:[{
                label:'Quizzes',
                data:[],
                backgroundColor: [
                    '#67EBB9',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderColor: (context)=>{
                    const chart = context.chart;
                    const {ctx,chartArea} = chart;
                    if(!chartArea){
                        return null;
                    }
                    return getGradient(ctx,chartArea);
                },
                tension: 0.2,
            }]
        },
        plugins:[],
        options:{
            scales:{
                y:{
                    beginAtZero:true
                }
            },
            elements:{
                point:{
                    radius:5,
                    borderWidth:2
                }
            }
        }
    });
    var endpoint = '/grade/quizzes/api/cs12';
    window.addEventListener('DOMContentLoaded',(e)=>{
        $.ajax({
            method:'GET',
            url:endpoint,
            success:(data)=>{
                myChart1.data.labels = data.labels;
                myChart1.data.datasets[0].data = data.data
                myChart1.update();
            },
            error:(error)=>{
                console.error(error)
            }
        })
    })
}