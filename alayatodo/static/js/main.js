$(function () {
    setTimeout(() => {
        $('.alert').alert('close')
    }, 10000);

    var csrftoken = $('input[name=csrf_token]').val()
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })

    // complete todos
    $('.todo-complete').click(function () {
        var todoId = $(this).val()

        $.post("/complete-todo/" + todoId, function (todo) {
            if (todo.completed) {
                return $('.todo-' + todoId).addClass('todo-completed');
            }

            return $('.todo-' + todoId).removeClass('todo-completed');
        })
    });
});