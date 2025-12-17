import React, { useEffect, useRef } from 'react';
import { Network } from 'vis-network/standalone';
import './GraphVisualization.css';

function GraphVisualization({ graphData }) {
  const networkRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    if (!graphData || !containerRef.current) return;

    // Deduplicate nodes and ensure unique IDs
    const nodeMap = new Map();
    const seenIds = new Set();
    
    graphData.nodes.forEach(node => {
      // Create unique ID if not already prefixed
      let uniqueId = node.id;
      if (!node.id.startsWith('company_') && 
          !node.id.startsWith('industry_') && 
          !node.id.startsWith('tag_') && 
          !node.id.startsWith('tech_')) {
        // Add prefix based on group
        const prefix = node.group === 'Company' ? 'company_' :
                      node.group === 'Industry' ? 'industry_' :
                      node.group === 'Tag' ? 'tag_' :
                      node.group === 'Technology' ? 'tech_' : 'node_';
        uniqueId = `${prefix}${node.id}`;
      }
      
      // Ensure truly unique ID
      let finalId = uniqueId;
      let counter = 1;
      while (seenIds.has(finalId)) {
        finalId = `${uniqueId}_${counter}`;
        counter++;
      }
      
      if (!nodeMap.has(finalId)) {
        const colorConfig = getNodeColor(node.group);
        nodeMap.set(finalId, {
          id: finalId,
          label: node.label,
          color: colorConfig,
          shape: node.group === 'Company' ? 'box' : 'dot',
          size: node.group === 'Company' ? 30 : node.group === 'Industry' ? 20 : 15,
          font: {
            size: node.group === 'Company' ? 16 : 14,
            face: 'Arial',
            bold: node.group === 'Company' || node.group === 'Industry',
            color: '#333'
          },
          borderWidth: node.group === 'Company' ? 3 : 2,
          shadow: true
        });
        seenIds.add(finalId);
      }
    });

    const nodes = Array.from(nodeMap.values());

    // Create mapping from old IDs to new IDs for edges
    const idMapping = new Map();
    graphData.nodes.forEach((node, idx) => {
      const newNode = nodes.find(n => n.label === node.label && 
        (node.id.startsWith('company_') ? n.id.startsWith('company_') :
         node.id.startsWith('industry_') ? n.id.startsWith('industry_') :
         node.id.startsWith('tag_') ? n.id.startsWith('tag_') :
         node.id.startsWith('tech_') ? n.id.startsWith('tech_') : true));
      if (newNode) {
        idMapping.set(node.id, newNode.id);
      }
    });

    // Process edges with mapped IDs
    const edgeMap = new Map();
    graphData.edges.forEach(edge => {
      const sourceId = idMapping.get(edge.source) || edge.source;
      const targetId = idMapping.get(edge.target) || edge.target;
      
      // Find actual node IDs if mapping didn't work
      const sourceNode = nodes.find(n => n.id === sourceId || n.id.includes(edge.source.split('_').pop()));
      const targetNode = nodes.find(n => n.id === targetId || n.id.includes(edge.target.split('_').pop()));
      
      if (sourceNode && targetNode) {
        const edgeKey = `${sourceNode.id}_${targetNode.id}`;
        if (!edgeMap.has(edgeKey)) {
          edgeMap.set(edgeKey, {
            from: sourceNode.id,
            to: targetNode.id,
            label: edge.label,
            arrows: 'to',
            width: 2,
            color: { 
              color: getEdgeColor(edge.label),
              highlight: '#667eea',
              hover: '#667eea'
            },
            font: { 
              size: 11, 
              align: 'middle',
              color: '#666'
            },
            smooth: {
              type: 'continuous',
              roundness: 0.5
            }
          });
        }
      }
    });

    const edges = Array.from(edgeMap.values());

    const data = { nodes, edges };

    const options = {
      nodes: {
        borderWidth: 2,
        shadow: {
          enabled: true,
          color: 'rgba(0,0,0,0.2)',
          size: 5,
          x: 2,
          y: 2
        },
        font: {
          size: 14,
          face: 'Arial',
          color: '#333'
        },
        scaling: {
          min: 10,
          max: 30
        }
      },
      edges: {
        width: 2,
        shadow: {
          enabled: true,
          color: 'rgba(0,0,0,0.1)',
          size: 3
        },
        smooth: {
          type: 'continuous',
          roundness: 0.5
        },
        arrows: {
          to: {
            enabled: true,
            scaleFactor: 1.2
          }
        }
      },
      physics: {
        enabled: true,
        stabilization: {
          enabled: true,
          iterations: 250,
          fit: true
        },
        barnesHut: {
          gravitationalConstant: -3000,
          centralGravity: 0.2,
          springLength: 250,
          springConstant: 0.05,
          damping: 0.1,
          avoidOverlap: 0.8
        }
      },
      interaction: {
        hover: true,
        tooltipDelay: 150,
        zoomView: true,
        dragView: true,
        selectConnectedEdges: true
      },
      layout: {
        improvedLayout: true,
        hierarchical: {
          enabled: false
        }
      }
    };

    const network = new Network(containerRef.current, data, options);

    networkRef.current = network;

    // Handle node click
    network.on('click', (params) => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        const node = nodes.find(n => n.id === nodeId);
        if (node) {
          console.log('Clicked node:', node);
          // Highlight connected nodes
          network.selectNodes([nodeId]);
          network.focus(nodeId, {
            scale: 1.2,
            animation: {
              duration: 500,
              easingFunction: 'easeInOutQuad'
            }
          });
        }
      } else if (params.edges.length > 0) {
        // Highlight edge
        network.selectEdges([params.edges[0]]);
      } else {
        // Deselect all
        network.unselectAll();
      }
    });

    // Handle hover
    network.on('hoverNode', (params) => {
      containerRef.current.style.cursor = 'pointer';
    });

    network.on('blurNode', () => {
      containerRef.current.style.cursor = 'default';
    });

    return () => {
      if (networkRef.current) {
        networkRef.current.destroy();
      }
    };
  }, [graphData]);

  const getNodeColor = (group) => {
    const colors = {
      'Company': {
        background: '#667eea',
        border: '#5568d3',
        highlight: { background: '#5568d3', border: '#4457c2' }
      },
      'Industry': {
        background: '#764ba2',
        border: '#653a91',
        highlight: { background: '#653a91', border: '#542b80' }
      },
      'Tag': {
        background: '#f093fb',
        border: '#e082ea',
        highlight: { background: '#e082ea', border: '#d071d9' }
      },
      'Technology': {
        background: '#4facfe',
        border: '#3e9bed',
        highlight: { background: '#3e9bed', border: '#2e8adc' }
      }
    };
    return colors[group] || { background: '#999', border: '#888' };
  };

  const getEdgeColor = (label) => {
    if (label === 'OPERATES_IN') return '#764ba2';
    if (label === 'TAGGED_AS') return '#f093fb';
    if (label === 'USES_TECH') return '#4facfe';
    return '#999';
  };

  if (!graphData || !graphData.nodes || graphData.nodes.length === 0) {
    return null;
  }

  return (
    <div className="graph-container">
      <div className="graph-header">
        <h3>Knowledge Graph Visualization</h3>
        <p>Interactive network showing company relationships</p>
      </div>
      <div ref={containerRef} className="graph-canvas"></div>
      <div className="graph-legend">
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#667eea' }}></span>
          <span>Company</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#764ba2' }}></span>
          <span>Industry</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#f093fb' }}></span>
          <span>Tag</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#4facfe' }}></span>
          <span>Technology</span>
        </div>
      </div>
    </div>
  );
}

export default GraphVisualization;

