// Generic renderer for every node. Specific styles change colors and borders
function drawNode(node, context, settings, style) {
  const prefix = settings("prefix") || "";
  const size =
    node[prefix + "size"] * style["size"] || node[prefix + "size"] || 1;
  const selectedRatio = 1.5;
  if (style) {
    if (node.selected) {
      window[style.shape](
        context,
        node[prefix + "x"],
        node[prefix + "y"],
        size * selectedRatio,
        style.color || "rgba(0,0,0,0)",
        2,
        "red"
      );
    } else if (node.inHighlighted) {
      window[style.shape](
        context,
        node[prefix + "x"],
        node[prefix + "y"],
        size * selectedRatio,
        style.color || "rgba(0,0,0,0)",
        2,
        "orange"
      );
    } else if (node.outHighlighted) {
      window[style.shape](
        context,
        node[prefix + "x"],
        node[prefix + "y"],
        size * selectedRatio,
        style.color || "rgba(0,0,0,0)",
        2,
        "green"
      );
    } else {
      window[style.shape](
        context,
        node[prefix + "x"],
        node[prefix + "y"],
        size,
        style.color || "rgba(0,0,0,0)",
        style.border,
        style.borderColor || "black"
      );
    }
  } else {
    circle(
      context,
      node[prefix + "x"],
      node[prefix + "y"],
      size,
      style.color || "rgba(0,0,0,0)",
      style.border,
      style.borderColor || "black"
    );
  }
}

function drawEdge(edge, source, target, context, settings, style) {
  let color = style["color"];
  const prefix = settings("prefix") || "";
  const edgeColor = style["color"] || settings("edgeColor");
  const defaultNodeColor = settings("defaultNodeColor");
  const defaultEdgeColor = settings("defaultEdgeColor");
  let size =
    edge[prefix + "size"] * style["size"] * edge.weight ||
    edge[prefix + "size"] * style["size"] ||
    style["size"] ||
    edge[prefix + "size"] ||
    1;
  if (edge.inHighlighted || edge.outHighlighted) {
    size *= 5;
  }
  let tSize = target[prefix + "size"] || target[prefix + "size"];
  if (target.inHighlighted || target.outHighlighted || target.selected) {
    tSize *= 2;
  }
  const sX = source[prefix + "x"];
  const sY = source[prefix + "y"];
  const tX = target[prefix + "x"];
  const tY = target[prefix + "y"];
  const aSize = Math.max(
    size * 2.5 * style["arrow_size"] || size * 2.5,
    settings("minArrowSize")
  );
  const d = Math.sqrt(Math.pow(tX - sX, 2) + Math.pow(tY - sY, 2));
  const aX = sX + ((tX - sX) * (d - aSize - tSize)) / d;
  const aY = sY + ((tY - sY) * (d - aSize - tSize)) / d;
  const vX = ((tX - sX) * aSize) / d;
  const vY = ((tY - sY) * aSize) / d;

  if (!color) {
    switch (edgeColor) {
      case "source":
        color = source.color || defaultNodeColor;
        break;
      case "target":
        color = target.color || defaultNodeColor;
        break;
      default:
        color = defaultEdgeColor;
        break;
    }
  }
  if (edge.inHighlighted) {
    color = "rgba(255,165,0.5)";
  } else if (edge.outHighlighted) {
    color = "rgba(0,128,0,0.5)";
  }

  context.strokeStyle = color;
  context.lineWidth = size;
  context.beginPath();
  context.moveTo(sX, sY);
  context.lineTo(aX, aY);
  context.stroke();

  // Arrow
  if ("arrow_size" in style && style["arrow_size"] === 0) return;

  context.fillStyle = color;
  context.beginPath();
  context.moveTo(aX + vX, aY + vY);
  context.lineTo(aX + vY * 0.6, aY - vX * 0.6);
  context.lineTo(aX - vY * 0.6, aY + vX * 0.6);
  context.lineTo(aX + vX, aY + vY);
  context.closePath();
  context.fill();
}
