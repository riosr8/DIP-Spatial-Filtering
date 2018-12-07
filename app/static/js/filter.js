
const k_value_row = '<div id="k_value_row" class="row" style="display:none;">' +
    '<div class="form-group col-xs-3">' +
    '<label for="k_value">Intensity Value (k)</label>' +
    '<input name="k_value" type="text" class="form-control" id="k_value" value="1" required>' +
    '</div>' +
    '<div class="col-xs-3"></div>' +
    '<div class="col-xs-6">' +
    '<p id="current_kvalue">No k value set.</p>' +
    '</div>' +
    '</div>';

const threshold_row = '<div id="threshold_row" class="row" style="display:none;">' +
    '<div class="form-group col-xs-3">' +
    '<label for="threshold">Threshold</label>' +
    '<input name="threshold" type="text" class="form-control" id="threshold" value="1" required>' +
    '</div>' +
    '<div class="col-xs-3"></div>' +
    '<div class="col-xs-6">' +
    '<p id="current_threshold">No threshold set.</p>' +
    '</div>' +
    '</div>';

function remove_existing_fields() {
    if ($('#k_value_row').length) {
        $('#k_value_row').remove();
    }

    if ($('#threshold_row').length) {
        $('#threshold_row').remove();
    }
}

$(function () {
    $('select#filters').change(function () {
        selection = $(this).val();
        console.log($(this).val());
        if ($(this).val() === 'unsharp_mask') {
            remove_existing_fields();
            $(k_value_row).insertAfter($('#mask_row'));
            $('#k_value_row').show();
            $(threshold_row).insertAfter($('#k_value_row'));
            $('#threshold_row').show();
        } else if ($(this).val() === 'first_order_deriv') {
            remove_existing_fields();
            $(threshold_row).insertAfter($('#mask_row'));
            $('#threshold_row').show();
        } else {
            $('#k_value_row').remove();
            $('#threshold_row').remove();
        }
    });
});



$.validator.setDefaults({
    submitHandler: function () {
        $('img#filtered_img_res').css('opacity', '0.1');
        $('div#img_spinner').addClass('spinner');
        $.ajax({
            url: '/processImage',
            data: $('form').serialize(),
            type: 'POST',
            success: function (response) {
                console.log(response);
                $('img#filtered_img_res').css('opacity', '1');
                $('div#img_spinner').removeClass('spinner')
                $('#current_filter').text('Currently selected filter: ' + $("select#filters option:checked").val());
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
    }
});

$(document).ready(function () {
    $('#k_value_row').remove();
    $('#threshold_row').remove();
    $("#filter_form").validate({
        rules: {
            mask_size: "required",
            k_value: {
                required: true,
                range: [1, 10]
            },
            threshold: {
                required: true,
                range: [0, 10]
            }
        },
        messages: {
            mask_size: 'Please enter an integer for mask size.',
            k_value: {
                required: 'Please enter an intensity value, k.',
                range: 'The k value must be in the range 1-10'
            },
            threshold: {
                required: "Please enter a threshold.",
                minlength: "The threshold must be in the range 0-10."
            }
        },
        errorElement: "em",
        errorPlacement: function (error, element) {
            // Add the `help-block` class to the error element
            error.addClass("help-block");

            // Add `has-feedback` class to the parent div.form-group
            // in order to add icons to inputs
            element.parents(".col-xs-3").addClass("has-feedback");

            if (element.prop("type") === "checkbox") {
                error.insertAfter(element.parent("label"));
            } else {
                error.insertAfter(element);
            }

            // Add the span element, if doesn't exists, and apply the icon classes to it.
            if (!element.next("span")[0]) {
                $("<span class='glyphicon glyphicon-remove form-control-feedback'></span>").insertAfter(element);
            }
        },
        success: function (label, element) {
            // Add the span element, if doesn't exists, and apply the icon classes to it.
            if (!$(element).next("span")[0]) {
                $("<span class='glyphicon glyphicon-ok form-control-feedback'></span>").insertAfter($(element));
            }
        },
        highlight: function (element, errorClass, validClass) {
            $(element).parents(".col-xs-3").addClass("has-error").removeClass("has-success");
            $(element).next("span").addClass("glyphicon-remove").removeClass("glyphicon-ok");
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).parents(".col-xs-3").addClass("has-success").removeClass("has-error");
            $(element).next("span").addClass("glyphicon-ok").removeClass("glyphicon-remove");
        }
    });
});
