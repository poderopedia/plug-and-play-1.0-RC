/* Time between each scrolling frame */
jQuery.fn.dataTableExt.oPagination.iTweenTime = 100;
 
jQuery.fn.dataTableExt.oPagination.scrolling = {
	"fnInit": function ( oSettings, nPaging, fnCallbackDraw )
	{
		/* Store the next and previous elements in the oSettings object as they can be very
		 * usful for automation - particularly testing
		 */
		var nPrevious = document.createElement( 'div' );
		var nNext = document.createElement( 'div' );
		
                //oSettings.sTableId = '1'
		if ( oSettings.sTableId !== '' )
		{
			nPaging.setAttribute( 'id', oSettings.sTableId+'_paginate' );
			nPrevious.setAttribute( 'id', oSettings.sTableId+'_previous' );
			nNext.setAttribute( 'id', oSettings.sTableId+'_next' );
		} else {
		
                    nPaging.setAttribute( 'id', 'paginate' );
		    nPrevious.setAttribute( 'id', 'previous' );
		    nNext.setAttribute( 'id', 'next' );
                }
		nPrevious.className = "paginate_disabled_previous";
		nNext.className = "paginate_disabled_next";
		
		nPrevious.title = oSettings.oLanguage.oPaginate.sPrevious;
		nNext.title = oSettings.oLanguage.oPaginate.sNext;
		
		nPaging.appendChild( nPrevious );
		nPaging.appendChild( nNext );
		
		jQuery(nPrevious).click( function() {
			/* Disallow paging event during a current paging event */
			if ( typeof oSettings.iPagingLoopStart != 'undefined' && oSettings.iPagingLoopStart != -1 )
			{
				return;
			}
			
			oSettings.iPagingLoopStart = oSettings._iDisplayStart;
			oSettings.iPagingEnd = oSettings._iDisplayStart - oSettings._iDisplayLength;
			
			/* Correct for underrun */
			if ( oSettings.iPagingEnd < 0 )
			{
			  oSettings.iPagingEnd = 0;
			}
			
			var iTween = jQuery.fn.dataTableExt.oPagination.iTweenTime;
			var innerLoop = function () {
				if ( oSettings.iPagingLoopStart > oSettings.iPagingEnd ) {
					oSettings.iPagingLoopStart--;
					oSettings._iDisplayStart = oSettings.iPagingLoopStart;
					fnCallbackDraw( oSettings );
					setTimeout( function() { innerLoop(); }, iTween );
				} else {
					oSettings.iPagingLoopStart = -1;
				}
			};
			innerLoop();
		} );
		
		jQuery(nNext).click( function() {
			/* Disallow paging event during a current paging event */
			if ( typeof oSettings.iPagingLoopStart != 'undefined' && oSettings.iPagingLoopStart != -1 )
			{
				return;
			}
			
			oSettings.iPagingLoopStart = oSettings._iDisplayStart;
			
			/* Make sure we are not over running the display array */
			if ( oSettings._iDisplayStart + oSettings._iDisplayLength < oSettings.fnRecordsDisplay() )
			{
				oSettings.iPagingEnd = oSettings._iDisplayStart + oSettings._iDisplayLength;
			}
			
			var iTween = jQuery.fn.dataTableExt.oPagination.iTweenTime;
			var innerLoop = function () {
				if ( oSettings.iPagingLoopStart < oSettings.iPagingEnd ) {
					oSettings.iPagingLoopStart++;
					oSettings._iDisplayStart = oSettings.iPagingLoopStart;
					fnCallbackDraw( oSettings );
					setTimeout( function() { innerLoop(); }, iTween );
				} else {
					oSettings.iPagingLoopStart = -1;
				}
			};
			innerLoop();
		} );
		
		/* Take the brutal approach to cancelling text selection */
		jQuery(nPrevious).bind( 'selectstart', function () { return false; } );
		jQuery(nNext).bind( 'selectstart', function () { return false; } );
	},
	
	"fnUpdate": function ( oSettings, fnCallbackDraw )
	{
		if ( !oSettings.aanFeatures.p )
		{
			return;
		}
		
		/* Loop over each instance of the pager */
		var an = oSettings.aanFeatures.p;
		for ( var i=0, iLen=an.length ; i<iLen ; i++ )
		{
			if ( an[i].childNodes.length !== 0 )
			{
				an[i].childNodes[0].className = 
					( oSettings._iDisplayStart === 0 ) ? 
					oSettings.oClasses.sPagePrevDisabled : oSettings.oClasses.sPagePrevEnabled;
				
				an[i].childNodes[1].className = 
					( oSettings.fnDisplayEnd() == oSettings.fnRecordsDisplay() ) ? 
					oSettings.oClasses.sPageNextDisabled : oSettings.oClasses.sPageNextEnabled;
			}
		}
	}
}