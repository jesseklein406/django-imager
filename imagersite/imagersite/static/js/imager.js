// Event Listener for Collapsible menu button
$('#navbar-toggle').on('click', function (e) {
    e.preventDefault();
    $('#navbar-collapse').toggleClass('collapse');
});
