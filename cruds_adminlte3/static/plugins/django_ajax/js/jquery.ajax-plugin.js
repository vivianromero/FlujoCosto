(function (e) {
    "use strict";
    function i(e, t, n) {
        var r = undefined;
        return e && t && ((r = n.closest(e).find(t)), r.length === 0 && (r = undefined)), r;
    }
    function s(t, n) {
        var r = n.data("success"),
            s = n.data("replace"),
            o = n.data("replace-closest"),
            u = n.data("replace-inner"),
            a = n.data("replace-closest-inner"),
            f = i(n.data("replace-father"), n.data("replace-child"), n),
            l = i(n.data("replace-father"), n.data("replace-child-inner"), n),
            c = n.data("append"),
            h = n.data("prepend"),
            p = n.data("refresh"),
            d = n.data("refresh-closest"),
            v = n.data("refresh-inner"),
            m = i(n.data("refresh-father"), n.data("refresh-child"), n),
            g = i(n.data("refresh-father"), n.data("refresh-child-inner"), n),
            y = n.data("clear"),
            b = n.data("clear-closest"),
            w = n.data("remove"),
            E = n.data("remove-closest");
        s && e(s).replaceWith(t.content),
            o && n.closest(o).replaceWith(t.content),
            u && e(u).html(t.content),
            f && f.replaceWith(t.content),
            l && l.html(t.content),
            a && n.closest(a).html(t.content),
            c && e(c).append(t.content),
            h && e(h).prepend(t.content),
            p &&
                e.each(e(p), function (t, n) {
                    ajaxGet(e(n).data("refresh-url"), function (t) {
                        e(n).replaceWith(t);
                    });
                }),
            v &&
                e.each(e(v), function (t, n) {
                    ajaxGet(e(n).data("refresh-url"), function (t) {
                        e(n).html(t);
                    });
                }),
            d &&
                e.each(e(d), function (t, r) {
                    ajaxGet(e(r).data("refresh-url"), function (t) {
                        n.closest(e(r)).replaceWith(t);
                    });
                }),
            m &&
                e.each(m, function (t, n) {
                    ajaxGet(e(n).data("refresh-url"), function (t) {
                        e(n).replaceWith(t);
                    });
                }),
            g &&
                e.each(g, function (t, n) {
                    ajaxGet(e(n).data("refresh-url"), function (t) {
                        e(n).html(t);
                    });
                }),
            y && e(y).html(""),
            w && e(w).remove(),
            b && n.closest(b).html(""),
            E && n.closest(E).remove();
        if (r)
            try {
                (r = window[r]), e.isFunction(r) && r(t.content);
            } catch (S) {
                alert(S.name + "\n" + S.message);
            }
    }
    var t = "[data-ajax-submit]",
        n = "[data-ajax]",
        r = function (r) {
            e(r).on("click", n, this.send), e(r).on("submit", t, this.submit);
        };
    (r.prototype.send = function (t) {
        var n = e(this),
            r = n.data("method"),
            i = n.attr("href") || n.data("href") || n.data("url") || null,
            o = n.data("data") || null,
            u = n.data("error") || null;
        t && t.preventDefault();
        if (!i) {
            alert("href, data-href or data-url attribute not found!");
            return;
        }
        if (u)
            try {
                (u = window[u]), e.isFunction(u) || (u = null);
            } catch (t) {
                alert(t.name + "\n" + t.message);
            }
        (r = r ? r.toLowerCase() : "get"), (i = i && i.replace(/.*(?=#[^\s]*$)/, "")), (o = o && o.replace(/'/g, '"'));
        try {
            o = e.parseJSON(o);
        } catch (t) {
            alert(t.name + "\n" + t.message);
            return;
        }
        ajax && e.isFunction(ajax)
            ? ajax(i, {
                  method: r,
                  data: o,
                  onSuccess: function (e) {
                      s(e, n);
                  },
                  onError: u,
              })
            : alert("jquery.ajax.js is required");
    }),
        (r.prototype.submit = function (t) {
            var n = e(this),
                r = n.attr("action"),
                i = n.attr("method"),
                o = n.serialize(),
                u = n.data("redirect-inner"),
                a = u
                    ? {
                          onRedirect: function (t) {
                              ajaxGet(t, function (t) {
                                  e(u).html(t);
                              });
                          },
                      }
                    : {};
            t.preventDefault(),
                (i = i ? i.toLowerCase() : "get"),
                ajaxMethod(
                    i,
                    r,
                    o,
                    function (e) {
                        var t = {};
                        (t.content = e), s(t, n);
                    },
                    a
                );
        });
    var o = e.fn.ajax;
    (e.fn.ajax = function (t) {
        return this.each(function () {
            var n = e(this),
                i = n.data("django.ajax");
            i || n.data("django.ajax", (i = new r(this))), typeof t == "string" && i[t].call(n);
        });
    }),
        (e.fn.ajax.Constructor = r),
        (e.fn.ajax.noConflict = function () {
            return (e.fn.ajax = o), this;
        }),
        e(document).on("click.ajax.data-api", n, r.prototype.send),
        e(document).on("submit.ajax.data-api", t, r.prototype.submit);
})(jQuery);
