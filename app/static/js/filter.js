
const k_value_row = '<div id="k_value_row" class="row" style="display:none;">' +
    '<div class="row">' +
    '<div class="col-md-7">' +
    '<div class="form-group">' +
    '<label for="k_value">Intensity Value (k)</label>' +
    '<div>' +
    '<div class="col-md-6 filter_form_input">' +
    '<input name="k_value" type="text" class="form-control" id="k_value" value="1" required>' +
    '</div>' +
    '</div>' +
    '</div>' +
    '</div>' +
    '<div class="col-md-5">' +
    '<p id="current_kvalue">No k value set.</p>' +
    '</div>' +
    '</div>' +
    '</div>';

const threshold_row = '<div id="threshold_row" class="row" style="display:none;">' +
    '<div class="row">' +
    '<div class="col-md-7">' +
    '<div class="form-group">' +
    '<label for="threshold">Threshold</label>' +
    '<div>' +
    '<div class="col-md-6 filter_form_input">' +
    '<input name="threshold" type="text" class="form-control" id="threshold" value="1" required>' +
    '</div>' +
    '</div>' +
    '</div>' +
    '</div>' +
    '<div class="col-md-5">' +
    '<p id="current_threshold">No threshold set.</p>' +
    '</div>' +
    '</div>' +
    '</div>';

const filters_with_odd_masks = ['guass_smoothing',
                                'unsharp_mask',
                                'laplacian_pos_zero',
                                'laplacian_pos_nonzero',
                                'laplacian_neg_zero',
                                'laplacian_neg_nonzero'
                                ];

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
        } else if ($(this).val() === 'first_order_sobel') {
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
                // console.log(response);
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

$.validator.addMethod('check_mask_size_input', function (value, element) {
    const selected_filter = $('select#filters').val();
    const input = parseInt(value);
    if (isNaN(input)) {
        return false;
    }

    if (input < 2) {
        return false;
    }

    if (filters_with_odd_masks.includes(selected_filter)) {
        if (input % 2 === 0) {
            return false;
        } else {
            return true;
        }
    } else {
        return true;
    }
}, 'Input for your selected filter must be an odd integer.');

$(document).ready(function () {
    $("#filter_form").validate({
        rules: {
            mask_size: {
                required: true,
                check_mask_size_input: true
            },
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
            mask_size: {
                required: 'Please enter an integer for mask size.',
                check_mask_size_input: 'Input for your selected filter must be an odd integer or >= 2.'
            },
            k_value: {
                required: 'Please enter an intensity value, k.',
                range: 'The k value must be in the range 1-10'
            },
            threshold: {
                required: "Please enter a threshold.",
                range: "The threshold must be in the range 0-10."
            }
        },
        errorElement: "em",
        errorPlacement: function (error, element) {
            // Add the `help-block` class to the error element
            error.addClass("help-block");

            // Add `has-feedback` class to the parent div.form-group
            // in order to add icons to inputs
            element.parents(".col-md-6").addClass("has-feedback");

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
            $(element).parents(".col-md-6").addClass("has-error").removeClass("has-success");
            $(element).next("span").addClass("glyphicon-remove").removeClass("glyphicon-ok");
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).parents(".col-md-6").addClass("has-success").removeClass("has-error");
            $(element).next("span").addClass("glyphicon-ok").removeClass("glyphicon-remove");
        }
    });
});
