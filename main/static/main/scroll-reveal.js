(function () {
    'use strict';

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (typeof IntersectionObserver === 'undefined') return;

    function isRevealSkipped(el) {
        if (!(el instanceof HTMLElement)) return true;
        if (el.closest && el.closest('[data-scroll-reveal="off"]')) return true;
        if (el.matches('script, style, noscript')) return true;
        if (el.classList.contains('service-details-modal')) return true;
        return false;
    }

    function mainRevealTargets() {
        var main = document.querySelector('main');
        if (!main) return [];

        var children = [];
        var i;
        var el;
        for (i = 0; i < main.children.length; i++) {
            el = main.children[i];
            if (isRevealSkipped(el)) continue;
            children.push(el);
        }

        if (children.length === 1 && children[0].tagName === 'SECTION') {
            var sec = children[0];
            var out = [];
            for (i = 0; i < sec.children.length; i++) {
                el = sec.children[i];
                if (isRevealSkipped(el)) continue;
                out.push(el);
            }
            return out;
        }

        return children.filter(function (c) {
            return !isRevealSkipped(c);
        });
    }

    var targets = mainRevealTargets();
    var footer = document.querySelector('footer.footer');

    targets.forEach(function (el) {
        el.classList.add('scroll-reveal-el');
    });

    if (footer && !footer.closest('[data-scroll-reveal="off"]')) {
        footer.classList.add('scroll-reveal-el');
    }

    if (!targets.length && !footer) return;

    var observer = new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('scroll-reveal-visible');
                observer.unobserve(entry.target);
            });
        },
        {
            threshold: 0,
            rootMargin: '0px 0px -8% 0px'
        }
    );

    targets.forEach(function (el) {
        observer.observe(el);
    });
    if (footer) observer.observe(footer);
})();
