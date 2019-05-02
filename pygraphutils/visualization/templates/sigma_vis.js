function defaultNodeRenderer(style) {
  sigma.canvas.nodes.def = function(node, context, settings) {
    // console.log(node);
    if (Object.keys(style).length > 0) {
      for (let layer in style) {
        const layer_style = style[layer];
        const attr_name = layer;
        if (attr_name in node) {
          drawNode(node, context, settings, layer_style[node[attr_name]]);
        }
      }
    } else {
      drawNode(node, context, settings, {
        size: 1,
        color: "blue",
        shape: "circle"
      });
    }
  };
}

function defaultEdgeRenderer(style) {
  // console.log(style);
  const graphDraw = this.graphDraw;
  sigma.canvas.edges.def = function(edge, source, target, context, settings) {
    if (Object.keys(style).length > 0) {
      for (let layer in style) {
        const layer_style = style[layer];
        const attr_name = layer;
        if (attr_name in edge) {
          drawEdge(
            edge,
            source,
            target,
            context,
            settings,
            layer_style[edge[attr_name]]
          );
        }
      }
    } else {
      const s = edge.weight || 1;
      let c = "gray";
      if (edge.weight) {
        c = `rgba(255,0,0,${edge.weight}`;
      }
      drawEdge(edge, source, target, context, settings, {
        size: s,
        color: c
      });
    }
  };
}

function apply_layout(g, layout) {
  for (let node of g.nodes) {
    node.x = layout[node.id][0];
    node.y = layout[node.id][1];
  }
}

function updateGraph(graphView, graph, layout, node_style, edge_style) {
  console.log(graph);
  console.log(layout);
  console.log(node_style);
  console.log(edge_style);

  // if (s) {
  //   s.kill();
  // }

  defaultNodeRenderer(node_style);
  defaultEdgeRenderer(edge_style);

  const addNodeProps = function(node) {
    node.size = node.size || 1; // Required for some reason
    return node;
  };

  const addEdgeProps = function(edge) {
    edge.size = edge.size || 1; // Required for some reason
    return edge;
  };

  graph.nodes.map(addNodeProps);
  graph.edges.map(addEdgeProps);

  apply_layout(graph, layout);

  s = new sigma({
    graph: graph,
    settings: {
      drawEdges: true,
      defaultEdgeType: "dep",
      defaultNodeType: "normal",
      minEdgeSize: 0.1,
      maxEdgeSize: 0.15,
      minArrowSize: 3,
      maxArrowSize: 10,
      minNodeSize: 2,
      maxNodeSize: 3,
      defaultLabelSize: 12,

      labelThreshold: 10000,

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

updateGraph("graph-view", g, layout, {}, {});
