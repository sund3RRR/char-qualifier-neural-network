var canvas = document.getElementById("canv");

function getMousePos(e) {
    var rect = canvas.getBoundingClientRect();
    return {
        x: e.clientX - rect.left + 80,
        y: e.clientY - rect.top + 80
    };
}
function resizeCanvas() {
    canvas.height = canvas.parentElement.clientHeight
    canvas.width = canvas.parentElement.clientWidth
    erase()
}
function distanceBetween(point1, point2) {
    return Math.sqrt(Math.pow(point2.x - point1.x, 2) + Math.pow(point2.y - point1.y, 2));
}
function angleBetween(point1, point2) {
    return Math.atan2( point2.x - point1.x, point2.y - point1.y );
}
canvas.onmousedown = function(e) {
    isDrawing = true;
    lastPoint = getMousePos(e);
};
canvas.onmouseup = function(e) {
    isDrawing = false;
    if (train_mode_status == 0)
        getData()
};
canvas.onmouseout = function(e) {
    isDrawing = false;
};  
function drawLine(e) {
    if (!isDrawing) return;

    var currentPoint = getMousePos(e);
    var dist = distanceBetween(lastPoint, currentPoint);
    var angle = angleBetween(lastPoint, currentPoint);
    
    for (var i = 0; i < dist; i+=2) {
        
        x = lastPoint.x + (Math.sin(angle) * i);
        y = lastPoint.y + (Math.cos(angle) * i);
        
        var radgrad = ctx.createRadialGradient(x-80, y-80, 5, x-80, y-80, 20);
        
        radgrad.addColorStop(0, '#000');
        radgrad.addColorStop(0.3, 'rgba(0,0,0,0.3)');
        radgrad.addColorStop(1, 'rgba(0,0,0,0)');
        
        ctx.fillStyle = radgrad;
        ctx.fillRect(x-100, y-100, 100, 100);
    }      
    lastPoint = currentPoint;
}
function resizeCanvas() {
    // canvas.height = canvas.parentElement.clientHeight
    // canvas.width = canvas.parentElement.clientWidth
    erase()
}

function erase() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "white"
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (!train_mode_status)
        for (var i = 0; i < 44; i++) {
            letter_fields[i].style.width = "0%"
        }
}