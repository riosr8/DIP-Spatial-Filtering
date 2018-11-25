$(function () {
    $('button').click(function () {
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
            },
            error: function (error) {
                console.log(error);
            }
        });
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