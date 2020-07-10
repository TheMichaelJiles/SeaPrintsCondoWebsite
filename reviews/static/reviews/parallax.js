var isRunning = false;

function parallax() {
    let lastPosition = 0;
    let performParallaxEffect = function() {
        let distanceFromTop = $(document).scrollTop();
        let newBackgroundY = Math.round((distanceFromTop - lastPosition) / 5) + lastPosition;
        lastPosition = newBackgroundY;

        let newBackgroundPositionCss = "50% " + newBackgroundY + "px";
        $("#review-container").css("background-position", newBackgroundPositionCss);
        isRunning = false;
    }
    return new Promise(() => {
        performParallaxEffect();
    });
}

async function asyncParallax() {
    isRunning = true;
    await parallax();
}

$(document).ready(function() {
    asyncParallax();
    $(document).scroll(function() {
        if (!isRunning) {
            asyncParallax();
        }
    })
});