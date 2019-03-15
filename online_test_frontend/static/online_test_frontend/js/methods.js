var myInterval, AttemptedAns = [], TotalTime = 0;
var studentName, examId, csrf_token;

function NextQuestion(e) {
    var t = $(".test-questions").find("li.active");
    if (CheckNextPrevButtons(), t.is(":last-child")) return !1;
    $(".test-questions").find("li").removeClass("active"), t.next().addClass("active"), OpenCurrentQue(t.next().find("a")), e && (t.find("a").addClass("que-state1"), t.find("a").removeClass("que-state0"));
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
    clearInterval(myInterval),
    $("title").text("Time Out"),
    $(".exam-paper").hide(),
    $(".exam-thankyou").show(),
    $("#divdrplngcng").hide();
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
        e += 1, r.children().hasClass("que-state2") ? a += 1 : r.children().hasClass("que-state4") ? n += 1 : r.children().hasClass("que-state3") ? s += 1 : r.children().hasClass("que-state1") ? t += 1 : i += 1
    }), $(".lblTotalQuestion").text(e), $(".lblNotAttempted").text(t), $(".lblTotalSaved").text(a), $(".lblTotalSaveMarkForReview").text(n), $(".lblTotalMarkForReview").text(s), $(".lblNotVisited").text(i)
}

function sendResponseData(questionNumber, selectedOption, state) {
    // state 1 = question not answered
    // state 2 = question answered
    // state 3 = marked for review
    // state 4 = answered and marked for review
    var answerResponse={
        "questionNumber" : parseInt(questionNumber),
        "choice": parseInt(selectedOption),
        "state": parseInt(state)
    };
    var answerResponseJ= JSON.stringify(answerResponse);
    $.ajax({
        type:'POST',
        url: URL,
        data:{
            student:studentName,
            exam_id: examId,
            progress: answerResponseJ,
            csrfmiddlewaretoken: csrf_token
        },
        success:function(){
            console.log(URL)
            console.log('saved')
        }
    });
}

