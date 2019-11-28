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
                alert(response.correct);
            }
        });
    });

    $(function ($) {
        $('.items-list').sortable();

    });
}
