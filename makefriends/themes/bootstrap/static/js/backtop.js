$(function () {

    $(window).scroll(function () {  //只要窗口滚动,就触发下面代码

        var scrollt = document.documentElement.scrollTop + document.body.scrollTop; //获取滚动后的高度

        if (scrollt > 200) {  //判断滚动后高度超过200px,就显示

            $("#back_top").fadeIn(400); //淡入

        } else {

            $("#back_top").stop().fadeOut(400); //如果返回或者没有超过,就淡出.必须加上stop()停止之前动画,否则会出现闪动

        }

    });

    $("#back_top").click(function () { //当点击标签的时候,使用animate在200毫秒的时间内,滚到顶部

        $("html,body").animate({scrollTop: "0px"}, 200);

    });

});

$(document).ready(function ($) {
    if ($.support.pjax) {
        $(document).on('click', 'a[data-pjax]', function (event) {
            // var container = $(this).closest('[data-pjax-container]')
            // var containerSelector = '#' + container.id
            // $.pjax.click(event, {container: containerSelector})
            console.log('pjax worked!')
        })
    }
});
