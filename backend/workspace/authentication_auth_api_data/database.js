const { Pool } = require('pg');
const config = require('../config/config');

const pool = new Pool({
  user: config.db.user,
  host: config.db.host,
  database: config.db.database,
  password: config.db.password,
  port: config.db.port,
});

pool.on('error', (err, client) => {
  console.error('Unexpected error on idle client', err);
  process.exit(-1);
});

const query = (text, params) => {
  return pool.query(text, params);
};

const close = () => {
  pool.end();
};

module.exports = {
  query,
  close,
};