$(document).ready(function() {
/* Portfolio Blocks */
$(function(){var o="";$(".btn").click(function(){o=$(this).attr("data-rel"),$("#cb-portfolio").fadeTo(100,.1),$("#cb-portfolio div").not("."+o).fadeOut().removeClass("scale-anm"),setTimeout(function(){$("."+o).fadeIn().addClass("scale-anm"),$("#cb-portfolio").fadeTo(300,1)},300)})});

/* navigation2 */
$(function(){$("#toggle").click(function(){$(this).toggleClass("active"),$("#overlay").toggleClass("open")})});

/* skills3 */
$(function(){$(".chart2").easyPieChart({scaleColor:"#fff",lineWidth:20,lineCap:"butt",barColor:"#1583c9",trackColor:"#fff",size:160,animate:500})});

/* skills4 */	
$(function(){$(".chart").easyPieChart({scaleColor:"#000",lineWidth:20,lineCap:"butt",barColor:"#1583c9",trackColor:"#fff",size:160,animate:500})});
	
/*skills5 */
$('.counter-count').each(function(){$(this).prop('Counter',0).animate({Counter:$(this).text()},{duration:2000,easing:'swing',step:function(now){$(this).text(Math.ceil(now))}})})	
});
/* media1 */
jQuery(document).ready(function(i){i(".cb-media1 .videoplay-on-hover").hover(function(){i(this).find("video").length>0&&i(this).find("video").get(0).play()},function(){i(this).find("video").length>0&&i(this).find("video").get(0).pause()})});


/* GRID 1 */
var $=jQuery.noConflict();$(window).on("ready load resize",function(){function o(){$(".box-background").css({opacity:1}),$(".box-info").css({opacity:1}),$("#box-area").css("background-size","100%")}function i(){$("body").hasClass("home")&&$(window).width()>1220&&(e++,e>=2&&$(window).scrollTop()>=s&&$(window).scrollTop()<=n?$("html, body").stop().animate({scrollTop:a},500):$(window).scrollTop()==a&&(e=0))}$(".box").mouseenter(function(){if($(window).width()>1220){var o=$(this).find(".back-image").css("background-image").replace(/^url\(['"](.+)['"]\)/,"$1");$("#box-area").css("background-image",'url("'+o+'")'),$("#box-area").stop().animate({backgroundSize:"100%"},0),$(".box-background").css({opacity:0}),$(this).find(".box-background").css({opacity:1}),$(".box-info").not(this).css({opacity:0}),$(this).find(".box-info").css({opacity:1}),$(this).css({opacity:1}),$(".box").not(this).removeClass("visible"),setTimeout(function(){$("#box-area").stop().animate({backgroundSize:"110%"},1e4)},100)}}),$("#box-area").mouseleave(function(){o()}),$(".visible").mouseleave(function(){$("#box-area").stop().css({backgroundSize:"100%"},0)}),$(".box").click(function(o){if($(window).width()>1220){o.preventDefault();var i=$(this).find(".box-link").attr("href");$(".box").not(this).addClass("disable-mouse"),$(".box").animate({borderWidth:0}),$("#box-area").addClass("cover"),$("body, html").animate({scrollTop:a+"px"},300),$(".box").addClass("disable-mouse").animate({opacity:0}),setTimeout(function(){window.location=i},1500)}});var a,s,n,e=(setInterval(i,500),0)});

/* Gallery 2 */
!function(s){"use strict";var i=0,o=0,l=s(".carousel").find("[class=thumb_scroll_y]"),t=s(".carousel").find("[class=thumb_scroll_x]");l&&s(".thumb_scroll_y").on("slid.bs.carousel",function(){var o=-1*s(".thumb_scroll_y .carousel-indicators li:first").position().top+s(".thumb_scroll_y .carousel-indicators li:last").position().top+s(".thumb_scroll_y .carousel-indicators li:last").height(),l=s(".thumb_scroll_y .carousel-indicators li.active").position().top+s(".thumb_scroll_y .carousel-indicators li.active").height()/1+i-s(".thumb_scroll_y .carousel-indicators").height()/2;l<0&&(l=0),l>o-s(".thumb_scroll_y .carousel-indicators").height()&&(l=o-s(".thumb_scroll_y .carousel-indicators").height()),s(".thumb_scroll_y .carousel-indicators").animate({scrollTop:l},800),i=l}),t&&s(".thumb_scroll_x").on("slid.bs.carousel",function(){var i=-1*s(".thumb_scroll_x .carousel-indicators li:first").position().left+s(".thumb_scroll_x .carousel-indicators li:last").position().left+s(".thumb_scroll_x .carousel-indicators li:last").width(),l=s(".thumb_scroll_x .carousel-indicators li.active").position().left+s(".thumb_scroll_x .carousel-indicators li.active").width()/1+o-s(".thumb_scroll_x .carousel-indicators").width()/1;l<0&&(l=0),l>i-s(".thumb_scroll_x .carousel-indicators").width()&&(l=i-s(".thumb_scroll_x .carousel-indicators").width()),s(".thumb_scroll_x .carousel-indicators").animate({scrollLeft:l},800),o=l}),s(".selfPauseVids").on("slide.bs.carousel",function(){s("video").each(function(){this.pause()})}),s(".selfPauseVidm").on("hide.bs.modal",function(){s("video").each(function(){this.pause()})}),s(".onlinePauseVideos").on("slide.bs.carousel",function(i){s(i.target).find("iframe").each(function(i,o){s(o).attr("src",s(o).attr("src"))})}),s(".onlinePauseVideom").on("hide.bs.modal",function(i){s(i.target).find("iframe").each(function(i,o){s(o).attr("src",s(o).attr("src"))})}),s(".carousel").swipe({swipe:function(i,o,l,t,c,r){"left"==o&&s(this).carousel("next"),"right"==o&&s(this).carousel("prev")},allowPageScroll:"vertical",threshold:0})}(jQuery);

