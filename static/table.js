function makeTable(data) {
   
    var tbody = d3.select("tbody");
   
    data.forEach(function(movies) {
        
        var row = tbody.append("tr");
        Object.entries(movies).forEach(function([key, value]) {
            var cell = row.append("td");
            cell.text(value);
        });
    });
};

d3.json("https://jabbas.herokuapp.com/movie_data").then((data) => {
    
    console.log(data);
    makeTable(data);

});

var button = d3.select("#filter-btn");

function PressButton()
    {
    d3.event.preventDefault();

    tableData = d3.json("https://jabbas.herokuapp.com/movie_data").then((data) => {
        console.log(`promiseResult ${data}`);
    
        var inputTitle = d3.select("#title").property("value");
        var inputGenre = d3.select("#genre").property("value");
        var inputYear = d3.select("#year").property("value");
        var inputRating = d3.select("#rating").property("value");
        var inputDirector = d3.select("#director").property("value");

        let inputValues = [
            [inputTitle, 'movie'],
            [inputGenre, 'genres'],
            [inputYear, 'year'],
            [inputRating, 'rating'],
            [inputDirector, 'director']
        ];

        // make a copy of the table to do the filter on
       // let filteredInfo = [];

        // loop through the inputs and filter each one that is given
      //  inputValues.forEach(i => {
            // check for not an empty string
           // if (i[0].length) {
                // apply filter
             //   filteredInfo.push = (data).filter(info => info[i[1]] === i[0]);
          //  }
     //   }); 
        filteredInfo = [];

        Object.entries(inputValues).forEach((k)=>{
            console.log(k[1][1], k[1][0])
            filteredInfo.push(data.filter(s => s[k[1][1]] == k[1][0]))
        });

        combined = filteredInfo[0].concat(...filteredInfo.slice(1, filteredInfo.length));

        // console.log(d3.event.target);
        console.log(combined);

        var tbody = d3.select("tbody");

        d3.select("tbody").html("");

        makeTable(combined)
    });
};
    
button.on("click", PressButton)

