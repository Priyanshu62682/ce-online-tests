var myInterval, AttemptedAns = [], TotalTime = 0;

function NextQuestion(e) {
    var t = $(".test-questions").find("li.active");
    if (CheckNextPrevButtons(), t.is(":last-child")) return !1;
    $(".test-questions").find("li").removeClass("active"), t.next().addClass("active"), OpenCurrentQue(t.next().find("a")), e && (t.find("a").addClass("que-not-answered"), t.find("a").removeClass("que-not-attempted"));
    var a = t.attr("data-seq");
    $(".nav-tab-sections").find("li").removeClass("active"), $(".nav-tab-sections").find("li[data-id=" + a + "]").addClass("active"), CheckQueAttemptStatus()
}

function PrevQuestion(e) {
    var t = $(".test-questions").find("li.active");
    if (CheckNextPrevButtons(), t.is(":first-child")) return !1;
    $(".test-questions").find("li").removeClass("active"), t.prev().addClass("active"), OpenCurrentQue(t.prev().find("a"));
    var a = t.attr("data-seq");
    $(".nav-tab-sections").find("li").removeClass("active"), $(".nav-tab-sections").find("li[data-id=" + a + "]").addClass("active"), CheckQueAttemptStatus()
}

function CheckNextPrevButtons() {
    var e = $(".test-questions").find("li.active");
    $("#btnPrevQue").removeAttr("disabled"), $("#btnNextQue").removeAttr("disabled"), e.is(":first-child") ? $("#btnPrevQue").attr("disabled", "disabled") : e.is(":last-child") && $("#btnNextQue").attr("disabled", "disabled")
}

function pad(e, t) {
    for (var a = e + ""; a.length < t;) a = "0" + a;
    return a
}

function OpenCurrentQue(e) {
    $(".tab-content").hide(), $("#lblQueNumber").text(e.text()), $("#" + e.attr("data-href")).show();
    var t = e.parent().attr("data-seq");
    $(".nav-tab-sections").find("li").removeClass("active"), $(".nav-tab-sections").find("li[data-id=" + t + "]").addClass("active"), CheckQueAttemptStatus()
}

function CoundownTimer(e) {
    var t = 60 * e;
    myInterval = setInterval(function () {
        myTimeSpan = 1e3 * t, $(".timer-title").text(GetTime(myTimeSpan)), t < 600 ? ($(".timer-title").addClass("time-ending"), $(".timer-title").removeClass("time-started")) : ($(".timer-title").addClass("time-started"), $(".timer-title").removeClass("time-ending")), t > 0 ? t -= 1 : CleartTimer()
    }, 1e3)
}

function CleartTimer() {
    clearInterval(myInterval), $("title").text("Time Out"), $("#btnYesSubmitConfirm").trigger("click")
}

function GetTime(e) {
    parseInt(e % 1e3 / 100);
    var t = parseInt(e / 1e3 % 60),
        a = parseInt(e / 6e4 % 60),
        n = parseInt(e / 36e5 % 24);
    return (n = n < 10 ? "0" + n : n) + ":" + (a = a < 10 ? "0" + a : a) + ":" + (t < 10 ? "0" + t : t)
}

function pretty_time_string(e) {
    return (e < 10 ? "0" : "") + e
}

function CheckQueExists(e) {
    $.each(AttemptedAns, function (t, a) {
        void 0 !== a && a[1] == e && AttemptedAns.splice(t, 1)
    })
}

function CheckQueAttemptStatus() {
    var e = 0,
        t = 0,
        a = 0,
        n = 0,
        s = 0,
        i = 0;
    $(".test-questions").find("li").each(function () {
        var r = $(this);
        e += 1, r.children().hasClass("que-save") ? a += 1 : r.children().hasClass("que-save-mark") ? n += 1 : r.children().hasClass("que-mark") ? s += 1 : r.children().hasClass("que-not-answered") ? t += 1 : i += 1
    }), $(".lblTotalQuestion").text(e), $(".lblNotAttempted").text(t), $(".lblTotalSaved").text(a), $(".lblTotalSaveMarkForReview").text(n), $(".lblTotalMarkForReview").text(s), $(".lblNotVisited").text(i)
}

