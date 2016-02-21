$(function() {
    $("#searchbox").keyup(function () {
        var term = $("#searchbox").val();
        $.get("search", {term:term}, function (data) {
            $("#search-suggestions").html(data);
        });
    });
});
