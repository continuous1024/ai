import React, { useState } from 'react';
import { Input, Button, Table, Alert } from 'antd';
import axios from 'axios';

const { TextArea } = Input;

export default function SQLConsole() {
  const [sql, setSql] = useState('SELECT * FROM table_name;');
  const [rows, setRows] = useState([]);
  const [columns, setColumns] = useState([]);
  const [explain, setExplain] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRun = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await axios.post('/api/sql', { sql });
      if (res.data.success) {
        const data = res.data.rows;
        setRows(data);
        setColumns(
          data.length > 0
            ? Object.keys(data[0]).map(key => ({ title: key, dataIndex: key, key }))
            : []
        );
        setExplain(res.data.explain);
      } else {
        setError(res.data.error);
      }
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>在线 SQL 控制台</h2>
      <TextArea
        rows={6}
        value={sql}
        onChange={e => setSql(e.target.value)}
        placeholder="请输入 Doris SQL"
        style={{ fontFamily: 'monospace', marginBottom: '8px' }}
      />
      <Button type="primary" onClick={handleRun} loading={loading}>
        运行
      </Button>
      {error && <Alert message={error} type="error" style={{ marginTop: '16px' }} />}
      {rows.length > 0 && (
        <Table
          dataSource={rows.map((row, idx) => ({ ...row, key: idx }))}
          columns={columns}
          style={{ marginTop: '16px' }}
          pagination={false}
        />
      )}
      {explain.length > 0 && (
        <div style={{ marginTop: '16px' }}>
          <h3>执行计划</h3>
          <pre>{JSON.stringify(explain, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
