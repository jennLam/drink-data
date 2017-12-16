Chart.defaults.global.defaultFontFamily = "Arial";
var options = { responsive: true };
var ctx= $("#buyRateChart").get(0).getContext("2d");
$.get("/buy-rate.json", function (data) {
    var myBarChart = new Chart(ctx, {
      type: 'bar',
      data: data,
      options: {
        scales: {
          xAxes: [{ barPercentage: 0.5 }]
        },
        legend: { display: false},
        title: {
          display: false,
          text: "Brand Buying Rates"
        }
            }
    });
});

function showResults(results) {
$("#searchResults").html("Number of Households: " + results.hh_count)
}

function getHh(evt) {
evt.preventDefault();

var searchInputs = {
  "brand": $("#brand").val(),
  "retailer": $("#retailer").val(),
  "start_date": $("#startDate").val(),
  "end_date": $("#endDate").val()
};

$.get("/search.json", searchInputs, showResults);
}

$("#hh-button").on("click", getHh);

function showAffinity(results) {
  $("#selected-brand").html(results.brand + " <span class='caret'></span>");
  $("#tab-comment").html("Top Retailer Affinity: " + results.top_affinity)
  $(".tab-head").html("<tr><th>Retailer</th><th>Affinity</th></tr>");
  $(".tab-body").html("<tr><tr>");
  $.each(results.affinity, function(key, value) {
    $(".tab-body").append("<tr><td>" + key + "</td><td>" + value + "x</td></tr>");
  });
}

function getBrand(evt) {
  evt.preventDefault();

  var brand = {
    "b": $(this).data("brand")
  };

  $.get("/affinity.json", brand, showAffinity);
}

$("a[href='#brand']").click(getBrand);