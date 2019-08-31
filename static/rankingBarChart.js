//Most of the code below is adapted from:
//J. Cruz-Benito, “Stacked Bar Chart with Legend,” [Online]. Available: https://gist.github.com/cbjuan/43f10523858abf6053ae [Accessed 31 8 2019].
//M. Stanaland, “Stacked bar chart with tooltips,” [Online]. Available: http://bl.ocks.org/mstanaland/6100713 [Accessed 31 8 2019].
//with some tweeks to fit the project

function RankingBarChart(id,data){
    
// set the dimensions and margins of the graph
    var margin = {top: 10, right: 120, bottom: 200, left: 50},
        width = Math.min(800, window.innerWidth - 10) - margin.left - margin.right,
        height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);
        

    // append the svg object to the body of the page
    var svg = d3.select(id)
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    
    console.log(data)
    // List of subgroups 
    var subgroups = Object.keys(data[0])
    subgroups.shift()
    subgroups.shift()
    console.log(subgroups)
    // List of groups 
    var groups = d3.map(data, function(d){return(d.product_name)}).keys()
    console.log(groups)
    // Add X axis
    var x = d3.scaleBand()
        .domain(groups)
        .range([0, width])
        .padding([0.4])
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickSizeOuter(0))
        .selectAll("text")
        .attr("y", 10)
        .attr("x", -5)
        .attr("dy", ".35em")
        .attr("transform", "rotate(-30)")
        .style("text-anchor", "end");

    svg.append("text")             
        .attr("transform",
              "translate(" + (width/2) + " ," + 
                             (height + margin.top + 80) + ")")
        .style("text-anchor", "middle")
        .text("Product Name");

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, data[0].total])
        .range([ height, 0 ]);
    svg.append("g")
        .call(d3.axisLeft(y));
        
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Total Percentage Score");

    // color palette = one color per subgroup
    var color = d3.scaleOrdinal()
        .domain(subgroups)
        .range(['#011f4b' , '#03396c' , '#005b96',  '#6497b1',  '#b3cde0' ,  '#ebf4f6' ,'#bdeaee' ,'#76b4bd','#58668b' ,'#5e5656' ])

    //stack the data? --> stack per subgroup
    var stackedData = d3.stack()
        .keys(subgroups)
        (data)
    console.log(data)
    //tooltip
    var tooltip = d3.select("body")
	.append("div")
	.style("position", "absolute")
	.style("z-index", "10")
	.style("visibility", "hidden")
	.text("a simple tooltip");

    var div = d3.select("body").append("div")	
    .attr("class", "tooltip")				
    .style("opacity", 0);

    // Show the bars
    svg.append("g")
        .selectAll("g")
        // Enter in the stack data = loop key per key = group per group
        .data(stackedData)
        .enter().append("g")
        .attr("fill", function(d) { return color(d.key); })
        .selectAll("rect")
        // enter a second time = loop subgroup per subgroup to add all rectangles
        .data(function(d) { return d; })
        .enter().append("rect")
            .attr("x", function(d) { return x(d.data.product_name); })
            .attr("y", function(d) { return y(d[1]); })
            .attr("height", function(d) { return y(d[0]) - y(d[1]); })
            .attr("width",x.bandwidth())
            .on("mouseover", function(d) {
                div.transition()		
                .duration(100)		
                .style("opacity", .9);		
                div.html((Math.round((d[1]-d[0])*100)).toString()+'%')	
                .style("left", (d3.event.pageX) + "px")		
                .style("top", (d3.event.pageY - 28) + "px")
            })
            .on("mousemove", function(d) {
                div.transition()		
                .duration(100)		
                .style("opacity", .9);		
                div.html((Math.round((d[1]-d[0])*100)).toString()+'%')	
                .style("left", (d3.event.pageX) + "px")		
                .style("top", (d3.event.pageY - 28) + "px")
            })
            .on("mouseout", function(d){
                div.transition()		
                .duration(400)		
                .style("opacity", 0);	
            })

    var legend = svg.selectAll(".legend")
        .data(color.range())
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(30," + i * 19 + ")"; });
       
    legend.append("rect")
        .attr("x", width - 18)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", function(d, i) {return color.range().slice().reverse()[i];});
    
    

    legend.append("text")
        .attr("x", width + 5)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "start")
        .text(function(d, i) { 
          return 'Principle ' + (10-i).toString()
          }
        );
    }
