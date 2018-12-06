$(function () {
    $('button#apply').click(function () {
        $.ajax({
            url: '/processImage',
            data: $('form').serialize(),
            type: 'POST',
            success: function (response) {
                console.log(response);
                $('#current_filter').text('Currently selected filter: ' +  $( "select#filters option:checked" ).val());
                $('#current_mask').text('Mask size: ' + $('#mask_size').val() + 'x' + $('#mask_size').val());
                $('#current_kvalue').text('k-Value: ' + $('#k_value').val());
                $('#current_threshold').text('threshold: ' + $('#threshold').val());
                $('#filtered_img_res').attr('src', `data:image/jpg;base64,${response}`);
                $('#img-download').attr('href', `data:image/jpg;base64,${response}`);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});
$(function() {
    $('select#filters').change(function() {
        selection = $(this).val();
        console.log($(this).val());
        if($(this).val() === 'unsharp_mask'){
            $('#k_value_row').show();
            $('#threshold_row').show();
        } else if ($(this).val() === 'first_order_deriv') {
            $('#threshold_row').show();
        }else {
            $('#k_value_row').hide();
            $('#threshold_row').hide();
        }
    });
});


// $(document).ready(function () {
//     $.ajax({
//         url: '/processImage',
//         data: $('form').serialize(),
//         type: 'POST',
//         success: function (response) {
//             // console.log(response);

//             $('#filtered_img_res').attr('src', `data:image/jpg;base64,${response}`);
//         },
//         error: function (error) {
//             console.log(error);
//         }
//     });
// });