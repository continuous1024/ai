const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const learningPath = require('./learningPath.json');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Doris connection pool
const pool = mysql.createPool({
  host: 'doris',
  user: 'root',
  password: '',
  port: 9030,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// Execute SQL
app.post('/api/sql', async (req, res) => {
  const { sql } = req.body;
  try {
    const [rows] = await pool.query(sql);
    const [explain] = await pool.query(`EXPLAIN ANALYZE ${sql}`);
    res.json({ success: true, rows, explain });
  } catch (error) {
    res.json({ success: false, error: error.message });
  }
});

app.get('/api/learningPath', (req, res) => {
  res.json({ success: true, learningPath });
});

const progressFile = path.join(__dirname, 'progress.json');
app.get('/api/progress', (req, res) => {
  fs.readFile(progressFile, 'utf-8', (err, data) => {
    if (err) return res.json({ success: false, error: err.message });
    const progress = JSON.parse(data || '{}');
    res.json({ success: true, progress });
  });
});

app.post('/api/progress', (req, res) => {
  const { chapterId, completed } = req.body;
  fs.readFile(progressFile, 'utf-8', (err, data) => {
    let progress = {};
    if (!err) {
      try { progress = JSON.parse(data); } catch {}
    }
    progress[chapterId] = completed;
    fs.writeFile(progressFile, JSON.stringify(progress, null, 2), err2 => {
      if (err2) return res.json({ success: false, error: err2.message });
      res.json({ success: true, progress });
    });
  });
});

app.listen(5000, () => console.log('Backend listening on port 5000'));
