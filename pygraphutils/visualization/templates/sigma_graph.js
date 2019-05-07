function updateGraph(graphView, graph, layout, node_style, edge_style) {
  console.log(graph);
  console.log(node_style);
  console.log(edge_style);

  // if (s) {
  //   s.kill();
  // }

  defaultNodeRenderer(node_style);
  defaultEdgeRenderer(edge_style);

  const addNodeProperties = function(node) {
    node.size = node.size || 1; // Required for some reason
    return node;
  };

  const addEdgeProperties = function(edge) {
    edge.size = edge.size || 1; // Required for some reason
    return edge;
  };

  graph.nodes.map(addNodeProperties);
  graph.edges.map(addEdgeProperties);

  apply_layout(graph, layout);

  s = new sigma({
    graph: graph,
    settings: {
      drawEdges: true,
      defaultEdgeType: "dep",
      defaultNodeType: "normal",
      minEdgeSize: 0.01,
      maxEdgeSize: 0.25,
      minArrowSize: 3,
      maxArrowSize: 20,
      minNodeSize: 1,
      maxNodeSize: 2,
      defaultLabelSize: 12,

      labelThreshold: 3,

      zoomingRatio: 1.7,
      zoomMin: 0.0001,
      batchEdgesDrawing: true,
      hideEdgesOnMove: false,
      canvasEdgesBatchSize: 500,
      webglEdgesBatchSize: 5000
    },
    renderer: {
      container: graphView,
      type: "canvas"
    }
  });
}
