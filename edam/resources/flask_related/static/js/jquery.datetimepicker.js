/*
 jQuery DateTimePicker plugin v2.2.8
 @homepage http://xdsoft.net/jqplugins/datetimepicker/
 (c) 2014, Chupurnov Valeriy.
 */
(function (b) {
    var c = {
        i18n: {
            bg: {
                months: "\u00d0\u00af\u00d0\u00bd\u00d1\u0192\u00d0\u00b0\u00d1\u20ac\u00d0\u00b8 \u00d0\u00a4\u00d0\u00b5\u00d0\u00b2\u00d1\u20ac\u00d1\u0192\u00d0\u00b0\u00d1\u20ac\u00d0\u00b8 \u00d0\u0153\u00d0\u00b0\u00d1\u20ac\u00d1\u201a \u00d0\u0090\u00d0\u00bf\u00d1\u20ac\u00d0\u00b8\u00d0\u00bb \u00d0\u0153\u00d0\u00b0\u00d0\u00b9 \u00d0\u00ae\u00d0\u00bd\u00d0\u00b8 \u00d0\u00ae\u00d0\u00bb\u00d0\u00b8 \u00d0\u0090\u00d0\u00b2\u00d0\u00b3\u00d1\u0192\u00d1\u0081\u00d1\u201a \u00d0\u00a1\u00d0\u00b5\u00d0\u00bf\u00d1\u201a\u00d0\u00b5\u00d0\u00bc\u00d0\u00b2\u00d1\u20ac\u00d0\u00b8 \u00d0\u017e\u00d0\u00ba\u00d1\u201a\u00d0\u00be\u00d0\u00bc\u00d0\u00b2\u00d1\u20ac\u00d0\u00b8 \u00d0\u009d\u00d0\u00be\u00d0\u00b5\u00d0\u00bc\u00d0\u00b2\u00d1\u20ac\u00d0\u00b8 \u00d0\u201d\u00d0\u00b5\u00d0\u00ba\u00d0\u00b5\u00d0\u00bc\u00d0\u00b2\u00d1\u20ac\u00d0\u00b8".split(" "),
                dayOfWeek: "\u00d0\u009d\u00d0\u00b4 \u00d0\u0178\u00d0\u00bd \u00d0\u2019\u00d1\u201a \u00d0\u00a1\u00d1\u20ac \u00d0\u00a7\u00d1\u201a \u00d0\u0178\u00d1\u201a \u00d0\u00a1\u00d0\u00b1".split(" ")
            },
            fa: {
                months: "\u00d9\u0081\u00d8\u00b1\u00d9\u02c6\u00d8\u00b1\u00d8\u00af\u00db\u0152\u00d9\u2020 \u00d8\u00a7\u00d8\u00b1\u00d8\u00af\u00db\u0152\u00d8\u00a8\u00d9\u2021\u00d8\u00b4\u00d8\u00aa \u00d8\u00ae\u00d8\u00b1\u00d8\u00af\u00d8\u00a7\u00d8\u00af \u00d8\u00aa\u00db\u0152\u00d8\u00b1 \u00d9\u2026\u00d8\u00b1\u00d8\u00af\u00d8\u00a7\u00d8\u00af \u00d8\u00b4\u00d9\u2021\u00d8\u00b1\u00db\u0152\u00d9\u02c6\u00d8\u00b1 \u00d9\u2026\u00d9\u2021\u00d8\u00b1 \u00d8\u00a2\u00d8\u00a8\u00d8\u00a7\u00d9\u2020 \u00d8\u00a2\u00d8\u00b0\u00d8\u00b1 \u00d8\u00af\u00db\u0152 \u00d8\u00a8\u00d9\u2021\u00d9\u2026\u00d9\u2020 \u00d8\u00a7\u00d8\u00b3\u00d9\u0081\u00d9\u2020\u00d8\u00af".split(" "),
                dayOfWeek: "\u00db\u0152\u00da\u00a9\u00d8\u00b4\u00d9\u2020\u00d8\u00a8\u00d9\u2021;\u00d8\u00af\u00d9\u02c6\u00d8\u00b4\u00d9\u2020\u00d8\u00a8\u00d9\u2021;\u00d8\u00b3\u00d9\u2021 \u00d8\u00b4\u00d9\u2020\u00d8\u00a8\u00d9\u2021;\u00da\u2020\u00d9\u2021\u00d8\u00a7\u00d8\u00b1\u00d8\u00b4\u00d9\u2020\u00d8\u00a8\u00d9\u2021;\u00d9\u00be\u00d9\u2020\u00d8\u00ac\u00d8\u00b4\u00d9\u2020\u00d8\u00a8\u00d9\u2021;\u00d8\u00ac\u00d9\u2026\u00d8\u00b9\u00d9\u2021;\u00d8\u00b4\u00d9\u2020\u00d8\u00a8\u00d9\u2021".split(";")
            },
            ru: {
                months: "\u00d0\u00af\u00d0\u00bd\u00d0\u00b2\u00d0\u00b0\u00d1\u20ac\u00d1\u0152 \u00d0\u00a4\u00d0\u00b5\u00d0\u00b2\u00d1\u20ac\u00d0\u00b0\u00d0\u00bb\u00d1\u0152 \u00d0\u0153\u00d0\u00b0\u00d1\u20ac\u00d1\u201a \u00d0\u0090\u00d0\u00bf\u00d1\u20ac\u00d0\u00b5\u00d0\u00bb\u00d1\u0152 \u00d0\u0153\u00d0\u00b0\u00d0\u00b9 \u00d0\u02dc\u00d1\u017d\u00d0\u00bd\u00d1\u0152 \u00d0\u02dc\u00d1\u017d\u00d0\u00bb\u00d1\u0152 \u00d0\u0090\u00d0\u00b2\u00d0\u00b3\u00d1\u0192\u00d1\u0081\u00d1\u201a \u00d0\u00a1\u00d0\u00b5\u00d0\u00bd\u00d1\u201a\u00d1\u008f\u00d0\u00b1\u00d1\u20ac\u00d1\u0152 \u00d0\u017e\u00d0\u00ba\u00d1\u201a\u00d1\u008f\u00d0\u00b1\u00d1\u20ac\u00d1\u0152 \u00d0\u009d\u00d0\u00be\u00d1\u008f\u00d0\u00b1\u00d1\u20ac\u00d1\u0152 \u00d0\u201d\u00d0\u00b5\u00d0\u00ba\u00d0\u00b0\u00d0\u00b1\u00d1\u20ac\u00d1\u0152".split(" "),
                dayOfWeek: "\u00d0\u2019\u00d1\u0081\u00d0\u00ba \u00d0\u0178\u00d0\u00bd \u00d0\u2019\u00d1\u201a \u00d0\u00a1\u00d1\u20ac \u00d0\u00a7\u00d1\u201a \u00d0\u0178\u00d1\u201a \u00d0\u00a1\u00d0\u00b1".split(" ")
            },
            en: {
                months: "January February March April May June July August September October November December".split(" "),
                dayOfWeek: "Sun Mon Tue Wed Thu Fri Sat".split(" ")
            },
            el: {
                months: "\u00ce\u2122\u00ce\u00b1\u00ce\u00bd\u00ce\u00bf\u00cf\u2026\u00ce\u00ac\u00cf\u0081\u00ce\u00b9\u00ce\u00bf\u00cf\u201a \u00ce\u00a6\u00ce\u00b5\u00ce\u00b2\u00cf\u0081\u00ce\u00bf\u00cf\u2026\u00ce\u00ac\u00cf\u0081\u00ce\u00b9\u00ce\u00bf\u00cf\u201a \u00ce\u0153\u00ce\u00ac\u00cf\u0081\u00cf\u201e\u00ce\u00b9\u00ce\u00bf\u00cf\u201a \u00ce\u2018\u00cf\u20ac\u00cf\u0081\u00ce\u00af\u00ce\u00bb\u00ce\u00b9\u00ce\u00bf\u00cf\u201a \u00ce\u0153\u00ce\u00ac\u00ce\u00b9\u00ce\u00bf\u00cf\u201a \u00ce\u2122\u00ce\u00bf\u00cf\u008d\u00ce\u00bd\u00ce\u00b9\u00ce\u00bf\u00cf\u201a \u00ce\u2122\u00ce\u00bf\u00cf\u008d\u00ce\u00bb\u00ce\u00b9\u00ce\u00bf\u00cf\u201a \u00ce\u2018\u00cf\u008d\u00ce\u00b3\u00ce\u00bf\u00cf\u2026\u00cf\u0192\u00cf\u201e\u00ce\u00bf\u00cf\u201a \u00ce\u00a3\u00ce\u00b5\u00cf\u20ac\u00cf\u201e\u00ce\u00ad\u00ce\u00bc\u00ce\u00b2\u00cf\u0081\u00ce\u00b9\u00ce\u00bf\u00cf\u201a \u00ce\u0178\u00ce\u00ba\u00cf\u201e\u00cf\u017d\u00ce\u00b2\u00cf\u0081\u00ce\u00b9\u00ce\u00bf\u00cf\u201a \u00ce\u009d\u00ce\u00bf\u00ce\u00ad\u00ce\u00bc\u00ce\u00b2\u00cf\u0081\u00ce\u00b9\u00ce\u00bf\u00cf\u201a \u00ce\u201d\u00ce\u00b5\u00ce\u00ba\u00ce\u00ad\u00ce\u00bc\u00ce\u00b2\u00cf\u0081\u00ce\u00b9\u00ce\u00bf\u00cf\u201a".split(" "),
                dayOfWeek: "\u00ce\u0161\u00cf\u2026\u00cf\u0081;\u00ce\u201d\u00ce\u00b5\u00cf\u2026;\u00ce\u00a4\u00cf\u0081\u00ce\u00b9;\u00ce\u00a4\u00ce\u00b5\u00cf\u201e;\u00ce \u00ce\u00b5\u00ce\u00bc;\u00ce \u00ce\u00b1\u00cf\u0081;\u00ce\u00a3\u00ce\u00b1\u00ce\u00b2".split(";")
            },
            de: {
                months: "Januar Februar M\u00c3\u00a4rz April Mai Juni Juli August September Oktober November Dezember".split(" "),
                dayOfWeek: "So Mo Di Mi Do Fr Sa".split(" ")
            },
            nl: {
                months: "januari februari maart april mei juni juli augustus september oktober november december".split(" "),
                dayOfWeek: "zo ma di wo do vr za".split(" ")
            },
            tr: {
                months: "Ocak \u00c5\u017eubat Mart Nisan May\u00c4\u00b1s Haziran Temmuz A\u00c4\u0178ustos Eyl\u00c3\u00bcl Ekim Kas\u00c4\u00b1m Aral\u00c4\u00b1k".split(" "),
                dayOfWeek: "Paz Pts Sal \u00c3\u2021ar Per Cum Cts".split(" ")
            },
            fr: {
                months: "Janvier F\u00c3\u00a9vrier Mars Avril Mai Juin Juillet Ao\u00c3\u00bbt Septembre Octobre Novembre D\u00c3\u00a9cembre".split(" "),
                dayOfWeek: "Dim Lun Mar Mer Jeu Ven Sam".split(" ")
            },
            es: {
                months: "Enero Febrero Marzo Abril Mayo Junio Julio Agosto Septiembre Octubre Noviembre Diciembre".split(" "),
                dayOfWeek: "Dom Lun Mar Mi\u00c3\u00a9 Jue Vie S\u00c3\u00a1b".split(" ")
            },
            th: {
                months: "\u00e0\u00b8\u00a1\u00e0\u00b8\u0081\u00e0\u00b8\u00a3\u00e0\u00b8\u00b2\u00e0\u00b8\u201e\u00e0\u00b8\u00a1;\u00e0\u00b8\u0081\u00e0\u00b8\u00b8\u00e0\u00b8\u00a1\u00e0\u00b8 \u00e0\u00b8\u00b2\u00e0\u00b8\u017e\u00e0\u00b8\u00b1\u00e0\u00b8\u2122\u00e0\u00b8\u02dc\u00e0\u00b9\u0152;\u00e0\u00b8\u00a1\u00e0\u00b8\u00b5\u00e0\u00b8\u2122\u00e0\u00b8\u00b2\u00e0\u00b8\u201e\u00e0\u00b8\u00a1;\u00e0\u00b9\u20ac\u00e0\u00b8\u00a1\u00e0\u00b8\u00a9\u00e0\u00b8\u00b2\u00e0\u00b8\u00a2\u00e0\u00b8\u2122;\u00e0\u00b8\u017e\u00e0\u00b8\u00a4\u00e0\u00b8\u00a9\u00e0\u00b8 \u00e0\u00b8\u00b2\u00e0\u00b8\u201e\u00e0\u00b8\u00a1;\u00e0\u00b8\u00a1\u00e0\u00b8\u00b4\u00e0\u00b8\u2013\u00e0\u00b8\u00b8\u00e0\u00b8\u2122\u00e0\u00b8\u00b2\u00e0\u00b8\u00a2\u00e0\u00b8\u2122;\u00e0\u00b8\u0081\u00e0\u00b8\u00a3\u00e0\u00b8\u0081\u00e0\u00b8\u017d\u00e0\u00b8\u00b2\u00e0\u00b8\u201e\u00e0\u00b8\u00a1;\u00e0\u00b8\u00aa\u00e0\u00b8\u00b4\u00e0\u00b8\u2021\u00e0\u00b8\u00ab\u00e0\u00b8\u00b2\u00e0\u00b8\u201e\u00e0\u00b8\u00a1;\u00e0\u00b8\u0081\u00e0\u00b8\u00b1\u00e0\u00b8\u2122\u00e0\u00b8\u00a2\u00e0\u00b8\u00b2\u00e0\u00b8\u00a2\u00e0\u00b8\u2122;\u00e0\u00b8\u2022\u00e0\u00b8\u00b8\u00e0\u00b8\u00a5\u00e0\u00b8\u00b2\u00e0\u00b8\u201e\u00e0\u00b8\u00a1;\u00e0\u00b8\u017e\u00e0\u00b8\u00a4\u00e0\u00b8\u00a8\u00e0\u00b8\u02c6\u00e0\u00b8\u00b4\u00e0\u00b8\u0081\u00e0\u00b8\u00b2\u00e0\u00b8\u00a2\u00e0\u00b8\u2122;\u00e0\u00b8\u02dc\u00e0\u00b8\u00b1\u00e0\u00b8\u2122\u00e0\u00b8\u00a7\u00e0\u00b8\u00b2\u00e0\u00b8\u201e\u00e0\u00b8\u00a1".split(";"),
                dayOfWeek: "\u00e0\u00b8\u00ad\u00e0\u00b8\u00b2. \u00e0\u00b8\u02c6. \u00e0\u00b8\u00ad. \u00e0\u00b8\u017e. \u00e0\u00b8\u017e\u00e0\u00b8\u00a4. \u00e0\u00b8\u00a8. \u00e0\u00b8\u00aa.".split(" ")
            },
            pl: {
                months: "stycze\u00c5\u201e luty marzec kwiecie\u00c5\u201e maj czerwiec lipiec sierpie\u00c5\u201e wrzesie\u00c5\u201e pa\u00c5\u00badziernik listopad grudzie\u00c5\u201e".split(" "),
                dayOfWeek: "nd pn wt \u00c5\u203ar cz pt sb".split(" ")
            },
            pt: {
                months: "Janeiro Fevereiro Mar\u00c3\u00a7o Abril Maio Junho Julho Agosto Setembro Outubro Novembro Dezembro".split(" "),
                dayOfWeek: "Dom Seg Ter Qua Qui Sex Sab".split(" ")
            },
            ch: {
                months: "\u00e4\u00b8\u20ac\u00e6\u0153\u02c6 \u00e4\u00ba\u0152\u00e6\u0153\u02c6 \u00e4\u00b8\u2030\u00e6\u0153\u02c6 \u00e5\u203a\u203a\u00e6\u0153\u02c6 \u00e4\u00ba\u201d\u00e6\u0153\u02c6 \u00e5\u2026\u00ad\u00e6\u0153\u02c6 \u00e4\u00b8\u0192\u00e6\u0153\u02c6 \u00e5\u2026\u00ab\u00e6\u0153\u02c6 \u00e4\u00b9\u009d\u00e6\u0153\u02c6 \u00e5\u008d\u0081\u00e6\u0153\u02c6 \u00e5\u008d\u0081\u00e4\u00b8\u20ac\u00e6\u0153\u02c6 \u00e5\u008d\u0081\u00e4\u00ba\u0152\u00e6\u0153\u02c6".split(" "),
                dayOfWeek: "\u00e6\u2014\u00a5 \u00e4\u00b8\u20ac \u00e4\u00ba\u0152 \u00e4\u00b8\u2030 \u00e5\u203a\u203a \u00e4\u00ba\u201d \u00e5\u2026\u00ad".split(" ")
            },
            se: {
                months: "Januari Februari Mars April Maj Juni Juli Augusti September Oktober November December".split(" "),
                dayOfWeek: "S\u00c3\u00b6n M\u00c3\u00a5n Tis Ons Tor Fre L\u00c3\u00b6r".split(" ")
            },
            kr: {
                months: "1\u00ec\u203a\u201d 2\u00ec\u203a\u201d 3\u00ec\u203a\u201d 4\u00ec\u203a\u201d 5\u00ec\u203a\u201d 6\u00ec\u203a\u201d 7\u00ec\u203a\u201d 8\u00ec\u203a\u201d 9\u00ec\u203a\u201d 10\u00ec\u203a\u201d 11\u00ec\u203a\u201d 12\u00ec\u203a\u201d".split(" "),
                dayOfWeek: "\u00ec\u009d\u00bc;\u00ec\u203a\u201d;\u00ed\u2122\u201d;\u00ec\u02c6\u02dc;\u00eb\u00aa\u00a9;\u00ea\u00b8\u02c6;\u00ed\u2020 ".split(";")
            },
            it: {
                months: "Gennaio Febbraio Marzo Aprile Maggio Giugno Luglio Agosto Settembre Ottobre Novembre Dicembre".split(" "),
                dayOfWeek: "Dom Lun Mar Mer Gio Ven Sab".split(" ")
            },
            da: {
                months: "January Februar Marts April Maj Juni July August September Oktober November December".split(" "),
                dayOfWeek: "S\u00c3\u00b8n Man Tir ons Tor Fre l\u00c3\u00b8r".split(" ")
            },
            ja: {
                months: "1\u00e6\u0153\u02c6 2\u00e6\u0153\u02c6 3\u00e6\u0153\u02c6 4\u00e6\u0153\u02c6 5\u00e6\u0153\u02c6 6\u00e6\u0153\u02c6 7\u00e6\u0153\u02c6 8\u00e6\u0153\u02c6 9\u00e6\u0153\u02c6 10\u00e6\u0153\u02c6 11\u00e6\u0153\u02c6 12\u00e6\u0153\u02c6".split(" "),
                dayOfWeek: "\u00e6\u2014\u00a5 \u00e6\u0153\u02c6 \u00e7\u0081\u00ab \u00e6\u00b0\u00b4 \u00e6\u0153\u00a8 \u00e9\u2021\u2018 \u00e5\u0153\u0178".split(" ")
            },
            vi: {
                months: "Th\u00c3\u00a1ng 1;Th\u00c3\u00a1ng 2;Th\u00c3\u00a1ng 3;Th\u00c3\u00a1ng 4;Th\u00c3\u00a1ng 5;Th\u00c3\u00a1ng 6;Th\u00c3\u00a1ng 7;Th\u00c3\u00a1ng 8;Th\u00c3\u00a1ng 9;Th\u00c3\u00a1ng 10;Th\u00c3\u00a1ng 11;Th\u00c3\u00a1ng 12".split(";"),
                dayOfWeek: "CN T2 T3 T4 T5 T6 T7".split(" ")
            },
            sl: {
                months: "Januar Februar Marec April Maj Junij Julij Avgust September Oktober November December".split(" "),
                dayOfWeek: "Ned Pon Tor Sre \u00c4\u0152et Pet Sob".split(" ")
            }
        },
        value: "",
        lang: "en",
        format: "Y/m/d H:i",
        formatTime: "H:i",
        formatDate: "Y/m/d",
        startDate: !1,
        step: 60,
        monthChangeSpinner: !0,
        closeOnDateSelect: !1,
        closeOnWithoutClick: !0,
        timepicker: !0,
        datepicker: !0,
        minDate: !1,
        maxDate: !1,
        minTime: !1,
        maxTime: !1,
        allowTimes: [],
        opened: !1,
        initTime: !0,
        inline: !1,
        onSelectDate: function () {
        },
        onSelectTime: function () {
        },
        onChangeMonth: function () {
        },
        onChangeDateTime: function () {
        },
        onShow: function () {
        },
        onClose: function () {
        },
        onGenerate: function () {
        },
        withoutCopyright: !0,
        inverseButton: !1,
        hours12: !1,
        next: "xdsoft_next",
        prev: "xdsoft_prev",
        dayOfWeekStart: 0,
        timeHeightInTimePicker: 25,
        timepickerScrollbar: !0,
        todayButton: !0,
        defaultSelect: !0,
        scrollMonth: !0,
        scrollTime: !0,
        scrollInput: !0,
        lazyInit: !1,
        mask: !1,
        validateOnBlur: !0,
        allowBlank: !0,
        yearStart: 1950,
        yearEnd: 2050,
        style: "",
        id: "",
        fixed: !1,
        roundTime: "round",
        className: "",
        weekends: [],
        yearOffset: 0
    };
    Array.prototype.indexOf || (Array.prototype.indexOf = function (b, c) {
        for (var a = c || 0, q = this.length; a < q; a++)if (this[a] === b)return a;
        return -1
    });
    Date.prototype.countDaysInMonth = function () {
        return (new Date(this.getFullYear(), this.getMonth() + 1, 0)).getDate()
    };
    b.fn.xdsoftScroller = function (c) {
        return this.each(function () {
            var g = b(this);
            if (!b(this).hasClass("xdsoft_scroller_box")) {
                var a = function (a) {
                        var b = {x: 0, y: 0};
                        if ("touchstart" == a.type || "touchmove" == a.type || "touchend" == a.type || "touchcancel" ==
                            a.type) a = a.originalEvent.touches[0] || a.originalEvent.changedTouches[0], b.x = a.pageX, b.y = a.pageY; else if ("mousedown" == a.type || "mouseup" == a.type || "mousemove" == a.type || "mouseover" == a.type || "mouseout" == a.type || "mouseenter" == a.type || "mouseleave" == a.type) b.x = a.pageX, b.y = a.pageY;
                        return b
                    }, q = 0, m = g.children().eq(0), n = g[0].clientHeight, e = m[0].offsetHeight,
                    u = b('<div class="xdsoft_scrollbar"></div>'), d = b('<div class="xdsoft_scroller"></div>'),
                    A = 100, v = !1;
                u.append(d);
                g.addClass("xdsoft_scroller_box").append(u);
                d.on("mousedown.xdsoft_scroller", function (a) {
                    n || g.trigger("resize_scroll.xdsoft_scroller", [c]);
                    var e = a.pageY, v = parseInt(d.css("margin-top")), m = u[0].offsetHeight;
                    b(document.body).addClass("xdsoft_noselect");
                    b([document.body, window]).on("mouseup.xdsoft_scroller", function C() {
                        b([document.body, window]).off("mouseup.xdsoft_scroller", C).off("mousemove.xdsoft_scroller", q).removeClass("xdsoft_noselect")
                    });
                    b(document.body).on("mousemove.xdsoft_scroller", q = function (a) {
                        a = a.pageY - e + v;
                        0 > a && (a = 0);
                        a + d[0].offsetHeight >
                        m && (a = m - d[0].offsetHeight);
                        g.trigger("scroll_element.xdsoft_scroller", [A ? a / A : 0])
                    })
                });
                g.on("scroll_element.xdsoft_scroller", function (a, b) {
                    n || g.trigger("resize_scroll.xdsoft_scroller", [b, !0]);
                    b = 1 < b ? 1 : 0 > b || isNaN(b) ? 0 : b;
                    d.css("margin-top", A * b);
                    m.css("marginTop", -parseInt((e - n) * b))
                }).on("resize_scroll.xdsoft_scroller", function (a, b, c) {
                    n = g[0].clientHeight;
                    e = m[0].offsetHeight;
                    a = n / e;
                    var k = a * u[0].offsetHeight;
                    1 < a ? d.hide() : (d.show(), d.css("height", parseInt(10 < k ? k : 10)), A = u[0].offsetHeight - d[0].offsetHeight, !0 !==
                    c && g.trigger("scroll_element.xdsoft_scroller", [b ? b : Math.abs(parseInt(m.css("marginTop"))) / (e - n)]))
                });
                g.mousewheel && g.mousewheel(function (a, b, d, c) {
                    d = Math.abs(parseInt(m.css("marginTop")));
                    g.trigger("scroll_element.xdsoft_scroller", [(d - 20 * b) / (e - n)]);
                    a.stopPropagation();
                    return !1
                });
                g.on("touchstart", function (b) {
                    v = a(b)
                });
                g.on("touchmove", function (b) {
                    if (v) {
                        var d = a(b), c = Math.abs(parseInt(m.css("marginTop")));
                        g.trigger("scroll_element.xdsoft_scroller", [(c - (d.y - v.y)) / (e - n)]);
                        b.stopPropagation();
                        b.preventDefault()
                    }
                });
                g.on("touchend touchcancel", function (a) {
                    v = !1
                })
            }
            g.trigger("resize_scroll.xdsoft_scroller", [c])
        })
    };
    b.fn.datetimepicker = function (k) {
        var g = !1, a = b.isPlainObject(k) || !k ? b.extend(!0, {}, c, k) : b.extend({}, c), q = 0, m = function (a) {
            a.on("open.xdsoft focusin.xdsoft mousedown.xdsoft", function d(b) {
                a.is(":disabled") || a.is(":hidden") || !a.is(":visible") || a.data("xdsoft_datetimepicker") || (clearTimeout(q), q = setTimeout(function () {
                        a.data("xdsoft_datetimepicker") || n(a);
                        a.off("open.xdsoft focusin.xdsoft mousedown.xdsoft", d).trigger("open.xdsoft")
                    },
                    100))
            })
        }, n = function (e) {
            function c() {
                var b = a.value ? a.value : e && e.val && e.val() ? e.val() : "";
                b && f.isValidDate(b = Date.parseDate(b, a.format)) ? d.data("changed", !0) : b = "";
                b || !1 === a.startDate || (b = f.strToDateTime(a.startDate));
                return b ? b : 0
            }

            var d = b("<div " + (a.id ? 'id="' + a.id + '"' : "") + " " + (a.style ? 'style="' + a.style + '"' : "") + ' class="xdsoft_datetimepicker xdsoft_noselect ' + a.className + '"></div>'),
                n = b('<div class="xdsoft_copyright"><a target="_blank" href="http://xdsoft.net/jqplugins/datetimepicker/">xdsoft.net</a></div>'),
                k = b('<div class="xdsoft_datepicker active"></div>'),
                m = b('<div class="xdsoft_mounthpicker"><button type="button" class="xdsoft_prev"></button><button type="button" class="xdsoft_today_button"></button><div class="xdsoft_label xdsoft_month"><span></span></div><div class="xdsoft_label xdsoft_year"><span></span></div><button type="button" class="xdsoft_next"></button></div>'),
                q = b('<div class="xdsoft_calendar"></div>'),
                z = b('<div class="xdsoft_timepicker active"><button type="button" class="xdsoft_prev"></button><div class="xdsoft_time_box"></div><button type="button" class="xdsoft_next"></button></div>'),
                w = z.find(".xdsoft_time_box").eq(0), r = b('<div class="xdsoft_time_variant"></div>'),
                C = b('<div class="xdsoft_scrollbar"></div>');
            b('<div class="xdsoft_scroller"></div>');
            var D = b('<div class="xdsoft_select xdsoft_monthselect"><div></div></div>'),
                E = b('<div class="xdsoft_select xdsoft_yearselect"><div></div></div>');
            m.find(".xdsoft_month span").after(D);
            m.find(".xdsoft_year span").after(E);
            m.find(".xdsoft_month,.xdsoft_year").on("mousedown.xdsoft", function (a) {
                m.find(".xdsoft_select").hide();
                var p = b(this).find(".xdsoft_select").eq(0),
                    d = 0, e = 0;
                f.currentTime && (d = f.currentTime[b(this).hasClass("xdsoft_month") ? "getMonth" : "getFullYear"]());
                p.show();
                for (var c = p.find("div.xdsoft_option"), h = 0; h < c.length && c.eq(h).data("value") != d; h++)e += c[0].offsetHeight;
                p.xdsoftScroller(e / (p.children()[0].offsetHeight - p[0].clientHeight));
                a.stopPropagation();
                return !1
            });
            m.find(".xdsoft_select").xdsoftScroller().on("mousedown.xdsoft", function (a) {
                a.stopPropagation();
                a.preventDefault()
            }).on("mousedown.xdsoft", ".xdsoft_option", function (l) {
                if (f && f.currentTime) f.currentTime[b(this).parent().parent().hasClass("xdsoft_monthselect") ?
                    "setMonth" : "setFullYear"](b(this).data("value"));
                b(this).parent().parent().hide();
                d.trigger("xchange.xdsoft");
                a.onChangeMonth && a.onChangeMonth.call && a.onChangeMonth.call(d, f.currentTime, d.data("input"))
            });
            d.setOptions = function (l) {
                a = b.extend(!0, {}, a, l);
                l.allowTimes && b.isArray(l.allowTimes) && l.allowTimes.length && (a.allowTimes = b.extend(!0, [], l.allowTimes));
                l.weekends && b.isArray(l.weekends) && l.weekends.length && (a.weekends = b.extend(!0, [], l.weekends));
                !a.open && !a.opened || a.inline || e.trigger("open.xdsoft");
                a.inline && (B = !0, d.addClass("xdsoft_inline"), e.after(d).hide());
                a.inverseButton && (a.next = "xdsoft_prev", a.prev = "xdsoft_next");
                a.datepicker ? k.addClass("active") : k.removeClass("active");
                a.timepicker ? z.addClass("active") : z.removeClass("active");
                a.value && (e && e.val && e.val(a.value), f.setCurrentTime(a.value));
                isNaN(a.dayOfWeekStart) || 0 > parseInt(a.dayOfWeekStart) || 6 < parseInt(a.dayOfWeekStart) ? a.dayOfWeekStart = 0 : a.dayOfWeekStart = parseInt(a.dayOfWeekStart);
                a.timepickerScrollbar || C.hide();
                a.minDate && /^-(.*)$/.test(a.minDate) &&
                (a.minDate = f.strToDateTime(a.minDate).dateFormat(a.formatDate));
                a.maxDate && /^\+(.*)$/.test(a.maxDate) && (a.maxDate = f.strToDateTime(a.maxDate).dateFormat(a.formatDate));
                m.find(".xdsoft_today_button").css("visibility", a.todayButton ? "visible" : "hidden");
                if (a.mask) {
                    var p = function (a, b) {
                        var l = a.replace(/([\[\]\/\{\}\(\)\-\.\+]{1})/g, "\\$1").replace(/_/g, "{digit+}").replace(/([0-9]{1})/g, "{digit$1}").replace(/\{digit([0-9]{1})\}/g, "[0-$1_]{1}").replace(/\{digit[\+]\}/g, "[0-9_]{1}");
                        return RegExp(l).test(b)
                    };
                    e.off("keydown.xdsoft");
                    switch (!0) {
                        case !0 === a.mask:
                            a.mask = a.format.replace(/Y/g, "9999").replace(/F/g, "9999").replace(/m/g, "19").replace(/d/g, "39").replace(/H/g, "29").replace(/i/g, "59").replace(/s/g, "59");
                        case "string" == b.type(a.mask):
                            p(a.mask, e.val()) || e.val(a.mask.replace(/[0-9]/g, "_")), e.on("keydown.xdsoft", function (l) {
                                var d = this.value, c = l.which;
                                switch (!0) {
                                    case 48 <= c && 57 >= c || 96 <= c && 105 >= c || 8 == c || 46 == c:
                                        var h;
                                        a:{
                                            try {
                                                if (document.selection && document.selection.createRange) {
                                                    h = document.selection.createRange().getBookmark().charCodeAt(2) -
                                                        2;
                                                    break a
                                                } else if (this.setSelectionRange) {
                                                    h = this.selectionStart;
                                                    break a
                                                }
                                            } catch (f) {
                                                h = 0;
                                                break a
                                            }
                                            h = void 0
                                        }
                                        var n = 8 != c && 46 != c ? String.fromCharCode(96 <= c && 105 >= c ? c - 48 : c) : "_";
                                        8 != c && 46 != c || !h || (h--, n = "_");
                                        for (; /[^0-9_]/.test(a.mask.substr(h, 1)) && h < a.mask.length && 0 < h;)h += 8 == c || 46 == c ? -1 : 1;
                                        d = d.substr(0, h) + n + d.substr(h + 1);
                                        if ("" == b.trim(d)) d = a.mask.replace(/[0-9]/g, "_"); else if (h == a.mask.length)break;
                                        for (h += 8 == c || 46 == c ? 0 : 1; /[^0-9_]/.test(a.mask.substr(h, 1)) && h < a.mask.length && 0 < h;)h += 8 == c || 46 == c ? -1 : 1;
                                        if (p(a.mask,
                                                d)) {
                                            if (this.value = d, d = this, d = "string" == typeof d || d instanceof String ? document.getElementById(d) : d) d.createTextRange ? (d = d.createTextRange(), d.collapse(!0), d.moveEnd(h), d.moveStart(h), d.select()) : d.setSelectionRange && d.setSelectionRange(h, h)
                                        } else"" == b.trim(d) ? this.value = a.mask.replace(/[0-9]/g, "_") : e.trigger("error_input.xdsoft");
                                        break;
                                    case !!~[65, 67, 86, 90, 89].indexOf(c) && g:
                                    case !!~[27, 38, 40, 37, 39, 116, 17, 9, 13].indexOf(c):
                                        return !0
                                }
                                l.preventDefault();
                                return !1
                            })
                    }
                }
                if (a.validateOnBlur) e.off("blur.xdsoft").on("blur.xdsoft",
                    function () {
                        a.allowBlank && !b.trim(b(this).val()).length ? (b(this).val(null), d.data("xdsoft_datetime").empty()) : (Date.parseDate(b(this).val(), a.format) || b(this).val(f.now().dateFormat(a.format)), d.data("xdsoft_datetime").setCurrentTime(b(this).val()));
                        d.trigger("changedatetime.xdsoft")
                    });
                a.dayOfWeekStartPrev = 0 == a.dayOfWeekStart ? 6 : a.dayOfWeekStart - 1;
                d.trigger("xchange.xdsoft").trigger("afterOpen.xdsoft")
            };
            d.data("options", a).on("mousedown.xdsoft", function (a) {
                a.stopPropagation();
                a.preventDefault();
                E.hide();
                D.hide();
                return !1
            });
            var F = z.find(".xdsoft_time_box");
            F.append(r);
            F.xdsoftScroller();
            d.on("afterOpen.xdsoft", function () {
                F.xdsoftScroller()
            });
            d.append(k).append(z);
            !0 !== a.withoutCopyright && d.append(n);
            k.append(m).append(q);
            b("body").append(d);
            var f = new function () {
                var b = this;
                b.now = function () {
                    var b = new Date;
                    a.yearOffset && b.setFullYear(b.getFullYear() + a.yearOffset);
                    return b
                };
                b.currentTime = this.now();
                b.isValidDate = function (a) {
                    return "[object Date]" !== Object.prototype.toString.call(a) ? !1 : !isNaN(a.getTime())
                };
                b.setCurrentTime = function (a) {
                    b.currentTime = "string" == typeof a ? b.strToDateTime(a) : b.isValidDate(a) ? a : b.now();
                    d.trigger("xchange.xdsoft")
                };
                b.empty = function () {
                    b.currentTime = null
                };
                b.getCurrentTime = function (a) {
                    return b.currentTime
                };
                b.nextMonth = function () {
                    var p = b.currentTime.getMonth() + 1;
                    12 == p && (b.currentTime.setFullYear(b.currentTime.getFullYear() + 1), p = 0);
                    b.currentTime.setDate(Math.min(Date.daysInMonth[p], b.currentTime.getDate()));
                    b.currentTime.setMonth(p);
                    a.onChangeMonth && a.onChangeMonth.call && a.onChangeMonth.call(d,
                        f.currentTime, d.data("input"));
                    d.trigger("xchange.xdsoft");
                    return p
                };
                b.prevMonth = function () {
                    var p = b.currentTime.getMonth() - 1;
                    -1 == p && (b.currentTime.setFullYear(b.currentTime.getFullYear() - 1), p = 11);
                    b.currentTime.setDate(Math.min(Date.daysInMonth[p], b.currentTime.getDate()));
                    b.currentTime.setMonth(p);
                    a.onChangeMonth && a.onChangeMonth.call && a.onChangeMonth.call(d, f.currentTime, d.data("input"));
                    d.trigger("xchange.xdsoft");
                    return p
                };
                b.strToDateTime = function (d) {
                    var c = [];
                    (c = /^(\+|\-)(.*)$/.exec(d)) && (c[2] =
                        Date.parseDate(c[2], a.formatDate)) ? (d = c[2].getTime() - 6E4 * c[2].getTimezoneOffset(), c = new Date(f.now().getTime() + parseInt(c[1] + "1") * d)) : c = d ? Date.parseDate(d, a.format) : b.now();
                    b.isValidDate(c) || (c = b.now());
                    return c
                };
                b.strtodate = function (d) {
                    d = d ? Date.parseDate(d, a.formatDate) : b.now();
                    b.isValidDate(d) || (d = b.now());
                    return d
                };
                b.strtotime = function (d) {
                    d = d ? Date.parseDate(d, a.formatTime) : b.now();
                    b.isValidDate(d) || (d = b.now());
                    return d
                };
                b.str = function () {
                    return b.currentTime.dateFormat(a.format)
                }
            };
            m.find(".xdsoft_today_button").on("mousedown.xdsoft",
                function () {
                    d.data("changed", !0);
                    f.setCurrentTime(0);
                    d.trigger("afterOpen.xdsoft")
                }).on("dblclick.xdsoft", function () {
                e.val(f.str());
                d.trigger("close.xdsoft")
            });
            m.find(".xdsoft_prev,.xdsoft_next").on("mousedown.xdsoft", function () {
                var d = b(this), c = 0, e = !1;
                (function L(b) {
                    f.currentTime.getMonth();
                    d.hasClass(a.next) ? f.nextMonth() : d.hasClass(a.prev) && f.prevMonth();
                    a.monthChangeSpinner && !e && (c = setTimeout(L, b ? b : 100))
                })(500);
                b([document.body, window]).on("mouseup.xdsoft", function h() {
                    clearTimeout(c);
                    e = !0;
                    b([document.body,
                        window]).off("mouseup.xdsoft", h)
                })
            });
            z.find(".xdsoft_prev,.xdsoft_next").on("mousedown.xdsoft", function () {
                var d = b(this), c = 0, e = !1, f = 110;
                (function h(b) {
                    var n = w[0].clientHeight, g = r[0].offsetHeight, k = Math.abs(parseInt(r.css("marginTop")));
                    d.hasClass(a.next) && g - n - a.timeHeightInTimePicker >= k ? r.css("marginTop", "-" + (k + a.timeHeightInTimePicker) + "px") : d.hasClass(a.prev) && 0 <= k - a.timeHeightInTimePicker && r.css("marginTop", "-" + (k - a.timeHeightInTimePicker) + "px");
                    w.trigger("scroll_element.xdsoft_scroller", [Math.abs(parseInt(r.css("marginTop")) /
                        (g - n))]);
                    f = 10 < f ? 10 : f - 10;
                    !e && (c = setTimeout(h, b ? b : f))
                })(500);
                b([document.body, window]).on("mouseup.xdsoft", function M() {
                    clearTimeout(c);
                    e = !0;
                    b([document.body, window]).off("mouseup.xdsoft", M)
                })
            });
            var I = 0;
            d.on("xchange.xdsoft", function (c) {
                clearTimeout(I);
                I = setTimeout(function () {
                    for (var c = "", e = new Date(f.currentTime.getFullYear(), f.currentTime.getMonth(), 1, 12, 0, 0), l = 0, n = f.now(); e.getDay() != a.dayOfWeekStart;)e.setDate(e.getDate() - 1);
                    for (var c = c + "<table><thead><tr>", h = 0; 7 > h; h++)c += "<th>" + a.i18n[a.lang].dayOfWeek[6 <
                        h + a.dayOfWeekStart ? 0 : h + a.dayOfWeekStart] + "</th>";
                    var c = c + "</tr></thead><tbody><tr>", g = h = !1;
                    !1 !== a.maxDate && (h = f.strtodate(a.maxDate), h = new Date(h.getFullYear(), h.getMonth(), h.getDate(), 23, 59, 59, 999));
                    !1 !== a.minDate && (g = f.strtodate(a.minDate), g = new Date(g.getFullYear(), g.getMonth(), g.getDate()));
                    for (var k, v, s, t = []; l < f.currentTime.countDaysInMonth() || e.getDay() != a.dayOfWeekStart || f.currentTime.getMonth() == e.getMonth();)t = [], l++, k = e.getDate(), v = e.getFullYear(), s = e.getMonth(), t.push("xdsoft_date"), (!1 !==
                    h && e > h || !1 !== g && e < g) && t.push("xdsoft_disabled"), f.currentTime.getMonth() != s && t.push("xdsoft_other_month"), (a.defaultSelect || d.data("changed")) && f.currentTime.dateFormat(a.formatDate) == e.dateFormat(a.formatDate) && t.push("xdsoft_current"), n.dateFormat(a.formatDate) == e.dateFormat(a.formatDate) && t.push("xdsoft_today"), (0 == e.getDay() || 6 == e.getDay() || ~a.weekends.indexOf(e.dateFormat(a.formatDate))) && t.push("xdsoft_weekend"), a.beforeShowDay && "function" == typeof a.beforeShowDay && t.push(a.beforeShowDay(e)),
                        c += '<td data-date="' + k + '" data-month="' + s + '" data-year="' + v + '" class="xdsoft_date xdsoft_day_of_week' + e.getDay() + " " + t.join(" ") + '"><div>' + k + "</div></td>", e.getDay() == a.dayOfWeekStartPrev && (c += "</tr>"), e.setDate(k + 1);
                    c += "</tbody></table>";
                    q.html(c);
                    m.find(".xdsoft_label span").eq(0).text(a.i18n[a.lang].months[f.currentTime.getMonth()]);
                    m.find(".xdsoft_label span").eq(1).text(f.currentTime.getFullYear());
                    var u = "";
                    s = c = "";
                    e = function (b, c) {
                        var e = f.now();
                        e.setHours(b);
                        b = parseInt(e.getHours());
                        e.setMinutes(c);
                        c = parseInt(e.getMinutes());
                        t = [];
                        (!1 !== a.maxTime && f.strtotime(a.maxTime).getTime() < e.getTime() || !1 !== a.minTime && f.strtotime(a.minTime).getTime() > e.getTime()) && t.push("xdsoft_disabled");
                        (a.initTime || a.defaultSelect || d.data("changed")) && parseInt(f.currentTime.getHours()) == parseInt(b) && (59 < a.step || Math[a.roundTime](f.currentTime.getMinutes() / a.step) * a.step == parseInt(c)) && (a.defaultSelect || d.data("changed") ? t.push("xdsoft_current") : a.initTime && t.push("xdsoft_init_time"));
                        parseInt(n.getHours()) == parseInt(b) &&
                        parseInt(n.getMinutes()) == parseInt(c) && t.push("xdsoft_today");
                        u += '<div class="xdsoft_time ' + t.join(" ") + '" data-hour="' + b + '" data-minute="' + c + '">' + e.dateFormat(a.formatTime) + "</div>"
                    };
                    if (a.allowTimes && b.isArray(a.allowTimes) && a.allowTimes.length)for (l = 0; l < a.allowTimes.length; l++)c = f.strtotime(a.allowTimes[l]).getHours(), s = f.strtotime(a.allowTimes[l]).getMinutes(), e(c, s); else for (h = l = 0; l < (a.hours12 ? 12 : 24); l++)for (h = 0; 60 > h; h += a.step)c = (10 > l ? "0" : "") + l, s = (10 > h ? "0" : "") + h, e(c, s);
                    r.html(u);
                    s = "";
                    l = 0;
                    for (l =
                             parseInt(a.yearStart, 10) + a.yearOffset; l <= parseInt(a.yearEnd, 10) + a.yearOffset; l++)s += '<div class="xdsoft_option ' + (f.currentTime.getFullYear() == l ? "xdsoft_current" : "") + '" data-value="' + l + '">' + l + "</div>";
                    E.children().eq(0).html(s);
                    l = 0;
                    for (s = ""; 11 >= l; l++)s += '<div class="xdsoft_option ' + (f.currentTime.getMonth() == l ? "xdsoft_current" : "") + '" data-value="' + l + '">' + a.i18n[a.lang].months[l] + "</div>";
                    D.children().eq(0).html(s);
                    b(d).trigger("generate.xdsoft")
                }, 10);
                c.stopPropagation()
            }).on("afterOpen.xdsoft", function () {
                if (a.timepicker) {
                    var b;
                    r.find(".xdsoft_current").length ? b = ".xdsoft_current" : r.find(".xdsoft_init_time").length && (b = ".xdsoft_init_time");
                    if (b) {
                        var d = w[0].clientHeight, c = r[0].offsetHeight;
                        b = r.find(b).index() * a.timeHeightInTimePicker + 1;
                        c - d < b && (b = c - d);
                        w.trigger("scroll_element.xdsoft_scroller", [parseInt(b) / (c - d)])
                    } else w.trigger("scroll_element.xdsoft_scroller", [0])
                }
            });
            var G = 0;
            q.on("click.xdsoft", "td", function (c) {
                c.stopPropagation();
                G++;
                c = b(this);
                var p = f.currentTime;
                if (c.hasClass("xdsoft_disabled"))return !1;
                p.setDate(1);
                p.setFullYear(c.data("year"));
                p.setMonth(c.data("month"));
                p.setDate(c.data("date"));
                d.trigger("select.xdsoft", [p]);
                e.val(f.str());
                (1 < G || !0 === a.closeOnDateSelect || 0 === a.closeOnDateSelect && !a.timepicker) && !a.inline && d.trigger("close.xdsoft");
                a.onSelectDate && a.onSelectDate.call && a.onSelectDate.call(d, f.currentTime, d.data("input"));
                d.data("changed", !0);
                d.trigger("xchange.xdsoft");
                d.trigger("changedatetime.xdsoft");
                setTimeout(function () {
                    G = 0
                }, 200)
            });
            r.on("click.xdsoft", "div", function (c) {
                c.stopPropagation();
                c = b(this);
                var e = f.currentTime;
                if (c.hasClass("xdsoft_disabled"))return !1;
                e.setHours(c.data("hour"));
                e.setMinutes(c.data("minute"));
                d.trigger("select.xdsoft", [e]);
                d.data("input").val(f.str());
                !a.inline && d.trigger("close.xdsoft");
                a.onSelectTime && a.onSelectTime.call && a.onSelectTime.call(d, f.currentTime, d.data("input"));
                d.data("changed", !0);
                d.trigger("xchange.xdsoft");
                d.trigger("changedatetime.xdsoft")
            });
            d.mousewheel && k.mousewheel(function (b, d, c, e) {
                if (!a.scrollMonth)return !0;
                0 > d ? f.nextMonth() : f.prevMonth();
                return !1
            });
            d.mousewheel &&
            w.unmousewheel().mousewheel(function (b, d, c, e) {
                if (!a.scrollTime)return !0;
                c = w[0].clientHeight;
                e = r[0].offsetHeight;
                var f = Math.abs(parseInt(r.css("marginTop"))), h = !0;
                0 > d && e - c - a.timeHeightInTimePicker >= f ? (r.css("marginTop", "-" + (f + a.timeHeightInTimePicker) + "px"), h = !1) : 0 < d && 0 <= f - a.timeHeightInTimePicker && (r.css("marginTop", "-" + (f - a.timeHeightInTimePicker) + "px"), h = !1);
                w.trigger("scroll_element.xdsoft_scroller", [Math.abs(parseInt(r.css("marginTop")) / (e - c))]);
                b.stopPropagation();
                return h
            });
            var B = !1;
            d.on("changedatetime.xdsoft",
                function () {
                    if (a.onChangeDateTime && a.onChangeDateTime.call) {
                        var b = d.data("input");
                        a.onChangeDateTime.call(d, f.currentTime, b);
                        b.trigger("change")
                    }
                }).on("generate.xdsoft", function () {
                a.onGenerate && a.onGenerate.call && a.onGenerate.call(d, f.currentTime, d.data("input"));
                B && (d.trigger("afterOpen.xdsoft"), B = !1)
            }).on("click.xdsoft", function (a) {
                a.stopPropagation()
            });
            var y = 0;
            e.mousewheel && e.mousewheel(function (b, c, g, n) {
                if (!a.scrollInput)return !0;
                if (!a.datepicker && a.timepicker)return y = r.find(".xdsoft_current").length ?
                    r.find(".xdsoft_current").eq(0).index() : 0, 0 <= y + c && y + c < r.children().length && (y += c), r.children().eq(y).length && r.children().eq(y).trigger("mousedown"), !1;
                if (a.datepicker && !a.timepicker)return k.trigger(b, [c, g, n]), e.val && e.val(f.str()), d.trigger("changedatetime.xdsoft"), !1
            });
            var H = function () {
                var c = d.data("input").offset(), e = c.top + d.data("input")[0].offsetHeight - 1, f = c.left,
                    g = "absolute";
                a.fixed ? (e -= b(window).scrollTop(), f -= b(window).scrollLeft(), g = "fixed") : (e + d[0].offsetHeight > b(window).height() + b(window).scrollTop() &&
                (e = c.top - d[0].offsetHeight + 1), 0 > e && (e = 0), f + d[0].offsetWidth > b(window).width() && (f = c.left - d[0].offsetWidth + d.data("input")[0].offsetWidth));
                d.css({left: f, top: e, position: g})
            };
            d.on("open.xdsoft", function () {
                var c = !0;
                a.onShow && a.onShow.call && (c = a.onShow.call(d, f.currentTime, d.data("input")));
                if (!1 !== c && (d.show(), H(), b(window).off("resize.xdsoft", H).on("resize.xdsoft", H), a.closeOnWithoutClick)) b([document.body, window]).on("mousedown.xdsoft", function K() {
                    d.trigger("close.xdsoft");
                    b([document.body, window]).off("mousedown.xdsoft",
                        K)
                })
            }).on("close.xdsoft", function (b) {
                var c = !0;
                a.onClose && a.onClose.call && (c = a.onClose.call(d, f.currentTime, d.data("input")));
                !1 === c || a.opened || a.inline || d.hide();
                b.stopPropagation()
            }).data("input", e);
            var J = 0;
            d.data("xdsoft_datetime", f);
            d.setOptions(a);
            f.setCurrentTime(c());
            e.data("xdsoft_datetimepicker", d).on("open.xdsoft focusin.xdsoft mousedown.xdsoft", function (a) {
                e.is(":disabled") || e.is(":hidden") || !e.is(":visible") || (clearTimeout(J), J = setTimeout(function () {
                    e.is(":disabled") || e.is(":hidden") ||
                    !e.is(":visible") || (B = !0, f.setCurrentTime(c()), d.trigger("open.xdsoft"))
                }, 100))
            }).on("keydown.xdsoft", function (a) {
                a = a.which;
                switch (!0) {
                    case !!~[13].indexOf(a):
                        return a = b("input:visible,textarea:visible"), d.trigger("close.xdsoft"), a.eq(a.index(this) + 1).focus(), !1;
                    case !!~[9].indexOf(a):
                        return d.trigger("close.xdsoft"), !0
                }
            })
        };
        b(document).off("keydown.xdsoftctrl keyup.xdsoftctrl").on("keydown.xdsoftctrl", function (a) {
            17 == a.keyCode && (g = !0)
        }).on("keyup.xdsoftctrl", function (a) {
            17 == a.keyCode && (g = !1)
        });
        return this.each(function () {
            var c;
            if (c = b(this).data("xdsoft_datetimepicker")) {
                if ("string" === b.type(k))switch (k) {
                    case "show":
                        b(this).select().focus();
                        c.trigger("open.xdsoft");
                        break;
                    case "hide":
                        c.trigger("close.xdsoft");
                        break;
                    case "destroy":
                        c = b(this);
                        var g = c.data("xdsoft_datetimepicker");
                        g && (g.data("xdsoft_datetime", null), g.remove(), c.data("xdsoft_datetimepicker", null).off("open.xdsoft focusin.xdsoft focusout.xdsoft mousedown.xdsoft blur.xdsoft keydown.xdsoft"), b(window).off("resize.xdsoft"), b([window, document.body]).off("mousedown.xdsoft"),
                        c.unmousewheel && c.unmousewheel());
                        break;
                    case "reset":
                        (this.value = this.defaultValue) && c.data("xdsoft_datetime").isValidDate(Date.parseDate(this.value, a.format)) || c.data("changed", !1), c.data("xdsoft_datetime").setCurrentTime(this.value)
                } else c.setOptions(k);
                return 0
            }
            "string" !== b.type(k) && (!a.lazyInit || a.open || a.inline ? n(b(this)) : m(b(this)))
        })
    };
    b.fn.datetimepicker.defaults = c
})(jQuery);
(function (b) {
    "function" === typeof define && define.amd ? define(["jquery"], b) : "object" === typeof exports ? module.exports = b : b(jQuery)
})(function (b) {
    function c(c) {
        var e = c || window.event, g = [].slice.call(arguments, 1), d = 0, k = 0, m = 0, x = 0, x = 0;
        c = b.event.fix(e);
        c.type = "mousewheel";
        e.wheelDelta && (d = e.wheelDelta);
        e.detail && (d = -1 * e.detail);
        e.deltaY && (d = m = -1 * e.deltaY);
        e.deltaX && (k = e.deltaX, d = -1 * k);
        void 0 !== e.wheelDeltaY && (m = e.wheelDeltaY);
        void 0 !== e.wheelDeltaX && (k = -1 * e.wheelDeltaX);
        x = Math.abs(d);
        if (!a || x < a) a = x;
        x = Math.max(Math.abs(m),
            Math.abs(k));
        if (!q || x < q) q = x;
        e = 0 < d ? "floor" : "ceil";
        d = Math[e](d / a);
        k = Math[e](k / q);
        m = Math[e](m / q);
        g.unshift(c, d, k, m);
        return (b.event.dispatch || b.event.handle).apply(this, g)
    }

    var k = ["wheel", "mousewheel", "DOMMouseScroll", "MozMousePixelScroll"],
        g = "onwheel" in document || 9 <= document.documentMode ? ["wheel"] : ["mousewheel", "DomMouseScroll", "MozMousePixelScroll"],
        a, q;
    if (b.event.fixHooks)for (var m = k.length; m;)b.event.fixHooks[k[--m]] = b.event.mouseHooks;
    b.event.special.mousewheel = {
        setup: function () {
            if (this.addEventListener)for (var a =
                g.length; a;)this.addEventListener(g[--a], c, !1); else this.onmousewheel = c
        }, teardown: function () {
            if (this.removeEventListener)for (var a = g.length; a;)this.removeEventListener(g[--a], c, !1); else this.onmousewheel = null
        }
    };
    b.fn.extend({
        mousewheel: function (a) {
            return a ? this.bind("mousewheel", a) : this.trigger("mousewheel")
        }, unmousewheel: function (a) {
            return this.unbind("mousewheel", a)
        }
    })
});
Date.parseFunctions = {count: 0};
Date.parseRegexes = [];
Date.formatFunctions = {count: 0};
Date.prototype.dateFormat = function (b) {
    if ("unixtime" == b)return parseInt(this.getTime() / 1E3);
    null == Date.formatFunctions[b] && Date.createNewFormat(b);
    return this[Date.formatFunctions[b]]()
};
Date.createNewFormat = function (b) {
    var c = "format" + Date.formatFunctions.count++;
    Date.formatFunctions[b] = c;
    for (var c = "Date.prototype." + c + " = function() {return ", k = !1, g = "", a = 0; a < b.length; ++a)g = b.charAt(a), k || "\\" != g ? k ? (k = !1, c += "'" + String.escape(g) + "' + ") : c += Date.getFormatCode(g) : k = !0;
    eval(c.substring(0, c.length - 3) + ";}")
};
Date.getFormatCode = function (b) {
    switch (b) {
        case "d":
            return "String.leftPad(this.getDate(), 2, '0') + ";
        case "D":
            return "Date.dayNames[this.getDay()].substring(0, 3) + ";
        case "j":
            return "this.getDate() + ";
        case "l":
            return "Date.dayNames[this.getDay()] + ";
        case "S":
            return "this.getSuffix() + ";
        case "w":
            return "this.getDay() + ";
        case "z":
            return "this.getDayOfYear() + ";
        case "W":
            return "this.getWeekOfYear() + ";
        case "F":
            return "Date.monthNames[this.getMonth()] + ";
        case "m":
            return "String.leftPad(this.getMonth() + 1, 2, '0') + ";
        case "M":
            return "Date.monthNames[this.getMonth()].substring(0, 3) + ";
        case "n":
            return "(this.getMonth() + 1) + ";
        case "t":
            return "this.getDaysInMonth() + ";
        case "L":
            return "(this.isLeapYear() ? 1 : 0) + ";
        case "Y":
            return "this.getFullYear() + ";
        case "y":
            return "('' + this.getFullYear()).substring(2, 4) + ";
        case "a":
            return "(this.getHours() < 12 ? 'am' : 'pm') + ";
        case "A":
            return "(this.getHours() < 12 ? 'AM' : 'PM') + ";
        case "g":
            return "((this.getHours() %12) ? this.getHours() % 12 : 12) + ";
        case "G":
            return "this.getHours() + ";
        case "h":
            return "String.leftPad((this.getHours() %12) ? this.getHours() % 12 : 12, 2, '0') + ";
        case "H":
            return "String.leftPad(this.getHours(), 2, '0') + ";
        case "i":
            return "String.leftPad(this.getMinutes(), 2, '0') + ";
        case "s":
            return "String.leftPad(this.getSeconds(), 2, '0') + ";
        case "O":
            return "this.getGMTOffset() + ";
        case "T":
            return "this.getTimezone() + ";
        case "Z":
            return "(this.getTimezoneOffset() * -60) + ";
        default:
            return "'" + String.escape(b) + "' + "
    }
};
Date.parseDate = function (b, c) {
    if ("unixtime" == c)return new Date(isNaN(parseInt(b)) ? 0 : 1E3 * parseInt(b));
    null == Date.parseFunctions[c] && Date.createParser(c);
    return Date[Date.parseFunctions[c]](b)
};
Date.createParser = function (b) {
    var c = "parse" + Date.parseFunctions.count++, k = Date.parseRegexes.length, g = 1;
    Date.parseFunctions[b] = c;
    for (var c = "Date." + c + " = function(input) {\nvar y = -1, m = -1, d = -1, h = -1, i = -1, s = -1, z = -1;\nvar d = new Date();\ny = d.getFullYear();\nm = d.getMonth();\nd = d.getDate();\nvar results = input.match(Date.parseRegexes[" + k + "]);\nif (results && results.length > 0) {", a = "", q = !1, m = "", n = 0; n < b.length; ++n)m = b.charAt(n), q || "\\" != m ? q ? (q = !1, a += String.escape(m)) : (obj = Date.formatCodeToRegex(m,
        g), g += obj.g, a += obj.s, obj.g && obj.c && (c += obj.c)) : q = !0;
    c += "if (y > 0 && z > 0){\nvar doyDate = new Date(y,0);\ndoyDate.setDate(z);\nm = doyDate.getMonth();\nd = doyDate.getDate();\n}if (y > 0 && m >= 0 && d > 0 && h >= 0 && i >= 0 && s >= 0)\n{return new Date(y, m, d, h, i, s);}\nelse if (y > 0 && m >= 0 && d > 0 && h >= 0 && i >= 0)\n{return new Date(y, m, d, h, i);}\nelse if (y > 0 && m >= 0 && d > 0 && h >= 0)\n{return new Date(y, m, d, h);}\nelse if (y > 0 && m >= 0 && d > 0)\n{return new Date(y, m, d);}\nelse if (y > 0 && m >= 0)\n{return new Date(y, m);}\nelse if (y > 0)\n{return new Date(y);}\n}return null;}";
    Date.parseRegexes[k] = new RegExp("^" + a + "$");
    eval(c)
};
Date.formatCodeToRegex = function (b, c) {
    switch (b) {
        case "D":
            return {g: 0, c: null, s: "(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)"};
        case "j":
        case "d":
            return {g: 1, c: "d = parseInt(results[" + c + "], 10);\n", s: "(\\d{1,2})"};
        case "l":
            return {g: 0, c: null, s: "(?:" + Date.dayNames.join("|") + ")"};
        case "S":
            return {g: 0, c: null, s: "(?:st|nd|rd|th)"};
        case "w":
            return {g: 0, c: null, s: "\\d"};
        case "z":
            return {g: 1, c: "z = parseInt(results[" + c + "], 10);\n", s: "(\\d{1,3})"};
        case "W":
            return {g: 0, c: null, s: "(?:\\d{2})"};
        case "F":
            return {
                g: 1, c: "m = parseInt(Date.monthNumbers[results[" +
                c + "].substring(0, 3)], 10);\n", s: "(" + Date.monthNames.join("|") + ")"
            };
        case "M":
            return {
                g: 1,
                c: "m = parseInt(Date.monthNumbers[results[" + c + "]], 10);\n",
                s: "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
            };
        case "n":
        case "m":
            return {g: 1, c: "m = parseInt(results[" + c + "], 10) - 1;\n", s: "(\\d{1,2})"};
        case "t":
            return {g: 0, c: null, s: "\\d{1,2}"};
        case "L":
            return {g: 0, c: null, s: "(?:1|0)"};
        case "Y":
            return {g: 1, c: "y = parseInt(results[" + c + "], 10);\n", s: "(\\d{4})"};
        case "y":
            return {
                g: 1, c: "var ty = parseInt(results[" + c + "], 10);\ny = ty > Date.y2kYear ? 1900 + ty : 2000 + ty;\n",
                s: "(\\d{1,2})"
            };
        case "a":
            return {
                g: 1,
                c: "if (results[" + c + "] == 'am') {\nif (h == 12) { h = 0; }\n} else { if (h < 12) { h += 12; }}",
                s: "(am|pm)"
            };
        case "A":
            return {
                g: 1,
                c: "if (results[" + c + "] == 'AM') {\nif (h == 12) { h = 0; }\n} else { if (h < 12) { h += 12; }}",
                s: "(AM|PM)"
            };
        case "g":
        case "G":
        case "h":
        case "H":
            return {g: 1, c: "h = parseInt(results[" + c + "], 10);\n", s: "(\\d{1,2})"};
        case "i":
            return {g: 1, c: "i = parseInt(results[" + c + "], 10);\n", s: "(\\d{2})"};
        case "s":
            return {
                g: 1, c: "s = parseInt(results[" + c + "], 10);\n",
                s: "(\\d{2})"
            };
        case "O":
            return {g: 0, c: null, s: "[+-]\\d{4}"};
        case "T":
            return {g: 0, c: null, s: "[A-Z]{3}"};
        case "Z":
            return {g: 0, c: null, s: "[+-]\\d{1,5}"};
        default:
            return {g: 0, c: null, s: String.escape(b)}
    }
};
Date.prototype.getTimezone = function () {
    return this.toString().replace(/^.*? ([A-Z]{3}) [0-9]{4}.*$/, "$1").replace(/^.*?\(([A-Z])[a-z]+ ([A-Z])[a-z]+ ([A-Z])[a-z]+\)$/, "$1$2$3")
};
Date.prototype.getGMTOffset = function () {
    return (0 < this.getTimezoneOffset() ? "-" : "+") + String.leftPad(Math.floor(Math.abs(this.getTimezoneOffset()) / 60), 2, "0") + String.leftPad(Math.abs(this.getTimezoneOffset()) % 60, 2, "0")
};
Date.prototype.getDayOfYear = function () {
    var b = 0;
    Date.daysInMonth[1] = this.isLeapYear() ? 29 : 28;
    for (var c = 0; c < this.getMonth(); ++c)b += Date.daysInMonth[c];
    return b + this.getDate()
};
Date.prototype.getWeekOfYear = function () {
    var b = this.getDayOfYear() + (4 - this.getDay()), c = 7 - (new Date(this.getFullYear(), 0, 1)).getDay() + 4;
    return String.leftPad(Math.ceil((b - c) / 7) + 1, 2, "0")
};
Date.prototype.isLeapYear = function () {
    var b = this.getFullYear();
    return 0 == (b & 3) && (b % 100 || 0 == b % 400 && b)
};
Date.prototype.getFirstDayOfMonth = function () {
    var b = (this.getDay() - (this.getDate() - 1)) % 7;
    return 0 > b ? b + 7 : b
};
Date.prototype.getLastDayOfMonth = function () {
    var b = (this.getDay() + (Date.daysInMonth[this.getMonth()] - this.getDate())) % 7;
    return 0 > b ? b + 7 : b
};
Date.prototype.getDaysInMonth = function () {
    Date.daysInMonth[1] = this.isLeapYear() ? 29 : 28;
    return Date.daysInMonth[this.getMonth()]
};
Date.prototype.getSuffix = function () {
    switch (this.getDate()) {
        case 1:
        case 21:
        case 31:
            return "st";
        case 2:
        case 22:
            return "nd";
        case 3:
        case 23:
            return "rd";
        default:
            return "th"
    }
};
String.escape = function (b) {
    return b.replace(/('|\\)/g, "\\$1")
};
String.leftPad = function (b, c, k) {
    b = String(b);
    for (null == k && (k = " "); b.length < c;)b = k + b;
    return b
};
Date.daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
Date.monthNames = "January February March April May June July August September October November December".split(" ");
Date.dayNames = "Sunday Monday Tuesday Wednesday Thursday Friday Saturday".split(" ");
Date.y2kYear = 50;
Date.monthNumbers = {Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5, Jul: 6, Aug: 7, Sep: 8, Oct: 9, Nov: 10, Dec: 11};
Date.patterns = {
    ISO8601LongPattern: "Y-m-d H:i:s",
    ISO8601ShortPattern: "Y-m-d",
    ShortDatePattern: "n/j/Y",
    LongDatePattern: "l, F d, Y",
    FullDateTimePattern: "l, F d, Y g:i:s A",
    MonthDayPattern: "F d",
    ShortTimePattern: "g:i A",
    LongTimePattern: "g:i:s A",
    SortableDateTimePattern: "Y-m-d\\TH:i:s",
    UniversalSortableDateTimePattern: "Y-m-d H:i:sO",
    YearMonthPattern: "F, Y"
};