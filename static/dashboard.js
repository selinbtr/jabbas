// fetch("/movie_data").then(data=>data.json()).then(d=>{

// })

d3.json("http://127.0.0.1:5000/movie_data").then((data) => {
    console.log(data)
    var selector=d3.select('#selDataset');

    // for (var i=0; i<data.length; i++)
    var genre_list = []
    data.forEach((movie)=> {
        var genre = movie.genres;
        genre_list.push(genre)
    })
       
     
    var unique_genres = Array.from(new Set(genre_list))
    console.log(unique_genres)
    unique_genres.forEach((genre)=> {
        selector.append('option')
        .property('value', genre)
        .text(genre)
    })

buildChart(unique_genres[0]);

});



function buildChart(selection) {
    d3.json("http://127.0.0.1:5000/movie_data").then((data)=> {
        var filterSubject = data.filter(data => data.genres==selection)
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
     

        var trace = {
            labels: labels, 
            values: values,
            type: "pie",
            text: labels, 
            textposition: "inside"
        };
        var layout = {
            // title: "Select a Movie by Content Rating",
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