/**
 * Created with PyCharm.
 * User: Evolutiva
 * Date: 10-05-13
 * Time: 11:41 AM
 * To change this template use File | Settings | File Templates.
 */

  $(function() {
    $( "#slider-vertical" ).slider({
      orientation: "vertical",
      range: "min",
      min: 0.5,
      max: 8,
      value: 1,
      slide: function( event, ui ) {
        $( "#amount" ).val( ui.value );
      }
    });
    $( "#amount" ).val( $( "#slider-vertical" ).slider( "value" ) );
  });

