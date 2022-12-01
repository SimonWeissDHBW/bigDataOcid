const express = require('express'),
  router = express.Router();

router.get('/:radio/:lonParam/:latParam', async function(req, res) {

  let sql = `SELECT MIN(st_distance_Sphere(point(TowersInRange.lon, TowersInRange.lat), point(${req.params.lonParam}, ${req.params.latParam}))) AS distance, TowersInRange.radio FROM 
	(SELECT radio, lon, lat  FROM towers_${req.params.radio} WHERE st_distance_Sphere(point(lon, lat), point(${req.params.lonParam}, ${req.params.latParam})) <= towers_${req.params.radio}.range) TowersInRange
  GROUP BY radio`;

  console.log(sql)
  await queryDB(sql, res);
});

async function queryDB(sql, res) {
  await db.query(sql, function(err, data, fields) {
    if (err) throw err;
    console.log("Success");
    res.json({
      status: 200,
      data,
      message: "Cell_towers lists retrieved successfully"
    })
  })
};

module.exports = router;
