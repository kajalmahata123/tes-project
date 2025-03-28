# React Design Patterns for Agent and Tool Graphs

## 1. Introduction

This document outlines the React design patterns and architecture for implementing agent graphs and tool graphs in the Content-Craft Visa API Agent application. The frontend visualizes complex agent workflows and tool interactions, providing an intuitive interface for understanding how the system processes queries and generates responses.

## 2. Core React Design Patterns

### 2.1 Component Architecture

The application follows a structured component hierarchy using functional components and hooks:

```
┌─────────────────────────────────────────────────┐
│                                                 │
│                  App Container                  │
│                                                 │
└───────────────────────┬─────────────────────────┘
                        │
        ┌───────────────┼───────────────────┐
        │               │                   │
        ▼               ▼                   ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│               │ │               │ │               │
│  Agent Graph  │ │ Conversation  │ │  Tool Graph   │
│   Component   │ │   Component   │ │   Component   │
│               │ │               │ │               │
└───────┬───────┘ └───────────────┘ └───────┬───────┘
        │                                   │
┌───────┴───────┐                   ┌───────┴───────┐
│               │                   │               │
│ Graph Nodes   │                   │ Tool Nodes    │
│ Component     │                   │ Component     │
│               │                   │               │
└───────┬───────┘                   └───────┬───────┘
        │                                   │
┌───────┴───────┐                   ┌───────┴───────┐
│               │                   │               │
│ Node Details  │                   │ Tool Details  │
│ Component     │                   │ Component     │
│               │                   │               │
└───────────────┘                   └───────────────┘
```

### 2.2 State Management

The application uses a combination of state management approaches:

1. **Local Component State**: For UI-specific state (useState hook)
2. **Context API**: For shared application state that spans multiple components
3. **Redux**: For complex state management and agent/tool graph state

Example Context structure:
```jsx
// AgentGraphContext.js
import React, { createContext, useReducer, useContext } from 'react';
import agentGraphReducer from './agentGraphReducer';

const AgentGraphContext = createContext();

export const AgentGraphProvider = ({ children }) => {
  const initialState = {
    nodes: [],
    edges: [],
    selectedNode: null,
    isLoading: false,
    error: null
  };

  const [state, dispatch] = useReducer(agentGraphReducer, initialState);

  return (
    <AgentGraphContext.Provider value={{ state, dispatch }}>
      {children}
    </AgentGraphContext.Provider>
  );
};

export const useAgentGraph = () => useContext(AgentGraphContext);
```

### 2.3 Component Composition

The application leverages component composition for reusability and separation of concerns:

```jsx
// GraphContainer.jsx
const GraphContainer = ({ title, children }) => (
  <div className="graph-container">
    <h2>{title}</h2>
    <div className="graph-content">
      {children}
    </div>
  </div>
);

// Usage
<GraphContainer title="Agent Workflow">
  <AgentGraph data={agentGraphData} />
  <GraphControls onZoomIn={handleZoomIn} onZoomOut={handleZoomOut} />
</GraphContainer>
```

## 3. Agent Graph Implementation

### 3.1 Graph Visualization

The agent graph uses react-flow or similar libraries to visualize the relationships between different agent components:

```jsx
// AgentGraph.jsx
import React, { useCallback } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  MiniMap,
  addEdge,
  useNodesState,
  useEdgesState 
} from 'reactflow';
import 'reactflow/dist/style.css';

import AgentNode from './AgentNode';
import ProcessNode from './ProcessNode';
import LLMNode from './LLMNode';

const nodeTypes = {
  agent: AgentNode,
  process: ProcessNode,
  llm: LLMNode
};

const AgentGraph = ({ initialNodes, initialEdges }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  return (
    <div style={{ height: 600, width: '100%' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
      >
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
};

export default AgentGraph;
```

### 3.2 Custom Node Components

Each agent type has a specialized node component:

```jsx
// AgentNode.jsx
import React, { memo } from 'react';
import { Handle, Position } from 'reactflow';

const AgentNode = ({ data }) => {
  return (
    <div className={`agent-node ${data.agentType}`}>
      <Handle type="target" position={Position.Top} />
      <div className="agent-title">{data.label}</div>
      <div className="agent-type">{data.agentType}</div>
      <div className="agent-metrics">
        <span>Success Rate: {data.metrics.successRate}%</span>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default memo(AgentNode);
```

### 3.3 Agent Graph Data Structure

The agent graph is represented as a directed graph with nodes and edges:

