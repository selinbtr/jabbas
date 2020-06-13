d3.json("http://127.0.0.1:5000/movie_data").then((data) => {
    console.log(data)
    var selector=d3.select('#selDataset');

    // for (var i=0; i<data.length; i++)
    var ratings_list = []
    data.forEach((movie)=> {
        var content_rating = movie.content_rating;
        ratings_list.push(content_rating)
    })
       
     
    var unique_ratings = Array.from(new Set(ratings_list))
    console.log(unique_ratings)
    unique_ratings.forEach((rating)=> {
        selector.append('option')
        .property('value', rating)
        .text(rating)
    })

buildChart(unique_ratings[0]);

});



function buildChart(selection) {
    d3.json("http://127.0.0.1:5000/movie_data").then((data)=> {
        var filterSubject = data.filter(data => data.content_rating==selection)
        console.log(filterSubject)
       
        var country_list = []
        var country_count = filterSubject.forEach((movie)=>{
                            var country = movie.country
                            country_list.push(country)
        
        });

        var country_dict = country_list.reduce((a,c)=> (a[c]=(a[c]||0)+1,a),Object.create(null));
        console.log(country_dict)
        var labels = Object.keys(country_dict)
        var values = Object.values(country_dict)
        console.log(values)
//         var unique_country = Array.from(new Set(country_list))
//         for (var i = 0; i<unique_country.length; i++){
//             country_dict.push({
//                 key: unique_country[i], 
//                 value: 1
//         })
       
//         }
//         console.log(country_dict)
//         var values = Object.values(country_dict)
//         var labels = Object.keys(country_dict)
//         console.log(country_list)
     

        var trace = {
            labels: labels, 
            values: values,
            type: "pie",
            text: labels, 
            textposition: "inside"
        };
        var layout = {
            title: "Select a Movie by Content Rating",
            showlegend: false
        };
        var data = [trace];
        Plotly.newPlot("pie", data, layout);
    });
}

function optionChanged(selectedRating) {
    console.log(selectedRating);
    buildChart(selectedRating);
    // demographicData(selectedSample);
};