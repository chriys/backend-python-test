$(function () {
    hideFlash();

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
                flash(todo.flash);
                return $('.todo-' + todoId).addClass('todo-completed');
            }

            flash(todo.flash);
            return $('.todo-' + todoId).removeClass('todo-completed');
        })
    });

    function flash(message) {
        showFlash(message);
        hideFlash();
    }

    function showFlash(message) {
        // remove previous messages
        $('.alert').remove()

        if (message == '') {
            return;
        }

        var flashHtml = "<div class='alert alert-success alert-dismissible fade in text-center' role=alert> \
            <button type=button class=close data-dismiss=alert aria-label=Close><span aria-hidden=true>&times;</span></button> \
            <span class='flash-message'>" + message + "</span></div>";

        // insert the message html
        $('.navbar').after(flashHtml);
        $('.alert').alert();
    }

    function hideFlash() {
        setTimeout(() => {
            $('.alert').alert('close')
        }, 5000);
    }
});