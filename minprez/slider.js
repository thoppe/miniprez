var _scroll_check_interval = 100;
var _slide_speed = 500;

//var _current_slide_n = 1;
//var _current_slide = null;
//var _multiple_slides_visible = false;
var _slides_visible = null;

var has_scrolled = true;

window.onscroll = function() {
    has_scrolled = true;
};

setInterval(function() {
    if(has_scrolled) {
        has_scrolled = false;
        onmove();
    }
}, _scroll_check_interval);


function checkVisible(elm) {
    var rect = elm.getBoundingClientRect();
    var viewHeight = Math.max(document.documentElement.clientHeight,
                              window.innerHeight);
    return !(rect.bottom < 0 || rect.top - viewHeight >= 0);
}

function onmove() {

    // Find and mark the least most visible slide
    _slides_visible = [];
    
    $('section').each( function( index, element ){
        if( checkVisible(this) ) {
            _slides_visible.push( $(this) );
            //return false;
        }
        
    });
    
    //console.log(_slides_visible);

    /*
    $('html, body').animate({
        scrollTop: item.offset().top
    }, _slide_speed);
    */
}

function moveTO(item) {
    $('html, body').animate({
        scrollTop: item.offset().top
    }, _slide_speed);
}

function moveDOWN() {
    if( _slides_visible.length > 1 ) {
        var item = _slides_visible[1];
        moveTO(item);
        _slides_visible = [item,];
    }
    else {
        var item = _slides_visible[0].next('section');
        if(item.length) {
            moveTO(item);
            _slides_visible = [item,];
        }
    }

    console.log("DOWN", _slides_visible); 
}

function moveUP() {
    var item = _slides_visible[0];

    if( _slides_visible.length > 1 ) {
        moveTO(item);
        _slides_visible = [item,];
    }
    else {
        item = item.prev("section");
        if(item.length) {
            moveTO(item);
            _slides_visible = [item,];
        }
    }

    console.log("UP", _slides_visible); 
}


$(document).keydown(function(e) {
    switch(e.which) {

    case 37: break;
    case 39: break;

    case 38: // up
        e.preventDefault();
        moveUP();
        break;

    case 40: // down
        e.preventDefault();
        moveDOWN();
        break;

        default: return; // exit this handler for other keys
    }
    e.preventDefault(); // prevent the default action (scroll / move caret)
});
