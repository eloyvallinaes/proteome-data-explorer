document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("x-log").onclick = varlog;
    document.getElementById("y-log").onclick = varlog;
    document.getElementById("y-choose").onchange = varchange;
    document.getElementById("x-choose").onchange = varchange;

    document.querySelectorAll(".choose").forEach((dropdown) => {
        dropdown.addEventListener('change', show_options);
        dropdown.addEventListener('change', add_highlight);

    });

    document.getElementById("add-highlight-dialog").onclick = add_highlight_dialog;

    // Search box action
    let scheduled_function = false
    $( "#taxa-search" ).on( "keyup", function () {
        event.preventDefault();
        console.log($(this).val())
        if (scheduled_function) {
                clearTimeout(scheduled_function)
            }
        // setTimeout returns the ID of the function to be executed
        // syntax is setTimeout(function, delay in ms, parameter (the query))
        scheduled_function = setTimeout(call_search_taxa, 1000, $(this).val())
    });

    // Create the chart with gray background scatter
    chart_init();
});

function chart_init() {
    let csrftoken = Cookies.get('csrftoken')
    fetch('/take_subset/', {
                            method : "POST",
                            body : JSON.stringify({
                                                    varx : "ncd1000",
                                                    vary : "mwkda",
                                                    pos  : 0,
                                                    rank : "kingdom",
                                                    value : "all",
                                                }),
                            credentials : "include",
                            headers : {"X-CSRFToken" : csrftoken}
                           }
         ).then( function(response) {
             if (response.ok === true) {
                 return response.json()
             } else {
                 console.log("error")
             };
         })
         .then( content => {
                var ctx = document.getElementById("myChart");
                // create the chart using the chart canvas
                var myChart = new Chart(ctx, {
                    type: 'scatter',
                    data: { datasets : [content.dataset]},
                    options: {
                                responsive : true,
                                resizeDelay: 1,
                                animation : false,
                                scales: {
                                    y: {
                                        title : {
                                            display : true,
                                            text : content.axislabels.y
                                                }

                                        },
                                    x : {
                                        title : {
                                            display : true,
                                            text : content.axislabels.x
                                                }
                                        }
                                },
                                plugins : {
                                    tooltip : {
                                                enabled: false,

                                              },
                                          },
                            },
                });
            });
};


// Request dataset from backend, add to datasets;
// idx is the index of Chart.datasets, where the new trace is being inserted
function add_trace(varx, vary, rank, value, idx) {
    let csrftoken = Cookies.get('csrftoken')
    // Recover chart instance
    var myChart = Chart.getChart("myChart");
    var datasets = myChart.data.datasets;
    return fetch('/take_subset/', {
                            method : "POST",
                            body : JSON.stringify({
                                                    varx : varx,
                                                    vary : vary,
                                                    pos  : idx,
                                                    rank : rank,
                                                    value : value,
                                                }),
                            credentials : "include",
                            headers : {"X-CSRFToken" : csrftoken}
                           }
         ).then( function(response) {
             if (response.ok === true) {
                 return response.json()
             } else {
                 console.log("error");
             };
         })
         .then( content => {
             datasets[idx]=content.dataset;
             myChart.options.scales.x.title.text = content.axislabels.x;
             myChart.options.scales.y.title.text = content.axislabels.y;
         });
    return true
};


// Detect click on log boxes and change scale
function varlog(event) {
    var myChart = Chart.getChart("myChart");
    var axname = event.target.id.split("-")[0]; // x or y
    if (event.target.checked === true) {
        myChart.options.scales[axname].type = "logarithmic"
    }
    else {
        myChart.options.scales[axname].type = "linear"
    };
    myChart.update();
};


// Update plot when value of variable dropdowns changes
function varchange() {
    var myChart = Chart.getChart("myChart");
    var datasets = myChart.data.datasets
    myChart.data.datasets = [];
    var varx = document.getElementById("x-choose").value;
    var vary = document.getElementById("y-choose").value;
    processed = 0
    datasets.forEach( (dataset, idx, arr) => {
        add_trace(varx, vary, dataset.rank, dataset.value, idx)
        .then(() => { if (processed === arr.length - 1) {
                    myChart.update()
                } else {
                    processed++
                };
        });

    })

};


