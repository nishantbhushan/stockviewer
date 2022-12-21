from chartjs.chart import Chart

def stockChart(stockValueDataframe):
    chart_data = {
        "labels" : [date.date() for date in stockValueDataframe["date"]],
        "datasets" :[
            {
                "label": "Cost",
                "data": stockValueDataframe["cumCost"],
                "backgroundColor": "rgba(255, 99, 132, 0.2)",
            },
            {
                "label": "Value",
                "data": stockValueDataframe["cumValue"],
                "backgroundColor": "rgba(255, 200, 132, 0.4)",
            },
            
        ]
    }

    stockdatachart = chart(type="line", data=chart_data)
    chart_html = stockdatachart.render
    return chart_html