```javascript
// Example agent graph data structure
const agentGraphData = {
  nodes: [
    {
      id: '1',
      type: 'agent',
      position: { x: 250, y: 50 },
      data: { 
        label: 'Visa API Agent', 
        agentType: 'visa_api_agent',
        metrics: { successRate: 95, queryCount: 1250 }
      }
    },
    {
      id: '2',
      type: 'process',
      position: { x: 100, y: 150 },
      data: { 
        label: 'Query Understanding', 
        processType: 'analysis',
        metrics: { avgTime: '0.3s' }
      }
    },
    {
      id: '3',
      type: 'llm',
      position: { x: 400, y: 150 },
      data: { 
        label: 'Claude 3.5 Sonnet', 
        model: 'claude-3-5-sonnet',
        metrics: { tokenCount: 24500, avgResponseTime: '2.1s' }
      }
    }
  ],
  edges: [
    { id: 'e1-2', source: '1', target: '2' },
    { id: 'e2-3', source: '2', target: '3' },
    { id: 'e3-1', source: '3', target: '1' }
  ]
};
```

### 3.4 Interactive Features

The agent graph offers interactive features for exploration and analysis:

- Zoom in/out and panning
- Node selection for detailed information
- Edge highlighting to trace information flow
- Filtering by agent type
- Real-time updates of agent activities

```jsx
// AgentGraphControls.jsx
const AgentGraphControls = ({ onFilterChange, filters, onLayoutChange }) => {
  return (
    <div className="agent-graph-controls">
      <div className="filter-controls">
        <h4>Filter Agents</h4>
        {Object.keys(filters).map(filter => (
          <label key={filter} className="filter-label">
            <input
              type="checkbox"
              checked={filters[filter]}
              onChange={() => onFilterChange(filter)}
            />
            {filter}
          </label>
        ))}
      </div>
      
      <div className="layout-controls">
        <h4>Layout</h4>
        <button onClick={() => onLayoutChange('horizontal')}>Horizontal</button>
        <button onClick={() => onLayoutChange('vertical')}>Vertical</button>
        <button onClick={() => onLayoutChange('radial')}>Radial</button>
      </div>
    </div>
  );
};
```

## 4. Tool Graph Implementation

### 4.1 Tool Visualization

The tool graph represents the ecosystem of tools available to agents:

```jsx
// ToolGraph.jsx
import React from 'react';
import { ForceGraph2D } from 'react-force-graph';

const ToolGraph = ({ data, onNodeClick }) => {
  return (
    <div className="tool-graph-container">
      <ForceGraph2D
        graphData={data}
        nodeLabel="name"
        nodeColor={node => node.category === 'knowledge' ? '#ff6b6b' : 
                           node.category === 'code' ? '#4ecdc4' : '#ffd166'}
        nodeRelSize={6}
        linkWidth={link => link.value}
        linkDirectionalParticles={2}
        linkDirectionalParticleSpeed={d => d.value * 0.01}
        onNodeClick={onNodeClick}
        width={800}
        height={600}
      />
    </div>
  );
};

export default ToolGraph;
```

### 4.2 Tool Categories and Relationships

Tools are organized into categories with relationships between them:

```javascript
// Example tool graph data structure
const toolGraphData = {
  nodes: [
    // Knowledge Tools
    { id: 'vector-search', name: 'Vector Search', category: 'knowledge', value: 25 },
    { id: 'semantic-search', name: 'Semantic Search', category: 'knowledge', value: 22 },
    { id: 'context-ranking', name: 'Context Ranking', category: 'knowledge', value: 18 },
    
    // Code Tools
    { id: 'code-generator', name: 'Code Generator', category: 'code', value: 30 },
    { id: 'syntax-checker', name: 'Syntax Checker', category: 'code', value: 15 },
    { id: 'test-generator', name: 'Test Generator', category: 'code', value: 12 },
    
    // Document Tools
    { id: 'pdf-parser', name: 'PDF Parser', category: 'document', value: 20 },
    { id: 'markdown-parser', name: 'Markdown Parser', category: 'document', value: 18 },
    { id: 'diagram-creator', name: 'Diagram Creator', category: 'document', value: 22 }
  ],
  links: [
    // Knowledge tool relationships
    { source: 'vector-search', target: 'semantic-search', value: 5 },
    { source: 'semantic-search', target: 'context-ranking', value: 8 },
    
    // Code tool relationships
    { source: 'code-generator', target: 'syntax-checker', value: 10 },
    { source: 'syntax-checker', target: 'test-generator', value: 7 },
    
    // Cross-category relationships
    { source: 'vector-search', target: 'code-generator', value: 3 },
    { source: 'context-ranking', target: 'diagram-creator', value: 6 },
    { source: 'markdown-parser', target: 'code-generator', value: 4 }
  ]
};
```

