import React from 'react'
import 'antd/dist/antd.css'; // or 'antd/dist/antd.less'
import './App.css';

import Code from './components/Code';
import CodeState from './context/Code/CodeState';

function App() {
  return (
    <CodeState>
      <Code />
    </CodeState>
  );
}

export default App;
