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


    // Fill search box with options
    let scheduled_function = false
    $( "#taxa-search" ).on( "keyup", function () {
        event.preventDefault();
        if (scheduled_function) {
                clearTimeout(scheduled_function)
            }
        // setTimeout returns the ID of the function to be executed
        // syntax is setTimeout(function, delay in ms, parameter (the query))
        scheduled_function = setTimeout(call_search_taxa, 1000, $(this).val())
    });


    // Create the chart with gray background scatter
    chart_init();


    // Remove all extra traces except background and make all options available
    $( "#reset" ).on("click", () => {
        var myChart = Chart.getChart("myChart");
        while (myChart.data.datasets.length > 1) {
            myChart.data.datasets.pop();
        };
        myChart.update();
        // remove extra rows in the add-highlight table
        var table = document.getElementById("highlight-menus");
        for (let i = table.rows.length - 1; i > 1; i--) {
            table.deleteRow(i)
        };
    });
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
    // Recover chart instance
    var myChart = Chart.getChart("myChart");
    var datasets = myChart.data.datasets;
    let i = datasets.length;
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
        $( "#taxa-options" ).empty();
        response.forEach( (item) => {
            var op = document.createElement("button")
            op.setAttribute("value", item["value"]);
            op.setAttribute("rank", item["rank"]);
            op.classList = "btn btn-link op-link";
            op.style = "text-align: left; width: 100%";
            op.setAttribute("href", "#");
            op.innerHTML = `${item["rank"]}: ${item["value"]}<br>@ ${item["kingdom"]}`
            $("#taxa-options").append(op);
        });
        // Bind: adding highlight through options on search box
        $( "#taxa-options > button" ).on("click", function (e) {
            e.preventDefault();
            let rank = e.target.getAttribute("rank");
            let value = e.target.value;
            let varx = $( "#x-choose" ).val();
            let vary = $( "#y-choose" ).val();
            // Recover chart instance
            var myChart = Chart.getChart("myChart");
            var datasets = myChart.data.datasets;
            let pos = datasets.length;
            add_trace(varx, vary, rank, value, pos)
            .then(() => { myChart.update() });

        });
    })
};
