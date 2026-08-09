{
  "name": "taskmaster-backend",
  "version": "1.0.0",
  "description": "TaskMaster backend application",
  "main": "app/app.js",
  "scripts": {
    "start": "node app/app.js",
    "test": "jest"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "bcrypt": "^5.0.1",
    "body-parser": "^1.20.0",
    "cookie-parser": "^1.4.6",
    "express": "^4.17.3",
    "jsonwebtoken": "^8.5.1",
    "mysql2": "^2.3.3",
    "sequelize": "^6.12.0"
  },
  "devDependencies": {
    "jest": "^28.1.0",
    "supertest": "^6.2.3"
  }
}