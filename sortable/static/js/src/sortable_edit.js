/* Javascript for SortableXBlockEdit. */
function SortableXBlockEdit(runtime, element) {
    var $element = $(element);

	function updateItemsOrder() {
		$('.item', element).each(function(index, item){
			$(item).find('.item-position').html(++index);
		});
	}

	function getItemsWithOrder() {
		var data = []
		$('.items-list-edit .item', element).each(function(index, item){
			var position = $(item).find('.item-position').html();
			var text = $(item).find('.item-text').html();

			data.push({'position': position, 'text': text});
		});

		return data
	}

    $element.on('click', '.remove-item', function() {
    	if($('.items-list-edit .item').length < 3) {
    		var $error = $element.find('.items-error');
    		setTimeout(function(){ $error.hide()}, 3000);
    		$error.show();
    		return;
    	}
        $(this).parent('.item').remove();
        updateItemsOrder();
    });

    $element.on('click', '#add-item', function() {
    	var itemHtml = '<div class="item"><span class="remove-item">&#10006;</span><span class="item-position"></span><span class="item-text" contenteditable="true">New item</span>';
        $('.items-list-edit', element).append(itemHtml);
        updateItemsOrder();
    });

    $element.find('.save-button').bind('click', function() {
        var data = {
            'display_name': $element.find('.display-name').val(),
            'max_attempts': $element.find(".max-attempts").val(),
            'question_text': $element.find('.question-text').val(),
            'show_problem_header': $element.find('.show-problem-header').is(':checked'),
            'item_background_color': $element.find('.item-background-color').val(),
            'item_text_color': $element.find('.item-text-color').val(),
            'data': getItemsWithOrder(),
        };

        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        runtime.notify('save', {state: 'start', message: "Saving"});
        $.post(handlerUrl, JSON.stringify(data), 'json').done(function(response) {
            if (response.result === 'success') {
                runtime.notify('save', {state: 'end'});
            } else {
                var message = response.messages.join(", ");
                runtime.notify('error', {
                    'title': "There was an error with your form.",
                    'message': message
                });
            }
        });
    });

    $element.find('.cancel-button').bind('click', function() {
        runtime.notify('cancel', {});
    });
}
