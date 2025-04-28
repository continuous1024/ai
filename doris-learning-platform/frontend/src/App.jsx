import React from 'react';
import { Layout, Menu } from 'antd';
import { Link, useLocation, Routes, Route } from 'react-router-dom';
import LearningPath from './pages/LearningPath';
import SQLConsole from './pages/SQLConsole';
import './index.css';

const { Header, Content, Sider } = Layout;

export default function App() {
  const location = useLocation();
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider breakpoint="lg" collapsedWidth="0">
        <div className="logo">Doris 学习平台</div>
        <Menu theme="dark" mode="inline" selectedKeys={[location.pathname]}>
          <Menu.Item key="/">
            <Link to="/">学习路径</Link>
          </Menu.Item>
          <Menu.Item key="/sql">
            <Link to="/sql">在线 SQL</Link>
          </Menu.Item>
        </Menu>
      </Sider>
      <Layout>
        <Header className="header">Apache Doris 交互式学习平台</Header>
        <Content style={{ margin: '16px' }}>
          <Routes>
            <Route path="/" element={<LearningPath />} />
            <Route path="/sql" element={<SQLConsole />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  );
}
