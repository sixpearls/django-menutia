IE_submenu_fix = function() {
    if (document.all&&document.getElementById) {
        navRoot = document.getElementById("menu-nav-menu");
        for (i=0; i<navRoot.childNodes.length; i++) {
            node = navRoot.childNodes[i];
            if (node.nodeName=="LI") {
                node.onmouseover=function() {
                    this.className+=" over";
                }
                node.onmouseout=function() {
                    this.className=this.className.replace(" over", "");
                }
            }
        }
   }
}
window.onload=IE_submenu_fix;

$(function() { //create select drop down for small screens
    // Create the dropdown base
    $("<select />").appendTo("nav#primary");

    // Create default option "Go to..."
    $("<option />", {
     "selected": "selected",
     "value"   : "",
     "text"    : "Go to..."
    }).appendTo("nav select");

    // Populate dropdown with menu items
    $("nav ul li a").each(function() {

        var el = $(this);
        var isChild = el.parents('.sub-menu').length;
        var menuText = el.text();

        if (isChild) {
            menuText = '— ' + menuText;
        }

        $("<option />", {
                "value"   : el.attr("href"),
                "text"    : menuText
        }).appendTo("nav select");
         
    });

    // To make dropdown actually work
    // To make more unobtrusive: http://css-tricks.com/4064-unobtrusive-page-changer/
    $("nav select").change(function() {
    window.location = $(this).find("option:selected").val();
    });

});
