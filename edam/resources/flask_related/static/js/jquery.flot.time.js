(function (q) {
    function p(e, c) {
        return c * Math.floor(e / c)
    }

    function r(e, c, f, n) {
        if ("function" == typeof e.strftime)return e.strftime(c);
        var h = function (a, b) {
            a = "" + a;
            return 1 == a.length ? "" + (null == b ? "0" : b) + a : a
        }, k = [], s = !1, m = e.getHours(), b = 12 > m;
        null == f && (f = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(" "));
        null == n && (n = "Sun Mon Tue Wed Thu Fri Sat".split(" "));
        var g;
        g = 12 < m ? m - 12 : 0 == m ? 12 : m;
        for (var d = 0; d < c.length; ++d) {
            var a = c.charAt(d);
            if (s) {
                switch (a) {
                    case "a":
                        a = "" + n[e.getDay()];
                        break;
                    case "b":
                        a = "" + f[e.getMonth()];
                        break;
                    case "d":
                        a = h(e.getDate());
                        break;
                    case "e":
                        a = h(e.getDate(), " ");
                        break;
                    case "h":
                    case "H":
                        a = h(m);
                        break;
                    case "I":
                        a = h(g);
                        break;
                    case "l":
                        a = h(g, " ");
                        break;
                    case "m":
                        a = h(e.getMonth() + 1);
                        break;
                    case "M":
                        a = h(e.getMinutes());
                        break;
                    case "q":
                        a = "" + (Math.floor(e.getMonth() / 3) + 1);
                        break;
                    case "S":
                        a = h(e.getSeconds());
                        break;
                    case "y":
                        a = h(e.getFullYear() % 100);
                        break;
                    case "Y":
                        a = "" + e.getFullYear();
                        break;
                    case "p":
                        a = b ? "am" : "pm";
                        break;
                    case "P":
                        a = b ? "AM" : "PM";
                        break;
                    case "w":
                        a = "" + e.getDay()
                }
                k.push(a);
                s = !1
            } else"%" == a ? s = !0 : k.push(a)
        }
        return k.join("")
    }

    function v(c) {
        function l(c, e, m, b) {
            c[e] = function () {
                return m[b].apply(m, arguments)
            }
        }

        var f = {date: c};
        void 0 != c.strftime && l(f, "strftime", c, "strftime");
        l(f, "getTime", c, "getTime");
        l(f, "setTime", c, "setTime");
        for (var n = "Date Day FullYear Hours Milliseconds Minutes Month Seconds".split(" "), h = 0; h < n.length; h++)l(f, "get" + n[h], c, "getUTC" + n[h]), l(f, "set" + n[h], c, "setUTC" + n[h]);
        return f
    }

    function t(c, l) {
        if ("browser" == l.timezone)return new Date(c);
        if (l.timezone && "utc" != l.timezone && "undefined" != typeof timezoneJS && "undefined" !=
            typeof timezoneJS.Date) {
            var f = new timezoneJS.Date;
            f.setTimezone(l.timezone);
            f.setTime(c);
            return f
        }
        return v(new Date(c))
    }

    var c = {second: 1E3, minute: 6E4, hour: 36E5, day: 864E5, month: 2592E6, quarter: 7776E6, year: 525949.2 * 6E4},
        u = [[1, "second"], [2, "second"], [5, "second"], [10, "second"], [30, "second"], [1, "minute"], [2, "minute"], [5, "minute"], [10, "minute"], [30, "minute"], [1, "hour"], [2, "hour"], [4, "hour"], [8, "hour"], [12, "hour"], [1, "day"], [2, "day"], [3, "day"], [.25, "month"], [.5, "month"], [1, "month"], [2, "month"]],
        w = u.concat([[3,
            "month"], [6, "month"], [1, "year"]]), x = u.concat([[1, "quarter"], [2, "quarter"], [1, "year"]]);
    q.plot.plugins.push({
        init: function (e) {
            e.hooks.processOptions.push(function (e, f) {
                q.each(e.getAxes(), function (e, h) {
                    var k = h.options;
                    "time" == k.mode && (h.tickGenerator = function (e) {
                        var m = [], b = t(e.min, k), g = 0,
                            d = k.tickSize && "quarter" === k.tickSize[1] || k.minTickSize && "quarter" === k.minTickSize[1] ? x : w;
                        null != k.minTickSize && (g = "number" == typeof k.tickSize ? k.tickSize : k.minTickSize[0] * c[k.minTickSize[1]]);
                        for (var a = 0; a < d.length - 1 &&
                        !(e.delta < (d[a][0] * c[d[a][1]] + d[a + 1][0] * c[d[a + 1][1]]) / 2 && d[a][0] * c[d[a][1]] >= g); ++a);
                        g = d[a][0];
                        d = d[a][1];
                        "year" == d && (null != k.minTickSize && "year" == k.minTickSize[1] ? g = Math.floor(k.minTickSize[0]) : (a = Math.pow(10, Math.floor(Math.log(e.delta / c.year) / Math.LN10)), g = e.delta / c.year / a, g = (1.5 > g ? 1 : 3 > g ? 2 : 7.5 > g ? 5 : 10) * a), 1 > g && (g = 1));
                        e.tickSize = k.tickSize || [g, d];
                        a = e.tickSize[0];
                        d = e.tickSize[1];
                        g = a * c[d];
                        "second" == d ? b.setSeconds(p(b.getSeconds(), a)) : "minute" == d ? b.setMinutes(p(b.getMinutes(), a)) : "hour" == d ? b.setHours(p(b.getHours(),
                            a)) : "month" == d ? b.setMonth(p(b.getMonth(), a)) : "quarter" == d ? b.setMonth(3 * p(b.getMonth() / 3, a)) : "year" == d && b.setFullYear(p(b.getFullYear(), a));
                        b.setMilliseconds(0);
                        g >= c.minute && b.setSeconds(0);
                        g >= c.hour && b.setMinutes(0);
                        g >= c.day && b.setHours(0);
                        g >= 4 * c.day && b.setDate(1);
                        g >= 2 * c.month && b.setMonth(p(b.getMonth(), 3));
                        g >= 2 * c.quarter && b.setMonth(p(b.getMonth(), 6));
                        g >= c.year && b.setMonth(0);
                        var h = 0, f = Number.NaN, l;
                        do if (l = f, f = b.getTime(), m.push(f), "month" == d || "quarter" == d)if (1 > a) {
                            b.setDate(1);
                            var n = b.getTime();
                            b.setMonth(b.getMonth() + ("quarter" == d ? 3 : 1));
                            var q = b.getTime();
                            b.setTime(f + h * c.hour + (q - n) * a);
                            h = b.getHours();
                            b.setHours(0)
                        } else b.setMonth(b.getMonth() + a * ("quarter" == d ? 3 : 1)); else"year" == d ? b.setFullYear(b.getFullYear() + a) : b.setTime(f + g); while (f < e.max && f != l);
                        return m
                    }, h.tickFormatter = function (e, f) {
                        var b = t(e, f.options);
                        if (null != k.timeformat)return r(b, k.timeformat, k.monthNames, k.dayNames);
                        var g = f.options.tickSize && "quarter" == f.options.tickSize[1] || f.options.minTickSize && "quarter" == f.options.minTickSize[1],
                            d = f.tickSize[0] * c[f.tickSize[1]], a = f.max - f.min, h = k.twelveHourClock ? " %p" : "",
                            l = k.twelveHourClock ? "%I" : "%H";
                        return r(b, d < c.minute ? l + ":%M:%S" + h : d < c.day ? a < 2 * c.day ? l + ":%M" + h : "%b %d " + l + ":%M" + h : d < c.month ? "%b %d" : g && d < c.quarter || !g && d < c.year ? a < c.year ? "%b" : "%b %Y" : g && d < c.year ? a < c.year ? "Q%q" : "Q%q %Y" : "%Y", k.monthNames, k.dayNames)
                    })
                })
            })
        },
        options: {xaxis: {timezone: null, timeformat: null, twelveHourClock: !1, monthNames: null}},
        name: "time",
        version: "1.0"
    });
    q.plot.formatDate = r;
    q.plot.dateGenerator = t
})(jQuery);