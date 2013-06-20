$('#btnAdd').click(function() {
    var num     = $('.clonedInput').length;
    var newNum  = new Number(num + 1);

    var newElem = $('#input' + num).clone().attr('id', 'input' + newNum);

    newElem.children(':first').attr('id', 'name' + newNum).attr('name', 'name' + newNum);
    $('#input' + num).after(newElem);
    $('#btnDel').attr('disabled','');

    if (newNum == 5)
        $('#btnAdd').attr('disabled','disabled');
});

$('#btnDel').click(function() {
    var num = $('.clonedInput').length;

    $('#input' + num).remove();
    $('#btnAdd').attr('disabled','');

    if (num-1 == 1)
        $('#btnDel').attr('disabled','disabled');
});

$('#btnDel').attr('disabled','disabled');