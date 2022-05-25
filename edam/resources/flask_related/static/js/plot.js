/**
 * Convert select to array with values
 */
function serealizeSelects(select) {
    var array = [];
    select.each(function () {
        array.push($(this).val())
    });
    return array.join();
}


$(document).ready(function () {
    $('.metrics-multiple').select2({
        placeholder: 'Select a metric',
        width: 'resolve'
    });
    $('.metrics-single').select2({
        placeholder: 'Select a metric',
        width: 'resolve'
    });
    $('.station-single').select2({
        placeholder: 'Select a station',
        width: 'resolve'
    });

});

$("#line-on-demand").on("click", function (e) {
    e.preventDefault();
    $.ajax({
        url: "/line",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'metrics': serealizeSelects($('#line-metric')),
            'stations': serealizeSelects($('#selected-station'))
        },
        dataType: "json",
        success: function (data) {
            Plotly.newPlot('bargraph', JSON.parse(data['data_json']), data['layout']);
        }
    });
})
