$(document).ready(function() {
    // Add Active On Navbar Lists
    $('.navbar li a').click(function () {

        $(this).parent().addClass('active').siblings().removeClass('active');

    });

    // Add active on category
    var access_url = window.location,
        target_url = $(".navbar .collapse > ul > li > a").toArray(),
        i;
    for (i = 0; i < target_url.length; i++) {
        var target = target_url[i];
        if (access_url.pathname == target.pathname) {
            $(target).parent().addClass("active").siblings().removeClass("active");
        } else {
            $(target).parent().removeClass("active");
        }
    }

    // Add active on link that handle the same hash
    var target_url = $(".profile .caption a").toArray(),
        i;

    for (i = 0; i < target_url.length; i++) {
        var target = target_url[i];
        if (access_url.hash == target.hash) {
            $(target).parent().addClass("active").siblings().removeClass("active");
        }
    }

    // Add Active On Link When You Click On
    $('.profile .caption li a').click(function () {

        $(this).parent().addClass('active').siblings().removeClass('active');

    });

    // Add Class Show To Show The Presentation You Want
    $(".trigger").click(function() {
        $($(this).data("target")).addClass('show').siblings().removeClass('show');
    });

    // link details
    $(function () {
        $('[data-tooltip="tooltip"]').tooltip()
    });

    // Add Placeholder Attribute Instead Of Django form_class
            // register
    $('.register input[name="username"]').attr({"placeholder": "Username", 'class': 'form-control'});
    $('.register input[name="first_name"]').attr({"placeholder": "First Name", 'class': 'form-control'});
    $('.register input[name="last_name"]').attr({"placeholder": "Last Name", 'class': 'form-control'});
    $('.register input[name="password1"]').attr({"placeholder": "Password", 'class': 'form-control'});
    $('.register input[name="password2"]').attr({"placeholder": "Confirm Password", 'class': 'form-control'});
    $('.register input[name="email"]').attr({"placeholder": "E-mail", 'class': 'form-control'});
            // login
    $('.login input[type="text"]').attr({"placeholder": "Username or Email", 'class': 'form-control'});
    $('.login input[type="password"]').attr({"placeholder": "Password", 'class': 'form-control', 'id': 'password-field'});
            // Password-reset-confirm
    $('.password-reset-confirm input[type="password"]').attr({'class': 'form-control'});
            // Edit form page
    $('.edit-form form input').attr({'class': 'form-control'})

    // Show Comment Field
    $(".showin").click(function() {
        $($(this).data("showin")).removeClass('hide');
    });

    // Show Number Phone
    $('.contact-us a').click(function () {

        $(this).hide(function() {
            $('.contact-us .number').show();
        });

    });

    $('.exception').css('display', 'none');

    // Show input required error
    var input = $(".tab-content input");
    input.blur(function()
    {
        if (!$(this).val())
        {
            var attr = $(this).attr('required');
            if (attr == 'required')
            {
                var msg = $(this).attr('placeholder');
                if (msg != undefined)
                {
                    //check if the next to this input i.e : p tag is not visible
                    if (!$(this).next("p.error-message").is(':visible'))
                    {
                        $(this).after("<p class='error-message'>" + msg + ' is a required field ' + "<b>!</b>" + "</p>");
                    }
                }
            }
        }
        else
        {
            //hide next p tag
            $(this).next("p.error-message").empty();
            $(this).next("p.error-message").css("display", "none");
        }
    });

    // Show input border required error
    var input = $("input, textarea");
    input.blur(function ()
    {
        if (!$(this).val())
        {
            var attr = $(this).attr('required');
            if (attr == 'required')
            {
                $(this).css({
                      'background-color': '#fce4e4',
                      'border': '1px solid #cc0033',
                      'outline': 'none'
                });
            }
        }
        else
        {
            $(this).css({
                  'background-color': '#FFF',
                  'border': '1px solid #ccc',
                  'outline': 'none'
            });
        }
    });
    // Show password
    $(".toggle-password").click(function()
    {
        $(this).toggleClass("fa-eye fa-eye-slash");
        var input = $($(this).attr("toggle"));
        if (input.attr("type") == "password") {
            input.attr("type", "text");
        } else {
            input.attr("type", "password");
        }
    });
});