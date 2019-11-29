/* Javascript for SortableXBlock. */
function SortableXBlock(runtime, element) {

    function getItemsState(result) {
        var data = []
        $('.item', element).each(function(index, item){
            data.push($(item).data('position'));
        });

        return data
    }

    var handlerUrl = runtime.handlerUrl(element, 'submit_answer');

    $('#submit-answer', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify(getItemsState()),
            success: function(response) {
                var $message = $(element).find('.feedback .message');
                var $remaining_attempts = $(element).find('.feedback .remaining-attempts .count');
                $message.html(response.message);
                $remaining_attempts.html(response.remaining_attempts);
                if(response.correct) {
                    $message.addClass('correct');
                    $(element).find('#submit-answer').prop('disabled', true);
                } else {
                    $message.addClass('incorrect');
                    setTimeout(function(){ 
                        $message.hide();
                        $message.removeClass('incorrect');
                        $message.removeClass('correct');
                        $message.html('');
                    }, 4000);
                }
                if(response.remaining_attempts == 0) {
                    $(element).find('#submit-answer').prop('disabled', true);
                }
                $message.show();
            },
            error: function (request, status, error) {
                var $message = $(element).find('.feedback .message');
                $message.html(request.responseJSON.error);
                $message.addClass('error');
                $message.show();
                $(element).find('#submit-answer').prop('disabled', true);
                setTimeout(function(){ 
                    $message.hide();
                    $message.removeClass('error');
                    $message.html('');
                }, 4000);
            }
        });
    });

    $(function ($) {
        Sortable.create($('.items-list')[0]);
    });
}
