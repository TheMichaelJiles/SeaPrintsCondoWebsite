function parallax() {
    let lastPosition = 0;
    let performParallaxEffect = function() {
        let distanceFromTop = $(document).scrollTop();
        let newBackgroundY = Math.round((distanceFromTop - lastPosition) / 5) + lastPosition;
        lastPosition = newBackgroundY;

        let newBackgroundPositionCss = newBackgroundY + "px";
        $("#review-container").animate({
            backgroundPositionY: newBackgroundPositionCss
        }, 10);
    }
    return new Promise(() => {
        performParallaxEffect();
    });
}

async function asyncParallax() {
    await parallax();
}

$(document).ready(function() {
    asyncParallax();
    $(document).scroll(function() {
        asyncParallax();
    })
});