function show_options(event) {
    console.log(event.target.id)
    var ranks = ["kingdom", "phylum", "taxClass", "order", "family", "genus", "species"]
    var rank = event.target.id.split("-")[0]
    if (rank === "genus") {
        return false
    } else {
        var rowno = event.target.id.split("-")[1]
        var lowerRank = ranks[ ranks.indexOf(rank) + 1]
        var value = event.target.value
        let csrftoken = Cookies.get('csrftoken');
        fetch("/options/", {
            method: "POST",
            body: JSON.stringify({
                'rank' : rank,
                'value' : value
            }),
            credentials : "include",
            headers : {"X-CSRFToken" : csrftoken}
        }).then( function(response) {
            if (response.ok === true) {
                return response.json()
            } else {
                console.log("error");
            };
        }).then( content => {
            var dropdown = document.getElementById(`${lowerRank}-${rowno}`);
            var placeholder = makePlaceholder();
            // remove all previous options, add placeholder
            Array.from(dropdown.children).forEach((child) => {child.remove()})
            dropdown.appendChild(placeholder);
            // add new options served by backend
            content.forEach(option => {
                var op = document.createElement("option");
                op.value = option.name;
                op.innerHTML = `${option.name} (N = ${option.count})`;
                dropdown.appendChild(op);
            });
        });
    };

};


function makePlaceholder() {
    var placeholder = document.createElement('option');
    placeholder.value = "placeholder";
    placeholder.innerHTML = "Choose here";
    placeholder.setAttribute('selected', true);
    placeholder.setAttribute('disabled', true);
    placeholder.setAttribute('hidden', true);

    return placeholder;
};


function add_highlight(event) {
    var rank = event.target.id.split("-")[0];
    // Including header, table initially has 2 rows while Chart has 1 dataset
    var pos = parseInt(event.target.id.split("-")[1]);
    var value = event.target.value;
    var varx = document.getElementById("x-choose").value;
    var vary = document.getElementById("y-choose").value;
    // Recover chart instance
    var myChart = Chart.getChart("myChart");
    var datasets = myChart.data.datasets;
    add_trace(varx, vary, rank, value, pos)
    .then(() => { myChart.update() });
};


// Add highlight dialog
function add_highlight_dialog(event) {
    event.preventDefault(); // prevent page from scrolling up
    var table = document.getElementById("highlight-menus");
    let i = table.rows.length;
    var nextRow = table.insertRow(table.rows.length);
    var rowModel = document.getElementById("rowmodel").cloneNode(deep = true);
    rowModel.setAttribute("id", "")
    Array.from(rowModel.children).forEach((column) => {
        var dropdown = column.getElementsByTagName("select")[0];
        let newId = dropdown.id.split("-")[0] + "-" + i;
        dropdown.setAttribute("id", newId);
    });
    nextRow.innerHTML = rowModel.innerHTML;
    document.querySelectorAll(".choose").forEach((dropdown) => {
        dropdown.addEventListener('change', show_options);
        dropdown.addEventListener('change', add_highlight);

    });

};

let call_search_taxa = function ( query ){
    $.getJSON("/taxa/", {
        q: query
    }).done( response => {
        $("#taxa-options").empty();
        response.forEach( (item) => {
            var op = document.createElement("option");
            op.setAttribute("value", item["value"]);
            op.setAttribute("rank", item["rank"]);
            op.innerHTML = `${item["rank"]}: ${item["value"]} @ ${item["kingdom"]}`
            $("#taxa-options").append(op);
        })
    })
};



//     var rowmodel = Handlebars.compile(document.getElementById("rowmodel").innerHTML);
//     nextrow.innerHTML = rowmodel({"i" : i});
//     // Add options
//     show_options(name = "all", rank = "kingdom", id = i);
//     // Add the event listeners
//     bind_dropdowns()
// };


// function bind_dropdowns() {
//   // Bind functions to dropdowns
//   var dropdowns = document.querySelectorAll(".choose");
//   dropdowns.forEach(
//     function (dropdown) {
//       dropdown.addEventListener("change", add_trace);
//       dropdown.addEventListener("change", show_options);
//       }
//   );
// };

