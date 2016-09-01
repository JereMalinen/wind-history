$(document).ready(function() {
    var drawGraph = function(data, id, header, o) {
        new Dygraph(document.getElementById(id), header + data, o);
    }

    function draw_speed(data) {
        drawGraph(data, "wind", "Aika,Perustuuli,Puuska\n", {fillGraph: true});
    }

    function draw_direction(data) {
        drawGraph(data, "direction", "Aika,Tuulen suunta\n", {});
    }

    function draw_graph(prefix, draw_f) {
        var dataArray = new Array();
        var requests = 0;
        function draw_combined() {
            requests += 1;
            if (requests == days) {
                var combined = '';
                for (i=dataArray.length-1; i>-1; i--) {
                    combined += dataArray[i];
                }
                draw_f(combined);
            }
        }

        function get_data(d, i) {
            $.ajax({
                url: prefix + d + '.csv', 
                success: function(data) {
                    dataArray[i] = data;
                },
                complete: function(data) {
                    draw_combined();
                }
            });
        }

        for (i = 0, len = days; i < len; i += 1) {
            dataArray[i] = '';
            var date = new Date();
            date.setDate(date.getDate() - i);
            var d = $.datepicker.formatDate('yy.mm.dd', date);
            get_data(d, i);
        }
    }

    function getURLParameter(name) {
        return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
    }

    var days = getURLParameter('d');
    if (days == null) {
        days = 1;
    }

    draw_graph("", draw_speed);
    draw_graph("direction_", draw_direction);
});