### 4.3 Tool Details Component

When a tool node is selected, detailed information is displayed:

```jsx
// ToolDetails.jsx
import React from 'react';

const ToolDetails = ({ tool }) => {
  if (!tool) return <div className="tool-details empty">Select a tool to view details</div>;

  return (
    <div className="tool-details">
      <h3>{tool.name}</h3>
      <div className="tool-category">Category: {tool.category}</div>
      
      <div className="tool-description">
        <h4>Description</h4>
        <p>{tool.description || 'No description available'}</p>
      </div>
      
      <div className="tool-usage">
        <h4>Usage Statistics</h4>
        <ul>
          <li>Usage Count: {tool.stats?.usageCount || 'N/A'}</li>
          <li>Success Rate: {tool.stats?.successRate || 'N/A'}%</li>
          <li>Avg. Processing Time: {tool.stats?.avgProcessingTime || 'N/A'}</li>
        </ul>
      </div>
      
      <div className="tool-examples">
        <h4>Example Usage</h4>
        <pre>{tool.example || 'No examples available'}</pre>
      </div>
    </div>
  );
};

export default ToolDetails;
```

## 5. Integration with Backend

### 5.1 API Integration

The React frontend integrates with the backend API to fetch graph data:

```jsx
// useAgentGraphData.js
import { useEffect, useState } from 'react';
import axios from 'axios';

const useAgentGraphData = () => {
  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAgentGraph = async () => {
      try {
        setLoading(true);
        // Fetch agent graph data from API
        const response = await axios.get('/api/v1/agents/graph', {
          headers: {
            'X-API-Key': process.env.REACT_APP_API_KEY
          }
        });
        
        setGraphData(response.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchAgentGraph();
  }, []);

  return { graphData, loading, error };
};

export default useAgentGraphData;
```

### 5.2 Real-time Updates

WebSockets or Server-Sent Events for real-time graph updates:

```jsx
// useRealTimeGraphUpdates.js
import { useEffect } from 'react';
import { useAgentGraph } from '../contexts/AgentGraphContext';

const useRealTimeGraphUpdates = () => {
  const { dispatch } = useAgentGraph();
  
  useEffect(() => {
    // Create WebSocket connection
    const socket = new WebSocket(process.env.REACT_APP_WS_URL);
    
    socket.onopen = () => {
      console.log('WebSocket connection established');
    };
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      // Handle different update types
      switch (data.type) {
        case 'NODE_UPDATE':
          dispatch({ type: 'UPDATE_NODE', payload: data.node });
          break;
        case 'EDGE_UPDATE':
          dispatch({ type: 'UPDATE_EDGE', payload: data.edge });
          break;
        case 'NEW_TRANSACTION':
          dispatch({ type: 'ADD_TRANSACTION', payload: data.transaction });
          break;
        default:
          console.log('Unknown update type:', data.type);
      }
    };
    
    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };
    
    // Clean up WebSocket on component unmount
    return () => {
      socket.close();
    };
  }, [dispatch]);
};

export default useRealTimeGraphUpdates;
```

## 6. Performance Optimization

### 6.1 Memoization

Using React.memo and useMemo to optimize rendering:

```jsx
// Optimized node component with memoization
import React, { memo, useMemo } from 'react';

const ToolNode = ({ data, selected }) => {
  // Memoize expensive calculations
  const nodeStyle = useMemo(() => ({
    background: selected ? '#f8f9fa' : '#ffffff',
    border: `2px solid ${data.category === 'knowledge' ? '#ff6b6b' : 
                         data.category === 'code' ? '#4ecdc4' : '#ffd166'}`,
    padding: '10px',
    borderRadius: '4px'
  }), [data.category, selected]);

  return (
    <div style={nodeStyle} className="tool-node">
      <div className="node-title">{data.name}</div>
      <div className="node-category">{data.category}</div>
    </div>
  );
};

export default memo(ToolNode);
```

### 6.2 Virtualization

For large graphs, virtualization improves performance:

```jsx
// Using react-window for virtualized lists
import React from 'react';
import { FixedSizeList as List } from 'react-window';

const ToolList = ({ tools, onToolSelect }) => {
  const Row = ({ index, style }) => {
    const tool = tools[index];
    return (
      <div 
        style={style} 
        className="tool-list-item"
        onClick={() => onToolSelect(tool)}
      >
        <div className="tool-name">{tool.name}</div>
        <div className="tool-category">{tool.category}</div>
      </div>
    );
  };

  return (
    <List
      height={400}
      width={300}
      itemCount={tools.length}
      itemSize={50}
    >
      {Row}
    </List>
  );
};

export default ToolList;
```

