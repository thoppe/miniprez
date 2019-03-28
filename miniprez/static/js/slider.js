var slide_speed = 300;
var slides_visible = null;

$( document ).ready(function() {
    onmove();
});

function checkVisible(elm) {
    var rect = elm.getBoundingClientRect();
    var viewHeight = Math.max(document.documentElement.clientHeight,
                              window.innerHeight);
    return !(rect.bottom < 0 || rect.top - viewHeight >= 0);
}

function onmove() {   
    // Find and mark visible slides start with the smallest
    slides_visible = [];
    
    $('section').each( function( index, element ){
        if( checkVisible(this) ) {
            slides_visible.push( $(this) );

            if(slides_visible.length >= 2) {
                return false;
	    }
        }        
    });
    
}

function moveTO(item) {
    $('html, body').animate({
        scrollTop: item.offset().top
    }, slide_speed);
}

function moveDOWN() {
    if( slides_visible.length > 1 ) {
        var item = slides_visible[1];
        moveTO(item);
        slides_visible = [item,];
    }
    else {
        var item = slides_visible[0].next('section');
        if(item.length) {
            moveTO(item);
            slides_visible = [item,];
        }
    }

}

function moveUP() {
    var item = slides_visible[0];

    if( slides_visible.length > 1 ) {
        moveTO(item);
        slides_visible = [item,];
    }
    else {
        item = item.prev("section");
        if(item.length) {
            moveTO(item);
            slides_visible = [item,];
        }
    }
}


$(document).keydown(function(e) {
    switch(e.which) {

    /*
    case 37: break;
    case 39: break;
    case 38: // up
    case 40: // down
    */
        
    case 33: // pageup
        e.preventDefault();
        moveUP();
        break;

    case 34: // pagedown
        e.preventDefault();
        moveDOWN();
        break;

    case 36: // home
        var first_slide = $('section').first();
        slides_visible = [first_slide,];
        moveTO(first_slide);
        break;
  		  
    case 35: // end
        var last_slide = $('section').last();
        slides_visible = [last_slide,];
        moveTO(last_slide);
        break;
 
    default: return; // exit this handler for other keys
    }
    
    e.preventDefault(); // prevent the default action (scroll / move caret)
    
});
