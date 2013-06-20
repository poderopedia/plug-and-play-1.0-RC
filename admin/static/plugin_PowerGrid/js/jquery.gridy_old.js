/*!
 * jQuery Gridy - A Grid Plugin - http://wbotelhos.com/gridy
 * ---------------------------------------------------------------------------------
 *
 * jQuery Gridy is a plugin that generates a highly customizable grid automatically.
 *
 * Licensed under The MIT License
 *
 * @version         0.2.0
 * @since           06.03.2011
 * @author          Washington Botelho dos Santos
 * @documentation   wbotelhos.com/gridy
 * @twitter         twitter.com/wbotelhos
 * @license         opensource.org/licenses/mit-license.php
 * @package         jQuery Plugins
 *
 * Usage with default values:
 * ---------------------------------------------------------------------------------
 * $('#grid').gridy({ url: 'url/gridy' });
 *
 * <div id="grid"></div>
 *
 * <script id="template" type="text/x-jquery-tmpl">
 *    <div>
 *       <div>${name}</div>
 *       <div>${email}</div>
 *
 *       <div class="gridy-button">
 *          <a href="#">edit</a>
 *       </div>
 *    </div>
 * </script>
 *
 */

;(function($) {

	var methods = {
		init: function(settings) {
			
		}, getSize: function(size) {
			return (isNaN(parseInt(size))) ? size : size + 'px';
		}, getNumber: function(number) {
			return (number < 10) ? '0' + number : number;
		}, getError: function(xhr) {
			return (xhr.responseText) ? xhr.responseText.substring(xhr.responseText.indexOf('(') + 1, xhr.responseText.indexOf(')')) : xhr.statusText;
		}, getNumber: function(number) {
			return (number < 10) ? '0' + number : number;
		}, debug: function(message) {
			if (window.console && window.console.log) {
				window.console.log(message);
			}
		}
	};

	$.fn.gridy = function(settings) {

		if (this.length == 0) {
			methods.debug('Selector invalid or missing!');
			return;
		} else if (this.length > 1) {
			return this.each(function() {
				$.fn.gridy.apply($(this), [settings]);
			});
		}

		var opt					= $.extend({}, $.fn.gridy.defaults, settings),
			id					= this.attr('id'),
			$this				= $(this).empty(),
			$currentPage		= $('<input id="current-page" type="hidden" value="' + opt.page + '"/>').appendTo($this),
			$currentSortName	= $('<input id="current-sort-name" type="hidden" value="' + opt.sortName + '"/>').appendTo($this),
			$currentSortOrder	= $('<input id="current-sort-order" type="hidden" value="' + opt.sortOrder + '"/>').appendTo($this);

		if (id === undefined) {
			id = 'gridy-' + $this.index();
			$this.attr('id', id); 
		}

		$this.addClass(opt.templateStyle).data('options', opt);

		var $searchField	= null,
			$searchButton	= null;

		if (opt.searchOption) {
			var $searchWrapper = $('<div class="gridy-search"/>').appendTo($this);

			$searchField = $('<input id="search" type="text" size="40" value="' + ((opt.search == '') ? opt.searchText : opt.search) + '" title="' + opt.searchText + '"/>').appendTo($searchWrapper);

			$searchField.blur(function() {
				if ($searchField.val() == '') {
					$searchField.removeClass('gridy-typed').val(opt.searchText);
				}
			}).focus(function() {
				if ($searchField.val() == opt.searchText) {
					$searchField.addClass('gridy-typed').val('');
				}
			}).keypress(function(evt) {
				if ((evt.keyCode ? evt.keyCode : evt.which) == 13) {
					listGridy(1, $currentSortName.val(), $currentSortOrder.val());
				}
			});

			$searchButton = $('<input type="button" value="' + opt.searchButtonLabel + '" title="' + opt.searchButtonTitle + '"/>').appendTo($searchWrapper);

			$searchButton.click(function() {
				listGridy(1, $currentSortName.val(), $currentSortOrder.val());
			});
		}

		function changeSortIndicator(clickedLink, sortOrder, sortIcon, isResetIcon) {
			var $sortWrapper	= clickedLink.parent().parent(),
				isHeader		= opt.headersName.length > 0 && $sortWrapper.attr('class') == 'gridy-header';

			if (isResetIcon) {
				var $sortedLink = $sortWrapper.find('a.gridy-sorted').attr('rel', 'desc').removeClass('gridy-sorted');

				$sortedLink = (isHeader) ? $sortedLink.next('div') : $sortedLink.prev('div');

				$sortedLink.removeClass().addClass(opt.arrowNone);
			}

			clickedLink.attr('rel', sortOrder).addClass('gridy-sorted');

			var $sortIcon = (isHeader) ? clickedLink.next('div') : clickedLink.prev('div');

			$sortIcon.removeClass().addClass(sortIcon);
		};

		var $sortBar		= null,
			$sorterItems	= null;

		if (opt.sortersName.length > 0) {
			var sorterContent	= '',
				sorterItem		= '',
				sorterLabel		= '';

			for (var i = 0; i < opt.sortersName.length; i++) {
				sorterItem = opt.sortersName[i][0];
				sorterLabel = opt.sortersName[i][1];

				sorterContent +=
						'<div class="gridy-sorter-item">' +
							'<div class="' + opt.arrowNone + '"></div>' +
							'<a id="sort-by-' + sorterItem + '" href="javascript:void(0);" name="' + sorterItem + '" rel="desc">' + sorterLabel + '</a>' +
						'</div>';
			}

			$sortBar = $('<div class="gridy-sorter-bar"/>').css('width', methods.getSize(opt.sorterWidth)).html(sorterContent).appendTo($this);

			$sorterItems = $sortBar.children().delegate('a', 'click', sortGridyFunction);

			var $sortInit = $sorterItems.find('a#sort-by-' + opt.sortName);

			if ($sortInit.length) {
				var sortIcon	= (opt.sortOrder == 'asc') ? opt.arrowUp : opt.arrowDown,
					isResetIcon	= false;
	
				changeSortIndicator($sortInit, opt.sortOrder, sortIcon, isResetIcon);
			}
		}

		function sortGridyFunction() {
			sortGridy($(this));
		};

		function sortGridy(clickedLink) {
			var sortName		= clickedLink.attr('name'),
				sortOrder		= clickedLink.attr('rel'),
				nextSortOrder	= (sortOrder == 'desc') ? 'asc' : 'desc',
				sortIcon		= (sortOrder == 'desc') ? opt.arrowUp : opt.arrowDown,
				isResetIcon		= clickedLink.parent().parent().find('a.gridy-sorted').length > 0;

			changeSortIndicator(clickedLink, nextSortOrder, sortIcon, isResetIcon);

			listGridy($currentPage.val(), sortName, nextSortOrder);
		};

		var $loading = null;

		if (opt.loadingOption) {
			$loading = $('<div class="' + opt.loadingIcon + '"><div>' + opt.loadingText + '</div></div>').appendTo($this).children();
		}

		var $result = null;

		if (opt.resultOption) {
			$result = $('<div class="gridy-result"/>').appendTo($this);
		}

		var $header			= null,
			$headerItems	= null;

		if (opt.headersName.length > 0) {
			$header = $('<div class="gridy-header"/>').appendTo($this);

			var $head		= null,
				$sortLink	= null,
				headName	= '',
				headLabel	= '';

			if (opt.headersWidth.length <= 0) {
				if (opt.colsWidth.length > 0) {
					opt.headersWidth = opt.colsWidth;
				} else {
					methods.debug(id + ': headersWith and colsWidth attributes invalid or missing!');
					return;
				}
			}

			for (var i = 0; i < opt.headersName.length; i++) {
				headName = opt.headersName[i][0];
				headLabel = opt.headersName[i][1];

				$sortLink = $('<a/>', { href: 'javascript:void(0);', html: headLabel });

				$head = $('<div class="gridy-head-item"/>');

				if (headName) {
					$sortLink.attr({ id: 'sort-by-' + headName, name: headName, rel: 'desc' });

					var $sortIcon = $('<div/>', { 'class': opt.arrowNone });

					$head.append($sortLink, $sortIcon);
				} else {
					$sortLink.attr('class', 'gridy-no-sort');
					$head.append($sortLink);
				}

				if (opt.headersName[i][2]) {
					$head.addClass(opt.headersName[i][2]);
				}

				$head.css('width', opt.headersWidth[i]).appendTo($header);
			}

			$headerItems = $header.children().delegate('a:not(".gridy-no-sort")', 'click', sortGridyFunction);

			var $sortInit = $('div.gridy-header a#sort-by-' + opt.sortName);

			if ($sortInit.length) {
				var sortIcon	= (opt.sortOrder == 'asc') ? opt.arrowUp : opt.arrowDown,
					isResetIcon	= false;

				changeSortIndicator($sortInit, opt.sortOrder, sortIcon, isResetIcon);
			}
		}

		var $content = $('<div class="gridy-content"/>').css({ 'height': methods.getSize(opt.height), 'width': methods.getSize(opt.width) }).appendTo($this);

		function startLoading(isStart) {
			if (opt.loadingOption) {
				if (isStart) {
					$loading.fadeIn('fast');
					$content.addClass('gridy-fade');
				} else {
					$loading.fadeOut();
					$content.removeClass('gridy-fade');
				}
			}
		};

		function showNoResult() {
			if (opt.noResultOption) {
				$content.html('<p class="gridy-no-result">' + opt.noResultText + '</p>');
	
				if (opt.resultOption) {
					$result.html($result.html().replace(/\d+/g, '--'));
				}
	
				if (opt.searchOption) {
					$searchField.focus().select();
				}
			}
		};

		var $footerBar = null;

		if (opt.findsName.length > 0 || opt.rowsNumber.length > 0  || opt.messageOption) {
			$footerBar = $('<div class="gridy-footer"/>').css('width', methods.getSize(opt.width)).appendTo($this);
		}

		var $findBox = null;

		if (opt.findsName.length > 0) {
			$findBox = $('<div class="gridy-find-option"><select></select></div>').appendTo($footerBar).children();

			var hasItem		= false,
				options		= '',
				findItem	= '',
				findLabel	= '';

			for (var i = 0; i < opt.findsName.length; i++) {
				findItem = opt.findsName[i][0];
				findLabel = opt.findsName[i][1];

				options += '<option value="' + findItem + '">' + findLabel + '</option>';

				if (findItem == opt.find) {
					hasItem = true;
				}
			}

			if (!hasItem) {
				$findBox.html('<option value="' + opt.find + '" checked="checked">' + opt.find + '</option>');
			}

			$findBox.append(options).val(opt.find).change().change(function(index, value) {
				if (opt.searchOption && opt.searchFocus) {
					$searchField.focus();
				}
			})
			.children('option[value="' + opt.find +  '"]').attr('checked', 'checked');
		}

		var $rowsBox = null;

		if (opt.rowsNumber.length > 0 ) {
			$rowsBox = $('<div class="gridy-row-option"><select></select></div>').appendTo($footerBar).children();

			var rows		= (opt.rows < 1) ? 1 : opt.rows,
				hasNumber	= false,
				options		= '',
				number		= '';

			for (var i = 0; i < opt.rowsNumber.length; i++) {
				number = opt.rowsNumber[i];

				if (number == rows) {
					hasNumber = true;
				}

				options += '<option value="' + number + '">' + methods.getNumber(number) + '</option>';
			}

			if (!hasNumber) {
				$rowsBox.html('<option value="' + rows + '" checked="checked">' + methods.getNumber(rows) + '</option>');
			}

			$rowsBox.append(options).val(rows).change().change(function(index, value) {
				listGridy(1, $currentSortName.val(), $currentSortOrder.val());
			})
			.children('option[value="' + rows +  '"]').attr('checked', 'checked');
		}

		if (opt.searchTarget) {
			$searchField.parent().appendTo(opt.searchTarget);
		}

		if (opt.findTarget) {
			$findBox.parent().appendTo(opt.findTarget);
		}

		if (opt.rowsTarget) {
			$rowsBox.parent().appendTo(opt.rowsTarget);
		}		

		var $buttons = null;
		
		if (opt.buttonOption) {
			$buttons = $('<div class="gridy-buttons"/>').css('width', methods.getSize(opt.buttonsWidth)).appendTo($this);
		}

		var $message = null;

		if (opt.messageOption) {
			$message = $('<div class="gridy-message"/>').appendTo($footerBar);
		}

		function showMessage(message) {
			if (opt.messageOption) {
				$message.html(message).show();

				setTimeout(function() {
					$message.fadeOut();
				}, opt.messageTimer);
			}
		};

		listGridy(opt.page, opt.sortName, opt.sortOrder);

		function enableGrid(isEnable) {
			if (isEnable) {
				if (opt.searchOption) {
					$searchField.removeAttr('readonly');
					$searchButton.removeAttr('disabled');
				}

				if (opt.sortersName.length > 0) {
					$sorterItems.delegate('a', 'click', sortGridyFunction);
					$headerItems.delegate('a:not(".gridy-no-sort")', 'click', sortGridyFunction);
				}

				if (opt.buttonOption) { $buttons.children().removeAttr('disabled'); }
				if (opt.findsName.length > 0) { $findBox.removeAttr('disabled'); }
				if (opt.rowsNumber.length > 0 ) { $rowsBox.removeAttr('disabled'); }
			} else {
				if (opt.searchOption) {
					$searchField.attr('readonly', 'readonly');
					$searchButton.attr('disabled', 'disabled');
				}

				if (opt.sortersName.length > 0) {
					$sorterItems.undelegate('a', 'click');
					$headerItems.undelegate('a:not(".gridy-no-sort")', 'click');
				}

				if (opt.buttonOption) { $buttons.children().attr('disabled', 'disabled'); }
				if (opt.findsName.length > 0) { $findBox.attr('disabled', 'disabled'); }
				if (opt.rowsNumber.length > 0 ) { $rowsBox.attr('disabled', 'disabled'); }
			}
		};

		function processCallback(wrapper, page, sortName, sortOrder, selectedRows) {
			if (typeof(wrapper) == 'string') {
				wrapper = $.parseJSON(wrapper);
			}

			if (opt.before) {
				var callback = opt.before.apply($this, [wrapper, page, sortName, sortOrder]);

				if (callback) {
					wrapper = callback;
				}
			}

			if (wrapper.total == 0) {
				showNoResult();
				enableGrid(true);
				return;
			} else {
				if (opt.sortersName.length > 0) {
					$sortBar.show();
				}
			}

			var entityList	= wrapper.entityList;

			$content.html($('#' + opt.template).tmpl(entityList));

			if (opt.colsWidth) {
				$content.children('div').addClass('gridy-row').each(function() {
					$(this).children('div').addClass('gridy-column').each(function(index) {
						$(this).width(opt.colsWidth[index]);
					});
				});
			}

			var rest		= wrapper.total % selectedRows,
				totalPage	= (wrapper.total - rest) / selectedRows;

			if (rest > 0) {
				totalPage++;
			};

			if (opt.resultOption) {
				var resultText = opt.resultText.replace(/{from}/, methods.getNumber(page)).replace(/{to}/, methods.getNumber(totalPage)).replace(/{total}/, methods.getNumber(wrapper.total));

				$result.html(resultText);
			}

			if (opt.buttonOption) {
				if (wrapper.total > selectedRows) {
					var buttonEmpty	= '<input type="button" value="..." disabled="disabled" class="gridy-empty"/>&nbsp;',
						buttons		= '',
						number		= 0,
						rangePage	= null,
						start		= 1,
						buttonMax	= opt.buttonMax,
						isEven		= (opt.buttonMax % 2 == 0);

					if (opt.buttonMax > totalPage) {
						buttonMax = totalPage;
					} else {
						buttonMax = opt.buttonMax;
					}

					if (isEven) {
						rangePage	= Math.ceil(buttonMax / 2);
						start		= page - rangePage + 1;
					} else {
						rangePage	= Math.floor(buttonMax / 2);
						start		= page - rangePage;
					}

					var end = parseInt(page) + rangePage;

					if (start == 0) {
						end++;
						start = 1;
					}

					if (start < 0) {
						end += Math.abs(start) + 1; // + 1 is the button 0.
						start = 1;
					}

					if (end > totalPage) {
						if (start > 1) {
							start -= (end - totalPage);
						}

						end = totalPage;
					}

					var	hasExceeded			= totalPage > buttonMax,
						hasBackNavigation	= hasExceeded && page > ((isEven) ? rangePage : rangePage + 1),
						hasNextNavigation	= hasExceeded && page < (totalPage - rangePage);

					if (hasBackNavigation) {
						buttons = '<input type="button" value="&lsaquo;" alt="' + opt.buttonBackTitle + '" title="' + opt.buttonBackTitle + '" class="gridy-back"/>&nbsp;';
						buttons += buttonEmpty;
					}

					for (var i = start; i <= end; i++) {
						number = methods.getNumber(i);
						buttons += '<input type="button" value="' + number + '" alt="' + number + '" title="' + opt.buttonTitle + ' ' + number + '"/>&nbsp;';
					}

					if (hasNextNavigation) {
						buttons += buttonEmpty;
						buttons += '<input type="button" value="&rsaquo;" alt="' + opt.buttonNextTitle + '" title="' + opt.buttonNextTitle + '" class="gridy-next"/>&nbsp;';
					}

					$buttons.html(buttons).children(':not(".gridy-empty")').click(function() {
						listGridy(parseInt(this.alt, 10), $currentSortName.val(), $currentSortOrder.val());
					});

					if (hasBackNavigation) {
						$buttons.children('.gridy-back').click(function() {
							listGridy(page - 1, $currentSortName.val(), $currentSortOrder.val());
						});
					}

					if (hasNextNavigation) {
						$buttons.children('.gridy-next').click(function() {
							listGridy(page + 1, $currentSortName.val(), $currentSortOrder.val());
						});
					}
				} else {
					$buttons.empty();
				}

				$('input[value="' + methods.getNumber(page) + '"]').attr('disabled', 'disabled').addClass('gridy-active');
			}

			enableGrid(true);

			$currentPage.val(page);
			$currentSortName.val(sortName);
			$currentSortOrder.val(sortOrder);
		};

		function listGridy(page, sortName, sortOrder) {
			enableGrid(false);
			startLoading(true);

			var search			= opt.search,
				selectedRows	= (opt.rowsNumber.length > 0 ) ? $rowsBox.val() : opt.rows,
				selectedFind	= (opt.findsName.length > 0) ? $findBox.val() : opt.find;

			if (opt.searchOption) {
				search = ($searchField.val() == opt.searchText) ? '' : $searchField.val();

				if (opt.searchFocus) {
					$searchField.focus();
				}
			}

			if (opt.data != null) {
				processCallback(opt.data, page, sortName, sortOrder);
				return;
			}

			if (opt.debug) {
				methods.debug('query string: search=' + search + '&page=' + page + '&sortName=' + sortName + '&sortOrder=' + sortOrder + '&find=' + selectedFind + '&rows=' + selectedRows + opt.params);
			}

			$.ajax({
				cache:			opt.cache,
				contentType:	opt.contentType,
				dataType:		opt.dataType,
				jsonp:			opt.jsonp,
				jsonpCallback:	opt.jsonpCallback,
				type:			opt.type,
				url:			opt.url,
				data:			'search=' + search + '&page=' + page + '&sortName=' + sortName + '&sortOrder=' + sortOrder + '&find=' + selectedFind + '&rows=' + selectedRows + opt.params,
				success: function(wrapper) {
					processCallback(wrapper, page, sortName, sortOrder, selectedRows);

					var scrollSufix = (opt.scroll) ? '-scroll' : '';

					if (opt.hoverFx) {
						$content.children().mouseenter(function() {
							$(this).addClass('gridy-item-hover' + scrollSufix);
						}).mouseleave(function() {
							$(this).removeClass('gridy-item-hover' + scrollSufix);
						});
					}

					if (opt.clickFx) {
						$content.children().click(function(evt) {
							var $this = $(this);

							if (!evt.shiftKey) {
								$this.parent().children('div.gridy-item-active' + scrollSufix).removeClass('gridy-item-active' + scrollSufix);
							}

							$this.toggleClass('gridy-item-active' + scrollSufix);
						});
					}

					if (opt.success) {
						opt.success();
					}
				}, error: function(xhr, status, error) {
					showMessage(methods.getError(xhr));

					if (opt.error) {
						opt.error();
					}
				}, complete: function() {
					startLoading(false);

					if (opt.scroll) {
						if (opt.height == 'auto') {
							methods.debug(id + ': height attribute missing!');
						}

						$content
						.css({ 'border': '1px solid #BBB', 'overflow': 'auto' })
							.children('div').addClass('gridy-scroll')
						.end()
							.children('div:last').css('border-bottom-color', '#FFF');
					}

					if (opt.complete) {
						opt.complete();
					}
				}
			});
		};

		return $this;
	};

	$.fn.gridy.reload = function(id, settings) {
		var $context	= $(id),
			options		= $context.data('options');

		if (settings !== undefined) {
			$.each(settings, function(attribute, value) {
				if (options[attribute] === undefined) {
					methods.debug('\'' + attribute + '\' is an invalid attribute!');
				} else {
					if (value != options[attribute]) {
						options[attribute] = value;
					}
				}
			});

			$context.data('options', options);
		}

		return $context.gridy(options);
	};

	$.fn.gridy.defaults = {
		arrowDown:			'gridy-arrow-down',
		arrowNone:			'gridy-arrow-none',
		arrowUp:			'gridy-arrow-up',
		before:				null,
		buttonBackTitle:	'&lsaquo; Back',
		buttonMax:			10,
		buttonNextTitle:	'Next &rsaquo;',
		buttonOption:		true,
		buttonsWidth:		'auto',
		buttonTitle:		'page',
		cache:				false,
		clickFx:			false,
		colsWidth:			[],
		complete:			null,
		contentType:		'application/x-www-form-urlencoded; charset=utf-8',
		dataType:			'json',
		debug:				false,
		error: 				null,
		find:				'',
		findsName:			[],
		findTarget:			null,
		headersName:		[],
		headersWidth:		[],
		height:				'auto',
		hoverFx:			false,
		jsonp:				false,
		jsonpCallback:		'callback',
		loadingIcon:		'gridy-loading',
		loadingOption:		true,
		loadingText:		'Loading...',
		messageOption:		true,
		messageTimer:		4000,
		noResultOption:		true,
		noResultText:		'No items found!',
		page:				1,
		params: 			'',
		resultOption:		true,
		resultText:			'Displaying {from} - {to} of {total} items',
		rows:				10,
		rowsNumber:			[5, 10, 25, 50, 100],
		rowsTarget:			null,
		scroll:				false,
		search:				'',
		searchButtonLabel:	'search',
		searchButtonTitle:	'Start the search',
		searchFocus:		true,
		searchOption:		true,
		searchTarget:		null,
		searchText:			'',
		sortersName:		[],
		sorterWidth:		'auto',
		sortName:			'',
		sortOrder:			'asc',
		success:			null,
		template:			'template',
		templateStyle:		'gridy-default',
		type:				'get',
		url:				'/gridy',
		width:				'auto'
	};

})(jQuery);