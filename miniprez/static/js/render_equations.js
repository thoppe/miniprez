// grab all elements in DOM with the class 'equation'
var tex = document.getElementsByClassName("inline-equation");

// for each element, render the expression attribute
Array.prototype.forEach.call(tex, function(el) {
    console.log(el);
    katex.render(el.getAttribute("data-expr"), el);
});
