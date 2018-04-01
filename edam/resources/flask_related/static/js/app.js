// JavaScript Document
function onLoad() {
    // set up tab navigation 
    $('.nav a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    // click on brand forwards to "home"
    $('.navbar-brand').click(function (e) {
        e.preventDefault();
        $(".nav a[href='#home']").tab('show');
    });

    // ensure quick links open in new window
    $('.quick-links a').each(function () {
        this.target = '_blank';
    });

    // update all targets of external links
    $('.dash-ext-link').each(function () {
        this.target = '_blank';
    });

    // update all doc links 
    $('.dash-doc-link').each(function () {
        var path = this.href.split("#")[1];
        this.target = '_blank';
    });
}