### 6.3 Code Splitting

Using React.lazy and Suspense for code splitting:

```jsx
// App.jsx with code splitting
import React, { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Loading from './components/common/Loading';

// Lazy-loaded components
const AgentGraphPage = lazy(() => import('./pages/AgentGraphPage'));
const ToolGraphPage = lazy(() => import('./pages/ToolGraphPage'));
const Dashboard = lazy(() => import('./pages/Dashboard'));

const App = () => {
  return (
    <BrowserRouter>
      <Suspense fallback={<Loading />}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/agent-graph" element={<AgentGraphPage />} />
          <Route path="/tool-graph" element={<ToolGraphPage />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
};

export default App;
```

## 7. Accessibility and Responsiveness

### 7.1 Keyboard Navigation

Ensuring graph components are keyboard accessible:

```jsx
// AccessibleGraph.jsx
const AccessibleGraph = ({ nodes, edges, onNodeSelect }) => {
  const handleKeyDown = (e, node) => {
    if (e.key === 'Enter' || e.key === ' ') {
      onNodeSelect(node);
      e.preventDefault();
    }
  };

  return (
    <div className="accessible-graph" role="application" aria-label="Agent Workflow Graph">
      <div className="node-list" role="list">
        {nodes.map(node => (
          <div 
            key={node.id}
            role="listitem"
            tabIndex={0}
            className="node-item"
            onClick={() => onNodeSelect(node)}
            onKeyDown={(e) => handleKeyDown(e, node)}
            aria-label={`${node.data.label} node of type ${node.data.agentType}`}
          >
            <div className="node-title">{node.data.label}</div>
            <div className="node-type">{node.data.agentType}</div>
          </div>
        ))}
      </div>
      
      <div className="edge-list" role="list">
        {edges.map(edge => (
          <div 
            key={edge.id}
            role="listitem"
            className="edge-description"
            aria-label={`Connection from ${nodes.find(n => n.id === edge.source)?.data.label} to ${nodes.find(n => n.id === edge.target)?.data.label}`}
          >
            {nodes.find(n => n.id === edge.source)?.data.label} → {nodes.find(n => n.id === edge.target)?.data.label}
          </div>
        ))}
      </div>
    </div>
  );
};
```

### 7.2 Responsive Design

Adapting graph layouts for different screen sizes:

```jsx
// ResponsiveAgentGraph.jsx
import React from 'react';
import { useMediaQuery } from 'react-responsive';
import AgentGraph from './AgentGraph';
import AgentGraphCompact from './AgentGraphCompact';

const ResponsiveAgentGraph = (props) => {
  const isTabletOrMobile = useMediaQuery({ query: '(max-width: 1024px)' });
  
  return isTabletOrMobile ? (
    <AgentGraphCompact {...props} />
  ) : (
    <AgentGraph {...props} />
  );
};

export default ResponsiveAgentGraph;
```

## 8. Theme and Styling

### 8.1 Styled Components

Using styled-components for consistent styling:

```jsx
// StyledGraphComponents.js
import styled from 'styled-components';

export const GraphContainer = styled.div`
  height: ${props => props.height || '600px'};
  width: ${props => props.width || '100%'};
  background-color: ${props => props.theme.graphBackground};
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

export const NodeContainer = styled.div`
  padding: 12px;
  background-color: ${props => props.theme.nodeBackground};
  border: 2px solid ${props => props.borderColor || props.theme.nodeBorder};
  border-radius: 6px;
  min-width: 150px;
  color: ${props => props.theme.nodeText};
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  
  &:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    transform: translateY(-2px);
    transition: all 0.2s ease;
  }
`;

export const NodeTitle = styled.div`
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 4px;
`;

export const NodeSubtitle = styled.div`
  font-size: 12px;
  color: ${props => props.theme.nodeSubtitle};
`;
```

### 8.2 Theme Provider

Supporting light and dark themes:

```jsx
// theme.js
export const lightTheme = {
  graphBackground: '#f8f9fa',
  nodeBackground: '#ffffff',
  nodeBorder: '#dee2e6',
  nodeText: '#212529',
  nodeSubtitle: '#6c757d',
  primary: '#4361ee',
  success: '#2ec4b6',
  warning: '#ff9f1c',
  danger: '#e71d36',
  info: '#3f88c5'
};

