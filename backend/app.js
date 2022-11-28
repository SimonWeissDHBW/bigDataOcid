const express = require('express')
const app = express()
const cors = require('cors')
const mysql_connector = require('mysql2')

const port = 3000

const cellTowersRouter = require('./routes/cellTowers')

db = mysql_connector.createConnection({
    host : 'localhost',
    user : 'root',
    password  :'ocidBigData',
    database : 'cell_towers'
});

app.use(cors())

app.use('/cellTowers', cellTowersRouter);


app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})