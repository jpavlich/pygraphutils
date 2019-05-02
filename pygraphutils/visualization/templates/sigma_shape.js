function circle(context, x, y, size, fillColor, borderWidth, borderColor) {
  context.fillStyle = fillColor;
  context.beginPath();
  context.arc(x, y, size, 0, Math.PI * 2, true);
  context.closePath();
  context.fill();
  if (borderWidth) {
    context.lineWidth = borderWidth;
    context.strokeStyle = borderColor;
    context.stroke();
  }
}

function triangle(context, x, y, size, fillColor, borderWidth, borderColor) {
  const r = size * 1.5;
  context.fillStyle = fillColor;
  context.beginPath();
  context.moveTo(x, y - r);
  context.lineTo(x + r * Math.cos(0.523599), y + r * Math.sin(0.523599));
  context.lineTo(x - r * Math.cos(0.523599), y + r * Math.sin(0.523599));
  context.closePath();
  context.fill();
  if (borderWidth) {
    context.lineWidth = borderWidth;
    context.strokeStyle = borderColor;
    context.stroke();
  }
}

function square(context, x, y, size, fillColor, borderWidth, borderColor) {
  context.fillStyle = fillColor;
  context.fillRect(x - size, y - size, size * 2, size * 2);
  if (borderWidth) {
    context.lineWidth = borderWidth;
    context.strokeStyle = borderColor;
    context.strokeRect(x - size, y - size, size * 2, size * 2);
  }
}

function drawText(ctx, text, x, y, color = "black") {
  ctx.fillStyle = color;
  ctx.fillText(text, x, y);
}
function drawShape(ctx, attr, value, y, style) {
  const size = 5;
  window[style[attr][value].shape](
    ctx,
    15 + size,
    y - size,
    size,
    style[attr][value].color || "rgba(255,255,255,0)",
    style[attr][value].border * 2,
    style[attr][value].borderColor || "black"
  );
}
