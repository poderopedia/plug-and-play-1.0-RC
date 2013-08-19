$ = jQuery;

var vis = $('svg g ');

zoom = d3.behavior.zoom();

function redraw() {
  vis.attr("transform",
      "translate(" + d3.event.translate + ")"
      + " scale(" + d3.event.scale + ")");
}

function get_current_view_params() {
  var params = $('svg g').attr('transform');
  if(!params) {
    return new Array(0, 0, 1);
  } else {
    params = params.match(/translate\(([^,]*),([^,]*)\) scale\((.*)\)/);
    params.shift();
    return params;
  }
}

//$('.zoom-in').click(function() {
//  if(typeof _gaq != 'undefined') _gaq.push(['_trackEvent', 'graph', 'zoom', 'in']);
//  var params = get_current_view_params();
//  console.log(params)
//  vis.attr('transform', 'translate(' + params[0] + ',' + params[1] + ') scale(' + parseFloat(params[2]) * 1.2 + ')');
//  zoom.translate([params[0], params[1]]).scale(params[2] * 1.2);
//  console.log(vis)
//});

$('.zoom-out').click(function() {
  if(typeof _gaq != 'undefined') _gaq.push(['_trackEvent', 'graph', 'zoom', 'out']);
  var params = get_current_view_params();
    console.log(params)
  vis.attr('transform', 'translate(' + params[0] + ',' + params[1] + ') scale(' + parseFloat(params[2]) / 1.2 + ')');
  zoom.translate([params[0], params[1]]).scale(params[2] / 1.2);
});

$('.zoom-reset').click(function() {
  // unset all nodes' positions, reset translation/scale
  if(typeof _gaq != 'undefined') _gaq.push(['_trackEvent', 'graph', 'reset', 'reset']);
  deselect();
  var n, ax=0, ay=0, ar=0;
  for(var i=0; i<all_nodes.length; i++) {
    n = all_nodes[i];
    delete n.fixed;
    if(n.node_type == 'root') {
      ar++;
      ax += n.x;
      ay += n.y;
    }
  }
  ax = bb2.width / 2 - ax / ar;
  ay = bb2.height / 2 - ay / ar;
  vis.attr('transform', 'translate(' + ax + ',' + ay + ') scale(1)');
  zoom.translate([ax, ay]).scale(1);
});


