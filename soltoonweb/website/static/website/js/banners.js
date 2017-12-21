(function () {
    bannersTimeline = new TimelineMax({
        repeat: -1
    });
    var banner = document.querySelector('.competition-banner');
    bannersTimeline.add(competitionBanner(banner));
})();

function competitionBanner(bannerElement) {
    player1pic = bannerElement.querySelector('.player1-picture');
    player2pic = bannerElement.querySelector('.player2-picture');
    player1title = bannerElement.querySelector('.player1-title');
    player2title = bannerElement.querySelector('.player2-title');
    bannerActions = bannerElement.querySelector('.banner-actions');
    pompingDots = bannerElement.querySelector('.pomping-dots').querySelectorAll('span');

    baseTimeline = new TimelineMax({});

    baseTimeline.add(TweenLite.fromTo(player1pic, 3, {ease: Power2.easeOut, x: '130%', y: '10%'}, {
        y: '0%',
        x: '10%'
    }));

    baseTimeline.add(TweenLite.fromTo(player2pic, 3, {ease: Power2.easeOut, x: '-130%', y: '10%'}, {
        y: '0%',
        x: '-10%'
    }), "-=3");

    baseTimeline.add(TweenLite.from(bannerActions, 1, {opacity: 0}), "-=1");
    baseTimeline.add(TweenLite.to(player1pic, 15, {x: '-5%'}));
    baseTimeline.add(TweenLite.to(player2pic, 15, {x: '5%'}), "-=15");
    baseTimeline.add(TweenLite.from(player1title, 1, {opacity: 0}), "-=16.5");
    baseTimeline.add(TweenLite.to(player1title, 14.5, {ease: Power2.easeOut, x: '-10%'}), "-=16.5");
    baseTimeline.add(TweenLite.from(player2title, 1, {opacity: 0}), "-=15.5");
    baseTimeline.add(TweenLite.to(player2title, 14.5, {ease: Power2.easeOut, x: '10%'}), "-=16.5");


    pompingDotsTimeline = new TimelineMax({repeat: 4, yoyo: true});
    for (i = pompingDots.length - 1; i >= 0; i--) {
        var e = pompingDots[i];
        pompingDotsTimeline.add(TweenLite.from(e, 0.5, {opacity: 0}));
    }
    for (i = pompingDots.length - 1; i >= 0; i--) {
        var e = pompingDots[i];
        pompingDotsTimeline.add(TweenLite.to(e, 0.5, {opacity: 0}));
    }

    baseTimeline.add(pompingDotsTimeline, "-=15");

    baseTimeline.add(TweenLite.to(player1pic, 1.5, {ease: Power2.easeIn, x: '10%', y: '30%', opacity: 0}));
    baseTimeline.add(TweenLite.to(player2pic, 1.5, {ease: Power2.easeIn, x: '-10%', y: '30%', opacity: 0}), '-=1.5');
    baseTimeline.add(TweenLite.to(bannerElement, 1, {opacity: 0}), '-=1');


    return baseTimeline;
}

// competitionBannerTimeline = new TimelineMax({});
// competitionBannerTimeline.add(TweenLite.fromTo(player1pic, 3, {ease: Power2.easeOut, x: '130%', y: '10%'}, {
//     y: '0%',
//     x: '10%'
// }));
// competitionBannerTimeline.add(TweenLite.fromTo(player2pic, 3, {ease: Power2.easeOut, x: '-130%', y: '10%'}, {
//     y: '0%',
//     x: '-10%'
// }), "-=3");
// competitionBannerTimeline.add(TweenLite.from(bannerActions, 1, {opacity: 0}), "-=1");
// competitionBannerTimeline.add(TweenLite.to(player1pic, 25, {x: '-5%'}));
// competitionBannerTimeline.add(TweenLite.to(player2pic, 25, {x: '5%'}), "-=25");
// competitionBannerTimeline.add(TweenLite.from(player1title, 1, {opacity: 0}), "-=26.5");
// competitionBannerTimeline.add(TweenLite.to(player1title, 24.5, {ease: Power4.easeOut, x: '-10%'}), "-=26.5");
// competitionBannerTimeline.add(TweenLite.from(player2title, 1, {opacity: 0}), "-=25.5");
// competitionBannerTimeline.add(TweenLite.to(player2title, 24.5, {ease: Power4.easeOut, x: '10%'}), "-=26.5");
//
// var competitionDots = new TimelineMax({yoyo: true, repeat: -1});
//
// for (i = pompingDots.length - 1; i >= 0; i--) {
//     var e = pompingDots[i];
//     competitionDots.add(TweenLite.from(e, 0.5, {opacity: 0}));
// }
// for (i = pompingDots.length - 1; i >= 0; i--) {
//     var e = pompingDots[i];
//     competitionDots.add(TweenLite.to(e, 0.5, {opacity: 0}));
// }
//
// competitionBannerTimeline.add(competitionDots, "-=25");
// competitionBannerTimeline.add(TweenLite.to(player1pic, 0.5, {x: '10%', y: '30%', opacity: 0}));
// competitionBannerTimeline.add(TweenLite.to(player2pic, 0.5, {x: '-10%', y: '30%', opacity: 0}), '-=0.5');
//
// competitionBannerTimeline.add(TweenLite.to(b, 0.5, {opacity: 0}), '-=0.5');
//
// t.append(competitionBannerTimeline);
// // t.pause()