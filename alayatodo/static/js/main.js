$(function () {
    setTimeout(() => {
        $('.alert').alert('close')
    }, 10000);

    // complete todos
    $('.complete').click(function () {
        // $('form').submit();
        console.log('call ajax')
    });
});