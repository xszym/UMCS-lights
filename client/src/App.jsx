import React from 'react'
import 'antd/dist/antd.css'; // or 'antd/dist/antd.less'
import './App.css';

import Code from './components/Code';
import CodeState from './context/Code/CodeState';

import axios from 'axios';

axios.defaults.baseURL = 'http://159.89.9.110:58894';
axios.defaults.headers.post['Content-Type'] = 'application/json';

function App() {
  return (
    <CodeState>
      <Code/>
    </CodeState>
  );
}

export default App;
