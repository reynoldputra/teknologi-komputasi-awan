const mysql = require('mysql2');

// mysql connection
var pool = mysql.createPool({
  host: process.env.MYSQL_HOST,
  user: process.env.MYSQL_USER_ROOT,
  password: process.env.MYSQL_ROOT_PASSWORD,
  port: process.env.MYSQL_PORT,
  database: process.env.MYSQL_DATABASE
});



module.exports = pool;
