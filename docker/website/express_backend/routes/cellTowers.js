const mysql_connector = require('mysql2/promise')
const express = require('express'),
router = express.Router();


router.get('/:radio/:lonParam/:latParam', async function(req, res) {

  let sql = `SELECT MIN(st_distance_Sphere(point(TowersInRange.lon, TowersInRange.lat), point(${req.params.lonParam}, ${req.params.latParam}))) AS distance FROM 
	(SELECT lon, lat  FROM towers_${req.params.radio} WHERE st_distance_Sphere(point(lon, lat), point(${req.params.lonParam}, ${req.params.latParam})) <= towers_${req.params.radio}.range) TowersInRange`;

  console.log(sql)
  await queryDB(sql, res);
});

db_info = {
  host : 'ocid',
  user : 'root',
  password  :'ocidBigData',
  database : 'cell_towers'
};

async function queryDB(sql, res) {

  db = await mysql_connector.createConnection((db_info))

  data = await db.execute(sql)

  res.json({
    status: 200,
    data,
    message: "Cell_towers lists retrieved successfully"
  })
};

module.exports = router;
