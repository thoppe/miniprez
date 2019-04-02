// grab all elements in DOM with the class 'equation'
var inline_eq = document.getElementsByClassName("inline-equation");

// for each element, render the expression attribute
Array.prototype.forEach.call(inline_eq, function(el) {
    tex = el.getAttribute("data-expr");
    katex.render(tex, el, { displayMode: false });
});

// grab all elements in DOM with the class 'equation'
var block_eq = document.getElementsByClassName("block-equation");

// for each element, render the expression attribute
Array.prototype.forEach.call(block_eq, function(el) {
    tex = el.getAttribute("data-expr");
    katex.render(tex, el, { displayMode: true });
});
