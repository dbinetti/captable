$(document).ready(function ($) {

// Popover support
  $("[rel=popover]").popover({
    'placement':'bottom'
  });

    // nested tables
    function getChildren($row) {
        var children = [];
        while($row.next().hasClass('child')) {
             children.push($row.next());
             $row = $row.next();
        }
        return children;
    }

    $('.parent').on('click', function() {

        var children = getChildren($(this));
        $.each(children, function() {
            $(this).fadeToggle();
        })
    });

});