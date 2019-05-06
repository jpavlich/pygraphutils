function apply_layout(g, layout) {
  for (let node of g.nodes) {
    node.x = layout[node.id][0];
    node.y = layout[node.id][1];
  }
}