$(document).ready(function () {
    studentName = $('#studentName').val();
    examId = $('#examId').val();
    csrf_token = $('#csrfToken').val();
    $("#page01").show(); $(".exam-paper").show();
    CoundownTimer(parseInt($("#hdfTestDuration").val()));
    CheckNextPrevButtons();
    CheckQueAttemptStatus();
    $("#btnPrevQue").click(function () {
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href"),
            questionNumber = parseInt(a.match(/(\d+)/g)[0]), //question number
            stateText = $(".test-questions").find("li.active").find("a").attr("class").split(' ')[1];
            if (stateText) {
                var state = stateText[stateText.length - 1];
                if (state == 1) {
                    sendResponseData(questionNumber, 0, 1);
                }
            } else {
                sendResponseData(questionNumber, 0, 1);
            }
        PrevQuestion(!0)
    });
    $("#btnNextQue").click(function () {
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href"),
            questionNumber = parseInt(a.match(/(\d+)/g)[0]), //question number
            stateText = $(".test-questions").find("li.active").find("a").attr("class").split(' ')[1];
            if (stateText) {
                var state = stateText[stateText.length - 1];
                if (state == 1) {
                    sendResponseData(questionNumber, 0, 1);
                }
            } else {
                sendResponseData(questionNumber, 0, 1);
            }
        NextQuestion(!0)
    });
    $(".test-ques").click(function () {
        var e = $(".test-questions").find("li.active").find("a"),
            a = e.attr("data-href"),
            questionNumber = parseInt(a.match(/(\d+)/g)[0]), //question number
            stateText = $(".test-questions").find("li.active").find("a").attr("class").split(' ')[1];
        if (stateText) {
            var state = stateText[stateText.length - 1];
            if (state == 1) {
                sendResponseData(questionNumber, 0, 1);
            }
        } else {
            sendResponseData(questionNumber, 0, 1);
        }
        $(".test-questions").find("li").removeClass("active"),
            $(this).parent().addClass("active"),
            $(this).hasClass("que-state2") || $(this).hasClass("que-state4") || $(this).hasClass("que-state3") || ($(this).addClass("que-state1"), $(this).removeClass("que-state0")), e.hasClass("que-state2") || e.hasClass("que-state4") || e.hasClass("que-state3") || (e.addClass("que-state1"), e.removeClass("que-state0")), OpenCurrentQue($(this))
        });

    $(".btn-save-answer").click(function (e) {
        e.preventDefault();
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href"),
            questionNumber = parseInt(a.match(/(\d+)/g)[0]), //question number
            selectedOption = $("input[name='radios" + a + "']:checked").val() ? $("input[name='radios" + a + "']:checked").val() : 0, //selected option
            n = ($("#" + a).find(".hdfQuestionID").val(), $("#" + a).find(".hdfPaperSetID").val(), $("#" + a).find(".hdfCurrectAns").val(), !1);
        if ($("input[name='radios" + a + "']").each(function () {
            $(this).is(":checked") && (n = !0)
        }), 0 == n) { alert("Please choose an option"); return !1 };
        $("input[name='radios" + a + "']:checked").val(), t.find("a").removeClass("que-state4"), t.find("a").removeClass("que-state3"), t.find("a").addClass("que-state2"), t.find("a").removeClass("que-state1"), t.find("a").removeClass("que-state0"), NextQuestion(!1), CheckQueAttemptStatus();
        sendResponseData(questionNumber, selectedOption, 2);
    });

    $(".btn-save-mark-answer").click(function (e) {
        e.preventDefault();
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href"),
            questionNumber = parseInt(a.match(/(\d+)/g)[0]) //question number
            selectedOption = $("input[name='radios" + a + "']:checked").val() ? $("input[name='radios" + a + "']:checked").val() : 0, //selected option
            n = ($("#" + a).find(".hdfQuestionID").val(),
                $("#" + a).find(".hdfPaperSetID").val(),
                $("#" + a).find(".hdfCurrectAns").val(),
                $("#" + a).find(".hdfCurrectAns").val(), !1);
        if ($("input[name='radios" + a + "']").each(function () {
            $(this).is(":checked") && (n = !0)
        }), 0 == n) { alert("Please choose an option"); return !1 };;
        $("input[name='radios" + a + "']:checked").val(), t.find("a").removeClass("que-state2"), t.find("a").removeClass("que-state3"), t.find("a").addClass("que-state4"), t.find("a").removeClass("que-state1"), t.find("a").removeClass("que-state0"), NextQuestion(!1), CheckQueAttemptStatus()
        sendResponseData(questionNumber, selectedOption, 4);
    });

    $(".btn-mark-answer").click(function (e) {
        e.preventDefault();
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href"),
            questionNumber = parseInt(a.match(/(\d+)/g)[0]); //question number
        $("#" + a).find(".hdfQuestionID").val(), $("#" + a).find(".hdfPaperSetID").val(), $("#" + a).find(".hdfCurrectAns").val(), $("#" + a).find(".hdfCurrectAns").val(), t.find("a").removeClass("que-state4"), t.find("a").removeClass("que-state2"), t.find("a").addClass("que-state3"), t.find("a").removeClass("que-state1"), t.find("a").removeClass("que-state0"), NextQuestion(!1), CheckQueAttemptStatus()
        sendResponseData(questionNumber, 0, 3);
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
            t.find("a").removeClass("que-state4"),
            t.find("a").removeClass("que-state3"),
            t.find("a").removeClass("que-state2"),
            t.find("a").removeClass("que-state0"),
            t.find("a").addClass("que-state1"),
            //NextQuestion(!1),
            CheckQueAttemptStatus()
    });

    $(".btn-submit-all-answers").click(function (e) {
        e.preventDefault(),
        $(".exam-paper").hide(),
        $(".stream_1").hide(),
        $("#divdrplngcng").hide(),
        $(".exam-summery").show(),
        CheckQueAttemptStatus();
    });

    $("#btnYesSubmit").on("click", function (e) {
        e.preventDefault();
        $(".exam-summery").hide();
        $(".exam-thankyou").show();
        $("#divdrplngcng").hide();
    });
    $("#btnNoSubmit").on("click", function (e) {
        e.preventDefault(), $(".exam-paper").show(), $(".stream_1").show(), $(".exam-summery").hide(), $("#divdrplngcng").show()
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

    $('.full_screen').on('click', function (e) {
        e.preventDefault();
        $('.full_screen').hide();
        $('.collapse_screen').show();
        $('#pallette').hide();
        $('#quest').removeClass('col-md-8');
        $('#quest').addClass('col-md-12');
    });
    $('.collapse_screen').on('click', function (e) {
        e.preventDefault();
        $('.collapse_screen').hide();
        $('.full_screen').show();
        $('#pallette').show();
        $('#quest').removeClass('col-md-12');
        $('#quest').addClass('col-md-8');
    });
});