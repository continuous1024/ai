import React, { useEffect, useState, useRef } from 'react';
import { Collapse, Checkbox, Progress } from 'antd';
import axios from 'axios';
import * as echarts from 'echarts';

const { Panel } = Collapse;

export default function LearningPath() {
  const [path, setPath] = useState([]);
  const [progress, setProgress] = useState({});

  useEffect(() => {
    axios.get('/api/learningPath').then(res => res.data.success && setPath(res.data.learningPath));
    axios.get('/api/progress').then(res => res.data.success && setProgress(res.data.progress));
  }, []);

  const handleChange = (id, checked) => {
    axios.post('/api/progress', { chapterId: id, completed: checked })
      .then(res => res.data.success && setProgress(res.data.progress));
  };

  const total = path.length;
  const done = Object.values(progress).filter(v => v).length;
  const percent = total ? Math.round((done / total) * 100) : 0;

  return (
    <div>
      <h2>学习路径</h2>
      <Progress percent={percent} style={{ marginBottom: '16px' }} />
      <Collapse accordion>
        {path.map(item => (
          <Panel header={`${item.title} (${item.level})`} key={item.id}>
            <p><strong>目标：</strong> {item.objectives.join('，')}</p>
            <p><strong>技能：</strong> {item.skills.join('，')}</p>
            <Checkbox
              checked={progress[item.id]}
              onChange={e => handleChange(item.id, e.target.checked)}
              style={{ marginTop: '8px' }}
            >已完成</Checkbox>
            {item.id === 'architecture' && <ArchitectureChart />}
          </Panel>
        ))}
      </Collapse>
    </div>
  );
}

function ArchitectureChart() {
  const ref = useRef();
  useEffect(() => {
    const chart = echarts.init(ref.current);
    const option = {
      tooltip: {},
      series: [{
        type: 'graph',
        layout: 'force',
        roam: true,
        symbolSize: 60,
        label: { show: true },
        data: [
          { id: 'FE', name: 'Frontend (FE)' },
          { id: 'Broker', name: 'Broker' },
          { id: 'BE', name: 'Backend (BE)' },
          { id: 'Storage', name: 'Storage' }
        ],
        links: [
          { source: 'FE', target: 'Broker' },
          { source: 'Broker', target: 'BE' },
          { source: 'BE', target: 'Storage' }
        ],
      }]
    };
    chart.setOption(option);
    window.addEventListener('resize', () => chart.resize());
    return () => { window.removeEventListener('resize', () => chart.dispose()); };
  }, []);
  return <div ref={ref} style={{ height: '400px', marginTop: '16px' }} />;
}
