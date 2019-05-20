function initPollBar(divid, chartData,chartName) {
	var series = [];

	var myChart = echarts.init(document.getElementById(divid + ""));
	var myColor = ['#FFA483', '#F97F53', '#F45922'];
	option = {
		backgroundColor: '#fff',
		grid: {
			left: '1%',
			right: '2%',
			bottom: '1%',
			top: '1%',
			containLabel: true
		},
		xAxis: [{
				show: false,
			},
			{
				show: false,
			}
		],
		yAxis: {
			type: 'category',
			inverse: true,
			show: false
		},

		series: [
			{
				show: true,
				type: 'bar',
				barWidth: '20%',
				itemStyle: {
					normal: {
						color: function(params) {
							var num = myColor.length;
							return myColor[params.dataIndex % num]
						}
					}
				},
				label: {
					normal: {
						show: true,
						textStyle: {
							color: '#000',
							fontSize: 20,
							fontWeight: 'bold'
						},
						position: 'right',
						formatter: function(data) {
							return chartData[data.dataIndex];
						}
					}
				},
				data: chartData
			},
        {
            show: true,
            type: 'bar',
            xAxisIndex: 1, //代表使用第二个X轴刻度
            barGap: '-100%',
            barWidth: '10%',
            itemStyle: {
                normal: {
                    barBorderRadius: 200,
                    color: 'transparent'
                }
            },
            label: {
                normal: {
                    show: true,
                    position: [0, '-20'],
                    textStyle: {
                        fontSize:14,
                        color: '#333',
                    },
                    formatter: function(data) {
                        return chartName[data.dataIndex];
                    }
                }
            },
            data: chartData
        }
		]
	};

	myChart.setOption(option);
}

function initPollPie(text,divid,  chartData,chartName) {
	var myChart = echarts.init(document.getElementById(divid + ""));
	option = {
    title : {
        text: text,
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data: chartName
    },
    series : [
        {
            name: '',
            type: 'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:chartData,
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};

	myChart.setOption(option);
}

function generateHtml(poll){
	var html = "";
	html = html 
	+'<fieldset class="layui-elem-field site-demo-button" style="margin-top: 10px;" >    '
	+'	<legend>'+poll.name+'</legend>                                                  '
	+'		<div style="padding: 20px; background-color: #F2F2F2;">                     '
	+'		  <div class="layui-row layui-col-space15">                                 '
	+'			<div class="layui-col-md12">                                            '
	+'			  <div class="layui-card">                                              '
	+'				<div class="layui-card-body">                                       '
	+'				  <div id="bar_'+poll.id+'" style="width: 100%;height:250px;margin: 0"></div>   '
	+'				</div>                                                              '
	+'			  </div>                                                                '
	+'			</div>                                                                  '
	+'			<div class="layui-col-md6">                                             '
	+'			  <div class="layui-card">                                              '
	+'				<div class="layui-card-body">                                       '
	+'				  <div id="m_pie_'+poll.id+'" style="width: 100%;height:250px;margin: 0"></div> '
	+'				</div>                                                              '
	+'			  </div>                                                                '
	+'			</div>                                                                  '
	+'			<div class="layui-col-md6">                                             '
	+'			<div class="layui-card">                                                '
	+'				<div class="layui-card-body">                                       '
	+'				<div id="fm_pie_'+poll.id+'" style="width: 100%;height:250px;margin: 0"></div>  '
	+'				</div>                                                              '
	+'			</div>                                                                  '
	+'			</div>                                                                  '
	+'		  </div>                                                                    '
	+'		</div>                                                                      '
	+'</fieldset>                                                                       ';
	return html;
}