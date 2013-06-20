# jQuery Gridy - A Grid Plugin - http://wbotelhos.com/gridy

jQuery Gridy is a plugin that automatically generates a highly customizable grid using templates.

## License

The jQuery Gridy is licensed under [The MIT License](http://www.opensource.org/licenses/mit-license.php)

## Version

	@version         0.2.0
	@since           06.03.2011
	@author          Washington Botelho dos Santos
	@documentation   wbotelhos.com/gridy
	@twitter         twitter.com/wbotelhos
	@package         jQuery Plugins

## Default values

	arrowDown:         'arrow-down'                              // Class used as icon on the descending sort.
	arrowNone:         'arrow-none'                              // Class used as icon when there is no sort.
	arrowUp:           'arrow-up'                                // Class used as icon on the ascending sort.
	before:            null                                      // Function executed before the grid load.
	buttonBackTitle:   '&lsaquo; Back'                           // Title of the navigation button back.
	buttonMax:         '&lsaquo; Back'                           // Number of paging buttons visible.
	buttonNextTitle:   'Next &rsaquo;'                           // Title of the navigation button next.
	buttonOption:      true                                      // Shows the pagination buttons.
	buttonsWidth:      'auto'                                    // Width of the buttons wrapper.
	buttonTitle:       'page'                                    // Alternative text prepended on the page buttons.
	cache:             false                                     // Enables the ajax cache.
	clickFx:           false                                     // Enables rows selection on click.
	colsWidth:         []                                        // List with the width of each column of the grid.
	complete:          nul                                       // Function executed when the grid load.
	contentType:       'application/x-www-form-urlencoded; charset=utf-8' // The content type of the ajax request.
	dataType:          'json'                                    // The data type of the ajax request.
	debug:             false                                     // Shows details of the grid request.
	error:             null                                      // Function executed when occurs an error.
	find:              ''                                        // Name of the column where research will be done.
	findsName:         []                                        // List with the name of the columns for research.
	findTarget:        null                                      // ID of the place where the find element will be appended.
	headersName:       []                                        // List of the names used on the header element.
	headersWidth:      []                                        // Width of the columns of the header element.
	height:            'auto'                                    // Height of the grid.
	hoverFx:           false                                     // Enables highlight rows on mouseover.
	jsonp:             false                                     // Enables the JSONP content type.
	jsonpCallback:     'callback'                                // Name of the callback function for JSONP content type.
	loadingIcon:       'loading'                                 // Name of the class used as a loading icon.
	loadingOption:     true                                      // Enables the presentation of the loading message.
	loadingText:       Loading...                                // Text that will appear during the loading.
	messageOption:     true                                      // Enables the display of messages about the grid.
	messageTimer:      4000                                      // Time in milliseconds to keep the messages on screen.
	noResultOption:    true                                      // Enables the presentation of the no result message.
	noResultText:      No results found!                         // Text shown when no result is found for the search.
	page:              1                                         // Number o the page to be displayed.
	params:            ''                                        // Further parameters to be added to the query string.
	resultOption:      true                                      // Enables the presentation of details of the result.
	resultText:        'Displaying {from} - {to} of {total} items' // Text displayed in the details of the result.
	rows:              10                                        // Number of rows displayed on each page.
	rowsNumber:        [5, 10, 25, 50, 100] 	                 // List with the numbers of lines should be displayed.
	rowsTarget:        null                                      // ID of the place where the rows element will be appended.
	scroll:            false                                     // Enables the display of the grid with scroll.
	search:            ''                                        // Default term to be consulted.
	searchButtonLabel: 'search'                                  // Label of the search button.
	searchButtonTitle: 'Start the search'                        // Title of the search button.
	searchFocus:       true                                      // Enables the automatic focus in the search field.
	searchOption:      true                                      // Enables the search field. 
	searchText:        ''                                        // Text displayed in the search field.
	sortersName:       []                                        // List with the names used on the sorter element.
	sorterWidth:       'auto'                                    // Width of the sorter element.
	sortName:          ''                                        // Name of the default column sorted.
	sortOrder:         'asc'                                     // Order of classification.
	success:           null                                      // Function executed when the grid loads successfully.
	template:          'template'                                // The ID of the script template to be loaded.
	templateStyle:     'gridy-default'                           // Name of the template style "CSS prefix".
	type:              'get'                                     // Type of the HTTP request.
	url:               '/gridy'                                  // Url to request the data.
	width:             'auto'                                    // Width of the grid.


## Usage with default values

	$('#grid').gridy({ url: 'url/gridy' });
	
	<div id="grid"></div>
	
	<script id="template" type="text/x-jquery-tmpl">
	   <div>
	      <div>${name}</div>
	      <div>${email}</div>
	
	      <div class="gridy-button">
	         <a href="#">edit</a>
	      </div>
	   </div>
	</script>

## Public functions

You must pass a ID to be the target of the action:
	
	$.fn.gridy.reload('#grid', { scroll: true }); // Reload the grid. The second param changes the properties and is optional.

## Buy me a coffee

You can do it by [PayPal](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=X8HEP2878NDEG&item_name=jQuery%20Gridy). Thanks! (:

## Contributors

+ Gabriel Benz