//     // Request dataset from Flask, add to datasets and remove option from menu
//     function add_trace(name = null, rank = null, count = null, rowno = null) {
//         // Recover chart instance
//         var myChart = Chart.instances[0];
//         var datasets = myChart.data.datasets;
//         if (!name || !rank || !count || !rowno) {
//             var rowno = parseInt(this.id.split("-")[2]);
//             [name, rank] = this.value.split(",");
//             var count = myChart.data.datasets.length;
//         };
//         // Find if this row already produced a datasets
//         var rowindex = datasets.findIndex((dataset) => {return dataset.row === rowno})
//         // Initialize new request
//         const request = new XMLHttpRequest();
//         request.open('POST', '/add_trace');
//         request.onload = () => {
//             const dataset = JSON.parse(request.responseText);
//             if (rowindex === -1) {
//                 // if no dataset already in chart
//                 addDataset(myChart, dataset);
//                 console.log("New dataset added: ", dataset["label"]);
//             }
//             else {
//                 myChart.data.datasets[rowindex] = dataset;
//                 myChart.update()
//                 console.log("Dataset replacement: ", dataset["label"]);
//             };
//         };
//         // Add data to send with request
//         const info = new FormData();
//         // rank and category just selected and number of active datasets
//         info.append('name', name);
//         info.append('rank', rank);
//         info.append('count', count);
//         info.append('rowno', rowno);
//         request.send(info);
//         return false;
//     }
//     // Remove all extra traces except background and make all options available
//     function reset() {
//         myChart = Chart.instances[0];
//         while (myChart.data.datasets.length > 1) {
//             myChart.data.datasets.pop();
//         }
//         myChart.update();
//         document.querySelectorAll("option").forEach(
//             function (option) {
//                 option.disabled = false;
//                 if (option.value === "placeholder") {
//                     option.selected = true;
//                 };
//             });
//         // remove extra rows in the add-highlight table
//         var table = document.getElementById("highlight-menus");
//         for (let i = table.rows.length - 1; i > 1; i--) {
//             table.deleteRow(i)
//         }
//     };
//     // Show options for lower levels when selected
//     function show_options(name = null, rank = null, rowno = 0) {
//         var levels = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
//         var placeholder = "<option value=\"placeholder\" selected disabled hidden>Choose here</option>\n"
//         if (!name || !rank) {
//             [name, rank] = this.value.split(",");
//             rowno = this.id.split("-")[2];
//         };
//         // reset all lower dropdowns
//         for (let i = levels.indexOf(rank) + 1; i < levels.length-1; i++) {
//             let levelname = levels[i];
//             document.querySelector(`#choose-${levelname}-${rowno}`).innerHTML = placeholder;
//         };
//         // if rank=kingdom and name=all do not send request and keep placeholders
//         if (rank === "kingdom" && name === "all") {
//             return false;
//         }
//         else {
//             // otherwise retrieve names of lower rank and fill table
//             var lower = levels[levels.indexOf(rank) + 1];
//             var optionmodel = Handlebars.compile(document.getElementById("optionmodel").innerHTML);
//             const request = new XMLHttpRequest();
//             request.open('POST', '/show_options');
//             request.onload = () => {
//                 const data = JSON.parse(request.responseText);
//                 // add options to immediately lower dropdown
//                 for (let i = 0; i < data.length; i++) {
//                     var item = data[i];
//                     var option = optionmodel({"name" : item.name, "rowno" : item.rowno, "rank" : lower})
//                     document.querySelector(`#choose-${lower}-${rowno}`).innerHTML += option;
//                 };
//             };
//             // Add data to send with request
//             const info = new FormData();
//             // category just selected
//             info.append('name', name);
//             info.append('rank', rank);
//             // Send request
//             request.send(info);
//         };
//
//     };
    // Update chart on value change of the varx, vary dropdowns

//     // Retrieve available value-label pairs for the axes from backend
//     function show_vars() {
//         const request = new XMLHttpRequest();
//         request.open('POST', '/show_vars');
//         varopmodel = Handlebars.compile(document.querySelector("#varopmodel").innerHTML)
//         request.onload = function () {
//             var response = JSON.parse(request.responseText)
//             for (var key of Object.keys(response)) {
//                 var varoption = varopmodel({"key" : key, "value" : response[key]})
//                 document.querySelector("#choose-x").innerHTML += varoption;
//                 document.querySelector("#choose-y").innerHTML += varoption;
//             }
//             // ensure default options match chart
//             document.querySelector("#choose-x").children[2].selected = true;
//             document.querySelector("#choose-y").children[1].selected = true;
//         }
//         request.send();
//     };
