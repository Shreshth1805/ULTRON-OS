const dotenv = require('dotenv');
const path = require('path');

dotenv.config({ path: path.join(__dirname, '../../.env') });

const config = {
  port: process.env.PORT || 3001,
  database: {
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || 'password',
    database: process.env.DB_NAME || 'taskmaster',
  },
  jwt: {
    secret: process.env.JWT_SECRET || 'secret',
    expires: process.env.JWT_EXPIRES || '1h',
  },
  bcrypt: {
    saltRounds: process.env.BCRYPT_SALT_ROUNDS || 10,
  },
};

module.exports = config;