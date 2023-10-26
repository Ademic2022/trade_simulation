// Wait for the document to be ready
var dimmer = $("#myDimmer"); // Replace "myDimmer" with the actual ID of your dimmer

// Check if the page has finished loading
$(window).on("load", function () {

  setTimeout(function () {
    // Remove the "active" class from the dimmer
    dimmer.removeClass("active");
  }, 1000);

});
$(document)
    .ready(function() {

      // fix menu when passed
      $('.masthead')
        .visibility({
          once: false,
          onBottomPassed: function() {
            $('.fixed.menu').transition('fade in');
          },
          onBottomPassedReverse: function() {
            $('.fixed.menu').transition('fade out');
          }
        })
      ;

      // create sidebar and attach to menu open
      $('.ui.sidebar')
        .sidebar('attach events', '.toc.item')
      ;
      
});
$('.message .close')
  .on('click', function() {
    $(this)
      .closest('.message')
      .transition('fade')
    ;
  })
;