export const darkTheme = {
  graphBackground: '#1e1e1e',
  nodeBackground: '#2d2d2d',
  nodeBorder: '#444444',
  nodeText: '#e0e0e0',
  nodeSubtitle: '#a0a0a0',
  primary: '#4cc9f0',
  success: '#2ec4b6',
  warning: '#f8961e',
  danger: '#f94144',
  info: '#90e0ef'
};

// ThemeProvider usage
import React, { useState } from 'react';
import { ThemeProvider } from 'styled-components';
import { lightTheme, darkTheme } from './theme';
import GlobalStyle from './GlobalStyle';

const App = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const theme = isDarkMode ? darkTheme : lightTheme;
  
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <button onClick={() => setIsDarkMode(!isDarkMode)}>
        Toggle {isDarkMode ? 'Light' : 'Dark'} Mode
      </button>
      {/* App content */}
    </ThemeProvider>
  );
};
```

## 9. Testing Strategy

### 9.1 Component Testing

Testing components with React Testing Library:

```jsx
// AgentNode.test.jsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import AgentNode from '../components/AgentNode';

describe('AgentNode Component', () => {
  const mockData = {
    label: 'Test Agent',
    agentType: 'visa_api_agent',
    metrics: { successRate: 95 }
  };
  
  const mockOnClick = jest.fn();
  
  it('renders with correct label', () => {
    render(<AgentNode data={mockData} onClick={mockOnClick} />);
    expect(screen.getByText('Test Agent')).toBeInTheDocument();
  });
  
  it('shows agent type', () => {
    render(<AgentNode data={mockData} onClick={mockOnClick} />);
    expect(screen.getByText('visa_api_agent')).toBeInTheDocument();
  });
  
  it('displays metrics', () => {
    render(<AgentNode data={mockData} onClick={mockOnClick} />);
    expect(screen.getByText('Success Rate: 95%')).toBeInTheDocument();
  });
  
  it('calls onClick when clicked', () => {
    render(<AgentNode data={mockData} onClick={mockOnClick} />);
    fireEvent.click(screen.getByText('Test Agent'));
    expect(mockOnClick).toHaveBeenCalledTimes(1);
  });
});
```

### 9.2 Integration Testing

Testing integration between components:

```jsx
// ToolGraph.test.jsx
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import ToolGraph from '../components/ToolGraph';
import { ToolGraphProvider } from '../contexts/ToolGraphContext';

// Mock data
const mockToolGraphData = {
  nodes: [
    { id: 'tool1', name: 'Vector Search', category: 'knowledge' },
    { id: 'tool2', name: 'Code Generator', category: 'code' }
  ],
  links: [
    { source: 'tool1', target: 'tool2', value: 5 }
  ]
};

// Mock API
jest.mock('../api/toolGraphApi', () => ({
  fetchToolGraphData: jest.fn(() => Promise.resolve(mockToolGraphData))
}));

describe('ToolGraph Integration', () => {
  it('loads and displays tool graph data', async () => {
    render(
      <ToolGraphProvider>
        <ToolGraph />
      </ToolGraphProvider>
    );
    
    // Check loading state
    expect(screen.getByText('Loading tool graph...')).toBeInTheDocument();
    
    // Wait for data to load
    await waitFor(() => {
      expect(screen.queryByText('Loading tool graph...')).not.toBeInTheDocument();
    });
    
    // Verify tools are rendered
    expect(screen.getByText('Vector Search')).toBeInTheDocument();
    expect(screen.getByText('Code Generator')).toBeInTheDocument();
  });
});
```

## 10. Future Enhancements

### 10.1 Planned Features

- **Interactive Simulation**: Allow users to simulate agent and tool interactions
- **Flow Builder**: Visual interface for creating custom agent workflows
- **Performance Dashboard**: Real-time metrics on agent and tool performance
- **A/B Testing Interface**: Compare different agent configurations
- **Exportable Reports**: Generate shareable reports of agent performance

### 10.2 Technical Roadmap

- Migrate to React 18 for improved concurrency
- Implement React Server Components for improved performance
- Add more advanced graph visualization capabilities
- Enhance accessibility features
- Develop plugins for custom tool visualization

## 11. Conclusion

This React design document provides a comprehensive approach to implementing agent graphs and tool graphs in the Content-Craft Visa API Agent application. By following these patterns and practices, the frontend will deliver an intuitive, performant, and maintainable visualization of complex agent workflows and tool interactions.

The design prioritizes:
- Component reusability and composition
- Efficient state management
- Performance optimization
- Accessibility and responsiveness
- Clear visualization of complex relationships
- Seamless integration with backend services

This architecture will support the current requirements while remaining flexible for future enhancements. 