function sendResponseData(studentName, examId, questionNumber, selectedOption, flag) {
    var answerResponse={
        "questionNumber" : parseInt(questionNumber),
        "choice": parseInt(selectedOption),
        "state": parseInt(selectedOption)
    };
    var answerResponseJ= JSON.stringify(answerResponse);
    $.ajax({
        type:'POST',
        url: "{% url 'online_test_frontend:submitselected' %}",
        data:{
            
            student:studentName,
            exam_id: examId,
            progress: answerResponseJ,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success:function(){
            console.log('saved')
        }
    });
}

$(document).ready(function () {
    $("#page01").show(); $(".exam-paper").show();
    CoundownTimer(parseInt($("#hdfTestDuration").val()));
    CheckNextPrevButtons();
    CheckQueAttemptStatus();
    $("#btnPrevQue").click(function () {
        PrevQuestion(!0)
    });
    $("#btnNextQue").click(function () {
        NextQuestion(!0)
    });
    $(".test-ques").click(function () {
        var e = $(".test-questions").find("li.active").find("a");
        $(".test-questions").find("li").removeClass("active"),
            $(this).parent().addClass("active"),
            $(this).hasClass("que-save") || $(this).hasClass("que-save-mark") || $(this).hasClass("que-mark") || ($(this).addClass("que-not-answered"), $(this).removeClass("que-not-attempted")), e.hasClass("que-save") || e.hasClass("que-save-mark") || e.hasClass("que-mark") || (e.addClass("que-not-answered"), e.removeClass("que-not-attempted")), OpenCurrentQue($(this))
    });

    $(".btn-save-answer").click(function (e) {
        e.preventDefault();
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href"),
            questionNumber = parseInt(a.match(/(\d+)/g)[0]), //question number
            selectedOption = $("input[name='radios" + a + "']:checked").val() ? $("input[name='radios" + a + "']:checked").val() : 0, //selected option
            studentName = $("input[name='radios" + a + "']").attr('studentName'),
            examId = $("input[name='radios" + a + "']").attr('class'),
            n = ($("#" + a).find(".hdfQuestionID").val(), $("#" + a).find(".hdfPaperSetID").val(), $("#" + a).find(".hdfCurrectAns").val(), !1);
        if ($("input[name='radios" + a + "']").each(function () {
            $(this).is(":checked") && (n = !0)
        }), 0 == n) { alert("Please choose an option"); return !1 };
        $("input[name='radios" + a + "']:checked").val(), t.find("a").removeClass("que-save-mark"), t.find("a").removeClass("que-mark"), t.find("a").addClass("que-save"), t.find("a").removeClass("que-not-answered"), t.find("a").removeClass("que-not-attempted"), NextQuestion(!1), CheckQueAttemptStatus();
        sendResponseData(studentName, examId, questionNumber, selectedOption, 0);
    });

    $(".btn-save-mark-answer").click(function (e) {
        e.preventDefault();
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href"),
            questionNumber = parseInt(a.match(/(\d+)/g)[0]) //question number
            selectedOption = $("input[name='radios" + a + "']:checked").val() ? $("input[name='radios" + a + "']:checked").val() : 0, //selected option
            studentName = $("input[name='radios" + a + "']").attr('studentName'),
            examId = $("input[name='radios" + a + "']").attr('class'),
            n = ($("#" + a).find(".hdfQuestionID").val(),
                $("#" + a).find(".hdfPaperSetID").val(),
                $("#" + a).find(".hdfCurrectAns").val(),
                $("#" + a).find(".hdfCurrectAns").val(), !1);
        if ($("input[name='radios" + a + "']").each(function () {
            $(this).is(":checked") && (n = !0)
        }), 0 == n) { alert("Please choose an option"); return !1 };;
        $("input[name='radios" + a + "']:checked").val(), t.find("a").removeClass("que-save"), t.find("a").removeClass("que-mark"), t.find("a").addClass("que-save-mark"), t.find("a").removeClass("que-not-answered"), t.find("a").removeClass("que-not-attempted"), NextQuestion(!1), CheckQueAttemptStatus()
        sendResponseData(studentName, examId, questionNumber, selectedOption, 1);
    });

    $(".btn-mark-answer").click(function (e) {
        e.preventDefault();
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href"),
            questionNumber = parseInt(a.match(/(\d+)/g)[0]), //question number
            studentName = $("input[name='radios" + a + "']").attr('studentName'),
            examId = $("input[name='radios" + a + "']").attr('class');
        $("#" + a).find(".hdfQuestionID").val(), $("#" + a).find(".hdfPaperSetID").val(), $("#" + a).find(".hdfCurrectAns").val(), $("#" + a).find(".hdfCurrectAns").val(), t.find("a").removeClass("que-save-mark"), t.find("a").removeClass("que-save"), t.find("a").addClass("que-mark"), t.find("a").removeClass("que-not-answered"), t.find("a").removeClass("que-not-attempted"), NextQuestion(!1), CheckQueAttemptStatus()
        sendResponseData(studentName, examId, questionNumber, 0, 1);
    });

    $(".btn-reset-answer").click(function (e) {
        e.preventDefault();
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href");
        $("#" + a).attr("data-queid"), t.find("a").removeClass("saved-que"),
            $("input[name='radios" + a + "']:checked").each(function () {
                $(this).prop("checked", !1).change()
            }), $("input[name='chk" + a + "']").each(function () {
                $(this).prop("checked", !1).change()
            }), $("input[type=checkbox]").prop("checked", !1).change(),
            $("input[type=text]").val(""), a = t.find("a").attr("data-href"),
            $("#" + a).find(".hdfQuestionID").val(), $("#" + a).find(".hdfPaperSetID").val(),
            $("#" + a).find(".hdfCurrectAns").val(), $("#" + a).find(".hdfCurrectAns").val(),
            t.find("a").removeClass("que-save-mark"),
            t.find("a").removeClass("que-mark"),
            t.find("a").removeClass("que-save"),
            t.find("a").removeClass("que-not-attempted"),
            t.find("a").addClass("que-not-answered"),
            //NextQuestion(!1),
            CheckQueAttemptStatus()
    });

    $(".btn-submit-all-answers").click(function (e) {
        e.preventDefault(), $(this),
            $(".test-questions").find("li").each(function () {
                var e = $(this),
                    t = !1;
                if (e.children().hasClass("que-save") ? t = !0 : e.children().hasClass("que-save-mark") && (t = !0), t) {
                    var a = e.find("a").attr("data-href");
                    //console.log(a), $("#" + a);
                    $("#" + a).find(".hdfCurrectAns").val();
                    $("#" + a).find("input[name='radios" + a + "']").each(function () {
                        var e = $(this);
                        e.is(":checked") && e.val()
                    });
                }
            }),
            $(".exam-paper").hide(),
            $(".stream_1").hide(),
            $("#divdrplngcng").hide()

            $(".exam-summery").show(),
            CheckQueAttemptStatus()
    });

    $("#btnYesSubmit").on("click", function (e) {
        e.preventDefault(), $(".exam-confirm").show(), $("#divdrplngcng").hide(), $(".exam-summery").hide()
    });
    $("#btnNoSubmit").on("click", function (e) {
        e.preventDefault(), $(".exam-paper").show(), $(".stream_1").show(), $(".exam-summery").hide(), $("#divdrplngcng").show()
    });
    $("#btnYesSubmitConfirm").on("click", function (e) {
        e.preventDefault(), $(".exam-thankyou").show(), $("#divdrplngcng").hide(), $(".exam-confirm").hide()
    });
    $("#btnNoSubmitConfirm").on("click", function (e) {
        e.preventDefault(), $(".exam-paper").show(), $(".stream_1").show(), $(".exam-confirm").hide(), $("#divdrplngcng").show()
    });
    $('.drplanguage').on('change', function (e) {
        e.preventDefault();
        var newlang = 'English';
        
        if ($(this).val() == 'english') {
            newlang = 'English';
        } else if ($(this).val() == 'hindi') {
            newlang = 'Hindi';
        } else if ($(this).val() == 'gujarati') {
            newlang = 'Gujarati';
        }
        var currentLang = $('#hdfCurrentLng').val();
        $('.question-height > .img-responsive').each(function (index, item) {
            var currentImg = $(this);
            var currentImgSrc = currentImg.attr('src');
            currentImg.attr('src', currentImgSrc.replace(currentLang, newlang) + '?' + new Date());
        });
        $('#hdfCurrentLng').val(newlang);
    });
    $('.stream_1').on('click', function (e) {
        e.preventDefault();
        var current_herf = $(this).attr('data-href');
        var a = $(".test-questions").find("li").find("a[data-href=" + current_herf + "]");
        a.trigger('click');
    });
    $('#btnViewResult').on('click', function (e) {
        e.preventDefault();
        CheckResult();
        $('.exam-result').show();
        $(".exam-thankyou").hide();
        $("#divdrplngcng").hide();
    });

    $('#btnRBack').on('click', function (e) {
        e.preventDefault();
        window.location.href = $('#hdfBaseURL').val() + "Quiz/Home/Index"
    });
});