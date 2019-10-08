$(document).ready(function () {
    $('#sex_tip').hide();
    $('#note_tip').hide();
    $('#tags_tip').hide();
    $('#sex').click(function () {
        $('#sex_tip').toggle(800);
    });
    $('#note').click(function () {
        $('#note_tip').toggle(800);
    });
    $('#tag').click(function () {
        $('#tags_tip').toggle(800);
    });
});

