function buildPlot(){
    /* data route */
    const url = "/get_piechart_data";
    d3.json(url).then(function(response) {
        console.log(response);
        var labels = response.map(row => row.category);
        var values = response.map(row => row.measure);
        var trace = {
            labels:labels, 
            values:values, 
            type: "pie", 
            text:labels,
            textposition: "inside"
        }
        var layout = {
            title: "Select a genre:",
            showlegend: false
        };
        var data = [trace];
        Plotly.newPlot("pie", data, layout);
    });

}
buildPlot();

function dropdown(){
    /* data route */
    const url = "/movie_data";
    d3.json(url).then(function(response) {
        var movie_list  = response.map(data => data.movie);
        console.log(movie_list);
        for (var i = 0; i < movie_list.length; i++) {
            selectBox = d3.select("#selDataset");
            selectBox.append("option").text(movie_list[i]);
          }
    });

}
dropdown();

