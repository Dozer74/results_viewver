$(document).ready($ => {
    $("#slider").slider();
    $("#slider").on("slide", function (slideEvt) {
        $("#slider-value").text(slideEvt.value);

    });
});

