$(function () {
    hideFlash();

    var csrftoken = $('input[name=csrf_token]').val()
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });

    // password suggestion helper
    checkPasswordStrength();

    // complete todos
    $('.todo-complete').click(function () {
        var todoId = $(this).val()

        $.post("/complete-todo/" + todoId, function (todo) {
            if (todo.completed) {
                flash(todo.flash);
                return $('.todo-' + todoId).addClass('todo-completed');
            }

            flash(todo.flash, 'danger');
            return $('.todo-' + todoId).removeClass('todo-completed');
        })
    });

    function checkPasswordStrength() {
        var $input = $('#password');
        var message = document.getElementById('password-message');
        var strength = document.getElementById('password-strength');
        $input.keyup(function () {
            if (!$input.val()) {
                $input.removeClass('valid')
                $input.removeClass('invalid')
                strength.className = '';
                message.innerHTML = 'password is required';
                return;
            }
            var ret = safe($input.val());
            $input.addClass(ret.valid ? 'valid' : 'invalid');
            strength.className = ret.strength;
            message.innerHTML = ret.message;
        });
    }

    function flash(message, category = 'success') {
        showFlash(message, category);
        hideFlash();
    }

    function showFlash(message, category) {
        // remove previous messages
        $('.alert').remove()

        if (message == '') {
            return;
        }

        var flashHtml = "<div class='alert alert-" + category + " alert-dismissible fade in text-center' role=alert> \
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