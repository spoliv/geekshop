// window.onload = function () {
//     $('.basket_list').on('click', 'input[type="number"]', function () {
//         var t_href = event.target;
//
//         $.ajax({
//             url: "/basket/edit/" + t_href.name + "/?quantity=" + t_href.value,
//         });
//
//         event.preventDefault();
//     });
// };

window.onload = function () {
    $('.basket_list').on('change', 'input[type="number"]', function (event) {
    // $(".basket_list input[type='number']").on("change", function (event) {
        var target = event.target;
        $.ajax({
            url: "/basket/edit/" + target.name + "/" + target.value + "/",
            success: function (data) {
                $('.basket_list').html(data.result);
            }
        });
    });
};