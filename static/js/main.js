$(document).ready(function () {
    !function(e,t,a){function r(){for(var e=0;e<s.length;e++){s[e].alpha<=0?(t.body.removeChild(s[e].el),s.splice(e,1)):(s[e].y--,s[e].scale+=0.004,s[e].alpha-=0.013,s[e].el.style.cssText="left:"+s[e].x+"px;top:"+s[e].y+"px;opacity:"+s[e].alpha+";transform:scale("+s[e].scale+","+s[e].scale+") rotate(45deg);background:"+s[e].color+";z-index:99999")}requestAnimationFrame(r)}function n(){var t="function"==typeof e.onclick&&e.onclick;e.onclick=function(e){t&&t(),o(e)}}function o(e){var a=t.createElement("div");a.className="heart",s.push({el:a,x:e.clientX-5,y:e.clientY-5,scale:1,alpha:1,color:c()}),t.body.appendChild(a)}function i(e){var a=t.createElement("style");a.type="text/css";try{a.appendChild(t.createTextNode(e))}catch(t){a.styleSheet.cssText=e}t.getElementsByTagName("head")[0].appendChild(a)}function c(){return"rgb("+~~(255*Math.random())+","+~~(255*Math.random())+","+~~(255*Math.random())+")"}var s=[];e.requestAnimationFrame=e.requestAnimationFrame||e.webkitRequestAnimationFrame||e.mozRequestAnimationFrame||e.oRequestAnimationFrame||e.msRequestAnimationFrame||function(e){setTimeout(e,1000/60)},i(".heart{width: 10px;height: 10px;position: fixed;background: #f00;transform: rotate(45deg);-webkit-transform: rotate(45deg);-moz-transform: rotate(45deg);}.heart:after,.heart:before{content: '';width: inherit;height: inherit;background: inherit;border-radius: 50%;-webkit-border-radius: 50%;-moz-border-radius: 50%;position: fixed;}.heart:after{top: -5px;}.heart:before{left: -5px;}"),n(),r()}(window,document);
    $('#sex_tip').hide();
    $('#note_tip').hide();
    $('#tags_tip').hide();
    $('#sex').click(function () {
        $('#sex_tip').toggle(800);
    });
    $('#note').click(function () {
        $('#note_tip').toggle(800);
    });
    $('#tag').click(function () {
        $('#tags_tip').toggle(800);
    });

    $('#down_1').click(function () {
        window.scrollTo({
            top:1000,
            behavior:'smooth'
        })
    });
    $('#top').click(function () {
        window.scrollTo({
            top:0,
            behavior:'smooth'
        })
    });
    $('#down_2').click(function () {
        window.scrollTo({
            top:1600,
            behavior:'smooth'
        })
    });
    $('#qq_login').click(function () {
        window.location.replace("/login");
    });
    $('.logout a').click(function () {
        $.ajax({
            type: 'GET',
            contentType: 'application/json; charset = UTF-8',
            dataType: 'json',
            url: '/logout',
            data: {'logout': 'logout'},
            timeout: 1000,
            success: function (data) {
                if (data["response"] === 0) {
                    window.location.replace('/')
                }
                else {
                    alert('注销失败，请刷新页面!')
                }
            },
        })
    });

    $('.fa-star').click(function () {
        var open_id = $('.logon_id').html();
        var weibo_nick_name = $('.name').html();
        console.log(open_id, 'open_iddddd');
        weibo_nick_name = weibo_nick_name.slice(5);
        console.log(weibo_nick_name, 'weibo_nick_name');
        $.ajax({
            type: 'GET',
            contentType: 'application/json; charset = UTF-8',
            dataType: 'json',
            url: '/collection',
            data: {'open_id': open_id, 'weibo_name': weibo_nick_name},
            timeout: 1000,
            success: function (data) {
                if (data["response"] === 0) {
                    alert('收藏成功！')
                }
                else {
                    alert('收藏失败，请刷新页面!')
                }
            },
        })
    });
    $(".item").click(function () {
        var nick_name = $('.logon_id').html();
        console.log(nick_name, '222');
        if (nick_name === 'None' || nick_name === '' ){
            alert('请登录');
            return false;
        }
    })

});



