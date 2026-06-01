(function () {
    var config = window.CONFIG || {};
    var admin = config.personal || {};
    var copyright = config.copyright || {};
    var scriptSrc = document.currentScript ? document.currentScript.getAttribute("src") : "";
    var assetsRoot = scriptSrc ? scriptSrc.replace(/js\/site-admin\.js$/, "") : "assets/";

    function setText(selector, value) {
        if (!value) return;
        document.querySelectorAll(selector).forEach(function (element) {
            element.textContent = value;
        });
    }

    function setHref(selector, value) {
        if (!value) return;
        document.querySelectorAll(selector).forEach(function (element) {
            element.setAttribute("href", value);
        });
    }

    function setFooterCopyright() {
        if (!admin.name) return;

        document.querySelectorAll("[data-site-copyright]").forEach(function (element) {
            element.innerHTML = "&copy; " + admin.name + ". Design: <a href=\"" +
                (copyright.templateUrl || "https://html5up.net") + "\">" +
                (copyright.template || copyright.templateName || "HTML5 UP") + "</a>.";
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        setText("[data-admin-name]", admin.name);
        setText("[data-admin-email]", admin.email);
        setText("[data-admin-phone]", admin.phone);
        setText("[data-admin-location]", admin.location);
        setText("[data-admin-location-full]", admin.locationFull || admin.location);

        setHref("[data-admin-email-href]", admin.email ? "mailto:" + admin.email : "");
        setHref("[data-admin-phone-href]", admin.phoneHref ? "tel:" + admin.phoneHref : "");
        setHref("[data-admin-linkedin-href]", admin.linkedin);
        setHref("[data-admin-github-href]", admin.github);
        setHref("[data-admin-resume-href]", resolveAssetPath(admin.resumePDF));

        setFooterCopyright();
    });

    function resolveAssetPath(path) {
        if (!path) return "";
        if (/^(https?:)?\/\//.test(path) || path.charAt(0) === "/") return path;
        return path.replace(/^assets\//, assetsRoot);
    }
}());
