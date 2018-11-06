
$(function() {
    $('button').click(function() {
        $.ajax({
            url: '/processImage',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                // console.log(response);

                $('#filtered_img_res').attr('src', `data:image/jpg;base64,${response}`);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});